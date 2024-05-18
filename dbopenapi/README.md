# DB증권 OpenApi Package

This is a simple package for DB RestAPI version.

## Installation

```bash
pip install dbopenapi
```

## Usage
모든 요청은 비동기로 처리되며, 요청에 대한 응답은 await 키워드를 사용하여 받을 수 있습니다.
<BR/>
Samples: https://github.com/teranum/db-openapi-samples

### 로그인 요청은 반드시 먼저 수행되어야 하며, 로그인이 성공하면 다른 요청을 수행할 수 있습니다.
```python
import asyncio
import dbopenapi
from app_keys import appkey, appsecretkey # app_keys.py 파일에 appkey, appsecretkey 변수를 정의하고 사용하세요

async def main():
    api=dbopenapi.OpenApi()
    
    logined:bool = False
    logined = await api.login(appkey, appsecretkey)
    
    # 옵션1: 당일 발급받은 access_token 이 있는 경우, access_token 으로 로그인
    # logined = await api.login('', '', access_token=saved__access_token)
    
    # 옵션2: 모의투자 일 경우 is_simulation 옵션을 True 로 설정
    # logined = await api.login(appkey, appsecretkey, is_simulation=True)
    
    # 옵션3: 해외선물옵션인 경우 wss_domain 옵션을 dbopenapi.WSS_URL_GLOBAL 로 설정
    # logined = await api.login(appkey, appsecretkey, wss_domain=dbopenapi.WSS_URL_GLOBAL)

    if not logined:
        print(f'연결실패: {api.last_message}')
        return
    
    print('연결성공, 접속서버: ' + ('모의투자' if api.is_simulation else '실투자'))
    
    # 발급된 access_token 출력
    print('access_token: ', api.access_token)
    
    ... # 다른 작업 수행
    await api.close()

asyncio.run(main())
```

