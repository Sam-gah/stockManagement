import sys
from PyQt5.QtWidgets import QApplication ,QDialog  # type: ignore
from database.db_manager import DatabaseManager
from ui.mainAppWindow import MainAppWindow
from ui.login import LoginWindow # type: ignore


def main():
    app = QApplication(sys.argv)
    db_manager = DatabaseManager() 
    login_window = LoginWindow()
    login_window.show()
    if login_window.exec_() == QDialog.Accepted:
        # If login is successful, open the main application window with the database manager
        main_app = MainAppWindow(db_manager)
        main_app.show()
        sys.exit(app.exec_())
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()