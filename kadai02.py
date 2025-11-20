from pydub import AudioSegment
import os

## ---------------------------------------------
## 設定項目
## ---------------------------------------------
# 入力するWAVファイル名
input_wav_file = "python-audio-output.wav"

# 出力するファイル名
before_file = "audio-output-before.wav"
after_file = "audio-output-after.wav"
## ---------------------------------------------

print("--- 課題02: 音声スライス処理開始 ---")

# 入力ファイルが存在するかチェック
if not os.path.exists(input_wav_file):
    print(f"エラー: 入力ファイル '{input_wav_file}' が見つかりません。")
    print("先に録音を実行するか、同じフォルダにWAVファイルを置いてください。")
else:
    try:
        # WAVファイルを読み込む
        audio = AudioSegment.from_file(input_wav_file, format="wav")

        # 4秒より前の部分を抽出して保存 (pydubはミリ秒単位)
        end_ms = 4000
        before_audio = audio[:end_ms]
        before_audio.export(before_file, format="wav")

        # 4秒以降の部分を抽出して保存
        start_ms = 4000
        after_audio = audio[start_ms:]
        after_audio.export(after_file, format="wav")

        print(f"✅ 音声が4秒の前後でスライスされ、'{before_file}' と '{after_file}' として保存されました。")

    except Exception as e:
        print(f"エラー: 音声のスライス中に問題が発生しました: {e}")

print("--- 課題02: 音声スライス処理終了 ---\n")