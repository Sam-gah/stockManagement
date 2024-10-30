from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLineEdit, QPushButton, QMessageBox) # type: ignore

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('Login')
        self.setGeometry(300, 300, 300, 150)
        
        layout = QVBoxLayout()
        
        # Username input
        self.username = QLineEdit()
        self.username.setPlaceholderText('Username')
        layout.addWidget(self.username)
        
        # Password input
        self.password = QLineEdit()
        self.password.setPlaceholderText('Password')
        self.password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password)
        
        # Login button
        login_button = QPushButton('Login')
        login_button.clicked.connect(self.handle_login)
        layout.addWidget(login_button)
        
        self.setLayout(layout)
    
    def handle_login(self):
        if (self.username.text() == "admin" and 
            self.password.text() == "1234"):
            self.accept()
        else:
            QMessageBox.warning(
                self, 'Error', 'Invalid username or password')
            
