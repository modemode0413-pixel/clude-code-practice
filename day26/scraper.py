import sys
import requests
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

url = "https://example.com"

print(f"取得URL：{url}")
print("-" * 40)

response = requests.get(url, verify=False)
soup = BeautifulSoup(response.text, "html.parser")

# タイトルを取得
title = soup.title.text if soup.title else "タイトルなし"
print(f"ページタイトル：{title}")

# メインテキストを取得
print("\nメインテキスト：")
for tag in soup.find_all(["h1", "h2", "p"]):
    text = tag.get_text(strip=True)
    if text:
        print(f"  {text}")
