import asyncio, time

from PyQt5.QAxContainer import QAxWidget
from PyQt5.QtCore import QObject, pyqtSignal

from .kh_dispatch import KHOpenApiDispatch
from .kf_dispatch import KFOpenApiDispatch
from .models import ResponseData

class KhAsync(KHOpenApiDispatch, QObject):
    '''
    키움증권 국내 API 비동기 처리 클래스
    '''

    OnReceiveTrData = pyqtSignal(str, str, str, str, str, int, str, str, str)
    OnReceiveMsg = pyqtSignal(str, str, str, str)
    OnEventConnect = pyqtSignal(int)
    OnReceiveTrCondition = pyqtSignal(str, str, str, int, int)
    OnReceiveConditionVer = pyqtSignal(int, str)

    def __init__(self, ocx = None):
        super().__init__()

        if ocx is None:
            ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")

        # Connect signals
        ocx.OnReceiveTrData.connect(self.__inner_OnReceiveTrData)
        ocx.OnReceiveMsg.connect(self.__inner_OnReceiveMsg)
        ocx.OnEventConnect.connect(self.__inner_OnEventConnect)
        ocx.OnReceiveTrCondition.connect(self.__inner_OnReceiveTrCondition)
        ocx.OnReceiveConditionVer.connect(self.__inner_OnReceiveConditionVer)

        # Register signals
        self.OnReceiveRealData = ocx.OnReceiveRealData
        self.OnReceiveChejanData = ocx.OnReceiveChejanData
        self.OnReceiveInvestRealData = ocx.OnReceiveInvestRealData
        self.OnReceiveRealCondition = ocx.OnReceiveRealCondition

        # Register methods
        self.CommConnect = ocx.CommConnect
        self.CommRqData = ocx.CommRqData
        self.GetLoginInfo = ocx.GetLoginInfo
        self.SendOrder = ocx.SendOrder
        self.SendOrderFO = ocx.SendOrderFO
        self.SetInputValue = ocx.SetInputValue
        self.SetOutputFID = ocx.SetOutputFID
        self.CommGetData = ocx.CommGetData
        self.DisconnectRealData = ocx.DisconnectRealData
        self.GetRepeatCnt = ocx.GetRepeatCnt
        self.CommKwRqData = ocx.CommKwRqData
        self.GetAPIModulePath = ocx.GetAPIModulePath
        self.GetCodeListByMarket = ocx.GetCodeListByMarket
        self.GetConnectState = ocx.GetConnectState
        self.GetMasterCodeName = ocx.GetMasterCodeName
        self.GetMasterListedStockCnt = ocx.GetMasterListedStockCnt
        self.GetMasterConstruction = ocx.GetMasterConstruction
        self.GetMasterListedStockDate = ocx.GetMasterListedStockDate
        self.GetMasterLastPrice = ocx.GetMasterLastPrice
        self.GetMasterStockState = ocx.GetMasterStockState
        self.GetDataCount = ocx.GetDataCount
        self.GetOutputValue = ocx.GetOutputValue
        self.GetCommData = ocx.GetCommData
        self.GetCommRealData = ocx.GetCommRealData
        self.GetChejanData = ocx.GetChejanData
        self.GetThemeGroupList = ocx.GetThemeGroupList
        self.GetThemeGroupCode = ocx.GetThemeGroupCode
        self.GetFutureList = ocx.GetFutureList
        self.GetFutureCodeByIndex = ocx.GetFutureCodeByIndex
        self.GetActPriceList = ocx.GetActPriceList
        self.GetMonthList = ocx.GetMonthList
        self.GetOptionCode = ocx.GetOptionCode
        self.GetOptionCodeByMonth = ocx.GetOptionCodeByMonth
        self.GetOptionCodeByActPrice = ocx.GetOptionCodeByActPrice
        self.GetSFutureList = ocx.GetSFutureList
        self.GetSFutureCodeByIndex = ocx.GetSFutureCodeByIndex
        self.GetSActPriceList = ocx.GetSActPriceList
        self.GetSMonthList = ocx.GetSMonthList
        self.GetSOptionCode = ocx.GetSOptionCode
        self.GetSOptionCodeByMonth = ocx.GetSOptionCodeByMonth
        self.GetSOptionCodeByActPrice = ocx.GetSOptionCodeByActPrice
        self.GetSFOBasisAssetList = ocx.GetSFOBasisAssetList
        self.GetOptionATM = ocx.GetOptionATM
        self.GetSOptionATM = ocx.GetSOptionATM
        self.GetBranchCodeName = ocx.GetBranchCodeName
        self.CommInvestRqData = ocx.CommInvestRqData
        self.SendOrderCredit = ocx.SendOrderCredit
        self.KOA_Functions = ocx.KOA_Functions
        self.SetInfoData = ocx.SetInfoData
        self.SetRealReg = ocx.SetRealReg
        self.GetConditionLoad = ocx.GetConditionLoad
        self.GetConditionNameList = ocx.GetConditionNameList
        self.SendCondition = ocx.SendCondition
        self.SendConditionStop = ocx.SendConditionStop
        self.GetCommDataEx = ocx.GetCommDataEx
        self.SetRealRemove = ocx.SetRealRemove
        self.GetMarketType = ocx.GetMarketType

        # Register properties
        self.ocx = ocx
        self.AsyncTimeOut = 5
        self._asyncNodes = []

    def __inner_OnReceiveTrData(self, sScrNo, sRQName, sTrCode, sRecordName, sPrevNext, nDataLength, sErrorCode, sMessage, sSplmMsg):
        hashid_order = _asyncNode.get_hash_id(sRQName, "SendOrderAsync", sScrNo)
        hashid = _asyncNode.get_hash_id(sRQName, sTrCode, sScrNo)
        for node in self._asyncNodes:
            if node.hashid == hashid_order or node.hashid == hashid:
                node.async_evented = True
                if node.callback is not None:
                    node.callback(sScrNo, sRQName, sTrCode, sRecordName, sPrevNext, nDataLength, sErrorCode, sMessage, sSplmMsg)
                node.set()
                return
        self.OnReceiveTrData.emit(sScrNo, sRQName, sTrCode, sRecordName, sPrevNext, nDataLength, sErrorCode, sMessage, sSplmMsg)

    def __inner_OnReceiveMsg(self, sScrNo, sRQName, sTrCode, sMsg):
        hashid_order = _asyncNode.get_hash_id(sRQName, "SendOrderAsync", sScrNo)
        hashid = _asyncNode.get_hash_id(sRQName, sTrCode, sScrNo)
        for node in self._asyncNodes:
            if node.hashid == hashid_order or node.hashid == hashid:
                node.async_evented = True
                node.async_msg = sMsg
                return
        self.OnReceiveMsg.emit(sScrNo, sRQName, sTrCode, sMsg)

    def __inner_OnEventConnect(self, err_code):
        hashid = _asyncNode.get_hash_id("CommConnectAsync")
        for node in self._asyncNodes:
            if node.hashid == hashid:
                node.async_evented = True
                node.async_result = err_code
                node.set()
                return
        self.OnEventConnect.emit(err_code)

    def __inner_OnReceiveTrCondition(self, sScrNo, strCodeList, strConditionName, nIndex, nNext):
        hashid = _asyncNode.get_hash_id(sScrNo, strConditionName, "SendConditionAsync")
        for node in self._asyncNodes:
            if node.hashid == hashid:
                node.async_evented = True
                node.async_result = 1
                node.async_msg = strCodeList
                node.set()
                return
        self.OnReceiveTrCondition.emit(sScrNo, strCodeList, strConditionName, nIndex, nNext)

    def __inner_OnReceiveConditionVer(self, lRet, sMsg):
        hashid = _asyncNode.get_hash_id("GetConditionLoadAsync")
        for node in self._asyncNodes:
            if node.hashid == hashid:
                node.async_evented = True
                node.async_result = lRet
                if lRet == 1:
                    node.async_msg = self.GetConditionNameList()
                else:
                    node.async_msg = sMsg
                node.set()
                return
        self.OnReceiveConditionVer.emit(lRet, sMsg)

    _requreMinIndex = 9950
    _requreMaxIndex = 9999
    _requestIndex = _requreMinIndex

    def __get_request_scrNum(self):
        self._requestIndex += 1
        if self._requestIndex > self._requreMaxIndex:
            self._requestIndex = self._requreMinIndex
        return str(self._requestIndex).zfill(4)

    async def CommConnectAsync(self) -> tuple[int, str]:
        '''
        비동기 로그인 함수
        결과값 : (ret, msg)
        ret : 0 - 성공, 그외 - 실패, msg : 에러메시지
        '''
        if self.GetConnectState() == 1:
            return 0, '이미 로그인 되어 있습니다'

        hashid = _asyncNode.get_hash_id("CommConnectAsync")
        # Check if the same request is already in the list
        for node in self._asyncNodes:
            if node.hashid == hashid:
                return -901, self.GetErrorMesage(-901)
        # Create a new node
        node = _asyncNode(hashid)
        self._asyncNodes.append(node)
        ret = self.CommConnect()
        if ret == 0:
            await node.wait()
            ret = node.async_result
        self._asyncNodes.remove(node)
        return ret, self.GetErrorMesage(ret)

    async def GetConditionLoadAsync(self) -> tuple[int, str]:
        '''
        비동기 조건검색 목록 로드 함수
        결과값 : (ret, msg)
        ret : 1 - 성공, 그외 - 실패, msg : 에러메시지
        성공시 msg : 조건검색 목록 (GetConditionNameList() 결과값)
        '''
        hashid = _asyncNode.get_hash_id("GetConditionLoadAsync")
        # Check if the same request is already in the list
        for node in self._asyncNodes:
            if node.hashid == hashid:
                return -901, ''
        # Create a new node
        node = _asyncNode(hashid)
        self._asyncNodes.append(node)
        ret = self.GetConditionLoad()
        if ret == 1:
            await node.wait()
            ret = node.async_result
        self._asyncNodes.remove(node)
        return ret, node.async_msg

    async def SendConditionAsync(self, sScrNo: str, strConditionName: str, nIndex: int, nSearch: int) -> tuple[int, str]:
        '''
        비동기 조건검색 요청 함수
        결과값 : (ret, msg)
        ret : 1 - 성공, 그외 - 실패, msg : 에러메시지
        성공시 msg : 검색된 종목코드 리스트(OnReceiveTrCondition 이벤트 strCodeList 값)
        '''
        hashid = _asyncNode.get_hash_id(sScrNo, strConditionName, "SendConditionAsync")
        # Check if the same request is already in the list
        for node in self._asyncNodes:
            if node.hashid == hashid:
                return -901, self.GetErrorMesage(-901)
        # Create a new node
        node = _asyncNode(hashid)
        self._asyncNodes.append(node)
        ret = self.SendCondition(sScrNo, strConditionName, nIndex, nSearch)
        if ret == 1:
            await node.wait(self.AsyncTimeOut)
            ret = node.async_result
        self._asyncNodes.remove(node)
        if ret == 1:
            return ret, node.async_msg
        return ret, '잠시 후 다시 요청해 주세요'

    async def CommRqDataAsync(self, sRQName: str, sTrCode: str, nPrevNext: int, sScreenNo: str, callback) -> tuple[int, str]:
        '''
        비동기 TR 요청 함수
        callback : def callback(sScrNo, sRQName, sTrCode, sRecordName, sPrevNext, sMessage) 로 OnReceiveTrData 이벤트 처리부 호출
        결과값 : (ret, msg)
        ret : 0 - 성공, 그외 - 실패, msg : 에러메시지
        '''
        if self.GetConnectState() == 0:
            return -10, self.GetErrorMesage(-10)

        hashid = _asyncNode.get_hash_id(sRQName, sTrCode, sScreenNo)
        # Create a new node
        node = _asyncNode(hashid)
        node.callback = callback
        self._asyncNodes.append(node)
        ret = self.CommRqData(sRQName, sTrCode, nPrevNext, sScreenNo)
        if ret == 0:
            await node.wait(self.AsyncTimeOut)
            ret = node.async_result
        msg = node.async_msg
        if msg == '':
            msg = self.GetErrorMesage(ret)
        self._asyncNodes.remove(node)
        return ret, msg

    async def CommKwRqDataAsync(self, arrCode: list, next: int, codeCount: int, typeFlag: int, sRQName: str, screenNo: str, callback) -> tuple[int, str]:
        '''
        비동기 관심종목정보요청 함수
        callback : def callback(sScrNo, sRQName, sTrCode, sRecordName, sPrevNext, sMessage) 로 OnReceiveTrData 이벤트 처리부 호출
        결과값 : (ret, msg)
        ret : 0 - 성공, 그외 - 실패, msg : 에러메시지
        '''
        if self.GetConnectState() == 0:
            return -10, self.GetErrorMesage(-10)

        tr_cd = "OPTKWFID" if typeFlag == 0 else "OPTFOFID"
        hashid = _asyncNode.get_hash_id(sRQName, tr_cd, screenNo)
        # Create a new node
        node = _asyncNode(hashid)
        node.callback = callback
        self._asyncNodes.append(node)
        ret = self.CommKwRqData(arrCode, next, codeCount, typeFlag, sRQName, screenNo)
        if ret == 0:
            await node.wait(self.AsyncTimeOut)
            ret = node.async_result
        msg = node.async_msg
        if msg == '':
            msg = self.GetErrorMesage(ret)
        self._asyncNodes.remove(node)
        return ret, msg

    async def RequestTrAsync(self, tr_cd: str, indata: dict
                             , in_singles: list = []
                             , in_multis: list = []
                             , cont_key: str = '') -> ResponseData:
        '''
        비동기 TR 요청 함수
        tr_cd : TR 코드
        indata : 입력값(딕셔너리)
        in_singles : 가져올 단일데이터 리스트
        in_multis : 가져올 멀티데이터 리스트

        결과값 : ResponseData
        ResponseData : 결과값을 담은 객체
        ResponseData.result_code : 0 - 성공, 그외 - 실패
        ResponseData.msg : 에러메시지
        ResponseData.single_datas : 단일데이터 리스트
        ResponseData.multi_datas : 멀티데이터 리스트(2차원 리스트)
        ResponseData.cont_key : 연속키
        ResponseData.in_singles : 입력된 단일데이터 리스트
        ResponseData.in_multis : 입력된 멀티데이터 리스트

        ※ 화면번호 자동할당(9950~9999)
        요청시 실시간연결은 자동해제
        출력데이터는 strip 처리하여 반환
        관심종목요청은 OPTKWFID로 요청, indata에 "종목코드", "타입구분"을 설정

        '''
        scr_num = self.__get_request_scrNum()

        response = ResponseData()
        response.tr_cd = tr_cd
        response.in_singles = in_singles
        response.in_multis = in_multis

        def inner_callback(sScrNo, sRQName, sTrCode, sRecordName, sPrevNext, nDataLength, sErrorCode, sMessage, sSplmMsg):
            self.DisconnectRealData(sScrNo)
            if sPrevNext == '2':
                response.cont_key = '2'
            if len(in_singles) > 0:
                for field in in_singles:
                    response.single_datas.append(self.GetCommData(sTrCode, sRQName, 0, field).strip())

            if len(in_multis) > 0:
                repeatCount = self.GetRepeatCnt(sTrCode, sRQName)
                for i in range(repeatCount):
                    row = []
                    for field in in_multis:
                        row.append(self.GetCommData(sTrCode, sRQName, i, field).strip())
                    response.multi_datas.append(row)

        if tr_cd == "OPTKWFID": # 관심종목정보요청
            종목코드 = indata.get("종목코드")
            if 종목코드 is None:
                response.result_code = -300
                response.msg = "관심요청 입력값 오류: 종목코드를 설정해주세요"
                return response
            codes = 종목코드.split(';')
            # 빈문자열 제거
            codes = list(filter(None, codes))
            if len(codes) == 0:
                response.result_code = -300
                response.msg = "관심요청 입력값 오류: 종목코드가 없습니다"
                return response
            # ';'로 구분된 종목코드를 다시 연결
            종목코드 = ';'.join(codes)
            request_time = time.time()
            start_time = time.perf_counter_ns()
            (response.result_code, response.msg) = await self.CommKwRqDataAsync(종목코드, 0, len(codes), 0, "관심종목정보요청", scr_num, inner_callback)
            response.request_time = request_time
            response.elapsed_ms = (time.perf_counter_ns() - start_time) / 1000000
            return response

        # TR 입력값 설정
        for key, value in indata.items():
            self.SetInputValue(key, value)

        # TR 요청
        request_time = time.time()
        start_time = time.perf_counter_ns()
        (response.result_code, response.msg) = await self.CommRqDataAsync(tr_cd, tr_cd, 2 if cont_key == '2' else 0, scr_num, inner_callback)
        response.request_time = request_time
        response.elapsed_ms = (time.perf_counter_ns() - start_time) / 1000000
        return response

    async def SendOrderAsync(self, sRQName: str, sScreenNo: str, sAccNo: str, nOrderType: int, sCode: str, nQty: int, nPrice: int, sHogaGb: str, sOrgOrderNo: str) -> tuple[int, str]:
        '''
        비동기 주문 요청 함수
        결과값 : (ret, msg)
        ret : 0 - 성공, 그외 - 실패, msg : 에러메시지
        '''
        hashid = _asyncNode.get_hash_id(sRQName, "SendOrderAsync", sScreenNo)
        response = ResponseData()
        def inner_callback(sScrNo, sRQName, sTrCode, sRecordName, sPrevNext, nDataLength, sErrorCode, sMessage, sSplmMsg):
            response.msg = self.GetCommData(sTrCode, sRQName, 0, "주문번호")
        node = _asyncNode(hashid)
        node.callback = inner_callback
        self._asyncNodes.append(node)
        ret = self.SendOrder(sRQName, sScreenNo, sAccNo, nOrderType, sCode, nQty, nPrice, sHogaGb, sOrgOrderNo)
        if ret == 0:
            await node.wait(self.AsyncTimeOut)
            ret = node.async_result
        if ret == 0 and response.msg == '':
            ret = -903 # 주문번호가 없습니다.
        self._asyncNodes.remove(node)
        msg = node.async_msg
        if msg == '':
            msg = self.GetErrorMesage(ret)
        return ret, msg

    async def SendOrderFOAsync(self, sRQName: str, sScreenNo: str, sAccNo: str, sCode: str, lOrdKind: int, sSlbyTp: str, sOrdTp: str, lQty: int, sPrice: str, sOrgOrdNo: str) -> tuple[int, str]:
        '''
        비동기 선물옵션 주문 요청 함수
        결과값 : (ret, msg)
        ret : 0 - 성공, 그외 - 실패, msg : 에러메시지
        '''
        hashid = _asyncNode.get_hash_id(sRQName, "SendOrderAsync", sScreenNo)
        response = ResponseData()
        def inner_callback(sScrNo, sRQName, sTrCode, sRecordName, sPrevNext, nDataLength, sErrorCode, sMessage, sSplmMsg):
            response.msg = self.GetCommData(sTrCode, sRQName, 0, "주문번호")
        node = _asyncNode(hashid)
        node.callback = inner_callback
        self._asyncNodes.append(node)
        ret = self.SendOrderFO(sRQName, sScreenNo, sAccNo, sCode, lOrdKind, sSlbyTp, sOrdTp, lQty, sPrice, sOrgOrdNo)
        if ret == 0:
            await node.wait(self.AsyncTimeOut)
            ret = node.async_result
        if ret == 0 and response.msg == '':
            ret = -903 # 주문번호가 없습니다.
        self._asyncNodes.remove(node)
        msg = node.async_msg
        if msg == '':
            msg = self.GetErrorMesage(ret)
        return ret, msg

    async def SendOrderCreditAsync(self, sRQName: str, sScreenNo: str, sAccNo: str, nOrderType: int, sCode: str, nQty: int, nPrice: int, sHogaGb: str, sCreditGb: str, sLoanDate: str, sOrgOrderNo: str) -> tuple[int, str]:
        '''
        비동기 신용주문 요청 함수
        결과값 : (ret, msg)
        ret : 0 - 성공, 그외 - 실패, msg : 에러메시지
        '''
        hashid = _asyncNode.get_hash_id(sRQName, "SendOrderAsync", sScreenNo)
        response = ResponseData()
        def inner_callback(sScrNo, sRQName, sTrCode, sRecordName, sPrevNext, nDataLength, sErrorCode, sMessage, sSplmMsg):
            response.msg = self.GetCommData(sTrCode, sRQName, 0, "주문번호")
        node = _asyncNode(hashid)
        node.callback = inner_callback
        self._asyncNodes.append(node)
        ret = self.SendOrderCredit(sRQName, sScreenNo, sAccNo, nOrderType, sCode, nQty, nPrice, sHogaGb, sCreditGb, sLoanDate, sOrgOrderNo)
        if ret == 0:
            await node.wait(self.AsyncTimeOut)
            ret = node.async_result
        if ret == 0 and response.msg == '':
            ret = -903 # 주문번호가 없습니다.
        self._asyncNodes.remove(node)
        msg = node.async_msg
        if msg == '':
            msg = self.GetErrorMesage(ret)
        return ret, msg

    def GetErrorMesage(self, err_code: int) -> str:
        match err_code:
            case 1: return "정상처리"
            case 0: return "정상처리"
            case -10 : return "실패"
            case -11 : return "조건번호 없음"
            case -12 : return "조건번호와 조건식 불일치"
            case -13 : return "조건검색 조회요청 초과"
            case -100 : return "사용자정보교환 실패"
            case -101 : return "서버 접속 실패"
            case -102 : return "버전처리 실패"
            case -103 : return "개인방화벽 실패"
            case -104 : return "메모리 보호실패"
            case -105 : return "함수입력값 오류"
            case -106 : return "통신연결 종료"
            case -107 : return "보안모듈 오류"
            case -108 : return "공인인증 로그인 필요"
            case -200 : return "시세조회 과부하"
            case -201 : return "전문작성 초기화 실패"
            case -202 : return "전문작성 입력값 오류"
            case -203 : return "데이터 없음"
            case -204 : return "조회가능한 종목수 초과"
            case -205 : return "데이터 수신 실패"
            case -206 : return "조회가능한 FID수 초과"
            case -207 : return "실시간 해제 오류"
            case -209 : return "시세조회제한"
            case -300 : return "입력값 오류"
            case -301 : return "계좌비밀번호 없음"
            case -302 : return "타인계좌 사용오류"
            case -303 : return "주문가격이 주문착오 금액기준 초과"
            case -304 : return "주문가격이 주문착오 금액기준 초과"
            case -305 : return "주문수량이 총발행주수의 1% 초과오류"
            case -306 : return "주문수량은 총발행주수의 3% 초과오류"
            case -307 : return "주문전송 실패"
            case -308 : return "주문전송 과부하"
            case -309 : return "주문수량 300계약 초과"
            case -310 : return "주문수량 500계약 초과"
            case -311 : return "주문전송제한 과부하"
            case -340 : return "계좌정보 없음"
            case -500 : return "종목코드 없음"
            case -901 : return "비동기요청: 이미 작동중 입니다"
            case -902 : return "비동기요청: 타임아웃"
            case -903 : return "비동기요청: 주문번호가 없습니다."

        return f'[{err_code}]: unknown'

    pass

class KfAsync(KFOpenApiDispatch, QObject):
    '''
    키움증권 해외 API 비동기 처리 클래스
    '''

    OnReceiveTrData = pyqtSignal(str, str, str, str, str, int, str, str, str)
    OnReceiveMsg = pyqtSignal(str, str, str, str)
    OnEventConnect = pyqtSignal(int)

    def __init__(self, ocx = None):
        super().__init__()

        if ocx is None:
            ocx = QAxWidget("KFOPENAPI.KFOpenAPICtrl.1")

        # Connect signals
        ocx.OnReceiveTrData.connect(self.__inner_OnReceiveTrData)
        ocx.OnReceiveMsg.connect(self.__inner_OnReceiveMsg)
        ocx.OnEventConnect.connect(self.__inner_OnEventConnect)

        # Register signals
        self.OnReceiveRealData = ocx.OnReceiveRealData
        self.OnReceiveChejanData = ocx.OnReceiveChejanData

        # Register methods
        self.CommConnect = ocx.CommConnect
        self.CommRqData = ocx.CommRqData
        self.SetInputValue = ocx.SetInputValue
        self.GetCommData = ocx.GetCommData
        self.CommTerminate = ocx.CommTerminate
        self.GetRepeatCnt = ocx.GetRepeatCnt
        self.DisconnectRealData = ocx.DisconnectRealData
        self.GetCommRealData = ocx.GetCommRealData
        self.GetChejanData = ocx.GetChejanData
        self.SendOrder = ocx.SendOrder
        self.GetLoginInfo = ocx.GetLoginInfo
        self.GetGlobalFutureItemlist = ocx.GetGlobalFutureItemlist
        self.GetGlobalOptionItemlist = ocx.GetGlobalOptionItemlist
        self.GetGlobalFutureCodelist = ocx.GetGlobalFutureCodelist
        self.GetGlobalOptionCodelist = ocx.GetGlobalOptionCodelist
        self.GetConnectState = ocx.GetConnectState
        self.GetAPIModulePath = ocx.GetAPIModulePath
        self.GetCommonFunc = ocx.GetCommonFunc
        self.GetConvertPrice = ocx.GetConvertPrice
        self.GetGlobalFutOpCodeInfoByType = ocx.GetGlobalFutOpCodeInfoByType
        self.GetGlobalFutOpCodeInfoByCode = ocx.GetGlobalFutOpCodeInfoByCode
        self.GetGlobalFutureItemlistByType = ocx.GetGlobalFutureItemlistByType
        self.GetGlobalFutureCodeByItemMonth = ocx.GetGlobalFutureCodeByItemMonth
        self.GetGlobalOptionCodeByMonth = ocx.GetGlobalOptionCodeByMonth
        self.GetGlobalOptionMonthByItem = ocx.GetGlobalOptionMonthByItem
        self.GetGlobalOptionActPriceByItem = ocx.GetGlobalOptionActPriceByItem
        self.GetGlobalFutureItemTypelist = ocx.GetGlobalFutureItemTypelist
        self.GetCommFullData = ocx.GetCommFullData

        # Register properties
        self.ocx = ocx
        self.AsyncTimeOut = 10
        self._asyncNodes: list[_asyncNode] = []

    def __inner_OnReceiveTrData(self, sScrNo, sRQName, sTrCode, sRecordName, sPrevNext, sMessage):
        hashid_order = _asyncNode.get_hash_id(sRQName, "SendOrderAsync", sScrNo)
        hashid = _asyncNode.get_hash_id(sRQName, sTrCode, sScrNo)
        for node in self._asyncNodes:
            if node.hashid == hashid_order or node.hashid == hashid:
                node.async_evented = True
                if node.callback is not None:
                    node.callback(sScrNo, sRQName, sTrCode, sRecordName, sPrevNext, sMessage)
                node.set()
                return
        self.OnReceiveTrData.emit(sScrNo, sRQName, sTrCode, sRecordName, sPrevNext, sMessage)

    def __inner_OnReceiveMsg(self, sScrNo, sRQName, sTrCode, sMsg):
        hashid_order = _asyncNode.get_hash_id(sRQName, "SendOrderAsync", sScrNo)
        hashid = _asyncNode.get_hash_id(sRQName, sTrCode, sScrNo)
        for node in self._asyncNodes:
            if node.hashid == hashid_order or node.hashid == hashid:
                node.async_evented = True
                node.async_msg = sMsg
            return
        self.OnReceiveMsg.emit(sScrNo, sRQName, sTrCode, sMsg)

    def __inner_OnEventConnect(self, err_code):
        hashid = _asyncNode.get_hash_id("CommConnectAsync")
        for node in self._asyncNodes:
            if node.hashid == hashid:
                node.async_evented = True
                node.async_result = err_code
                node.set()
                return
        self.OnEventConnect.emit(err_code)

    _requreMinIndex = 9950
    _requreMaxIndex = 9999
    _requestIndex = _requreMinIndex

    def __get_request_scrNum(self):
        self._requestIndex += 1
        if self._requestIndex > self._requreMaxIndex:
            self._requestIndex = self._requreMinIndex
        return str(self._requestIndex).zfill(4)

    async def CommConnectAsync(self, nAutoUpgrade: int) -> tuple[int, str]:
        '''
        비동기 로그인 함수
        결과값 : (ret, msg)
        ret : 0 - 성공, 그외 - 실패, msg : 에러메시지
        '''
        hashid = _asyncNode.get_hash_id("CommConnectAsync")
        # Check if the same request is already in the list
        for node in self._asyncNodes:
            if node.hashid == hashid:
                return -901, self.GetErrorMesage(-901)
        # Create a new node
        node = _asyncNode(hashid)
        self._asyncNodes.append(node)
        ret = self.CommConnect(nAutoUpgrade)
        if ret == 0:
            await node.wait()
            ret = node.async_result
        self._asyncNodes.remove(node)
        return ret, self.GetErrorMesage(ret)

    async def CommRqDataAsync(self, sRQName: str, sTrCode: str, sPrevNext: str, sScreenNo: str, callback) -> tuple[int, str]:
        '''
        비동기 TR 요청 함수
        callback : def callback(sScrNo, sRQName, sTrCode, sRecordName, sPrevNext, sMessage) 로 OnReceiveTrData 이벤트 처리부 호출
        결과값 : (ret, msg)
        ret : 0 - 성공, 그외 - 실패, msg :
        '''
        hashid = _asyncNode.get_hash_id(sRQName, sTrCode, sScreenNo)
        # Create a new node
        node = _asyncNode(hashid)
        node.callback = callback
        self._asyncNodes.append(node)
        ret = self.CommRqData(sRQName, sTrCode, sPrevNext, sScreenNo)
        if ret == 0:
            await node.wait(self.AsyncTimeOut)
            ret = node.async_result
        msg = node.async_msg
        if msg == '':
            msg = self.GetErrorMesage(ret)
        self._asyncNodes.remove(node)
        return ret, msg

    async def SendOrderAsync(self, sRQName: str, sScreenNo: str, sAccNo: str, nOrderType: int, sCode: str, nQty: int, sPrice: str, sStopPrice: str, sHogaGb: str, sOrgOrderNo: str) -> tuple[int, str]:
        '''
        비동기 주문 함수
        결과값 : (ret, msg)
        ret : 0 - 성공, 그외 - 실패, msg : 에러메시지
        '''
        hashid = _asyncNode.get_hash_id(sRQName, "SendOrderAsync", sScreenNo)
        response = ResponseData()
        def inner_callback(sScrNo, sRQName, sTrCode, sRecordName, sPrevNext, sMessage):
            response.msg = self.GetCommData(sTrCode, sRQName, 0, "주문번호")
        node = _asyncNode(hashid)
        node.callback = inner_callback
        self._asyncNodes.append(node)
        ret = self.SendOrder(sRQName, sScreenNo, sAccNo, nOrderType, sCode, nQty, sPrice, sStopPrice, sHogaGb, sOrgOrderNo)
        if ret == 0:
            await node.wait(self.AsyncTimeOut)
            ret = node.async_result
        if ret == 0 and response.msg == '':
            ret = -903
        self._asyncNodes.remove(node)
        msg = node.async_msg
        if msg == '':
            msg = self.GetErrorMesage(ret)
        return ret, msg

    async def RequestTrAsync(self, tr_cd: str, indata: dict
                            , in_singles: list = []
                            , in_multis: list = []
                            , cont_key: str = '') -> ResponseData:
        '''
        비동기 간편 TR 요청 함수
        tr_cd : TR 코드
        indata : 입력값(딕셔너리)
        in_singles: 가져올 단일데이터 필드 리스트
        in_multis: 가져올 다중데이터 필드 리스트

        결과값 : ResponseData객체
        ResponseData.result_code : 0 - 성공, 그외 - 실패
        ResponseData.msg : 에러메시지
        ResponseData.single_datas : 단일데이터
        ResponseData.multi_datas : 다중데이터(2차원 리스트)
        ResponseData.cont_key : 연속키
        ResponseData.in_singles : 입력된 단일데이터 리스트
        ResponseData.in_multis : 입력된 멀티데이터 리스트

        ※ 화면번호 자동할당(9950~9999)
        요청시 실시간연결은 자동해제
        출력데이터는 strip 처리하여 반환
        '''
        scr_num = self.__get_request_scrNum()
    
        for key, value in indata.items():
            self.SetInputValue(key, value)
    
        response = ResponseData()
        response.tr_cd = tr_cd
        response.in_singles = in_singles
        response.in_multis = in_multis
    
        def inner_callback(sScrNo, sRQName, sTrCode, sRecordName, sPrevNext, sMessage):
            self.DisconnectRealData(sScrNo)
            response.cont_key = sPrevNext
            if in_singles is not None:
                for field in in_singles:
                    response.single_datas.append(self.GetCommData(sTrCode, sRQName, 0, field).strip())
    
            if in_multis is not None:
                repeatCount = self.GetRepeatCnt(sTrCode, sRQName)
                for i in range(repeatCount):
                    row = []
                    for field in in_multis:
                        row.append(self.GetCommData(sTrCode, sRQName, i, field).strip())
                    response.multi_datas.append(row)
    
        request_time = time.time()
        start_time = time.perf_counter_ns()
        (response.result_code, response.msg) = await self.CommRqDataAsync(tr_cd, tr_cd, cont_key, scr_num, inner_callback)
        response.request_time = request_time
        response.elapsed_ms = (time.perf_counter_ns() - start_time) / 1000000
        return response

    def GetErrorMesage(self, err_code: int) -> str:
        match err_code:
            case 1: return "정상처리"
            case 0: return "정상처리"
            case -1 : return "미접속상태"
            case -100 : return "로그인시 접속 실패 (아이피오류 또는 접속정보 오류)"
            case -101 : return "서버 접속 실패"
            case -102 : return "버전처리 실패"
            case -103 : return "TrCode가 존재하지 않습니다."
            case -104 : return "해외OpenAPI 미신청"
            case -200 : return "시세조회 과부하"
            case -201 : return "주문과부하"
            case -202 : return "전문작성 입력값 오류"
            case -203 : return "데이터 없음"
            case -300 : return "주문입력값 오류"
            case -301 : return "계좌비밀번호 없음"
            case -302 : return "타인계좌 사용오류"
            case -303 : return "경고-주문수량 200개 초과"
            case -304 : return "제한-주문수량 400개 초과"
            case -901 : return "비동기요청: 이미 작동중 입니다"
            case -902 : return "비동기요청: 타임아웃"
            case -903 : return "비동기요청: 주문번호가 없습니다."

        return f'[{err_code}]: unknown'


    pass

class _asyncNode:
    def __init__(self, hashid):
        self.__event = asyncio.Event()
        self.hashid = hashid
        self.async_evented : bool = False
        self.async_msg : str = ''
        self.async_result = 0
        self.callback = None

    def __hash__(self):
        return self.hashid

    def __eq__(self, other):
        return self.hashid == other.hashid

    def set(self):
        self.__event.set()

    async def wait(self, timeout=None):
        if timeout is None:
            await self.__event.wait()
            return True
        try:
            await asyncio.wait_for(self.__event.wait(), timeout)
            return True
        except asyncio.TimeoutError:
            if self.async_evented is False:
                self.async_result = -902
            return False

    @staticmethod
    def get_hash_id(*args):
        hashid = 0
        for i in args:
            hashid += hash(i)
        return hashid
