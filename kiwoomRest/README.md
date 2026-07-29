# kiwoomRest

> 키움증권 OpenAPI REST 서비스를 위한 비동기 Python 클라이언트 패키지

[![PyPI](https://img.shields.io/pypi/v/kiwoomRest)](https://pypi.org/project/kiwoomRest/)
[![Python](https://img.shields.io/pypi/pyversions/kiwoomRest)](https://pypi.org/project/kiwoomRest/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 목차

- [설치](#설치)
- [빠른 시작](#빠른-시작)
- [사용 예제](#사용-예제)
  - [국내주식 조회 / 연속조회](#국내주식-조회--연속조회)
  - [미국주식 조회](#미국주식-조회)
  - [조건검색 조회 / 실시간](#조건검색-조회--실시간)
  - [실시간 시세 등록 / 해제](#실시간-시세-등록--해제)
- [API 레퍼런스](#api-레퍼런스)
  - [프로퍼티](#프로퍼티)
  - [메소드](#메소드)
  - [이벤트](#이벤트)
  - [ResponseData](#responsedata)

---

## 설치

```bash
pip install kiwoomRest
```

---

## 빠른 시작

> **⚠️ 모든 요청은 비동기(`async/await`)로 처리됩니다.**  
> 로그인은 반드시 다른 요청보다 먼저 수행되어야 합니다.

```python
import asyncio
from kiwoomRest import KwRestApi
from app_keys import appkey, secretkey  # app_keys.py에 appkey, secretkey 변수를 정의하세요

async def main():
    api = KwRestApi()

    # 실시간 이벤트 핸들러 등록
    api.on_realtime.connect(lambda data: print(f"실시간: {data}"))

    # 국내주식 실거래 로그인 (모의투자: is_simulation=True)
    if not await api.login(appkey, secretkey, is_simulation=False):
        print(f"로그인 실패: {api.last_message}")
        return
    print("로그인 성공")

    # 작업 수행...
    await asyncio.sleep(5)

    await api.close()

asyncio.run(main())
```

**미국주식 로그인**

```python
# 미국주식 실거래 로그인 (모의투자: is_simulation=True)
if not await api.login(appkey, secretkey, is_simulation=False, is_us=True):
    print(f"로그인 실패: {api.last_message}")
    return
```

---

## 사용 예제

### 국내주식 조회 / 연속조회

```python
# 종목정보 리스트 조회
inputs = {
    "mrkt_tp": "0"  # 0:코스피, 10:코스닥, 3:ELW, 8:ETF, 30:K-OTC, 50:코넥스
}
response = await api.request("ka10099", inputs)

# 주식 종목정보 조회 (삼성전자)
inputs = {"stk_cd": "005930"}
response = await api.request("ka10001", inputs)

# 주식 일봉 차트 조회
inputs = {
    "stk_cd":       "005930",   # 종목코드
    "base_dt":      "00000000", # 기준일자 (00000000: 현재일)
    "upd_stkpc_tp": "1"         # 수정주가 적용여부 (0:미적용, 1:적용)
}
response = await api.request("ka10081", inputs)

# 연속조회
while response.return_code == 0 and response.cont_yn == "Y":
    response = await api.request("ka10081", inputs,
                                 cont_yn=response.cont_yn,
                                 next_key=response.next_key)

# 결과 확인
if response.return_code == 0:
    print("조회 성공:", response.body)
else:
    print(f"조회 실패: {response.return_msg}")
```

---

### 미국주식 조회

```python
# 미국주식 조건검색 목록 조회
inputs = {"trnm": "GCNSRLST"}
response = await api.request("usa20280", inputs)

if response.return_code == 0:
    print("조회 성공:", response.body)
else:
    print(f"조회 실패: {response.return_msg}")
```

---

### 조건검색 조회 / 실시간

```python
# 서버저장 조건 리스트 조회
response = await api.request("ka10171", {"trnm": "CNSRLST"})

# 조건검색 일반 조회
inputs = {
    "trnm":        "CNSRREQ",  # 고정값
    "seq":         "4",        # 조건검색식 일련번호
    "search_type": "0",        # 0:일반조회
    "stex_tp":     "K",        # K:KRX
    "cont_yn":     "N",        # Y:연속조회, N:단순조회
    "next_key":    ""
}
response = await api.request("ka10172", inputs)

# 조건검색 실시간 등록
api.on_realtime.connect(print)
inputs = {
    "trnm":        "CNSRREQ",
    "seq":         "4",
    "search_type": "1",        # 1:조건검색+실시간
    "stex_tp":     "K"
}
response = await api.realtime(inputs)

if response.return_code != 0:
    print(f"실시간 등록 실패: {response.return_msg}")
else:
    print("실시간 등록 성공")
    await asyncio.sleep(60)    # 60초 수신

    # 실시간 해제
    await api.realtime({"trnm": "CNSRCLR", "seq": "4"})
    print("실시간 해제 완료")
```

---

### 실시간 시세 등록 / 해제

```python
def on_realtime(data):
    print(f"실시간 이벤트: {data}")

api.on_realtime.connect(on_realtime)

# 삼성전자 실시간 체결시세 등록
inputs = {
    "trnm":    "REG",
    "grp_no":  "1",
    "refresh": "1",
    "data": [{
        " item": ["005930"],   # 종목코드 (복수: ["005930", "000660"])
        " type": ["0B"]        # 0B:체결시세, 0C:우선호가시세
    }]
}
response = await api.realtime(inputs)

await asyncio.sleep(60)  # 60초 수신

# 실시간 시세 해제
inputs["trnm"] = "REMOVE"
await api.realtime(inputs)
```

---

## API 레퍼런스

### 프로퍼티

| 프로퍼티 | 타입 | 설명 |
|---|---|---|
| `connected` | `bool` | 연결 여부 (`True`: 연결됨) |
| `is_simulation` | `bool` | 모의투자 여부 (`True`: 모의투자) |
| `is_us` | `bool` | 미국주식 여부 (`True`: 미국주식) |
| `access_token` | `str` | 발급된 액세스 토큰 |
| `last_message` | `str` | 마지막 메시지 (로그인/요청 실패 시 사유) |
| `last_response` | `ResponseData \| None` | 마지막 요청의 응답 데이터 |
| `timeout` | `int` | 요청 타임아웃(초), 기본값: `5` |

---

### 메소드

#### `login`
```python
await api.login(appkey, secretkey, is_simulation=False, is_us=False) -> bool
```
| 파라미터 | 타입 | 설명 |
|---|---|---|
| `appkey` | `str` | 앱키 |
| `secretkey` | `str` | 앱 시크릿키 |
| `is_simulation` | `bool` | 모의투자 서버 사용 여부, 기본값: `False` |
| `is_us` | `bool` | 미국주식 서버 사용 여부, 기본값: `False` |
| **return** | `bool` | 성공: `True`, 실패: `False` (실패 사유는 `last_message` 참조) |

---

#### `request`
```python
await api.request(api_id, indatas, *, cont_yn='N', next_key='', path=None) -> ResponseData
```
| 파라미터 | 타입 | 설명 |
|---|---|---|
| `api_id` | `str` | TR 코드 (api-id) |
| `indatas` | `dict` | 요청 데이터 |
| `cont_yn` | `str` | 연속조회 여부 (`Y`/`N`), 기본값: `N` |
| `next_key` | `str` | 연속조회 키, 기본값: `""` |
| `path` | `str \| None` | 요청 경로 (생략 시 자동 설정), ex) `'/api/dostk/stkinfo'` |
| **return** | `ResponseData` | 응답 데이터 (`return_code == 0`: 성공) |

---

#### `realtime`
```python
await api.realtime(indatas) -> ResponseData
```
| 파라미터 | 타입 | 설명 |
|---|---|---|
| `indatas` | `dict` | 실시간 요청 데이터 (`trnm` 필드 필수) |
| **return** | `ResponseData` | 응답 데이터 (`return_code == 0`: 성공) |

---

#### `close`
```python
await api.close() -> None
```
웹소켓 및 HTTP 세션 연결을 종료합니다.

---

### 이벤트

#### `on_message`
웹소켓 오류/연결 종료 시 발생합니다.
```python
api.on_message.connect(callback)  # callback(msg: str)
```
| 발생 상황 | 메시지 형식 |
|---|---|
| 예외 발생 | `'websocket exception. {e}'` |
| 연결 종료 | `'websocket closed. {msg}'` |
| 오류 발생 | `'websocket error. {msg}'` |

#### `on_realtime`
실시간 데이터 수신 시 발생합니다.
```python
api.on_realtime.connect(callback)  # callback(realdatas: dict)
```

**이벤트 핸들러 연결/해제**
```python
api.on_message.connect(my_handler)     # 연결
api.on_message.disconnect(my_handler)  # 해제
api.on_message.disconnect_all()        # 전체 해제
```

---

### ResponseData

| 필드 | 타입 | 설명 |
|---|---|---|
| `return_code` | `int` | 응답 코드 (`0`: 성공, 그 외: 실패) |
| `return_msg` | `str` | 응답 메시지 |
| `body` | `dict` | 응답 데이터 (조회 결과) |
| `cont_yn` | `str` | 연속조회 여부 (`Y`: 다음 페이지 있음) |
| `next_key` | `str` | 연속조회 키 |
| `api_id` | `str` | 요청 TR 코드 |
| `path` | `str` | 요청 경로 (URL) |
| `elapsed_ms` | `float` | 요청 소요 시간 (ms) |
