import schedule
import time
import os
from datetime import datetime

sys_encoding = 'utf-8'
LOG_PATH = os.path.join(os.path.dirname(__file__), "schedule_log.txt")

def record_time():
    now = datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
    message = f"[記録] {now}\n"
    print(message.strip())
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(message)

# 5秒ごとに実行
schedule.every(5).seconds.do(record_time)

print("スケジューラー起動中... (Ctrl+C で停止)")
print("5秒ごとに時刻を記録します\n")

# 30秒間実行して自動停止
start = time.time()
while time.time() - start < 30:
    schedule.run_pending()
    time.sleep(1)

print("\n30秒経過。スケジューラーを停止しました。")
print(f"ログファイル：{LOG_PATH}")
