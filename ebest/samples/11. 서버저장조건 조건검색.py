import asyncio
import ebest
from app_keys import *

async def main():
    api=ebest.OpenApi()
    if not await api.login(appkey, appsecretkey): return print(f"연결실패: {api.last_message}")
    
    request = {
        "t1859InBlock": {
            "query_index": cond_query_index, # t1866 TR에서 조회한 t1866OutBlock1.query_index
        }
    }
    response = await api.request("t1859", request)
    
    if not response: return print(f"요청실패: {api.last_message}")
    print(response.body)
    
    ... # 다른 작업 수행
    await api.close()


asyncio.run(main())
