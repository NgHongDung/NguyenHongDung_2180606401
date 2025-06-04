import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.rsa import Ui_mainWindow  # Đổi theo tên class trong UI bạn gửi
import requests

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)

        # Kết nối nút bấm, sửa tên nút Verify là pushButton_4 theo UI bạn gửi
        self.ui.btnGenKeys.clicked.connect(self.call_api_gen_keys)
        self.ui.btnEncrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btnDecrypt.clicked.connect(self.call_api_decrypt)
        self.ui.btnSign.clicked.connect(self.call_api_sign)
        self.ui.btnVerify.clicked.connect(self.call_api_verify)  # nút Verify tên pushButton_4

    def call_api_gen_keys(self):
        url = "http://127.0.0.1:5000/api/rsa/generate_keys"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText(data["message"])
                msg.exec_()
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText(f"Error: {response.status_code}\n{response.text}")
                msg.exec_()
        except requests.exceptions.RequestException as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(f"Request Error: {e}")
            msg.exec_()

    def call_api_encrypt(self):
        url = "http://127.0.0.1:5000/api/rsa/encrypt"
        payload = {
            "message": self.ui.textPlantext.toPlainText(),  # Sửa tên theo UI
            "key_type": "public"
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txtCipherText_2.setText(data["encrypted_message"])  # Sửa tên theo UI

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Encrypted Successfully")
                msg.exec_()
            else:
                error_message = f"Error: {response.status_code}"
                try:
                    error_data = response.json()
                    if "error" in error_data:
                        error_message += f"\n{error_data['error']}"
                    elif "message" in error_data:
                        error_message += f"\n{error_data['message']}"
                    else:
                        error_message += f"\n{response.text}"
                except ValueError:
                    error_message += f"\n{response.text}"

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText(error_message)
                msg.exec_()
        except requests.exceptions.RequestException as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(f"Request Error: {e}")
            msg.exec_()

    def call_api_decrypt(self):
        url = "http://127.0.0.1:5000/api/rsa/decrypt"
        payload = {
            "ciphertext": self.ui.txtCipherText_2.toPlainText(),  # Sửa tên theo UI
            "key_type": "private"
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.textPlantext.setText(data["decrypted_message"])  # Sửa tên theo UI

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Decrypted Successfully")
                msg.exec_()
            else:
                error_message = f"Error: {response.status_code}"
                try:
                    error_data = response.json()
                    if "error" in error_data:
                        error_message += f"\n{error_data['error']}"
                    elif "message" in error_data:
                        error_message += f"\n{error_data['message']}"
                    else:
                        error_message += f"\n{response.text}"
                except ValueError:
                    error_message += f"\n{response.text}"

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText(error_message)
                msg.exec_()
        except requests.exceptions.RequestException as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(f"Request Error: {e}")
            msg.exec_()

    def call_api_sign(self):
        url = "http://127.0.0.1:5000/api/rsa/sign"
        payload = {
            "message": self.ui.txtInfor.toPlainText()
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txtSign.setText(data["signature"])  # Sửa tên theo UI

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Signed Successfully")
                msg.exec_()
            else:
                error_message = f"Error: {response.status_code}"
                try:
                    error_data = response.json()
                    if "error" in error_data:
                        error_message += f"\n{error_data['error']}"
                    elif "message" in error_data:
                        error_message += f"\n{error_data['message']}"
                    else:
                        error_message += f"\n{response.text}"
                except ValueError:
                    error_message += f"\n{response.text}"

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText(error_message)
                msg.exec_()
        except requests.exceptions.RequestException as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(f"Request Error: {e}")
            msg.exec_()

    def call_api_verify(self):
        url = "http://127.0.0.1:5000/api/rsa/verify"
        payload = {
            "message": self.ui.txtInfor.toPlainText(),
            "signature": self.ui.txtSign.toPlainText()
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                if data.get("is_verified", False):
                    msg.setText("Verified Successfully")
                else:
                    msg.setText("Verification Failed")
                msg.exec_()
            else:
                error_message = f"Error: {response.status_code}"
                try:
                    error_data = response.json()
                    if "error" in error_data:
                        error_message += f"\n{error_data['error']}"
                    elif "message" in error_data:
                        error_message += f"\n{error_data['message']}"
                    else:
                        error_message += f"\n{response.text}"
                except ValueError:
                    error_message += f"\n{response.text}"

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText(error_message)
                msg.exec_()
        except requests.exceptions.RequestException as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(f"Request Error: {e}")
            msg.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
