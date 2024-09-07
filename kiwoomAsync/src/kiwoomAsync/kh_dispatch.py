class KHOpenApiDispatch(object):

    def CommConnect(self) -> int: 
        '''
        수동 로그인설정인 경우 로그인창을 출력.
        자동로그인 설정인 경우 로그인창에서 자동으로 로그인을 시도합니다.

        Returns:
        0: 성공, other: 실패

        요청이 성공하면 <OnEventConnect> 이벤트가 발생합니다.
        '''
        ...

    def CommTerminate(self) -> None:
        '''
        프로그램 종료없이 서버와의 접속만 단절시키는 함수입니다.
        ※ 함수 사용 후 사용자의 오해소지가 생기는 이유로 더 이상 사용할 수 없는 함수입니다.
        '''
        ...

    def CommRqData(self, sRQName: str, sTrCode: str, nPrevNext: int, sScreenNo: str) -> int:
        '''
        조회요청 함수입니다.
        조회데이터는 <OnReceiveTrData> 이벤트로 수신됩니다.

        Args:
        sRQName: 사용자 구분명 (임의로 지정, 한글지원)
        sTrCode: 조회하려는 TR이름
        nPrevNext: 연속조회여부
        sScreenNo: 화면번호 (4자리 숫자 임의로 지정)

        Returns:
        0: 성공, other: 실패

        요청이 성공하면 <OnReceiveTrData> 이벤트가 발생합니다.
        '''
        ...

    def GetLoginInfo(self, sTag: str) -> str:
        '''
        로그인 후 사용할 수 있으며 인자값에 대응하는 정보를 얻을 수 있습니다.

        Args:
        sTag: 사용자 정보 구분 TAG값
        "ACCOUNT_CNT" : 보유계좌 갯수를 반환합니다.
        "ACCLIST" 또는 "ACCNO" : 구분자 ';'로 연결된 보유계좌 목록을 반환합니다.
        "ACCTLIST_DETAIL" : 구분자 ';'로 연결된 보유계좌, 그 안에서 ','로 계좌번호, 계좌명, 계좌상품(위탁종합, 선물옵션, Fx마진, 해외선물, 금현물) 목록을 반환합니다.
        "USER_ID" : 사용자 ID를 반환합니다.
        "USER_NAME" : 사용자 이름을 반환합니다.
        "GetServerGubun" : 접속서버 구분을 반환합니다.(1 : 모의투자, 나머지 : 실거래 서버)
        "KEY_BSECGB" : 키보드 보안 해지여부를 반환합니다.(0 : 정상, 1 : 해지)
        "FIREW_SECGB" : 방화벽 설정여부를 반환합니다.(0 : 미설정, 1 : 설정, 2 : 해지)

        Returns:
        사용자 정보
        '''
        ...

    def SendOrder(self, sRQName: str, sScreenNo: str, sAccNo: str, nOrderType: int, sCode: str, nQty: int, nPrice: int, sHogaGb: str, sOrgOrderNo: str) -> int:
        '''
        서버에 주문을 전송하는 함수 입니다.

        Args:
        sRQName: 사용자 구분명 (임의로 지정, 한글지원)
        sScreenNo: 화면번호 (4자리 숫자 임의로 지정)
        sAccNo: 계좌번호 10자리
        nOrderType: 주문유형(1:신규매수, 2:신규매도, 3:매수취소, 4:매도취소, 5:매수정정, 6:매도정정, 7:프로그램매매 매수, 8:프로그램매매 매도)
        sCode: 종목코드 (6자리)
        nQty: 주문수량
        nPrice: 주문단가
        sHogaGb: 거래구분(혹은 호가구분)은 아래 참고
        sOrgOrderNo: 원주문번호. 신규주문에는 공백 입력, 정정/취소시 입력합니다.

        Returns:
        0: 성공, other: 실패

        ※ 시장가주문시 주문가격은 0으로 입력합니다. 주문가능수량은 해당 종목의 상한가 기준으로 계산됩니다.
        ※ 취소주문일때 주문가격은 0으로 입력합니다.
        ※ 프로그램매매 주문은 실거래 서버에서만 주문하실수 있으며 모의투자 서버에서는 지원하지 않습니다.
        [거래구분]
        00 : 지정가
        03 : 시장가
        05 : 조건부지정가
        06 : 최유리지정가
        07 : 최우선지정가
        10 : 지정가IOC
        13 : 시장가IOC
        16 : 최유리IOC
        20 : 지정가FOK
        23 : 시장가FOK
        26 : 최유리FOK
        61 : 장전시간외종가
        62 : 시간외단일가매매
        81 : 장후시간외종가
        ※ 모의투자에서는 지정가 주문과 시장가 주문만 가능합니다.

        [정규장 외 주문]
        장전 동시호가 주문
        08:30 ~ 09:00.	거래구분 00:지정가/03:시장가 (일반주문처럼)
        ※ 08:20 ~ 08:30 시간의 주문은 키움에서 대기하여 08:30 에 순서대로 거래소로 전송합니다.
        장전시간외 종가
        08:30 ~ 08:40. 	거래구분 61:장전시간외종가.  가격 0입력
        ※ 전일 종가로 거래. 미체결시 자동취소되지 않음
        장마감 동시호가 주문
        15:20 ~ 15:30.	거래구분 00:지정가/03:시장가 (일반주문처럼)
        장후 시간외 종가
        15:40 ~ 16:00.	거래구분 81:장후시간외종가.  가격 0입력
        시간외 단일가
        16:00 ~ 18:00.	거래구분 62:시간외단일가.  가격 입력
        ※ 10분 단위로 체결, 당일 종가대비 +-10% 가격으로 거래
        '''
        ...

    def SendOrderFO(self, sRQName: str, sScreenNo: str, sAccNo: str, sCode: str, lOrdKind: int, sSlbyTp: str, sOrdTp: str, lQty: int, sPrice: str, sOrgOrdNo: str) -> int:
        '''
        코스피지수200 선물옵션 주문을 전송하는 함수입니다.

        Args:
        sRQName: 사용자 구분명 (임의로 지정, 한글지원)
        sScreenNo: 화면번호 (4자리 숫자 임의로 지정)
        sAccNo: 계좌번호 10자리
        sCode: 종목코드
        lOrdKind: 주문종류(1:신규매매, 2:정정, 3:취소)
        sSlbyTp: 매매구분(1: 매도, 2:매수)
        sOrdTp: 거래구분(혹은 호가구분)은 아래 참고
        lQty: 주문수량
        sPrice: 주문가격
        sOrgOrdNo: 원주문번호. 신규주문에는 공백 입력, 정정/취소시 입력합니다.

        Returns:
        0: 성공, other: 실패

        [거래구분]<br/>
        1 : 지정가<br/>
        2 : 조건부지정가<br/>
        3 : 시장가<br/>
        4 : 최유리지정가<br/>
        5 : 지정가(IOC)<br/>
        6 : 지정가(FOK)<br/>
        7 : 시장가(IOC)<br/>
        8 : 시장가(FOK)<br/>
        9 : 최유리지정가(IOC)<br/>
        A : 최유리지정가(FOK)<br/>
        장종료 후 시간외 주문은 지정가 선택
        '''
        ...

    def SetInputValue(self, sID: str, sValue: str) -> None:
        '''
        조회요청시 TR의 Input값을 지정하는 함수입니다.

        Args:
        sID: TR에 명시된 Input이름
        sValue: Input이름으로 지정한 값
        '''
        ...

    def SetOutputFID(self, sID: str) -> int:
        '''
        SetOutputFID
        '''
        ...

    def DisconnectRealData(self, sScnNo: str) -> None:
        '''
        화면 내의 모든 리얼데이터 요청을 제거한다.

        Args:
        sScnNo: 화면번호 (4자리 숫자)

        시세데이터를 요청할때 사용된 화면번호를 이용하여 해당 화면번호로 등록되어져 있는 종목의 실시간시세를 서버에 등록해지 요청합니다.<br/>
        이후 해당 종목의 실시간시세는 수신되지 않습니다.<br/>
        단, 해당 종목이 또다른 화면번호로 실시간 등록되어 있는 경우 해당종목에대한 실시간시세 데이터는 계속 수신됩니다.
        '''
        ...

    def GetRepeatCnt(self, sTrCode: str, sRQName: str) -> int:
        '''
        수신데이타(멀티데이타) 반복횟수를 반환한다.
        이 함수는 <OnReceiveTrData> 이벤트가 발생될때 그 안에서 사용해야 합니다.

        Args:
        sTrCode: TRTr목록의 TrCode
        sRQName: 조회시 sRQName

        Returns:
        반복횟수
        '''
        ...

    def CommKwRqData(self, sArrCode: str, bNext: int, nCodeCount: int, nTypeFlag: int, sRQName: str, sScreenNo: str) -> int:
        '''
        한번에 100종목까지 조회할 수 있는 복수종목 조회함수 입니다.
        함수인자로 사용하는 종목코드 리스트는 조회하려는 종목코드 사이에 구분자';'를 추가해서 만들면 됩니다.
        수신되는 데이터는 TR목록에서 복수종목정보요청(OPTKWFID) Output을 참고하시면 됩니다.
        ※ OPTKWFID TR은 CommKwRqData()함수 전용으로, CommRqData 로는 사용할 수 없습니다.<br/>
        ※ OPTKWFID TR은 영웅문4 HTS의 관심종목과는 무관합니다.<br/>

        Args:
        sArrCode: 조회하려는 종목코드 리스트
        bNext: 연속조회 여부 0:기본값, 1:연속조회(지원안함)
        nCodeCount: 종목코드 갯수
        nTypeFlag: 조회구분 (0:주식 종목, 3:선물옵션 종목)
        sRQName: 사용자 구분명 (임의로 지정, 한글지원)
        sScreenNo: 화면번호 (4자리 숫자 임의로 지정)

        Returns:
        0: 성공, other: 실패

        요청이 성공하면 <OnReceiveTrData> 이벤트가 발생합니다.
        '''
        ...

    def GetAPIModulePath(self) -> str:
        '''
        ocx 모듈경로를 반환합니다.
        '''
        ...

    def GetCodeListByMarket(self, sMarket: str) -> str:
        '''
        주식 시장별 종목코드 리스트를 ';'로 구분해서 전달합니다.
        시장구분값을 ""공백으로하면 전체시장 코드리스트를 전달합니다.

        Args:
        sMarket: 시장구분 (0:장내, 10:코스닥, 3: ELQ, 8: ETF, 50: KONEX, 4: 뮤추얼펀드, 5: 신주인수권, 6: 리츠, 9: 하이얼펀드, 30: K-OTC)

        Returns:
        종목코드 리스트
        '''
        ...

    def GetConnectState(self) -> int:
        '''
        현재접속상태를 반환합니다.

        Returns:
        0: 미연결, 1: 연결완료
        '''
        ...

    def GetMasterCodeName(self, sTrCode: str) -> str:
        '''
        종목코드에 해당하는 한글 종목명을 반환합니다.

        Args:
        sTrCode: 종목코드

        Returns:
        종목명
        '''
        ...

    def GetMasterListedStockCnt(self, sTrCode: str) -> int:
        '''
        종목코드에 해당하는 상장주식수를 반환합니다.

        Args:
        sTrCode: 종목코드

        Returns:
        상장주식수
        '''
        ...

    def GetMasterConstruction(self, sTrCode: str) -> str:
        '''
        종목코드에 해당하는 감리구분을 반환합니다. (정상, 투자주의, 투자경고, 투자위험, 투자주의환기종목)

        Args:
        sTrCode: 종목코드

        Returns:
        감리구분
        '''
        ...

    def GetMasterListedStockDate(self, sTrCode: str) -> str:
        '''
        종목코드에 해당하는 상장일을 반환합니다.

        Args:
        sTrCode: 종목코드

        Returns:
        상장일
        '''
        ...

    def GetMasterLastPrice(self, sTrCode: str) -> str:
        '''
        입력한 종목의 당일 기준가를 전달합니다.

        Args:
        sTrCode: 종목코드

        Returns:
        당일 기준가
        '''
        ...

    def GetMasterStockState(self, sTrCode: str) -> str:
        '''
        입력한 종목의 증거금 비율, 거래정지, 관리종목, 감리종목, 투자융의종목, 담보대출, 액면분할, 신용가능 여부를 전달합니다.

        Args:
        sTrCode: 종목코드

        Returns:
        종목상태
        '''
        ...

    def GetDataCount(self, strRecordName: str) -> int:
        '''
        GetDataCount
        '''
        ...

    def GetOutputValue(self, strRecordName: str, nRepeatIdx: int, nItemIdx: int) -> str:
        '''
        GetOutputValue
        '''
        ...

    def GetCommData(self, strTrCode: str, strRecordName: str, nIndex: int, strItemName: str) -> str:
        '''
        OnReceiveTrData> 이벤트가 발생될때 수신한 데이터를 얻어오는 함수입니다.
        이 함수는 <OnReceiveTrData> 이벤트가 발생될때 그 안에서 사용해야 합니다.

        Args:
        strTrCode: TR목록의 TrCode
        strRecordName: 레코드이름
        nIndex: TR목록의 index
        strItemName: TR목록의 ItemName
        '''
        ...

    def GetCommRealData(self, strCode: str, nFid: int) -> str:
        '''
        실시간 데이터를 얻어오는 함수입니다.
        이 함수는 <OnReceiveRealData> 이벤트가 발생될때 그 안에서 사용해야 합니다.

        Args:
        strCode: Code
        nFid: 실시간목록의 Fid

        Returns:
        실시간 데이터
        '''
        ...

    def GetChejanData(self, nFid: int) -> str:
        '''
        체결/잔고 데이터를 얻어오는 함수입니다.
        이 함수는 <OnReceiveChejanData> 이벤트가 발생될때 그 안에서 사용해야 합니다.

        Args:
        nFid: 체결/잔고 Fid

        Returns:
        체결잔고 데이터
        '''
        ...

    def GetThemeGroupList(self, nType: int) -> str:
        '''
        GetThemeGroupList
        '''
        ...

    def GetThemeGroupCode(self, strThemeCode: str) -> str:
        '''
        GetThemeGroupCode
        '''
        ...

    def GetFutureList(self) -> str:
        '''
        지수선물 종목코드 리스트를 ';'로 구분해서 전달합니다.

        Returns:
        선물코드 리스트
        '''
        ...

    def GetFutureCodeByIndex(self, nIndex: int) -> str:
        '''
        지수선물 종목코드를 반환합니다.

        Args:
        nIndex: 종목인덱스

        Returns:
        종목코드
        '''
        ...

    def GetActPriceList(self) -> str:
        '''
        지수옵션 행사가에 100을 곱해서 소수점이 없는 값을 ';'로 구분해서 전달합니다.

        Returns:
        행사가 리스트
        '''
        ...

    def GetMonthList(self) -> str:
        '''
        지수옵션 월물정보를 ';'로 구분해서 전달하는데 순서는 콜 11월물 ~ 콜 최근월물 풋 최근월물 ~ 풋 최근월물가 됩니다.

        Returns:
        월물정보 리스트
        '''
        ...

    def GetOptionCode(self, strActPrice: str, nCp: int, strMonth: str) -> str:
        '''
        지수옵션 종목코드를 반환합니다.

        Args:
        strActPrice: 소수점을 포함한 행사가
        nCp: 콜풋구분값(콜:2, 풋:3)
        strMonth: 6자리 월물

        Returns:
        종목코드
        '''
        ...

    def GetOptionCodeByMonth(self, sTrCode: str, nCp: int, strMonth: str) -> str:
        '''
        GetOptionCodeByMonth
        '''
        ...

    def GetOptionCodeByActPrice(self, strCode: str, nCp: int, nTick: int) -> str:
        '''
        옵션전용 함수. 인자로 지정한 지수옵션 종목의 n틱 차이에 해당되는 종목코드를 전달합니다.

        Args:
        strCode: 종목코드
        nCp: 콜풋구분값(콜:2, 풋:3)
        nTick: 기준종목의 n틱 (0값 제외)

        Returns:
        종목코드
        '''
        ...

    def GetSFutureList(self, strBaseAssetCode: str) -> str:
        '''
        기초자산 구분값을 인자로 받아서 주식선물 종목코드, 종목명, 기초자산이름을 구할수 있습니다. 입력값을 공백으로 하면 주식선물 전체 종목코드를 얻을 수 있습니다.

        Args:
        strBaseAssetCode: 기초자산 구분값
        '''
        ...

    def GetSFutureCodeByIndex(self, strBaseAssetCode: str, nIndex: int) -> str:
        '''
        GetSFutureCodeByIndex
        '''
        ...

    def GetSActPriceList(self, strBaseAssetGb: str) -> str:
        '''
        GetSActPriceList
        '''
        ...

    def GetSMonthList(self, strBaseAssetGb: str) -> str:
        '''
        GetSMonthList
        '''
        ...

    def GetSOptionCode(self, strBaseAssetGb: str, strActPrice: str, nCp: int, strMonth: str) -> str:
        '''
        GetSOptionCode
        '''
        ...

    def GetSOptionCodeByMonth(self, strBaseAssetGb: str, sTrCode: str, nCp: int, strMonth: str) -> str:
        '''
        GetSOptionCodeByMonth
        '''
        ...

    def GetSOptionCodeByActPrice(self, strBaseAssetGb: str, sTrCode: str, nCp: int, nTick: int) -> str:
        '''
        GetSOptionCodeByActPrice
        '''
        ...

    def GetSFOBasisAssetList(self) -> str:
        '''
        GetSFOBasisAssetList
        '''
        ...

    def GetOptionATM(self) -> str:
        '''
        지수옵션 소수점을 제거한 ATM값을 전달합니다. 예를들어 ATM값이 247.50 인 경우 24750이 전달됩니다.
        '''
        ...

    def GetSOptionATM(self, strBaseAssetGb: str) -> str:
        '''
        GetSOptionATM
        '''
        ...

    def GetBranchCodeName(self) -> str:
        '''
        GetBranchCodeName
        '''
        ...

    def CommInvestRqData(self, sMarketGb: str, sRQName: str, sScreenNo: str) -> int:
        '''
        CommInvestRqData
        '''
        ...

    def SendOrderCredit(self, sRQName: str, sScreenNo: str, sAccNo: str, nOrderType: int, sCode: str, nQty: int, nPrice: int, sHogaGb: str, sCreditGb: str, sLoanDate: str, sOrgOrderNo: str) -> int:
        '''
        서버에 주문을 전송하는 함수 입니다. 국내주식 신용주문 전용함수입니다. 대주거래는 지원하지 않습니다.
        ※ 프로그램매매 주문은 실거래 서버에서만 주문하실수 있으며 모의투자 서버에서는 지원하지 않습니다.

        Args:
        sRQName: 사용자 구분명 (임의로 지정, 한글지원)
        sScreenNo: 화면번호 (4자리 숫자 임의로 지정)
        sAccNo: 계좌번호 10자리
        nOrderType: 주문유형(1:신규매수, 2:신규매도, 3:매수취소, 4:매도취소, 5:매수정정, 6:매도정정, 7:프로그램매매 매수, 8:프로그램매매 매도)
        sCode: 종목코드 (6자리)
        nQty: 주문수량
        nPrice: 주문단가
        sHogaGb: 거래구분(혹은 호가구분)은 아래 참고
        sCreditGb: 신용구분 (아래에서 참고)
        sLoanDate: 대출일
        sOrgOrderNo: 원주문번호. 신규주문에는 공백 입력, 정정/취소시 입력합니다.

        Returns:
        0: 성공, other: 실패

        [거래구분]<br/>
        00 : 지정가<br/>
        03 : 시장가<br/>
        05 : 조건부지정가<br/>
        06 : 최유리지정가<br/>
        07 : 최우선지정가<br/>
        10 : 지정가IOC<br/>
        13 : 시장가IOC<br/>
        16 : 최유리IOC<br/>
        20 : 지정가FOK<br/>
        23 : 시장가FOK<br/>
        26 : 최유리FOK<br/>
        61 : 장전시간외종가<br/>
        62 : 시간외단일가매매<br/>
        81 : 장후시간외종가<br/>
        ※ 모의투자에서는 지정가 주문과 시장가 주문만 가능합니다.<br/>

        [신용거래]<br/>
        03 : 신용매수 - 자기융자<br/>
        33 : 신용매도 - 자기융자<br/>

        [대출일]<br/>
        YYYYMMDD형식 날짜를 입력합니다. (ex 대출일이 2023년 1월 1일이면 "20230101"입력)<br/>
        신용매도 - 자기융자 일때는 종목별 대출일을 입력하고 신용매도 - 융자합이면 "99991231"을 입력합니다.<br/>

        '''
        ...

    def KOA_Functions(self, sFunctionName: str, sParam: str) -> str:
        '''
        OpenAPI기본 기능외에 기능을 사용하기 쉽도록 만든 함수입니다.

        Args:
        sFunctionName: 함수이름 혹은 기능이름
        sParam: 함수 매개변수
        '''
        ...

    def SetInfoData(self, sInfoData: str) -> int:
        '''
        SetInfoData
        '''
        ...

    def SetRealReg(self, strScreenNo: str, strCodeList: str, strFidList: str, strOptType: str) -> int:
        '''
        종목코드와 FID 리스트를 이용해서 실시간 시세를 등록하는 함수입니다.

        Args:
        strScreenNo: 화면번호
        strCodeList: 종목코드 리스트
        strFidList: 실시간 FID리스트
        strOptType: 실시간 등록 타입

        한번에 등록가능한 종목과 FID갯수는 100종목, 100개 입니다.
        실시간 등록타입을 0으로 설정하면 등록한 종목들은 실시간 해지되고 등록한 종목만 실시간 시세가 등록됩니다.
        실시간 등록타입을 1로 설정하면 먼저 등록한 종목들과 함께 실시간 시세가 등록됩니다
        '''
        ...

    def GetConditionLoad(self) -> int:
        '''
        서버에 저장된 사용자 조건검색 목록을 요청합니다.

        Returns:
        1: 성공, other: 실패

        요청이 성공하면 <OnReceiveConditionVer> 이벤트가 발생합니다.
        '''
        ...

    def GetConditionNameList(self) -> str:
        '''
        서버에서 수신한 사용자 조건식을 조건식의 고유번호와 조건식 이름을 한 쌍으로 하는 문자열들로 전달합니다.
        조건식 하나는 조건식의 고유번호와 조건식 이름이 구분자 '^'로 나뉘어져 있으며 각 조건식은 ';'로 나뉘어져 있습니다.
        이 함수는 <OnReceiveConditionVer> 이벤트에서 사용해야 합니다.

        Returns:
        조건검색 목록
        '''
        ...

    def SendCondition(self, strScrNo: str, strConditionName: str, nIndex: int, nSearch: int) -> int:
        '''
        서버에 조건검색을 요청합니다.

        Args:
        strScrNo: 화면번호
        strConditionName: 조건식 이름
        nIndex: 조건식 고유번호
        nSearch: 실시간옵션 (0:조건검색, 1:실시간 조건검색)

        Returns:
        1: 성공, other: 실패

        요청이 성공하면 <OnReceiveTrCondition> 이벤트가 발생합니다.
        '''
        ...

    def SendConditionStop(self, strScrNo: str, strConditionName: str, nIndex: int) -> None:
        '''
        실시간 조건검색을 중지할 때 사용하는 함수입니다.

        Args:
        strScrNo: 화면번호
        strConditionName: 조건식 이름
        nIndex: 조건식 고유번호
        '''
        ...

    def GetCommDataEx(self, strTrCode: str, strRecordName: str) -> object:
        '''
        조회 수신데이터 크기가 큰 차트데이터를 한번에 가져올 목적으로 만든 차트조회 전용함수입니다.
        이 함수는 <OnReceiveTrData> 이벤트가 발생될때 그 안에서 사용해야 합니다.

        Args:
        strTrCode: TR목록의 TrCode
        strRecordName: 레코드이름
        '''
        ...

    def SetRealRemove(self, strScrNo: str, strDelCode: str) -> None:
        '''
        실시간시세 해지 함수이며 화면번호와 종목코드를 이용해서 상세하게 설정할 수 있습니다.

        Args:
        strScrNo: 화면번호 또는 "ALL"
        strDelCode: 종목코드 또는 "ALL"
        '''
        ...

    def GetMarketType(self, strCode: str) -> int:
        '''
        종목코드에 해당하는 시장구분을 반환합니다.

        Args:
        strCode: 종목코드

        Returns:
        시장구분
        '''
        ...

    pass
