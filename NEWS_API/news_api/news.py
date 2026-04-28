import requests
import json
import os
from dotenv import load_dotenv
import argparse





parser = argparse.ArgumentParser(description="サンプル")

parser.add_argument('--q', type=str, default="(Google OR Amazon) AND Cloud", help='ニュースのキーワード')
parser.add_argument('--from_', type=str, default="2026-04-01T00:00:00", help="入力した時刻以降のニュースから抜粋")
parser.add_argument('--to', type=str, default="2026-04-28T00:00:00", help='入力した時刻以前のニュースから抜粋')
parser.add_argument('--pageSize', type=int, default=5, help='取得したいニュースの件数')

args = parser.parse_args()



load_dotenv()

API_KEY = os.getenv("News_API_key")

SLACK_WEBHOOK_URL = os.getenv("Slack_Webhook_URL")

BASE_URL = "https://newsapi.org/v2/everything"






# パラメータ設定
params = {
    "q": args.q,
    "from": args.from_,
    "to": args.to,
    "pageSize": args.pageSize,
    "apiKey": API_KEY
}



# APIリクエスト
response = requests.get(BASE_URL, params=params)

# レスポンスを出力
if response.status_code == 200:
    articles = response.json().get("articles", [])
    all_news = ""
    for i, article in enumerate(articles):
        news = (f"{i + 1}. {article['title']} - {article['source']['name']}\n{article['url']}\n\n")
        all_news += news
        print(news)
else:
    print(f"Error: {response.status_code} - {response.text}")

slack_payload = {
    "text": all_news
}

if SLACK_WEBHOOK_URL is None:
    raise ValueError("エラー：.envファイルに SLACK_WEBHOOK_URL が設定されていません。")

slack_response = requests.post(SLACK_WEBHOOK_URL, json=slack_payload)