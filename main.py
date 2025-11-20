# main.py
import sys
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QLabel,
    QTextEdit, QLineEdit, QVBoxLayout, QHBoxLayout, QGroupBox
)
from PySide6.QtCore import Qt

# Aが未実装でも動くダミー
try:
    from audio_processor import record_audio, slice_audio, transcribe_audio
except ImportError:
    def record_audio(*args, **kwargs):
        return "dummy_record.wav"

    def slice_audio(*args, **kwargs):
        return ["slice1.wav", "slice2.wav"]

    def transcribe_audio(*args, **kwargs):
        return "これはダミーの文字起こしです"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Audio Tool (GUI Base)")
        self.setMinimumSize(600, 500)

        main_layout = QVBoxLayout()

        # -------------------------
        # 録音エリア
        # -------------------------
        # 録音ボタン ("録音開始") を押すと:
        #   -> self.on_record_clicked() が呼ばれる
        #       -> 内部で record_audio() を呼び出す
        #       -> 戻り値: 録音ファイルのパス (例: "dummy_record.wav") を取得
        #       -> self.record_status に録音結果の可否を表示

        record_group = QGroupBox("録音")
        record_layout = QVBoxLayout()
        self.record_button = QPushButton("録音開始")
        self.record_button.clicked.connect(self.on_record_clicked)
        self.record_status = QLabel("待機中")
        record_layout.addWidget(self.record_button)
        record_layout.addWidget(self.record_status)
        record_group.setLayout(record_layout)
        main_layout.addWidget(record_group)

        # -------------------------
        # スライスエリア
        # -------------------------
        #   -> self.on_slice_clicked() が呼ばれる
        #       -> self.slice_time_input から秒数を取得
        #       -> slice_audio(duration=int(sec)) を呼び出す
        #       -> 戻り値: 分割された音声ファイルのリスト (例: ["slice1.wav", "slice2.wav"])
        #       -> self.slice_result_label に出力ファイルのリストを表示

        slice_group = QGroupBox("スライス")
        slice_layout = QVBoxLayout()
        slice_input_layout = QHBoxLayout()
        self.slice_time_input = QLineEdit()
        self.slice_time_input.setPlaceholderText("スライス秒数 (例: 5)")
        self.slice_button = QPushButton("スライス実行")
        self.slice_button.clicked.connect(self.on_slice_clicked)
        slice_input_layout.addWidget(self.slice_time_input)
        slice_input_layout.addWidget(self.slice_button)
        slice_layout.addLayout(slice_input_layout)
        self.slice_result_label = QLabel("出力パス: -")
        slice_layout.addWidget(self.slice_result_label)
        slice_group.setLayout(slice_layout)
        main_layout.addWidget(slice_group)

        # -------------------------
        # 文字起こしエリア
        # -------------------------
        trans_group = QGroupBox("文字起こし")
        trans_layout = QVBoxLayout()
        self.trans_button = QPushButton("文字起こし実行")
        self.trans_button.clicked.connect(self.on_transcribe_clicked)
        self.trans_result = QTextEdit()
        self.trans_result.setPlaceholderText("文字起こし結果がここに表示されます")
        self.trans_path_label = QLabel("保存パス: -")  # 保存パス表示用

        trans_layout.addWidget(self.trans_button)
        trans_layout.addWidget(self.trans_result)
        trans_layout.addWidget(self.trans_path_label)

        trans_group.setLayout(trans_layout)
        main_layout.addWidget(trans_group)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    # -------------------------
    # Slots
    # -------------------------
    def on_record_clicked(self):
        self.record_status.setText("録音中…（ダミー）")
        result = record_audio()
        self.record_status.setText(f"録音完了: {result}")

    def on_slice_clicked(self):
        sec = self.slice_time_input.text()
        if not sec.isdigit():
            self.slice_result_label.setText("エラー: 数字を入力して")
            return
        result_files = slice_audio(duration=int(sec))
        self.slice_result_label.setText(f"出力: {result_files}")

    def on_transcribe_clicked(self):
        text = transcribe_audio()
        self.trans_result.setPlainText(text)

        # 保存
        save_dir = Path.cwd() / "output"
        save_dir.mkdir(exist_ok=True)
        save_path = save_dir / "transcription.txt"
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(text)

        # 保存パスをGUIに表示
        self.trans_path_label.setText(f"保存パス: {save_path}")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
