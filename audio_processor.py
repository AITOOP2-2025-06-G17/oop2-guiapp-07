import ffmpeg
import os
import numpy as np
from pydub import AudioSegment
import mlx_whisper

# ==========================================
# 1. 録音機能
# ==========================================
def record_audio(output_file, duration=10, format='avfoundation', audio_device=':0'):
    """
    マイクから録音を行う関数
    :param output_file: 保存するファイル名 (例: 'output.wav')
    :param duration: 録音時間（秒）
    :param format: OSごとのオーディオドライバ (Macは'avfoundation')
    :param audio_device: デバイスID (Macは':0'など)
    :return: 成功ならTrue, 失敗ならFalse
    """
    print(f"🎙️ {duration}秒間の録音を開始します...")
    try:
        (
            ffmpeg
            .input(audio_device, format=format, t=duration)
            .output(output_file, acodec='pcm_s16le', ar='44100', ac=1)
            .run(overwrite_output=True, capture_stdout=True, capture_stderr=True)
        )
        print(f"✅ 録音完了: {output_file}")
        return True
    except ffmpeg.Error as e:
        print("❌ FFmpegエラー:", e.stderr.decode())
        return False
    except Exception as e:
        print(f"❌ 予期せぬエラー: {e}")
        return False

# ==========================================
# 2. 音声スライス機能
# ==========================================
def slice_audio(input_file, split_ms=4000):
    """
    音声を指定した時間で2つに分割する関数
    :param input_file: 元のWAVファイルパス
    :param split_ms: 分割する地点（ミリ秒） デフォルト4秒
    :return: (前半ファイル名, 後半ファイル名) のタプル。失敗時は(None, None)
    """
    if not os.path.exists(input_file):
        print(f"❌ ファイルが見つかりません: {input_file}")
        return None, None

    try:
        audio = AudioSegment.from_file(input_file, format="wav")
        
        # 前半・後半のファイル名を生成
        base, ext = os.path.splitext(input_file)
        before_file = f"{base}-before{ext}"
        after_file = f"{base}-after{ext}"

        # スライス処理
        before_audio = audio[:split_ms]
        after_audio = audio[split_ms:]

        # 保存
        before_audio.export(before_file, format="wav")
        after_audio.export(after_file, format="wav")
        
        print(f"✂️ スライス完了: {before_file}, {after_file}")
        return before_file, after_file

    except Exception as e:
        print(f"❌ スライスエラー: {e}")
        return None, None

# ==========================================
# 3. 文字起こし機能
# ==========================================
def preprocess_audio(sound):
    """Whisper用に音声を前処理する内部関数"""
    if sound.frame_rate != 16000:
        sound = sound.set_frame_rate(16000)
    if sound.sample_width != 2:
        sound = sound.set_sample_width(2)
    if sound.channels != 1:
        sound = sound.set_channels(1)
    return sound

def transcribe_audio(file_path, model_name="mlx-community/whisper-base-mlx"):
    """
    指定されたファイルを文字起こしする関数
    :param file_path: 文字起こしするファイルのパス
    :param model_name: 使用するWhisperモデル名
    :return: 文字起こしされたテキスト（文字列）。失敗時はエラーメッセージ。
    """
    if not os.path.exists(file_path):
        return "エラー: ファイルが見つかりません"

    print(f"📝 文字起こし中: {file_path}")
    try:
        # 音声読み込み
        audio_data = AudioSegment.from_file(file_path, format="wav")
        
        # 前処理
        sound = preprocess_audio(audio_data)
        
        # Numpy配列変換 (Metal/MLX用)
        arr = np.array(sound.get_array_of_samples()).astype(np.float32) / 32768.0
        
        # 推論実行
        result = mlx_whisper.transcribe(arr, path_or_hf_repo=model_name)
        
        text = result.get('text', '').strip()
        print(f"✅ 完了: {text[:30]}...") # 冒頭だけログ出力
        return text

    except Exception as e:
        print(f"❌ 文字起こしエラー: {e}")
        return f"エラーが発生しました: {e}"