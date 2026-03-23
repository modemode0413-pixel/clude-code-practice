import json
import os

# config.jsonを読み込む
config_path = os.path.join(os.path.dirname(__file__), "config.json")

with open(config_path, "r", encoding="utf-8") as f:
    config = json.load(f)

print("=" * 40)
print("ユーザー設定")
print("=" * 40)
print(f"ユーザー名　：{config['ユーザー名']}")
print(f"目標　　　　：{config['目標']}")
print(f"現在のDay　：{config['現在のDay']}")
print(f"開始日　　　：{config['開始日']}")
print(f"完了したDay：{len(config['完了したDay'])}日分")
print(f"完了リスト　：Day {config['完了したDay'][0]} 〜 Day {config['完了したDay'][-1]}")
print("=" * 40)
