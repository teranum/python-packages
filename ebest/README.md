# ebest Package

This is a simple package for eBEST OpenApi.
이베스트증권에서 LS증권으로 사명변경 (2024.06.01), 버젼1.0.0부터 LS증권 OpenApi를 지원합니다.

## Installation

```bash
pip install ebest
```

## Usage
모든 요청은 비동기로 처리되며, 요청에 대한 응답은 await 키워드를 사용하여 받을 수 있습니다.
<BR/>
Samples: https://github.com/teranum/ebest-openapi-samples

### 로그인 요청은 반드시 먼저 수행되어야 하며, 로그인이 성공하면 다른 요청을 수행할 수 있습니다.
```python
import asyncio
import ebest
from app_keys import appkey, appsecretkey # app_keys.py 파일에 appkey, appsecretkey 변수를 정의하고 사용하세요

async def main():
    api=ebest.OpenApi()
    if not await api.login(appkey, appsecretkey): return print(f"연결실패: {api.last_message}")
    print("연결성공, 접속서버: " + ("모의투자" if api.is_simulation else "실투자"))
    
    ... # 다른 작업 수행

    await api.close()

asyncio.run(main())
```

### 조회/연속 요청
```python
    # 주식 전종목 조회
    request = {
        "t8436InBlock": {
            "gubun": "0", # 구분(0: 전체, 1: 코스피, 2: 코스닥)
        }
    }
    response = await api.request("t8436", request)
    
    # 주식 종목별 시세 조회
    request = {
        "t1102InBlock": {
            "shcode": "005930", # 삼성전자
        }
    }
    response = await api.request("t1102", request)

    # 주식 차트 조회
    request = {
        "t8410InBlock": {
            "shcode": "005930", # 삼성전자
            "gubun": "2", # 주기구분(2:일3:주4:월5:년)
            "qrycnt": 100, # 요청건수(최대-압축:2000비압축:500)
            "sdate": "", # 시작일자
            "edate": "99999999", # 종료일자
            "cts_date": "", # 연속일자
            "comp_yn": "N", # 압축여부(Y:압축N:비압축)
            "sujung": "Y", # 수정주가여부(Y:적용N:비적용)
        }
    }
    response = await api.request("t8410", request)

    # 연속조회
    if response.tr_cont == "Y":
        await asyncio.sleep(1) # 1초 대기
        request["t8410InBlock"]["cts_date"] = response.body["t8410OutBlock"]["cts_date"]
        response = await api.request("t8410", request, tr_cont=response.tr_cont, tr_cont_key=response.tr_cont_key)

```

### 조건검색 리스트 조회/실시간 요청
```python
    api.on_realtime = on_realtime # 실시간 이벤트 핸들러 등록
    # 서버저장조건 리스트조회
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

    # 서버저장조건 실시간검색
    request = {
        "t1860InBlock": {
            "sSysUserFlag": "U", # 'U' 고정
            "sFlag": "E", # 'E:'등록, 'D':중지
            "sAlertNum": "", # Flag 값 'D':중지 일떄만 입력 - 등록 요청 시 수신받은 t1860OutBlock.sAlertNum 값
            "query_index": "0", # t1866 TR에서 조회한 t1866OutBlock1.query_index
        }
    }
    response = await api.request("t1860", request)
    
    sAlertNum:str = response.body["t1860OutBlock"]["sAlertNum"]
    if sAlertNum == "":
        print("실시간검색 등록실패")
    else:
        print("실시간검색 등록성공")
        await api.add_realtime("AFR", sAlertNum) # 실시간검색 등록
        await asyncio.sleep(60) # 60초동안 유효, 후에 중지
        await api.remove_realtime("AFR", sAlertNum) # 실시간검색 중지

def on_realtime(api, trcode, key, realtimedata):
    if trcode == "AFR":
        print(f"실시간조건검색: {trcode}, {key}, {realtimedata}")

```

### 웹소켓 실시간 요청/응답
```python
    api.on_realtime.connect(on_realtime) # 실시간 이벤트 핸들러 연결

    # 삼성전자 주식 실시간 시세 요청
    await api.add_realtime("S3_", "005930") # 삼성전자 주식 실시간 시세 요청
    
    # 60초후 삼성전자 주식 실시간 시세 중지
    await asyncio.sleep(60)
    await api.remove_realtime("S3_", "005930") # 삼성전자 주식 실시간 시세 중지

def on_realtime(api, trcode, key, realtimedata):
    if trcode == "S3_":
        print(f"체결시세: {trcode}, {key}, {realtimedata}")

```

## 프로퍼티, 메소드, 이벤트
```python
# 프로퍼티
    connected -> bool: 연결여부 (연결: True, 미연결: False)
    is_simulation -> bool: 모의투자인지 여부 (모의투자: True, 실거래: False))
    last_message -> str: 마지막 메시지
    mac_address -> str: MAC주소 (법인인 경우 필수 세팅)

# 메소드
    login(appkey:str, appsecretkey:str) -> bool: 로그인
        appkey:str - 앱키
        appsecretkey:str - 앱시크릿키
        reutrn: bool - 로그인 성공여부 (성공: True, 실패: False)
        
    request(tr_cd:str, data:dict, *, path:str=None, tr_cont:str='N', tr_cont_key:str='0') -> None: 요청
        tr_cd:str - TR 코드
        data:dict - 요청 데이터
        * - path, tr_cont, tr_cont_key는 옵션(기본값으로 설정됨)
        path:str - PATH경로, 기본값: None, 설정 필요시 URL값으로 세팅 ex) '/stock/market-data'
        tr_cont:str - 연속조회여부 (연속조회: 'Y', 단순조회: 'N'), 기본값: 'N'
        tr_cont_key:str - 연속조회키 (연속조회여부가 'Y'인 경우 필수 세팅), 기본값: '0'
        return: 응답 데이터 (dict), 요청 실패시 None
    
    add_realtime(tr_cd:str, tr_key:str) -> bool: 실시간 등록
        tr_cd:str - TR 코드
        tr_key:str - 키
        return: bool - 성공여부 (성공: True, 실패: False)
        
    remove_realtime(tr_cd:str, tr_key:str) -> bool: 실시간 해제
        tr_cd:str - TR 코드
        tr_key:str - 키
        return: bool - 성공여부 (성공: True, 실패: False)
        
    close() -> None: 연결 종료

# 이벤트:
    on_message(api, msg:str): 메시지 수신 이벤트 (실시간 구독/해지 또는 웹소켓 오류시 발생)
        api - 이벤트 발생한 API 객체
        msg - 메시지
        - ex.1 ) 'S3_(3): 정상처리되었습니다'
        - ex.2 ) 'websocket exception. {e}'
        - ex.3 ) 'websocket closed. {msg}'
        - ex.4 ) 'websocket error. {msg}'
        
    on_realtime(api, trcode:str, key:str, realtimedata:dict): 실시간 수신 이벤트 (실시간 데이터 수신시 발생)
        api - 이벤트 발생한 API 객체
        trcode - TR 코드
        key - 키
        realtimedata - 실시간 데이터

    이벤트 핸들러 연결 : api 객체 생성시 연결
        api = ebest.OpenApi()
        api.on_message.connect(my_on_message)
        api.on_realtime.connect(my_on_realtime)
```
