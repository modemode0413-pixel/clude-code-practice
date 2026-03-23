import json
import os

config_path = os.path.join(os.path.dirname(__file__), "config.json")

# 読み込む
with open(config_path, "r", encoding="utf-8") as f:
    config = json.load(f)

print("【更新前】")
print(f"現在のDay　：{config['現在のDay']}")
print(f"完了したDay：{len(config['完了したDay'])}日分")

# 更新する
config["現在のDay"] = 30
if 29 not in config["完了したDay"]:
    config["完了したDay"].append(29)

# 保存する
with open(config_path, "w", encoding="utf-8") as f:
    json.dump(config, f, ensure_ascii=False, indent=2)

print("\n【更新後】")
print(f"現在のDay　：{config['現在のDay']}")
print(f"完了したDay：{len(config['完了したDay'])}日分")
print("\nconfig.jsonを更新しました！")
