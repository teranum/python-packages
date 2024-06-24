tr_code_to_path:dict = {
    # 국내주식주문
    'CSPAT00600' : '/api/v1/trading/kr-stock/order', # 주식종합주문
    'CSPAT00700' : '/api/v1/trading/kr-stock/order-revision', # 주식정정주문
    'CSPAT00800' : '/api/v1/trading/kr-stock/order-cancel', # 주식취소주문
    'CSPAQ04800' : '/api/v1/trading/kr-stock/inquiry/transaction-history', # 체결/미체결조회
    'CSPBQ00100' : '/api/v1/trading/kr-stock/inquiry/able-orderqty', # 주식주문가능수량조회
    'CSPAQ03420' : '/api/v1/trading/kr-stock/inquiry/balance', # 주식잔고조회
    'CDPCQ00100' : '/api/v1/trading/kr-stock/inquiry/acnt-deposit', # 계좌예수금조회
    'CSPEQ00400' : '/api/v1/trading/kr-stock/inquiry/daliy-trade-report', # 일자별매매내역 ...
    'FOCCQ10800' : '/api/v1/trading/kr-stock/inquiry/rdterm-ernrate', # 임의기간수익률집계
    'CSPAQ07800' : '/api/v1/trading/kr-stock/inquiry/stock-ernrate', # 종목별수익률조회
    'CSPAQ00600' : '/api/v1/trading/kr-stock/inquiry/able-crdlimit', # 계좌별신용한도조회
    'CSPAQ09400' : '/api/v1/trading/kr-stock/inquiry/able-crdrepayment', # 신용상환가능총수량조회
    # 국내주식시세
    'JCODES' : '/api/v1/quote/kr-stock/inquiry/stock-ticker', # 주식종목 조회
    'WCODES' : '/api/v1/quote/kr-stock/inquiry/elw-ticker', # ELW 종목 조회
    'PRICE' : '/api/v1/quote/kr-stock/inquiry/price', # 현재가조회
    'HOGA' : '/api/v1/quote/kr-stock/inquiry/orderbook', # 호가조회
    'CONCLUSION' : '/api/v1/quote/kr-stock/inquiry/hour-price', # 시간대별체결조회
    'DAYTRADE' : '/api/v1/quote/kr-stock/inquiry/daily-price', # 일별체결조회
    'RANKLIST' : '/api/v1/quote/kr-stock/inquiry/rank-list', # 주식조건상승하락조회
    # 국내주식시세(실시간)
    'IS1' : '/websocket', # [실시간]주식주문체결
    'IS0' : '/websocket', # [실시간]주식주문접수
    'S01' : '/websocket', # [실시간]주식호가
    'S00' : '/websocket', # [실시간]주식체결가
    'W01' : '/websocket', # [실시간]ELW호가
    'W00' : '/websocket', # [실시간]ELW체결
    'U00' : '/websocket', # [실시간]업종지수체결가
    'U03' : '/websocket', # [실시간]업종지수등락
    'U05' : '/websocket', # [실시간]업종별투자자
    # 국내선물옵션주문
    'CFOAT00100' : '/api/v1/trading/kr-futureoption/order', # 선물옵션 주문
    'CFOAT00200' : '/api/v1/trading/kr-futureoption/order-revision', # 선물옵션 정정주문
    'CFOAT00300' : '/api/v1/trading/kr-futureoption/order-cancel', # 선물옵션 취소주문
    'CFOAQ04000' : '/api/v1/trading/kr-futureoption/inquiry/transaction-history', # 선물옵션 체결조회
    'CFOAQ42400' : '/api/v1/trading/kr-futureoption/inquiry/able-orderqty', # 선물옵션 주문가능수량
    'CFOAQ02500' : '/api/v1/trading/kr-futureoption/inquiry/balance', # 선물옵션 잔고조회
    'CFOAQ50100' : '/api/v1/trading/kr-futureoption/inquiry/balance-evalstatus', # 선물옵션 잔고_평가현황조회
    'CFOAQ02600' : '/api/v1/trading/kr-futureoption/inquiry/day-rlzpnl', # 선물옵션 당일실현손익
    'CFOEQ11100' : '/api/v1/trading/kr-futureoption/inquiry/deposit-detail', # 선물옵션 가정산예탁금 상세
    'CFOHT00100' : '/api/v1/trading/night-futureoption/order', # 선물옵션 주문 (야간)
    'CFOHT00200' : '/api/v1/trading/night-futureoption/order-revision', # 선물옵션 정정주문 (야간)
    'CFOHT00300' : '/api/v1/trading/night-futureoption/order-cancel', # 선물옵션 취소주문 (야간)
    'CFOHQ04000' : '/api/v1/trading/night-futureoption/inquiry/cmedt', # 선물옵션 체결조회 (야간)
    'CFOHQ02500' : '/api/v1/trading/night-futureoption/inquiry/balance', # 선물옵션 잔고조회 (야간)
    # 국내선물옵션시세
    'FCODES' : '/api/v1/quote/kr-futureoption/inquiry/future-ticker', # 선물종목 조회
    'OCODES' : '/api/v1/quote/kr-futureoption/inquiry/option-ticker', # 옵션종목 조회
    'FPRICE' : '/api/v1/quote/kr-futureoption/inquiry/price', # 현재가조회 ...............
    'FHOGA' : '/api/v1/quote/kr-futureoption/inquiry/orderbook', # 호가조회 ...............
    'FDAYTRADE' : '/api/v1/quote/kr-futureoption/inquiry/daily-price', # 일별체결조회 ...............
    'FCONCLUSION' : '/api/v1/quote/kr-futureoption/inquiry/hour-price', # 시간대별체결조회 ...............
    # 국내선물옵션시세(실시간)
    'IF0' : '/websocket', # [실시간]선물옵션주문체결
    'F01' : '/websocket', # [실시간]지수선물호가
    'F00' : '/websocket', # [실시간]지수선물체결
    'F91' : '/websocket', # [실시간]미니지수선물호가
    'F90' : '/websocket', # [실시간]미니지수선물체결
    'F71' : '/websocket', # [실시간]섹터지수선물호가
    'F70' : '/websocket', # [실시간]섹터지수선물체결
    'F21' : '/websocket', # [실시간]주식선물호가
    'F20' : '/websocket', # [실시간]주식선물체결
    'F11' : '/websocket', # [실시간]상품선물호가
    'F10' : '/websocket', # [실시간]상품선물체결
    'O01' : '/websocket', # [실시간]지수옵션호가
    'O00' : '/websocket', # [실시간]지수옵션체결
    'O21' : '/websocket', # [실시간]주식옵션호가
    'O20' : '/websocket', # [실시간]주식옵션체결
    'O91' : '/websocket', # [실시간]미니지수옵션호가
    'O90' : '/websocket', # [실시간]미니지수옵션체결
    'OB1' : '/websocket', # [실시간]K200지수위클리옵션호가
    'OB0' : '/websocket', # [실시간]K200지수위클리옵션체결
    'OA1' : '/websocket', # [실시간]KOSDAQ150옵션호가
    'OA0' : '/websocket', # [실시간]KOSDAQ150옵션체결
    'F40' : '/websocket', # [실시간]선물체결(야간)
    'F41' : '/websocket', # [실시간]선물호가(야간)
    'O30' : '/websocket', # [실시간]옵션체결(야간)
    'O31' : '/websocket', # [실시간]옵션호가(야간)
    # 국내주식/선물차트
    'CHARTTICK' : '/api/v1/quote/kr-chart/tick', # 틱차트조회
    'CHARTMIN' : '/api/v1/quote/kr-chart/min', # 분차트조회
    'CHARTDAY' : '/api/v1/quote/kr-chart/day', # 일차트조회
    'CHARTWEEK' : '/api/v1/quote/kr-chart/week', # 주차트조회
    'CHARTMONTH' : '/api/v1/quote/kr-chart/month', # 월차트조회
    # 해외주식주문
    'CAZCT00100' : '/api/v1/trading/overseas-stock/order', # 해외주식 주문
    'CAZCQ00100' : '/api/v1/trading/overseas-stock/inquiry/transaction-history', # 해외주식 체결내역조회
    'CAZCQ00400' : '/api/v1/trading/overseas-stock/inquiry/balance-margin', # 해외주식 잔고/증거금 조회
    'CAZCQ00200' : '/api/v1/trading/overseas-stock/inquiry/trading-history', # 해외주식 매매내역 조회
    'CAZCQ01600' : '/api/v1/trading/overseas-stock/inquiry/trade-history', # 해외주식 거래내역 조회
    'CAZCQ01300' : '/api/v1/trading/overseas-stock/inquiry/able-orderqty', # 해외주식 주문가능금액 조회
    'CAZCQ00300' : '/api/v1/trading/overseas-stock/inquiry/day-rlzpnl', # 해외주식 실현손익 조회
    'CAZCQ01400' : '/api/v1/trading/overseas-stock/inquiry/deposit-detail', # 해외주식 예수금상세
    'CAZCQ03400' : '/api/v1/trading/overseas-stock/inquiry/avg-pur-price', # 해외주식 평균매입단가 조회
    # 해외주식시세
    'FSTKCODES' : '/api/v1/quote/overseas-stock/inquiry/stock-ticker', # 해외주식 종목조회
    'FSTKPRICE' : '/api/v1/quote/overseas-stock/inquiry/price', # 해외주식 현재가조회
    'FSTKHOGA' : '/api/v1/quote/overseas-stock/inquiry/orderbook', # 해외주식 호가조회
    'FSTKCONCLUSION' : '/api/v1/quote/overseas-stock/inquiry/hour-price', # 해외주식 시간대별체결조회
    'FSTKCHARTTICK' : '/api/v1/quote/overseas-stock/chart/tick', # 해외주식 틱차트조회
    'FSTKCHARTMIN' : '/api/v1/quote/overseas-stock/chart/min', # 해외주식 분차트조회
    'FSTKCHARTDAY' : '/api/v1/quote/overseas-stock/chart/day', # 해외주식 일차트조회
    'FSTKCHARTWEEK' : '/api/v1/quote/overseas-stock/chart/week', # 해외주식 주차트조회
    'FSTKCHARTMONTH' : '/api/v1/quote/overseas-stock/chart/month', # 해외주식 월차트조회
    # 해외주식시세(실시간)
    'IS2' : '/websocket', # [실시간]해외주식 주문체결
    'V60' : '/websocket', # [실시간]해외주식 체결가
    'V61' : '/websocket', # [실시간]해외주식 호가
    'V10' : '/websocket', # [실시간]해외주식 지연체결가
    'V11' : '/websocket', # [실시간]해외주식 지연호가
    # 해외선물옵션주문
    'ph700101o' : '/api/v1/trading/overseas-futureoption/order', # 주문
    'ph700201o' : '/api/v1/trading/overseas-futureoption/order-revision', # 정정/취소주문
    'ph710201o' : '/api/v1/trading/overseas-futureoption/inquiry/able-orderqty', # 주문가능수량조회
    'ph800404o' : '/api/v1/trading/overseas-futureoption/inquiry/product-margin', # 상품별증거금조회
    'ph020101o' : '/api/v1/trading/overseas-futureoption/inquiry/order-history', # 주문내역조회
    'ph020301o' : '/api/v1/trading/overseas-futureoption/inquiry/transaction-history', # 체결내역조회
    'ph020201o' : '/api/v1/trading/overseas-futureoption/inquiry/untransaction-history', # 미체결내역조회
    'ph020401o' : '/api/v1/trading/overseas-futureoption/inquiry/open-interest', # 미결제 약정 조회
    'ph131101o' : '/api/v1/trading/overseas-futureoption/inquiry/daily-open-interest', # 일별 미결제 약정내역
    'ph131601o' : '/api/v1/trading/overseas-futureoption/inquiry/balance', # 예탁잔고현황
    'ph131501o' : '/api/v1/trading/overseas-futureoption/inquiry/deposit', # 예탁자산현황
    'ph135102o' : '/api/v1/trading/overseas-futureoption/inquiry/term-trade-history', # 기간별 거래내역 조회
    # 해외선물옵션시세
    'pibo7042' : '/api/v1/quote/overseas-futureoption/inquiry/orderbook-price', # 호가 & 현재가 조회
    'pibo7044' : '/api/v1/quote/overseas-futureoption/inquiry/daily-price', # 일자별 시세추이
    'pibg7301' : '/api/v1/quote/overseas-futureoption/future-chart/tick', # 해외선물 틱차트조회
    'pibg7302' : '/api/v1/quote/overseas-futureoption/future-chart/min', # 해외선물 분차트조회
    'pibg7303' : '/api/v1/quote/overseas-futureoption/future-chart/dwmonth', # 해외선물 일주월차트조회
    'pibg7401' : '/api/v1/quote/overseas-futureoption/option-chart/tick', # 해외옵션 틱차트조회
    'pibg7402' : '/api/v1/quote/overseas-futureoption/option-chart/min', # 해외옵션 분차트조회
    'pibg7403' : '/api/v1/quote/overseas-futureoption/option-chart/dwmonth', # 해외옵션 일주월차트조회
    # 해외선물옵션시세(실시간)
    'O' : '/websocket', # [실시간]주문체결
    'P' : '/websocket', # [실시간]잔고
    'L01' : '/websocket', # [실시간]해외선물호가
    'K01' : '/websocket', # [실시간]해외선물시세
    'K02' : '/websocket', # [실시간]해외옵션시세
    'L02' : '/websocket', # [실시간]해외옵션호가
    # 장내채권주문
    'CSPAT02000' : '/api/v1/trading/krx-bond/order', # 채권주문
    'CSPAT02100' : '/api/v1/trading/krx-bond/order-revision', # 채권정정주문
    'CSPAT02200' : '/api/v1/trading/krx-bond/order-cancel', # 채권취소주문
    'CSPAQ05700' : '/api/v1/trading/krx-bond/inquiry/transaction-history', # 채권주문체결조회
    'CSPAQ01200' : '/api/v1/trading/krx-bond/inquiry/balance', # 채권잔고조회
    'CSPAQ07900' : '/api/v1/trading/krx-bond/inquiry/balance-evalstatus', # 채권잔고평가조회
    # 장내채권시세
    'BO_SEARCH' : '/api/v1/quote/krx-bond/search', # 장내채권 상세검색
    'BO_SISE' : '/api/v1/quote/krx-bond/inquiry/price', # 장내채권 현재가조회
    'BO_HOGA' : '/api/v1/quote/krx-bond/inquiry/orderbook', # 장내채권 호가조회
    #장내채권시세(실시간)
    'B00' : '/websocket', # [실시간]일반채권체결
    'B01' : '/websocket', # [실시간]일반채권호가
    'B10' : '/websocket', # [실시간]소액채권체결
    'B11' : '/websocket', # [실시간]소액채권호가
    }
