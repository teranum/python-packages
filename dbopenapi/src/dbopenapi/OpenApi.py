import asyncio
import json
import aiohttp
from dbopenapi.tr_code_to_path import tr_code_to_path
from dbopenapi.code_realtime_account import code_realtime_account

BASE_URL = 'https://openapi.db-fi.com:8443'
WSS_URL_REAL = 'wss://openapi.db-fi.com:7070'
WSS_URL_SIMULATION = 'wss://openapi.db-fi.com:17070'

#해외선물옵션
WSS_URL_GLOBAL = 'wss://openapi.db-fi.com:7071'

class ResponseValue:
    def __init__(
        self,
        cont_yn: str,
        cont_key: str,
        body: dict,
    ) -> None:
        self.cont_yn = cont_yn
        self.cont_key = cont_key
        self.body = body

class OpenApi:
    def __init__(self):
        super().__init__()

        self._access_token = ''
        self.expires_in = 0
        self._http = None
        self._websocket = None
        self._connected:bool = False
        self._is_simulation:bool = False
        self._last_message:str = ''
        self._mac_address : str = ''
    
        # 이벤트 핸들러
        self._on_message = lambda sender, msg: print(f'on_message: {msg}')
        self._on_realtime = lambda sender, trcode, key, realtimedata: print(f'on_realtime: {trcode}, {key}, {realtimedata}')
        self._is_async_on_message:bool = False
        self._is_async_on_realtime:bool = False

    @property
    def connected(self) -> bool:
        '''로그인 연결상태.
        True: 연결됨, False: 연결안됨

        A readonly property.
        '''
        return self._connected
    
    @property
    def is_simulation(self) -> bool:
        '''서버모드
        True: 모의투자, False: 실투자

        A readonly property.
        '''
        return self._is_simulation

    @property
    def last_message(self) -> str:
        '''last error message.

        A readonly property.
        '''
        return self._last_message

    @property
    def access_token(self) -> str:
        '''access_token 당일 재 로그인에 이용'''
        return self._access_token

    @property
    def mac_address(self) -> str:
        '''법인인 경우 필수 세팅'''
        return self._mac_address

    @mac_address.setter
    def mac_address(self, value:str) : self._mac_address = value

    @property
    def on_message(self) :
        '''메시지 수신 이벤트 핸들러
        on_message(sender:OpenApi, msg:str)
        '''
        return self._on_message
    
    @on_message.setter
    def on_message(self, value):
        self._is_async_on_message = asyncio.iscoroutinefunction(value)
        self._on_message = value

    @property
    def on_realtime(self) :
        '''실시간 데이터 수신 이벤트 핸들러
        on_realtime(sender:OpenApi, trcode:str, key:str, realtimedata:dict)
        '''
        return self._on_realtime
    
    @on_realtime.setter
    def on_realtime(self, value) :
        self._is_async_on_realtime = asyncio.iscoroutinefunction(value)
        self._on_realtime = value
    
    async def close(self) -> None:
        '''연결 종료'''
        self._connected = False
        if self._websocket and not self._websocket.closed:
            await self._websocket.close()
        if self._http and not self._http.closed:
            await self._http.close()

    async def login(self, appkey:str, appsecretkey:str
                    ,*
                    , is_simulation:bool=False
                    , wss_domain:str=''
                    , access_token:str='') -> bool:
        '''
        로그인 요청 (모의투자인 경우에는 is_simulation을 True로 설정, 해외선물옵션인 경우에는 wss_domain을 dbopenapi.WSS_URL_GLOBAL 로 설정)
        appkey: 앱키
        appsecretkey: 앱시크릿키
        *
        is_simulation: 모의투자 여부(기본값: False)
        wss_domain: 웹소켓 도메인(해외선물옵션인 경우에만 설정, dbopenapi.WSS_URL_GLOBAL 으로 설정)
        access_token: 토큰(기본값: ''), 토큰이 있는 경우에는 토큰을 사용하고, 없는 경우에는 새로 토큰을 가져옴
        return: True: 성공, False: 실패, 실패시 last_message에 실패사유가 저장됨
        '''
        if self._connected :
            self._last_message = 'aleady connected'
            return True
        
        timeout = aiohttp.ClientTimeout(total=10) # 10초 타임아웃
        httpclient = aiohttp.ClientSession(timeout=timeout)
        if access_token == '':
            # 토큰 가져오기
            if appkey == '' or appsecretkey == '':
                self._last_message = 'appkey or appsecretkey is empty'
                return False
    
            token_response = await httpclient.post(BASE_URL + '/oauth2/token'
                        , data={'grant_type': 'client_credentials', 'appkey': appkey, 'appsecretkey': appsecretkey, 'scope': 'oob'}
                        )
            if token_response.status != 200:
                await httpclient.close()
                self._last_message = 'Failed to retrieve authentication key.'
                return False
    
            # 인증성공
            response_data = await token_response.json()
            access_token = response_data['access_token']
            self.expires_in = response_data['expires_in']
        
        httpclient.headers['Authorization'] = f'Bearer {access_token}'
        httpclient.headers['Content-Type'] = 'application/json; charset=UTF-8'
        self._access_token = access_token
        
        self._http = httpclient
        self._connected = True
        
        # 모의투자인지 실투자인지 구분한다.
        # request = dict()
        # response = await self.request('CSPEQ00400', request)
        # if not response :
        #     self._connected = False
        #     self._last_message = 'Failed to require CSPEQ00400'
        #     await httpclient.close()
        #     return False
    
        # rsp_msg:str = response.body['rsp_msg']
        # if rsp_msg.__contains__('모의투자'):
        #     self._is_simulation = True

        self._is_simulation = is_simulation

        # 웹소켓 연결
        if wss_domain == '':
            wss_domain = WSS_URL_SIMULATION if self._is_simulation else WSS_URL_REAL
        self._connected = False
        try:
            websocket = await  httpclient.ws_connect(wss_domain + '/websocket')
            self._connected = not websocket.closed
        except :
            pass
    
        if not self._connected:
            await httpclient.close()
            self._last_message = 'websocket connection failed.'
            return False
    
        self._websocket = websocket
        asyncio.create_task(self._websocket_listen())
        
        return True

    async def request(self, tr_cd:str, data:dict
                             ,*
                             , path:str=''
                             , cont_yn:str='N'
                             , cont_key:str=''
                             ) -> ResponseValue | None:
        '''
        TR데이터 요청
        tr_cd: TR코드
        data: 데이터
        return: 성공시 ResponseValue, 실패시 None, 실패시 last_message에 실패사유가 저장됨
        '''
        self._last_message = ''
        if not self._connected:
            self._last_message = 'Not connected'
            return None

        if path == '':
            if not tr_code_to_path.__contains__(tr_cd):
                self._last_message = 'Not supported tr code'
                return None
            path = tr_code_to_path[tr_cd]
    
        headers = {
            'cont_yn' : cont_yn,
            'cont_key' : cont_key,
            }
        if self._mac_address != '':
            headers['mac_address'] = self._mac_address
        
        try:
            response = await self._http.post(BASE_URL + path, headers=headers, data=json.dumps(data))
            if response.status != 200:
                self._last_message = await response.json()
                return None
            body = await response.json()
            return ResponseValue(response.headers['cont_yn'], response.headers['cont_key'], body)
        except Exception as e:
            self._last_message = f'exception: {e}'

        return None

    def add_realtime(self, tr_cd:str, tr_key:str) :
        '''실시간 데이터 요청
        tr_cd: TR코드
        tr_key: TR키/종목코드
        '''
        return self._realtime_request(tr_cd , tr_key, '3' if code_realtime_account.__contains__(tr_cd) else '1')

    def remove_realtime(self, tr_cd:str, tr_key:str) :
        '''실시간 데이터 중지
        tr_cd: TR코드
        tr_key: TR키/종목코드
        '''
        return self._realtime_request(tr_cd, tr_key, '4' if code_realtime_account.__contains__(tr_cd) else '2')

    async def _realtime_request(self, tr_cd:str, tr_key:str, tr_type:str) -> bool:
        if not self._connected:
            self._last_message = 'Not connected'
            return False
        if self._websocket.closed:
            self._last_message = 'websocket closed.'
            return False
        data = f'{{\"header\":{{\"token\":\"{self._access_token}\",\"tr_type\":\"{tr_type}\"}},\"body\":{{\"tr_cd\":\"{tr_cd}\",\"tr_key\":\"{tr_key}\"}}}}'
        await self._websocket.send_str(data)
        return True

    async def _websocket_listen(self):
        async for msg in self._websocket:
            if msg.type == aiohttp.WSMsgType.TEXT:
                try:
                    jsondata = json.loads(msg.data)
                except Exception as e:
                    self._last_message = e
                    await self._inner_on_mesage(f'websocket exception. {e}')
                    continue
                header = jsondata.get('header', None)
                if header is not None:
                    tr_cd = header.get('tr_cd', None)
                    rsp_msg = header.get('rsp_msg', None)
                    if rsp_msg is not None:
                        self._last_message = ''
                        tr_type = header.get('tr_type', None)
                        await self._inner_on_mesage(f'{tr_cd}({tr_type}): {rsp_msg}')
                    body = jsondata.get('body', None)
                    tr_key = header.get('tr_key', None)
                    if body is not None:
                        await self._inner_on_realtime(tr_cd, tr_key, body)
            elif msg.type == aiohttp.WSMsgType.CLOSED:
                self._last_message = msg
                await self._inner_on_mesage(f'websocket closed. {msg}')
                break
            elif msg.type == aiohttp.WSMsgType.ERROR:
                self._last_message = msg
                await self._inner_on_mesage(f'websocket error. {msg}')

    async def _inner_on_mesage(self, msg:str):
        if self._is_async_on_message:
            await self._on_message(self, msg)
        else:
            self._on_message(self, msg)

    async def _inner_on_realtime(self, trcode:str, key:str, realtimedata):
        if self._is_async_on_realtime:
            await self._on_realtime(self, trcode, key, realtimedata)
        else:
            self._on_realtime(self, trcode, key, realtimedata)
