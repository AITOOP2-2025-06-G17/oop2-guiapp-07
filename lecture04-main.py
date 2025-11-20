# lecture04_main.py

# 必要なライブラリをインポート
import ffmpeg
import time
from pydub import AudioSegment
import mlx_whisper
import numpy as np

# ==============================================================================
# 課題01: マイクから10秒間録音
# ==============================================================================
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


# ==============================================================================
# 課題02: 録音した音声ファイルをスライス
# ==============================================================================
print("--- 課題02: 音声スライス処理開始 ---")

try:
    # 録音したWAVファイルを読み込む
    audio = AudioSegment.from_file(output_file, format="wav")

    # 4秒より前の部分を抽出して保存 (pydubはミリ秒単位で扱う)
    end_ms = 4000
    before_audio = audio[:end_ms]
    before_file = "audio-output-before.wav"
    before_audio.export(before_file, format="wav")

    # 4秒以降の部分を抽出して保存
    start_ms = 4000
    after_audio = audio[start_ms:]
    after_file = "audio-output-after.wav"
    after_audio.export(after_file, format="wav")

    print(f"音声が4秒の前後でスライスされ、'{before_file}' と '{after_file}' として保存されました。")

except FileNotFoundError:
    print(f"エラー: '{output_file}' が見つかりません。録音が正常に完了したか確認してください。")
except Exception as e:
    print(f"音声のスライス中にエラーが発生しました: {e}")

print("--- 課題02: 音声スライス処理終了 ---\n")


# ==============================================================================
# 課題03: Whisperを使用して文字起こし
# ==============================================================================
print("--- 課題03: 文字起こし処理開始 ---")

# モデル名を指定
model_name = "mlx-community/whisper-base-mlx"

# 1. 元の音声ファイル全体を文字起こし
try:
    print(f"\n[1/3] '{output_file}' の文字起こし中...")
    result_full = mlx_whisper.transcribe(
        output_file, path_or_hf_repo=model_name
    )
    print("--- 結果 ---")
    print(result_full)
    print("------------")

except Exception as e:
    print(f"'{output_file}' の文字起こし中にエラーが発生しました: {e}")


# 2. スライスした音声ファイルをそれぞれ文字起こし
# 音声データをWhisperが要求する形式に前処理する関数
def preprocess_audio(sound):
    if sound.frame_rate != 16000:
        sound = sound.set_frame_rate(16000)
    if sound.sample_width != 2:
        sound = sound.set_sample_width(2)
    if sound.channels != 1:
        sound = sound.set_channels(1)
    return sound

# 文字起こし対象のファイルリスト
sliced_files = [before_file, after_file]

for i, file_path in enumerate(sliced_files):
    try:
        print(f"\n[{i+2}/3] '{file_path}' の文字起こし中...")
        # 音声データをファイルから読み込む
        audio_data = AudioSegment.from_file(file_path, format="wav")
        
        # 前処理を実行
        sound = preprocess_audio(audio_data)
        
        # Metal (GPU) が扱えるNumpy Array形式に変換
        arr = np.array(sound.get_array_of_samples()).astype(np.float32) / 32768.0
        
        # 文字起こしを実行
        result_sliced = mlx_whisper.transcribe(
            arr, path_or_hf_repo=model_name
        )
        print("--- 結果 ---")
        print(result_sliced)
        print("------------")

    except FileNotFoundError:
        print(f"エラー: '{file_path}' が見つかりません。音声スライスが正常に完了したか確認してください。")
    except Exception as e:
        print(f"'{file_path}' の文字起こし中にエラーが発生しました: {e}")

print("\n--- 課題03: 文字起こし処理終了 ---")
print("\n全ての処理が完了しました。")