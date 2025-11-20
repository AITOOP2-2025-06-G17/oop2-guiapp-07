import mlx_whisper
from pydub import AudioSegment
import numpy as np
import os

# 文字起こしに使用するモデル
model_name = "mlx-community/whisper-base-mlx"

# 入力するWAVファイル名
full_audio_file   = "python-audio-output.wav"
before_audio_file = "audio-output-before.wav"
after_audio_file  = "audio-output-after.wav"
## ---------------------------------------------

print("--- 課題03: 文字起こし処理開始 ---")

# 文字起こし対象のファイルリスト
files_to_transcribe = [full_audio_file, before_audio_file, after_audio_file]

# 音声データを前処理する関数
def preprocess_audio(sound):
    if sound.frame_rate != 16000:
        sound = sound.set_frame_rate(16000)
    if sound.sample_width != 2:
        sound = sound.set_sample_width(2)
    if sound.channels != 1:
        sound = sound.set_channels(1)
    return sound

# 各ファイルを順番に文字起こし
for i, file_path in enumerate(files_to_transcribe):
    print(f"\n[{i+1}/{len(files_to_transcribe)}] '{file_path}' の文字起こし中...")
    
    # ファイルが存在するかチェック
    if not os.path.exists(file_path):
        print(f"エラー: 入力ファイル '{file_path}' が見つかりません。")
        continue # 次のファイルへ

    try:
        # 音声データをファイルから読み込む
        audio_data = AudioSegment.from_file(file_path, format="wav")
        
        # 前処理を実行
        sound = preprocess_audio(audio_data)
        
        # Numpy Array形式に変換
        arr = np.array(sound.get_array_of_samples()).astype(np.float32) / 32768.0
        
        # 文字起こしを実行
        result = mlx_whisper.transcribe(
            arr, path_or_hf_repo=model_name
        )
        print("--- 結果 ---")
        print(result['text'])
        print("------------")

    except Exception as e:
        print(f"エラー: '{file_path}' の文字起こし中に問題が発生しました: {e}")

print("\n--- 課題03: 文字起こし処理終了 ---")