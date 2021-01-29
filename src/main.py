from PyQt5.QtWidgets import QApplication, QFileDialog, QWidget, QLineEdit, QPushButton, QLabel, QVBoxLayout, QMessageBox
import sys
import subprocess

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(300, 500)

        layout = QVBoxLayout()

        self.binaryLabel = QLabel()
        self.binaryLabel.setText("Select the mp4decrypt binary file:")
        layout.addWidget(self.binaryLabel)

        self.binaryInput = QLineEdit()
        layout.addWidget(self.binaryInput)

        self.binaryButton = QPushButton("Select file")
        self.binaryButton.clicked.connect(self.getBinary)
        layout.addWidget(self.binaryButton)
                
        self.kidLabel = QLabel()
        self.kidLabel.setText("Enter the KID/key ID:")
        layout.addWidget(self.kidLabel)

        self.kidInput = QLineEdit()
        layout.addWidget(self.kidInput)

        self.keyLabel = QLabel()
        self.keyLabel.setText("Enter the key:")
        layout.addWidget(self.keyLabel)

        self.keyInput = QLineEdit()
        layout.addWidget(self.keyInput)

        self.encLabel = QLabel()
        self.encLabel.setText("Select the encrypted video/audio file:")
        layout.addWidget(self.encLabel)

        self.encInput = QLineEdit()
        layout.addWidget(self.encInput)

        self.encButton = QPushButton("Select file")
        self.encButton.clicked.connect(self.getEncrypted)
        layout.addWidget(self.encButton)

        self.dirLabel = QLabel()
        self.dirLabel.setText("Select the directory to save the decrypted video in:")
        layout.addWidget(self.dirLabel)

        self.dirInput = QLineEdit()
        layout.addWidget(self.dirInput)

        self.dirButton = QPushButton("Select directory")
        self.dirButton.clicked.connect(self.getDir)
        layout.addWidget(self.dirButton)
                
        self.startButton = QPushButton("Start")
        self.startButton.clicked.connect(self.decrypt)
        self.startButton.setStyleSheet("margin-top: 25px;padding: 4px")
        layout.addWidget(self.startButton)

        self.setLayout(layout)


    def getBinary(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open binary file", filter="Windows binary files (*.exe);;All Files (*)")

        if filename:
            self.binaryInput.setText(filename)
        else:
            self.binaryInput.setText("")


    def getEncrypted(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open encrypted file", filter="All Files (*)")

        if filename:
            self.encInput.setText(filename)
        else:
            self.encInput.setText("")

    
    def getDir(self):
        dirname = QFileDialog.getExistingDirectory(self, "Choose directory")

        if dirname:
            self.dirInput.setText(dirname)
        else:
            self.dirInput.setText("")


    def decrypt(self):
        if self.binaryInput.text() == "":
            self.msgError(text="No binary file provided.")
            return
        if self.kidInput.text() == "":
            self.msgError(text="No KID/key ID provided.")
            return
        if self.keyInput.text() == "":
            self.msgError(text="No key provided.")
            return
        if self.encInput.text() == "":
            self.msgError(text="No encrypted file provided.")
            return
        if self.dirInput.text() == "":
            self.msgError(text="No target directory provided.")
            return

        temp = self.encInput.text().split("/")[-1].split(".")[0]
        try:
            subprocess.run(args=[self.binaryInput.text(), "--key", f"{self.kidInput.text()}:{self.keyInput.text()}", self.encInput.text(), f"{self.dirInput.text()}/{temp}.mp4"], shell=True, check=True)
            msg = QMessageBox()
            msg.setText("Decryption complete!")
            msg.setIcon(QMessageBox.Information)
            x = msg.exec_()
        except:
            self.msgError(text="Decryption failed!")


    def msgError(self, text):
        msg = QMessageBox()
        msg.setText(text)
        msg.setIcon(QMessageBox.Critical)
        x = msg.exec_()
        return


if __name__ == "__main__":
    qapp = QApplication(sys.argv)

    app = App()
    app.show()

    sys.exit(qapp.exec_())
