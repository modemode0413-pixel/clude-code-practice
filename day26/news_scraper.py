import sys
import requests
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

url = "https://news.ycombinator.com"

print("Hacker News トップ記事 TOP5")
print("=" * 40)

response = requests.get(url, verify=False)
soup = BeautifulSoup(response.text, "html.parser")

titles = soup.find_all("span", class_="titleline")

for i, title in enumerate(titles[:5], 1):
    link = title.find("a")
    if link:
        print(f"{i}. {link.get_text(strip=True)}")

print("=" * 40)
