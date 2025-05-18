############################################################################
# 키움증권 REST API 비동기 클라이언트
# 키움증권 가이드 참고: https://openapi.kiwoom.com/guide/apiguide
############################################################################

import asyncio
import aiohttp
import json
import time

BASE_URL_REAL = "https://api.kiwoom.com"
BASE_URL_SIMUL = "https://mockapi.kiwoom.com"
WSS_URL_REAL = "wss://api.kiwoom.com:10000/api/dostk/websocket"
WSS_URL_SIMULATION = "wss://mockapi.kiwoom.com:10000/api/dostk/websocket"

from .tr_code_to_path import tr_code_to_path


class ResponseData:
    def __init__(self,
        api_id: str
    ) -> None:
        self.api_id = api_id
        self.path = str()
        self.return_code = int(-1)
        self.return_msg = str()
        self.cont_yn = str()
        self.next_key = str()
        self.body = {}
        # additional variables
        self.inputs = dict()
        self.in_cont_yn = str()
        self.in_next_key = str()
        self.request_time = 0.0
        self.elapsed_ms = 0.0

    def __str__(self) -> str:
        return f"ResponseData(api_id={self.api_id}, path={self.path}, return_code={self.return_code}, return_msg={self.return_msg}, cont_yn={self.cont_yn}, next_key={self.next_key}, body={self.body})"

class KwRestApi(object):

    class _event_signal:
        class _slot:
            def __init__(self, func):
                self.func = func
                self.is_coroutine = asyncio.iscoroutinefunction(func)
            def __eq__(self, other):
                return self.func == other
        def __init__(self):
            self.__slots: list[KwRestApi._event_signal._slot] = []
        def connect(self, func):
            # check callable
            if not hasattr(func, "__call__") :
                raise ValueError("slot must be callable")
            # check exist
            exist_slot = next((s for s in self.__slots if s.func == func), None)
            if exist_slot:
                return
            # add slot
            self.__slots.append(self._slot(func))
        def disconnect(self, func):
            exist_slot = next((s for s in self.__slots if s.func == func), None)
            if exist_slot:
                self.__slots.remove(exist_slot)
        def disconnect_all(self):
            self.__slots.clear()
        async def emit_signal(self, *args):
            for slot in self.__slots:
                if slot.is_coroutine:
                    await slot.func(*args)
                else:
                    slot.func(*args)

    class _asyncNode:
        def __init__(self, hashid):
            self.__event = asyncio.Event()
            self.hashid = hashid
            self.jsondata = {}

        def set(self):
            self.__event.set()

        async def wait(self, timeout=None):
            if timeout is None:
                await self.__event.wait()
                return True
            try:
                await asyncio.wait_for(self.__event.wait(), timeout)
                return True
            except asyncio.TimeoutError:
                return False

    def __init__(self):
        super().__init__()
        
        self._access_token = ""
        self._http = None
        self._websocket = None
        self._base_url:str = ""
        self._connected:bool = False
        self._is_simulation:bool = False
        self._last_message:str = ""
        self._timeout = 5
        self._last_response_value = None
    
        # 이벤트 핸들러
        self._on_message = self._event_signal()
        self._on_realtime = self._event_signal()

        # 웹소켓 비동기 요청 노드
        self._ws_asyncnode:KwRestApi._asyncNode | None = None

    @property
    def connected(self) -> bool:
        """로그인 연결상태.
        True: 연결됨, False: 연결안됨

        A readonly property.
        """
        return self._connected
    
    @property
    def is_simulation(self) -> bool:
        """서버모드
        True: 모의투자, False: 실투자

        A readonly property.
        """
        return self._is_simulation

    @property
    def last_message(self) -> str:
        """last error message.

        A readonly property.
        """
        return self._last_message

    @property
    def on_message(self) :
        """메시지 수신 이벤트 핸들러, 웹소켓 오류/끊김 시 발생
        on_message(msg:str)
        """
        return self._on_message

    @property
    def on_realtime(self) :
        """실시간 데이터 수신 이벤트 핸들러
        on_realtime(realdata:dict)
        """
        return self._on_realtime

    @property
    def last_response(self) -> ResponseData | None:
        """마지막 요청 응답값
        ResponseValue: 응답값
        """
        return self._last_response_value

    @property
    def access_token(self) -> str:
        """access token
        access_token: access token
        """
        return self._access_token

    @property
    def timeout(self) -> int:
        """timeout
        timeout: timeout
        """
        return self._timeout

    @timeout.setter
    def timeout(self, value: int) -> None:
        """timeout setter
        value: timeout
        """
        if value <= 0:
            raise ValueError("timeout must be greater than 0")
        self._timeout = value
    
    async def close(self) -> None:
        """연결 종료"""
        self._connected = False
        if self._websocket and not self._websocket.closed:
            await self._websocket.close()
        if self._http and not self._http.closed:
            await self._http.close()

    async def login(self, appkey:str, secretkey:str, is_simulation:bool = False) -> bool:
        '''
        로그인 요청
        appkey: 앱키
        secretkey: 앱시크릿키
        is_simulation: 모의투자 로그인 시 True, 실투자 로그인 시 False (default)
        return: True: 성공, False: 실패, 실패시 last_message에 실패사유가 저장됨
        '''
        if self._connected :
            self._last_message = "aleady connected"
            return True
        
        if appkey == "" or secretkey == "":
            self._last_message = "appkey or secretkey is empty"
            return False
    
        self._is_simulation = is_simulation
        self._base_url = BASE_URL_SIMUL if self._is_simulation else BASE_URL_REAL

        timeout = aiohttp.ClientTimeout(total=10) # 10초 타임아웃
        self._http = aiohttp.ClientSession(timeout=timeout)

        # 토큰 가져오기
        self._connected = True
        inputs = {'grant_type': 'client_credentials', 'appkey': appkey, 'secretkey': secretkey}
        response = await self.request("oauth2", inputs, path="/oauth2/token")
        if response.return_code == 0:
            # 토큰발급 성공
            token = response.body["token"]
            self._http.headers["Authorization"] = f"Bearer {token}"
            self._access_token = token
            # 웹소켓 연결/인증요청
            try:
                websocket = await  self._http.ws_connect(WSS_URL_SIMULATION if self._is_simulation else WSS_URL_REAL)
                if not websocket.closed:
                    self._websocket = websocket
                    asyncio.create_task(self._websocket_listen())
                    response = await self.realtime({"trnm":"LOGIN", "token" : self._access_token})
                    if response.return_code == 0:
                        # 인증성공
                        self._last_message = "Login success"
                        return True
                    else:
                        self._last_message = response.return_msg
                else:
                    self._last_message = "websocket connection failed."
            except Exception as e:
                self._last_message = str(e)
        else:
            self._last_message = response.return_msg
        await self.close()
        return False

    async def request(self
            , api_id:str
            , indatas:dict
            ,*
            , cont_yn:str="N"
            , next_key:str=""
            , path:str=None
            ) -> ResponseData:
        '''
        TR/실시간 요청
        api_id: TR코드(api-id)
        indatas: 입력데이터(dictionary)
        cont_yn: TR연속요청여부
        next_key: TR연속요청키
        path: 요청경로(생략시 자동으로 결정)
        return: ResponseValue, 성공시 return_code = 0, 그외 실패, 실패시 return_msg에 실패사유가 저장됨

        example:
        # 삼성전자 종목정보 조회
        inputs = {
            "stk_cd" : "005930"
        }
        response = await api.request("ka10001", inputs)
        print(response)

        # 조건검색식 목록 조회
        inputs = {
            "trnm" : "CNSRLST"
        }
        response = await api.request("ka10171", inputs)
        print(response)
        '''
        result = ResponseData(api_id)
        result.in_cont_yn = cont_yn
        result.in_next_key = next_key
        result.inputs = indatas

        if not path:
            path = tr_code_to_path.get(api_id, None)
            if not path:
                self._last_message = "Not supported tr_code-path"
                result.return_msg = self._last_message
                return result

        result.path = path

        self._last_response_value = result
        if not self._connected:
            self._last_message = "Not connected"
            result.return_msg = self._last_message
            return result

        # check if websocket request
        if path.endswith("/websocket"):
            result.request_time = time.time()
            start_time = time.perf_counter_ns()
            ws_result = await self._ws_request(indatas)
            result.elapsed_ms = (time.perf_counter_ns() - start_time) / 1000000
            if ws_result != None:
                result.return_code = ws_result.get("return_code", -1)
                result.return_msg = ws_result.get("return_msg", "")
                result.body = ws_result
                return result
            else:
                result.return_code = -1
                result.return_msg = self._last_message
                return result

        headers = dict()
        headers["api-id"] = api_id
        headers["cont-yn"] = cont_yn
        headers["next-key"] = next_key
        
        try:
            result.request_time = time.time()
            start_time = time.perf_counter_ns()
            response = await self._http.post(self._base_url + path, headers=headers, json=indatas)
            response_data:dict = await response.json()
            result.elapsed_ms = (time.perf_counter_ns() - start_time) / 1000000
            if response.status != 200:
                self._last_message = f"Request failed. {response.status}"
                result.return_msg = self._last_message
                return result
            result.cont_yn = response.headers.get("cont-yn", "N")
            result.next_key = response.headers.get("next-key", "")
            result.body = response_data
            result.return_code = result.body.get("return_code", -1)
            self._last_message = result.body.get("return_msg", "")
            result.return_msg = self._last_message
        except Exception as e:
            self._last_message = str(e)
            result.return_msg = self._last_message

        return result

    def realtime(self, indatas:dict):
        '''
        # ex: 삼성전자, SK하이닉스 실시간 체결 시세 등록
        inputs = {
            "trnm" : "REG",
            "grp_no" : "1",
            "refresh" : "1",
            "data" : [{
                " item" : [ "005930", "000660" ],
                " type" : [ "0B" ] # 우선호가시세 까지 함께 등록할 경우 ["0B", "0C" ]로 설정
            }]
        }
        response = await api.realtime(inputs)
        print(response)

        # 실시간 시세 해제 시 "REG" -> "REMOVE" 로 변경
        inputs["trnm"] = "REMOVE"
        response = await api.realtime(inputs)
        '''
        return self.request("realtime", indatas, path="/api/dostk/websocket", cont_yn="")

    async def ws_sendmessage(self, text:str) -> bool:
        '''
        웹소켓 메시지 전송
        text: 전송할 메시지
        return: True: 성공, False: 실패, 실패시 last_message에 실패사유가 저장됨
        '''
        if not self._connected or self._websocket.closed:
            self._last_message = "Not connected"
            return False
        await self._websocket.send_str(text)
        return True

    async def _ws_request(self, indatas:dict) -> dict | None:
        # check connection
        if not self._connected:
            self._last_message = "Not connected"
            return None

        # check async node
        if self._ws_asyncnode != None:
            # already requested
            self._last_message = "Already requested"
            return None

        trnm = indatas.get("trnm", None)
        if trnm == None:
            self._last_message = "trnm is not define."
            return None

        # create async node
        node = KwRestApi._asyncNode(trnm)
        self._ws_asyncnode = node

        # send message
        try:
            await self._websocket.send_json(indatas)
            # wait for response
            if not await self._ws_asyncnode.wait(self.timeout):
                # timeout
                self._last_message = "Timeout"
                self._ws_asyncnode = None
                return None
        except Exception as e:
            self._last_message = f"websocket request error. {e}"
            self._ws_asyncnode = None
            return None

        # set response and return
        self._ws_asyncnode = None
        return node.jsondata

    async def _websocket_listen(self):
        async for msg in self._websocket:
            if msg.type == aiohttp.WSMsgType.TEXT:
                json_text = msg.data
                try:
                    jsondata = json.loads(json_text)
                    trnm = jsondata.get("trnm", None)
                    if trnm != None:
                        # proc PING
                        if trnm == "PING":
                            await self._websocket.send_str(json_text)
                            continue
                        # check async node
                        if self._ws_asyncnode != None and self._ws_asyncnode.hashid == trnm:
                            # setting jsondata, set event
                            self._ws_asyncnode.jsondata = jsondata
                            self._ws_asyncnode.set()
                            continue
                    # raise event
                    await self._on_realtime.emit_signal(jsondata)
                except Exception as e:
                    self._last_message = f"websocket exception. {e}"
                    await self._on_message.emit_signal(self._last_message)
                    continue

            elif msg.type == aiohttp.WSMsgType.CLOSED:
                break

            elif msg.type == aiohttp.WSMsgType.ERROR:
                self._last_message = f"websocket error. {msg}"
                await self._on_message.emit_signal(self._last_message)

        if self._connected:
            self._last_message = f"websocket closed."
            await self._on_message.emit_signal(self._last_message)
