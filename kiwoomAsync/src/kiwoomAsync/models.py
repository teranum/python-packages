class ResponseData:
    '''
    RequestTrAsync ��û ���� Ŭ����
    '''

    result_code = 0
    ''' ��� �ڵ�, 0 - ����, �׿� - ����, �����޽����� msg'''

    msg = ''
    ''' �����޽��� '''

    tr_cd = ''
    ''' TR �ڵ� '''

    single_datas = []
    ''' ���� ������ ����Ʈ '''

    multi_datas = []
    ''' ���� ������(2���� ����Ʈ) '''

    cont_key = ''
    ''' ����Ű '''


    in_singles = []
    ''' �Էµ� ���� ������ ����Ʈ '''

    in_multis = []
    ''' �Էµ� ���� ������ ����Ʈ '''

    pass

