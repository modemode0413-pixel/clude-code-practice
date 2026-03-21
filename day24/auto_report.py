import subprocess
import glob
import csv
import os
from datetime import datetime

base = r"C:\Users\0413b\OneDrive\デスクトップ\clude-code_practice"

# 1. Gitコミット数を取得
result = subprocess.run(
    ["git", "rev-list", "--count", "HEAD"],
    capture_output=True, text=True, cwd=base
)
commit_count = result.stdout.strip()

# 2. txtファイルの数を取得
txt_files = glob.glob(os.path.join(base, "**", "*.txt"), recursive=True)
txt_count = len(txt_files)

# 3. scores.csvの平均スコアを計算
scores = []
csv_path = os.path.join(base, "day23", "scores.csv")
with open(csv_path, encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            scores.append(int(row["スコア"]))
        except:
            pass

avg = sum(scores) / len(scores) if scores else 0
high = max(scores) if scores else 0
low = min(scores) if scores else 0

# 4. レポートを作成
today = datetime.now().strftime("%Y年%m月%d日")
report = f"""=============================
Claude Code 学習 総合レポート
生成日：{today}
=============================

【Gitコミット数】
{commit_count} コミット

【.txtファイル数】
{txt_count} ファイル

【学習スコア分析（scores.csv）】
平均スコア：{avg:.1f} 点
最高スコア：{high} 点
最低スコア：{low} 点

=============================
"""

# 5. ファイルに保存
report_path = os.path.join(base, "day24", "report.txt")
with open(report_path, "w", encoding="utf-8") as f:
    f.write(report)

print(report)
print("→ day24/report.txt に保存しました！")
