import sys
import time
from PyQt6.QtCore import QCoreApplication
from async_worker import AudioWorker

# PyQtのシグナルを受け取るための最小限の設定
app = QCoreApplication(sys.argv)

def on_finished(result):
    print(f"\n🎉 完了通知が来ました: {result}")
    app.quit() # テスト終了

def on_error(err):
    print(f"\n⚠️ エラー通知が来ました: {err}")
    app.quit() # テスト終了

print("--- 非同期処理テスト開始 ---")
print("メイン処理は止まりません。裏で録音(3秒)を開始します...")

# Workerを作成して設定
# テスト用に短く3秒で録音
worker = AudioWorker("record", filename="async_test.wav", duration=3)

# 完了・エラー時の連絡先を登録
worker.finished_signal.connect(on_finished)
worker.error_signal.connect(on_error)

# お仕事開始！
worker.start()

# Workerが動いている間、メイン側で別の表示を出してみる
for i in range(5):
    time.sleep(0.5)
    print(".", end="", flush=True)

# イベントループ開始（処理が終わるのを待つ）
sys.exit(app.exec())