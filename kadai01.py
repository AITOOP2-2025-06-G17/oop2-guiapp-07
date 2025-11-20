import ffmpeg
import time

print("--- 課題01: 録音処理開始 ---")

# 録音時間（秒）と出力ファイル名を設定
duration = 10
output_file = 'python-audio-output.wav'

try:
    print(f"{duration}秒間、マイクからの録音を開始します...")
    # FFmpegを使用してマイクから録音
    # macOSの場合は'avfoundation'、Windowsは'dshow'、Linuxは'alsa'を指定
    (
        ffmpeg
        .input(':0', format='avfoundation', t=duration) # macOSの例
        .output(output_file, acodec='pcm_s16le', ar='44100', ac=1)
        .run(overwrite_output=True, capture_stdout=True, capture_stderr=True)
    )
    print(f"録音が完了しました。'{output_file}' に保存されました。")

except ffmpeg.Error as e:
    print("エラーが発生しました: FFmpegの実行に失敗しました。")
    print(f"STDERR: {e.stderr.decode()}")
except Exception as e:
    print(f"予期せぬエラーが発生しました: {e}")

print("--- 課題01: 録音処理終了 ---\n")