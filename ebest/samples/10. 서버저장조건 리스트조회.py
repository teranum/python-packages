import asyncio
import ebest
from app_keys import appkey, appsecretkey # app_keys.py 파일에 appkey, appsecretkey 변수를 정의하고 사용하세요

async def main():
    api=ebest.OpenApi()
    if not await api.login(appkey, appsecretkey): return print(f"연결실패: {api.last_message}")
    
    request = {
        "t1866InBlock": {
            "user_id": "abcdefgh", # 사용자ID 8자리
            "gb": "0", # 0 : 그룹+조건리스트 조회, 1 : 그룹리스트조회, 2 : 그룹명에 속한 조건리스트조회
            "group_name": "",
            "cont": "0",
            "cont_key": "",
        }
    }
    response = await api.request("t1866", request)
    
    if not response: return print(f"요청실패: {api.last_message}")
    print(response.body)
    
    ... # 다른 작업 수행
    await api.close()

asyncio.run(main())
