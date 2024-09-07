class ResponseData:
    '''
    RequestTrAsync 요청 응답 클래스
    '''

    result_code = 0
    ''' 결과 코드, 0 - 성공, 그외 - 실패, 오류메시지는 msg'''

    msg = ''
    ''' 에러메시지 '''

    tr_cd = ''
    ''' TR 코드 '''

    single_datas = []
    ''' 단일 데이터 리스트 '''

    multi_datas = []
    ''' 다중 데이터(2차원 리스트) '''

    cont_key = ''
    ''' 연속키 '''


    in_singles = []
    ''' 입력된 단일 데이터 리스트 '''

    in_multis = []
    ''' 입력된 다중 데이터 리스트 '''

    pass

