import sys
from dashboard import *
from data_manipulation import *

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(GLOBAL_STYLES)
    db = DataHandler()
    window = DashBoard(db)
    window.show()
    sys.exit(app.exec_())