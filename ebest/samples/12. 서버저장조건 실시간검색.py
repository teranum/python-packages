import asyncio
import ebest
from app_keys import *

# 실시간검색은 실서버에서만 가능

async def main():
    api=ebest.OpenApi()
    api.on_message = on_message
    api.on_realtime = on_realtime
    if not await api.login(appkey, appsecretkey): return print(f"연결실패: {api.last_message}")
    
    request = {
        "t1860InBlock": {
            "sSysUserFlag": "U", # 'U' 고정
            "sFlag": "E", # 'E:'등록, 'D':중지
            "sAlertNum": "", # Flag 값 'D':중지 일떄만 입력 - 등록 요청 시 수신받은 t1860OutBlock.sAlertNum 값
            "query_index": cond_query_index, # t1866 TR에서 조회한 t1866OutBlock1.query_index
        }
    }
    response = await api.request("t1860", request)
    
    if not response: return print(f"요청실패: {api.last_message}")
    print(response.body)
    
    sAlertNum:str = response.body["t1860OutBlock"]["sAlertNum"]
    if sAlertNum == "":
        print("실시간검색 등록실패")
    else:
        print("실시간검색 등록성공")
        await api.add_realtime("AFR", sAlertNum)
        await asyncio.sleep(60) # 60초동안 유효, 후에 중지
        await api.remove_realtime("AFR", sAlertNum)
        await asyncio.sleep(1)
    
    ... # 다른 작업 수행
    await api.close()

def on_message(api:ebest.OpenApi, msg:str): print(f"on_message: {msg}")

def on_realtime(api:ebest.OpenApi, trcode, key, realtimedata):
    if trcode == "AFR":
        print(f"실시간조건검색: {trcode}, {key}, {realtimedata}")

asyncio.run(main())
