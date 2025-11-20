# main_gui.py
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QLineEdit,
    QVBoxLayout, QWidget, QFileDialog, QMessageBox
)
from PyQt6.QtCore import Qt

from async_worker import AudioWorker
import config_manager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("音声録音・文字起こしアプリ")
        self.setGeometry(100, 100, 400, 250)

        # 設定読み込み
        self.config = config_manager.load_config()

        # ウィジェット作成
        self.filename_label = QLabel(f"出力ファイル: {self.config['output_filename']}")
        self.status_label = QLabel("ステータス: 待機中")
        self.duration_input = QLineEdit(str(self.config.get('record_duration', 10)))
        self.duration_input.setPlaceholderText("録音時間（秒）")

        self.record_button = QPushButton("録音開始")
        self.transcribe_button = QPushButton("文字起こし")
        self.select_file_button = QPushButton("ファイル選択")
        self.save_config_button = QPushButton("設定保存")

        # レイアウト
        layout = QVBoxLayout()
        layout.addWidget(self.filename_label)
        layout.addWidget(self.select_file_button)
        layout.addWidget(QLabel("録音時間（秒）:"))
        layout.addWidget(self.duration_input)
        layout.addWidget(self.record_button)
        layout.addWidget(self.transcribe_button)
        layout.addWidget(self.save_config_button)
        layout.addWidget(self.status_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # シグナル接続
        self.record_button.clicked.connect(self.start_record)
        self.transcribe_button.clicked.connect(self.start_transcribe)
        self.select_file_button.clicked.connect(self.select_file)
        self.save_config_button.clicked.connect(self.save_config)

    def select_file(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "保存先を選択", self.config.get('output_filename', 'output.wav'), "WAV Files (*.wav)"
        )
        if file_path:
            self.config['output_filename'] = file_path
            self.filename_label.setText(f"出力ファイル: {file_path}")

    def save_config(self):
        # 録音時間を保存
        try:
            self.config['record_duration'] = int(self.duration_input.text())
        except ValueError:
            QMessageBox.warning(self, "警告", "録音時間は整数で入力してください。")
            return

        config_manager.save_config(self.config)
        QMessageBox.information(self, "情報", "設定を保存しました。")

    def start_record(self):
        self.status_label.setText("ステータス: 録音中...")
        filename = self.config['output_filename']
        duration = int(self.duration_input.text())
        self.record_button.setEnabled(False)
        self.transcribe_button.setEnabled(False)

        self.worker = AudioWorker("record", filename=filename, duration=duration)
        self.worker.finished_signal.connect(self.on_success)
        self.worker.error_signal.connect(self.on_error)
        self.worker.start()

    def start_transcribe(self):
        self.status_label.setText("ステータス: 文字起こし中...")
        filename = self.config['output_filename']
        model = self.config.get('model_name', 'mlx-community/whisper-base-mlx')
        self.record_button.setEnabled(False)
        self.transcribe_button.setEnabled(False)

        self.worker = AudioWorker("transcribe", filename=filename, model=model)
        self.worker.finished_signal.connect(self.on_success)
        self.worker.error_signal.connect(self.on_error)
        self.worker.start()

    def on_success(self, result):
        self.status_label.setText(f"ステータス: 完了")
        QMessageBox.information(self, "完了", str(result))
        self.record_button.setEnabled(True)
        self.transcribe_button.setEnabled(True)

    def on_error(self, msg):
        self.status_label.setText("ステータス: エラー")
        QMessageBox.critical(self, "エラー", msg)
        self.record_button.setEnabled(True)
        self.transcribe_button.setEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())