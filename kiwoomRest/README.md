# kiwoomRest Package

키움증권 REST API 간편이용 패키지.

## Installation

```bash
pip install kiwoomRest
```

## Usage
모든 요청은 비동기로 처리되며, 요청에 대한 응답은 await 키워드를 사용하여 받을 수 있습니다.
<BR/>
Samples: https://github.com/teranum/kiwoom-restapi-samples

### 로그인 요청은 반드시 먼저 수행되어야 하며, 로그인이 성공하면 다른 요청을 수행할 수 있습니다.
```python
import asyncio
from kiwoomRest import KwRestApi
from app_keys import appkey, secretkey # app_keys.py 파일에 appkey, secretkey 변수를 정의하고 사용하세요

async def main():
    # Kiwoom API 객체 생성
    api = KwRestApi()

    # 실시간 이벤트 핸들러 등록
    api.on_realtime.connect(lambda realdatas: print(f"on_realtime: {realdatas}"))

    # 로그인
    ret = await api.login(appkey, secretkey, is_simulation=False) # 실거래서버 사용, 모의투자서버 사용시 is_simulation=True
    if not ret:
        print(api.last_message)
        return
    print("Login success")

    # 다른 작업...
    await asyncio.sleep(5)

    # 연결 종료
    await api.close()


asyncio.run(main())
```

### 조회/연속 요청
```python
    # 종목정보 리스트 조회
    inputs = {
        "mrkt_tp": "0" # 시장구분: 0:코스피, 10:코스닥, 3:ELW, 8:ETF, 30:K-OTC, 50:코넥스, 5:신주인수권, 4:뮤추얼펀드, 6:리츠, 9:하이일드
    }
    response = await api.request("ka10099", inputs)
    
    # 주식 종목정보 조회
    inputs = {
        "stk_cd" : "005930" # 종목코드: 삼성전자
    }
    response = await api.request("ka10001", inputs)

    # 주식 차트 조회
    inputs = {
        "stk_cd": "005930",     # 종목코드: 삼성전자
        "base_dt": "00000000",  # 기준일자: 00000000(현재일자)
        "upd_stkpc_tp": "1"     # 수정주가구분: 0(미적용), 1(적용)
    }
    response = await api.request("ka10081", inputs)

    # 연속조회
    if response.cont_yn == "Y":
        response = await api.request("t8410", request, cont_yn=response.cont_yn, next_key=response.next_key)

    # response 출력
    if response.return_code == 0:
        print("조회 성공")
        print(response.body)
    else:
        print(f"조회 실패: {response.return_msg}")

```

### 조건검색 조회/실시간
```python
    # 서버저장조건 리스트조회
    inputs = {
        "trnm" : "CNSRLST"      # CNSRLST 고정값
    }
    response = await api.request("ka10171", inputs)

    # 조건검색 요청 일반
    inputs = {
        "trnm" : "CNSRREQ",     # CNSRREQ 고정값
        "seq" : "4",            # 조건검색식 일련번호
        "search_type" : "0",    # 0:조건검색 
        "stex_tp" : "K",        # K:KRX
        "cont_yn" : "N",        # 연속조회여부 (Y:연속조회, N:단순조회)
        "next_key" : ""         # 연속조회키 (연속조회여부가 'Y'인 경우 필수 세팅)
    }
    response = await api.request("ka10172", inputs)

    # 조건검색 실시간 검색 등록
    api.on_realtime.connect(print) # 실시간 이벤트 핸들러 등록
    inputs = {
        "trnm" : "CNSRREQ",     # CNSRREQ 고정값
        "seq" : "4",            # 조건검색식 일련번호
        "search_type" : "1",    # 1: 조건검색+실시간조건검색
        "stex_tp" : "K"         # K:KRX
    }
    response = await api.realtime(inputs)
    
    if response.return_code != 0:
        print(f"실시간검색 등록실패: {response.return_msg}")
        return

    print("실시간검색 등록성공")
    print(response.body)

    await asyncio.sleep(60) # 60초동안 유효, 후에 중지

    # 조건검색 실시간 해제
    inputs = {
        "trnm" : "CNSRCLR",     # CNSRCLR 고정값
        "seq" : "4",            # 조건검색식 일련번호
    }
    response = await api.realtime(inputs)
    print("실시간검색 해제")

```

### 웹소켓 실시간 시세 등록/해제
```python
    api.on_realtime.connect(on_realtime) # 실시간 이벤트 핸들러 연결

    # 삼성전자 실시간 체결 시세 등록
    inputs = {
        "trnm" : "REG",
        "grp_no" : "1",
        "refresh" : "1",
        "data" : [{
            " item" : ["005930"],   # 삼성전자. or SK하이닉스 함께 등록할 경우 ["005930", "000660"] 로 설정
            " type" : ["0B"]        # 체결시세. or 우선호가시세 함께 등록할 경우 ["0B", "0C"]로 설정
        }]
    }
    response = await api.realtime(inputs)
    
    # 60초후 실시간 시세 중지
    await asyncio.sleep(60)

    # 실시간 시세 해제 시 "REG" -> "REMOVE" 로 변경
    inputs["trnm"] = "REMOVE"
    response = await api.realtime(inputs)

def on_realtime(realdatas):
    print(f"실시간이벤트: {realdatas}")

```

## 프로퍼티, 메소드, 이벤트
```python
# 프로퍼티
    connected -> bool: 연결여부 (연결: True, 미연결: False)
    is_simulation -> bool: 모의투자 여부 (모의투자: True, 실거래: False))
    access_token -> str: 발급된 엑세스토큰
    last_message -> str: 마지막 메시지, 로그인 또는 요청 실패시 사유 저장

# 메소드
    login(appkey:str, secretkey:str, is_simulation:bool = False) -> bool: 로그인
        appkey:str - 앱키
        secretkey:str - 앱시크릿키
        is_simulation:bool - 모의서버 사용여부 (모의서버: True, 실거래서버: False), 기본값: False
        reutrn: bool - 로그인 성공여부 (성공: True, 실패: False), 실패시 last_message에 실패 사유 저장
        
    request(api_id:str, indatas:dict, *, cont_yn:str='N', next_key:str='0', path:str=None) -> ResponseData: TR요청
        api_id:str - api-id (TR코드)
        indatas:dict - 요청 데이터
        * - cont_yn, next_key, path는 옵션(기본값으로 설정됨)
        cont_yn:str - 연속조회여부 (연속조회: 'Y', 단순조회: 'N'), 기본값: 'N'
        next_key:str - 연속조회키 (연속조회여부가 'Y'인 경우 필수 세팅), 기본값: '0'
        path:str - PATH경로, 기본값: None(자동으로 설정 됨), 설정 필요시 URL값으로 세팅 ex) '/api/dostk/stkinfo'
        return: ResponseData - 응답 데이터, 요청 성공 여부는 return_code로 확인 가능 (0: 성공, 그 외: 실패)
    
    realtime(indatas:dict) -> ResponseData: 실시간 등록/해제
        indatas:dict - 실시간 요청 데이터
        return: ResponseData - 응답 데이터, 요청 성공 여부는 return_code로 확인 가능 (0: 성공, 그 외: 실패)
        
    close() -> None: 연결 종료


# 이벤트:
    on_message(msg:str): 메시지 수신 이벤트 (웹소켓 오류시 발생)
        msg - 메시지
        - ex.1 ) 'websocket exception. {e}'
        - ex.2 ) 'websocket closed. {msg}'
        - ex.3 ) 'websocket error. {msg}'
        
    on_realtime(realdatas:dict): 실시간 수신 이벤트 (실시간 데이터 수신시 발생)
        realdatas - 실시간 데이터

    이벤트 핸들러 연결 : api 객체 생성시 연결
        api = KwRestApi()
        api.on_message.connect(print)
        api.on_realtime.connect(print)

# 응답데이터 : ResponseData
    return_code -> int: 응답코드 (0: 성공, 그 외: 실패)
    return_msg -> str: 응답메시지 (성공/실패 메시지)
    body -> dict: 응답데이터 (조회결과 데이터)
    cont_yn -> str: 연속조회여부 (연속조회 있을 경우: 'Y'로 세팅됨)
    next_key -> str: 연속조회키

    api_id -> str: 요청 api-id (TR코드)
    path -> str: 요청 PATH경로(URL)
```
