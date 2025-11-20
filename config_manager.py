import json
import os

# 設定ファイルの保存場所
CONFIG_FILE = "app_config.json"

# デフォルト（初期）設定
DEFAULT_CONFIG = {
    "model_name": "mlx-community/whisper-base-mlx",
    "record_duration": 10,      # 秒
    "slice_time_ms": 4000,      # ミリ秒
    "output_filename": "output.wav"
}

def load_config():
    """
    設定ファイルを読み込む。
    ファイルがない場合はデフォルト設定を返し、ファイルを作成する。
    """
    if not os.path.exists(CONFIG_FILE):
        print("ℹ️ 設定ファイルが見つからないため、デフォルト設定を作成します。")
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG

    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)
            # デフォルト設定にないキーがあれば補完する（バージョンの違い対策）
            for key, value in DEFAULT_CONFIG.items():
                if key not in config:
                    config[key] = value
            return config
    except Exception as e:
        print(f"⚠️ 設定読み込みエラー: {e}。デフォルト設定を使用します。")
        return DEFAULT_CONFIG

def save_config(config_data):
    """
    設定をファイルに保存する。
    """
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=4, ensure_ascii=False)
        print(f"💾 設定を保存しました: {CONFIG_FILE}")
        return True
    except Exception as e:
        print(f"❌ 設定保存エラー: {e}")
        return False