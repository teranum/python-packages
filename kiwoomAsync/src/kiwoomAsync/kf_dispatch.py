class KFOpenApiDispatch(object):

    def CommConnect(self, nAutoUpgrade: int) -> int:
        '''
        로그인 윈도우를 실행한다.

        Args:
        nAutoUpgrade: 버전처리시, 수동 또는 자동 설정을 위한 구분값(0 : 수동진행, 1 : 자동진행)

        Returns:
        0: 성공, 음수값: 실패
        '''
        ...

    def CommRqData(self, sRQName: str, sTrCode: str, sPrevNext: str, sScreenNo: str) -> int:
        '''
        TR을 서버로 송신한다.

        Args:
        sRQName: 사용자 구분명
        sTrCode: TR이름
        sPrevNext: 연속조회요청
        sScreenNo: 화면번호(4자리 숫자형식)

        Returns:
        0: 성공, 음수값: 실패
        '''
        ...

    def SetInputValue(self, sID: str, sValue: str) -> None:
        '''
        조회 입력값을 설정한다.

        Args:
        sID: 입력 아이디명
        sValue: 입력 값
        '''
        ...

    def GetCommData(self, sTrCode: str, sRQName: str, nIndex: int, sItemName: str) -> str:
        '''
        수신 데이터를 반환한다.

        Args:
        sTrCode: Tr목록의 TrCode
        sRQName: 조회시 sRQName
        nIndex: Row 인덱스
        sItemName: TR에서 얻어오려는 출력항목 이름

        Returns:
        수신 데이터
        '''
        ...

    def CommTerminate(self) -> None:
        '''
        OpenAPI의 서버 접속을 해제한다.
        프로그램 종료시 적용시키는 함수이며, 미적용되어도 OpenAPI 내부에서 처리하게 되어 있음.
        '''
        ...

    def GetRepeatCnt(self, sTrCode: str, sRQName: str) -> int:
        '''
        수신 데이터의 반복 개수를 반환한다.

        Args:
        sTrCode: TrCode
        sRQName: 조회시 sRQName

        Returns:
        수신 데이터의 반복 개수
        '''
        ...

    def DisconnectRealData(self, sScreenNo: str) -> None:
        '''
        화면번호로 등록된 모든 실시간 데이터 요청을 제거한다.

        Args:
        sScreenNo: 화면번호
        '''
        ...

    def GetCommRealData(self, sRealType: str, nFid: int) -> str:
        '''
        실시간 데이터를 반환한다.

        Args:
        sRealType: "해외선물시세", "해외옵션시세", "해외선물호가", "해외옵션호가" 입력 (미입력해도 가능)
        nFid: 실시간 FID

        Returns:
        실시간 데이터
        '''
        ...

    def GetChejanData(self, nFid: int) -> str:
        '''
        체결잔고 실시간 데이터를 반환한다.

        Args:
        nFid: 체결잔고 FID

        Returns:
        체결잔고 데이터
        '''
        ...

    def SendOrder(self, sRQName: str, sScreenNo: str, sAccNo: str, nOrderType: int, sCode: str, nQty: int, sPrice: str, sStopPrice: str, sHogaGb: str, sOrgOrderNo: str) -> int:
        '''
        주문을 서버로 전송한다.

        Args:
        sRQName: 사용자 구분명
        sScreenNo: 화면번호(4자리 숫자형식)
        sAccNo: 계좌번호
        nOrderType: 주문유형(1:신규매도, 2:신규매수 3:매도취소, 4:매수취소, 5:매도정정, 6:매수정정)
        sCode: 종목코드
        nQty: 주문수량
        sPrice: 주문가격
        sStopPrice: 스탑가격
        sHogaGb: 거래구분(1:시장가, 2:지정가, 3:STOP, 4:STOP LIMIT)
        sOrgOrderNo: 원주문번호

        Returns:
        0: 성공, 음수값: 실패
        '''
        ...

    def GetLoginInfo(self, sTag: str) -> str:
        '''
        로그인한 사용자 정보를 반환한다.

        Args:
        sTag: 사용자 정보 구분값

        Returns:
        사용자 정보

        [sTag]<br/>
        ACCOUNT_CNT	- 전체 계좌 개수를 반환한다.<br/>
        ACCNO		- 전체 계좌를 반환한다. 계좌별 구분은 ‘;’이다.<br/>
        USER_ID		- 사용자 ID를 반환한다.<br/>
        USER_NAME	- 사용자명을 반환한다.<br/>
        KEY_BSECGB	- 키보드보안 해지여부. 0:정상, 1:해지<br/>
        FIREW_SECGB	- 방화벽 설정 여부. 0:미설정, 1:설정, 2:해지
        '''
        ...

    def GetGlobalFutureItemlist(self) -> str:
        '''
        해외선물 상품 리스트를 반환한다.

        Returns:
        해외선물 상품 리스트, 상품간 구분은 ";"
        '''
        ...

    def GetGlobalOptionItemlist(self) -> str:
        '''
        해외옵션 상품 리스트를 반환한다.

        Returns:
        해외옵션 상품 리스트, 상품간 구분은 ";"
        '''
        ...

    def GetGlobalFutureCodelist(self, sItem: str) -> str:
        '''
        해외상품별 해외선물 종목 리스트를 반환한다.

        Args:
        sItem: 해외상품 입력 (6A, ES, ...)

        Returns:
        해외선물 종목 리스트, 종목간 구분은 ";"
        '''
        ...

    def GetGlobalOptionCodelist(self, sItem: str) -> str:
        '''
        해외상품별 해외옵션 종목 리스트를 반환한다.

        Args:
        sItem: 해외상품 입력 (6A, ES, ...)

        Returns:
        해외옵션 종목 리스트, 종목간 구분은 ";"
        '''
        ...

    def GetConnectState(self) -> int:
        '''
        현재접속 상태를 반환한다.

        Returns:
        0: 미연결, 1: 연결
        '''
        ...

    def GetAPIModulePath(self) -> str:
        '''
        OpenAPI 모듈의 경로를 반환한다.

        Returns:
        OpenAPI 모듈의 경로
        '''
        ...

    def GetCommonFunc(self, sFuncName: str, sParam: str) -> str:
        '''
        공통함수로 추후 추가함수가 필요시 사용할 함수이다.

        Args:
        sFuncName: 함수명
        sParam: 파라미터

        Returns:
        함수 호출 결과
        '''
        ...

    def GetConvertPrice(self, sCode: str, sPrice: str, nType: int) -> str:
        '''
        가격 진법에 따라 변환된 가격을 반환한다.

        Args:
        sCode: 종목코드
        sPrice: 가격
        nType: 변환유형(0 : 진법(표시가격) -> 10진수,  1 : 10진수 -> 진법(표시가격))

        Returns:
        변환된 가격
        '''
        ...

    def GetGlobalFutOpCodeInfoByType(self, nGubun: int, sType: str) -> str:
        '''
        해외선물옵션 코드 타입별로 정보를 반환한다.

        Args:
        nGubun: 구분값(0:선물, 1:옵션)
        sType: 상품타입 입력 ("" : 전체, IDX : 지수, CUR : 통화, INT : 금리, MTL : 금속, ENG : 에너지, CMD : 농산물)

        Returns:
        해외선물옵션 코드 정보
        '''
        ...

    def GetGlobalFutOpCodeInfoByCode(self, sCode: str) -> str:
        '''
        해외선물옵션 코드별 정보를 반환한다.

        Args:
        sCode: 종목코드

        Returns:
        해외선물옵션 코드 정보
        '''
        ...

    def GetGlobalFutureItemlistByType(self, sType: str) -> str:
        '''
        해외선물 상품 리스트를 타입별로 반환한다.

        Args:
        sType: 상품타입 입력 (IDX : 지수, CUR : 통화, INT : 금리, MTL : 금속, ENG : 에너지, CMD : 농산물)

        Returns:
        해외선물 상품 리스트
        '''
        ...

    def GetGlobalFutureCodeByItemMonth(self, sItem: str, sMonth: str) -> str:
        '''
        해외선물종목코드를 상품/월물별로 반환한다.

        Args:
        sItem: 상품코드 입력 (6A, ES...)
        sMonth: 월물 입력 ("201606")

        Returns:
        종목코드를 문자값으로 반환한다
        '''
        ...

    def GetGlobalOptionCodeByMonth(self, sItem: str, sCPGubun: str, sActivePrice: str, sMonth: str) -> str:
        '''
        해외옵션 종목코드를 상품/콜풋/행사가/월물별로 반환한다.

        Args:
        sItem: 상품코드 입력 (6A, ES...)
        sCPGubun: 콜풋구분 입력 (C:콜, P:풋)
        sActivePrice: 행사가 입력 (0.7615)
        sMonth: 월물 입력 ("201606")

        Returns:
        종목코드를 문자값으로 반환한다
        '''
        ...

    def GetGlobalOptionMonthByItem(self, sItem: str) -> str:
        '''
        해외옵션월물리스트을 상품별로 반환한다.

        Args:
        sItem: 상품코드 입력 (6A, ES...)

        Returns:
        월물리스트을 문자값으로 반환한다
        '''
        ...

    def GetGlobalOptionActPriceByItem(self, sItem: str) -> str:
        '''
        해외옵션행사가리스트를 상품별로 반환한다.

        Args:
        sItem: 상품코드 입력 (6A, ES...)

        Returns:
        행사가리스트를 문자값으로 반환한다
        '''
        ...

    def GetGlobalFutureItemTypelist(self) -> str:
        '''
        해외선물 상품 타입 리스트를 반환한다.

        Returns:
        해외선물 상품 타입 리스트
        '''
        ...

    def GetCommFullData(self, sTrCode: str, sRecordName: str, nGubun: int) -> str:
        '''
        수신 데이터를 반환한다.

        Args:
        sTrCode: TrCode
        sRecordName: 사용자구분명 입력
        nGubun: 수신데이타 구분 입력 (0 : 전체(싱글+멀티),  1 : 싱글데이타, 2 : 멀티데이타)

        Returns:
        수신 데이터
        '''
        ...

    pass




