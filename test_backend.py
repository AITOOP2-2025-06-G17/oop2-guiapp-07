# 作成したモジュールをインポート
import audio_processor

def main():
    # 設定
    input_filename = "test_record.wav"
    model = "mlx-community/whisper-base-mlx"

    print("=== テスト開始 ===")

    # 1. 録音テスト
    print("\n--- Step 1: 録音 ---")
    success = audio_processor.record_audio(input_filename, duration=5) # テスト用に5秒
    
    if not success:
        print("録音に失敗したため終了します。")
        return

    # 2. スライステスト
    print("\n--- Step 2: スライス ---")
    file_before, file_after = audio_processor.slice_audio(input_filename, split_ms=2000) # 2秒でカット

    if not file_before:
        print("スライスに失敗したため終了します。")
        return

    # 3. 文字起こしテスト
    print("\n--- Step 3: 文字起こし ---")
    
    # 全体の文字起こし
    text_full = audio_processor.transcribe_audio(input_filename, model)
    print(f"\n[全体]: {text_full}")

    # 前半の文字起こし
    text_before = audio_processor.transcribe_audio(file_before, model)
    print(f"\n[前半]: {text_before}")

    # 後半の文字起こし
    text_after = audio_processor.transcribe_audio(file_after, model)
    print(f"\n[後半]: {text_after}")

    print("\n=== テスト終了 ===")

if __name__ == "__main__":
    main()