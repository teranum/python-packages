import sys, asyncio
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from qasync import QEventLoop, asyncSlot
from kiwoomAsync import KhAsync

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.api = KhAsync()
        self.setWindowTitle('키움 API 비동기 테스트')
        self.setGeometry(300, 300, 300, 150)
        self.login_btn = QPushButton('로그인', self)
        self.login_btn.move(20, 20)
        self.login_btn.clicked.connect(self.func_login)

    @asyncSlot()
    async def func_login(self):
        self.login_btn.setEnabled(False)
        (ret, msg) = await self.api.CommConnectAsync()
        if ret != 0:
            print(f'로그인 실패: {msg}')
        simulation = self.api.GetLoginInfo("GetServerGubun") == '1';
        print('로그인 성공: ' + ('모의투자' if simulation else '실투자'))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    window = MainWindow()
    window.show()
    
    with loop:
        # loop.run_until_complete(window.func_login()) # 메인창 생성 후 바로 로그인 시도
        loop.run_forever()


