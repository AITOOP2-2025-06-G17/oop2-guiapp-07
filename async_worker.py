from PyQt6.QtCore import QThread, pyqtSignal
import audio_processor

class AudioWorker(QThread):
    """
    重い処理（録音・文字起こし）をバックグラウンドで実行するクラス
    """
    # 完了したときにGUIに通知するシグナル (成功時の結果, またはメッセージ)
    finished_signal = pyqtSignal(object)
    # エラーが起きたときに通知するシグナル
    error_signal = pyqtSignal(str)

    def __init__(self, task_type, **kwargs):
        """
        :param task_type: "record" または "transcribe"
        :param kwargs: 必要な引数 (filename, duration, model など)
        """
        super().__init__()
        self.task_type = task_type
        self.kwargs = kwargs

    def run(self):
        """
        start() が呼ばれると、この run() の中身が別スレッドで実行されます
        """
        try:
            if self.task_type == "record":
                # 録音処理を実行
                filename = self.kwargs.get('filename')
                duration = self.kwargs.get('duration', 10)
                
                success = audio_processor.record_audio(filename, duration=duration)
                
                if success:
                    self.finished_signal.emit(f"録音が完了しました: {filename}")
                else:
                    self.error_signal.emit("録音に失敗しました（FFmpegエラーなど）")

            elif self.task_type == "transcribe":
                # 文字起こし処理を実行
                filename = self.kwargs.get('filename')
                model = self.kwargs.get('model')
                
                text = audio_processor.transcribe_audio(filename, model)
                
                if "エラー" in text:
                    self.error_signal.emit(text)
                else:
                    self.finished_signal.emit(text)

        except Exception as e:
            self.error_signal.emit(f"予期せぬエラー: {e}")