import re
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

# ファイル読み込み
file_path = os.path.join(os.path.dirname(__file__), "sample.txt")
with open(file_path, encoding="utf-8") as f:
    text = f.read()

# 電話番号パターン（例：090-1234-5678）
phones = re.findall(r'0\d{2}-\d{4}-\d{4}', text)
print("【電話番号】")
for p in phones:
    print(f"  {p}")

# メールアドレスパターン
emails = re.findall(r'[\w.+-]+@[\w-]+\.[\w.]+', text)
print("\n【メールアドレス】")
for e in emails:
    print(f"  {e}")

# 日付パターン（例：2026/03/23）
dates = re.findall(r'\d{4}/\d{2}/\d{2}', text)
print("\n【日付】")
for d in dates:
    print(f"  {d}")
