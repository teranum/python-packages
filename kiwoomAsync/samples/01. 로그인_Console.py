import sys, asyncio
from PyQt5.QtWidgets import QApplication
from qasync import QEventLoop
from kiwoomAsync import KhAsync

global api # 전역변수로 선언

async def main():

    # 비동기 로그인 함수 호출
    (ret, msg) = await api.CommConnectAsync()
    if ret != 0:
        print(f'로그인 실패: {msg}')
        return
    print('로그인 성공: ' + ('모의투자' if api.GetLoginInfo("GetServerGubun") == '1' else '실투자'))

    # 계좌정보 조회
    accounts = api.GetLoginInfo('ACCTLIST_DETAIL').split(';')[:-1];
    print(f'계좌정보: {accounts}')

    # 삼성전자 기본정보 조회 (opt10001, 싱글데이터)
    code = '005930'
    response = await api.RequestTrAsync('opt10001', {'종목코드': code}
                                        , ['종목명', '현재가'])
    if response.result_code != 0:
        print(f'종목정보 조회 실패: {response.msg}')
        return
    print(f'종목명: {response.single_datas[0]}, 현재가: {response.single_datas[1]}')

    # 삼성전자 60분봉 조회 (opt10080, 싱글데이터+멀티데이터)
    times = 60
    response = await api.RequestTrAsync('opt10080', {'종목코드': code, '틱범위': str(times), '수정주가구분': '1'}
                                        , ['종목코드']
                                        , ['체결시간', '시가', '고가', '저가', '현재가', '거래량'])
    if response.result_code != 0:
        print(f'차트 조회 실패: {response.msg}')
        return
    print(f'종목코드: {response.single_datas[0]}, {times}분봉 차트 데이터 개수: {len(response.multi_datas)}')
    last_candle = response.multi_datas[0]
    print(f'최근봉 시간/시고저종/거래량: {last_candle[0]}, {last_candle[1]}, {last_candle[2]}, {last_candle[3]}, {last_candle[4]}, {last_candle[5]}')

    # 조건검색식 목록 조회
    (ret, condlist) = await api.GetConditionLoadAsync()
    if ret != 1:
        print(f'조건검색식 목록 조회 실패: {condlist}')
        return
    conds = condlist.split(';')[:-1]
    print(f'조건검색식 목록: {conds}')
    ... # 이하 생략


if __name__ == '__main__':
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    api = KhAsync()

    with loop:
        loop.run_until_complete(main())
        loop.run_forever()


# 실행결과:
'''
로그인 성공: 모의투자
계좌정보: ['1234567890,상시_XX,선물옵션', '2345678901,상시_YY,위탁']
종목명: 삼성전자, 현재가: +74300
종목코드: 삼성전자, 60분봉 차트 데이터 개수: 900
최근봉 시간/시고저종/거래량: 20240830150000, +74700, +74800, +74300, +74300, 5758172
조건검색식 목록: ['000^조건식1', '001^조건식2', '002^조건식3', '003^조건식4']
'''