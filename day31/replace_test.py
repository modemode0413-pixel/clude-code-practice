import re
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

# ファイル読み込み
file_path = os.path.join(os.path.dirname(__file__), "sample.txt")
with open(file_path, encoding="utf-8") as f:
    text = f.read()

print("【マスキング前】")
print(text)

# 電話番号をマスキング
masked = re.sub(r'0\d{2}-\d{4}-\d{4}', '***-****-****', text)

print("【マスキング後】")
print(masked)
