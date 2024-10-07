class ResponseData:
    '''
    RequestTrAsync 요청 응답 클래스
    '''

    def __init__(self):
        self.result_code = 0
        ''' 결과 코드, 0 - 성공, 그외 - 실패, 오류메시지는 msg'''
        self.msg = ''
        ''' 에러메시지 '''
        self.tr_cd = ''
        ''' TR 코드 '''
        self.single_datas = []
        ''' 단일 데이터 리스트 '''
        self.multi_datas = []
        ''' 다중 데이터(2차원 리스트) '''
        self.cont_key = ''
        ''' 연속키 '''
        self.in_singles = []
        ''' 입력된 단일 데이터 리스트 '''
        self.in_multis = []
        ''' 입력된 다중 데이터 리스트 '''
