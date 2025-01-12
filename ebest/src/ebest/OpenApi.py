import aiohttp, asyncio, json, time
from .tr_code_to_path import tr_code_to_path
from .code_realtime_account import code_realtime_account

# BASE_URL = "https://openapi.ebestsec.co.kr:8080"
# WSS_URL_REAL = "wss://openapi.ebestsec.co.kr:9443/websocket"
# WSS_URL_SIMULATION = "wss://openapi.ebestsec.co.kr:29443/websocket"

# 2024-06-01. 이베스트증권에서 LS증권으로 변경됨.
BASE_URL = "https://openapi.ls-sec.co.kr:8080"
WSS_URL_REAL = "wss://openapi.ls-sec.co.kr:9443/websocket"
WSS_URL_SIMULATION = "wss://openapi.ls-sec.co.kr:29443/websocket"

import warnings


class ResponseValue:
    def __init__(
        self,
        path: str,
        tr_cd: str,
        tr_cont: str,
        tr_cont_key: str,
        response_text: str,
    ) -> None:
        self.path = path
        self.tr_cd = tr_cd
        self.tr_cont = tr_cont
        self.tr_cont_key = tr_cont_key
        self.body = json.loads(response_text)
        self.response_text = response_text
        # additional variables
        self.in_tr_cont = str()
        self.in_tr_cont_key = str()
        self.request_text = str()
        self.request_time = 0.0
        self.elapsed_ms = 0.0

class OpenApi:

    class _event_signal:
        class _slot:
            def __init__(self, func):
                self.func = func
                self.is_coroutine = asyncio.iscoroutinefunction(func)
            def __eq__(self, other):
                return self.func == other
        def __init__(self):
            self.__slots: list[self._slot] = []
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

    def __init__(self):
        super().__init__()
        
        self._access_token = ""
        self._http = None
        self._websocket = None
        self._connected:bool = False
        self._is_simulation:bool = False
        self._last_message:str = ""
        self._mac_address : str|None = None
        self._last_respose_value = None
    
        # 이벤트 핸들러
        self._on_message = self._event_signal()
        self._on_realtime = self._event_signal()
        # self._on_message = lambda sender, msg: print(f"on_message: {msg}")
        # self._on_realtime = lambda sender, trcode, key, realtimedata: print(f"on_realtime: {trcode}, {key}, {realtimedata}")

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
    def mac_address(self) -> str:
        """법인인 경우 필수 세팅"""
        return self._mac_address

    @mac_address.setter
    def mac_address(self, value:str) : self._mac_address = value

    @property
    def on_message(self) :
        """메시지 수신 이벤트 핸들러
        on_message(sender:OpenApi, msg:str)
        """
        return self._on_message
    
    @on_message.setter
    def on_message(self, slot) :
        if not hasattr(slot, "__call__") :
            raise ValueError("slot must be callable")
        warnings.warn("setter is deprecated. use on_message.connect({}).".format(slot.__name__),
                      category=DeprecationWarning,
                      stacklevel=2)
        self._on_message.connect(slot)

    @property
    def on_realtime(self) :
        """실시간 데이터 수신 이벤트 핸들러
        on_realtime(sender:OpenApi, trcode:str, key:str, realtimedata:dict)
        """
        return self._on_realtime
    
    @on_realtime.setter
    def on_realtime(self, slot) :
        if not hasattr(slot, "__call__") :
            raise ValueError("slot must be callable")
        warnings.warn("setter is deprecated. use on_realtime.connect({}).".format(slot.__name__),
                      category=DeprecationWarning,
                      stacklevel=2)
        self._on_realtime.connect(slot)
    
    async def close(self) -> None:
        """연결 종료"""
        self._connected = False
        if self._websocket and not self._websocket.closed:
            await self._websocket.close()
        if self._http and not self._http.closed:
            await self._http.close()

    async def login(self, appkey:str, appsecretkey:str) -> bool:
        '''
        로그인 요청
        appkey: 앱키
        appsecretkey: 앱시크릿키
        return: True: 성공, False: 실패, 실패시 last_message에 실패사유가 저장됨
        '''
        if self._connected :
            self._last_message = "aleady connected"
            return True
        
        if appkey == "" or appsecretkey == "":
            self._last_message = "appkey or appsecretkey is empty"
            return False
    
        # 토큰 가져오기
        timeout = aiohttp.ClientTimeout(total=10) # 10초 타임아웃
        httpclient = aiohttp.ClientSession(timeout=timeout)
        token_response = await httpclient.post(BASE_URL + "/oauth2/token"
                    , data={'grant_type': 'client_credentials', 'appkey': appkey, 'appsecretkey': appsecretkey, 'scope': 'oob'}
                    )
        if token_response.status != 200:
            await httpclient.close()
            self._last_message = "Failed to retrieve authentication key."
            return False
    
        # 인증성공
        token = (await token_response.json())['access_token']
        httpclient.headers["Authorization"] = f"Bearer {token}"
        httpclient.headers["Content-Type"] = "application/json; charset=UTF-8"
        self._access_token = token
        self._http = httpclient
        self._connected = True
        
        # 모의투자인지 실투자인지 구분한다.
        FOCCQ33600 = dict()
        FOCCQ33600['FOCCQ33600InBlock1'] = {}
        
        response = await self.request("FOCCQ33600", FOCCQ33600)
        if not response :
            self._connected = False
            self._last_message = "Failed to require FOCCQ33600"
            await httpclient.close()
            return False
    
        rsp_msg:str = response.body["rsp_msg"]
        if rsp_msg.__contains__("모의투자"):
            self._is_simulation = True

        # 웹소켓 연결
        self._connected = False
        try:
            websocket = await  httpclient.ws_connect(WSS_URL_SIMULATION if self._is_simulation else WSS_URL_REAL)
            self._connected = not websocket.closed
        except :
            pass
    
        if not self._connected:
            await httpclient.close()
            self._last_message = "websocket connection failed."
            return False
    
        self._websocket = websocket
        asyncio.create_task(self._websocket_listen())
        return True

    async def request(self, tr_cd:str, data:dict|str
                             ,*
                             , path:str=None
                             , tr_cont:str="N"
                             , tr_cont_key:str="0"
                             ) -> ResponseValue | None:
        '''
        TR데이터 요청
        tr_cd: TR코드
        data: 데이터
        return: 성공시 ResponseValue, 실패시 None, 실패시 last_message에 실패사유가 저장됨
        '''
        self._last_message = ""
        self._last_respose_value = None
        if not self._connected:
            self._last_message = "Not connected"
            return None

        if not path:
            if not tr_code_to_path.__contains__(tr_cd):
                self._last_message = "Not supported tr code"
                return None
            path = tr_code_to_path[tr_cd]
    
        headers = dict()
        headers["tr_cd"] = tr_cd
        headers["tr_cont"] = tr_cont
        headers["tr_cont_key"] = tr_cont_key
        if self._mac_address:
            headers["mac_address"] = self._mac_address
        
        try:
            if isinstance(data, str):
                request_text = data
            else:
                request_text = json.dumps(data)
            request_time = time.time()
            start_time = time.perf_counter_ns()
            response = await self._http.post(BASE_URL + path, headers=headers, data=request_text)
            if response.status != 200:
                self._last_message = await response.json()
                return None
            response_text = await response.text()
            elapsed_ms = (time.perf_counter_ns() - start_time) / 1000000
            result = ResponseValue(path, tr_cd, response.headers["tr_cont"], response.headers["tr_cont_key"], response_text)
            result.in_tr_cont = tr_cont
            result.in_tr_cont_key = tr_cont_key
            result.request_text = request_text
            result.request_time = request_time
            result.elapsed_ms = elapsed_ms
            self._last_respose_value = result
            return result
        except Exception as e:
            self._last_message = e

        return None

    def add_realtime(self, tr_cd:str, tr_key:str) :
        """실시간 데이터 요청
        tr_cd: TR코드
        tr_key: TR키/종목코드
        """
        return self._realtime_request(tr_cd , tr_key, "1" if code_realtime_account.__contains__(tr_cd) else "3")

    def remove_realtime(self, tr_cd:str, tr_key:str) :
        """실시간 데이터 중지
        tr_cd: TR코드
        tr_key: TR키/종목코드
        """
        return self._realtime_request(tr_cd, tr_key, "2" if code_realtime_account.__contains__(tr_cd) else "4")

    async def _websocket_listen(self):
        async for msg in self._websocket:
            if msg.type == aiohttp.WSMsgType.TEXT:
                try:
                    jsondata = json.loads(msg.data)
                except Exception as e:
                    self._last_message = e
                    await self._inner_on_mesage(f"websocket exception. {e}")
                    continue
                header = jsondata.get("header", None)
                if header != None:
                    tr_cd = header.get("tr_cd", None)
                    rsp_msg = header.get("rsp_msg", None)
                    if rsp_msg != None:
                        self._last_message = ""
                        tr_type = header.get("tr_type", None)
                        await self._inner_on_mesage(f"{tr_cd}({tr_type}): {rsp_msg}")
                    body = jsondata.get("body", None)
                    tr_key = header.get("tr_key", None)
                    if body != None:
                        await self._inner_on_realtime(tr_cd, tr_key, body)
            elif msg.type == aiohttp.WSMsgType.CLOSED:
                self._last_message = msg
                await self._inner_on_mesage(f"websocket closed. {msg}")
                break
            elif msg.type == aiohttp.WSMsgType.ERROR:
                self._last_message = msg
                await self._inner_on_mesage(f"websocket error. {msg}")

    async def _realtime_request(self, tr_cd:str, tr_key:str, tr_type:str) -> bool:
        if not self._connected:
            self._last_message = "Not connected"
            return False
        data = f"{{\"header\":{{\"token\":\"{self._access_token}\",\"tr_type\":\"{tr_type}\"}},\"body\":{{\"tr_cd\":\"{tr_cd}\",\"tr_key\":\"{tr_key}\"}}}}"
        await self._websocket.send_str(data)
        return True

    async def _inner_on_mesage(self, msg:str):
        await self._on_message.emit_signal(self, msg)

    async def _inner_on_realtime(self, trcode:str, key:str, realtimedata):
        await self._on_realtime.emit_signal(self, trcode, key, realtimedata)
