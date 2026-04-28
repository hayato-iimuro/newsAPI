import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("News_API_key")  # 取得したAPIキーを設定

SLACK_WEBHOOK_URL = os.getenv("Slack_Webhook_URL")

BASE_URL = "https://newsapi.org/v2/everything"  # NewsAPIのエンドポイント

# パラメータ設定
params = {
    "q": "(Google OR Amazon OR Anthropic) AND Cloud", # キーワード
    "from": "2026-04-01T00:00:00",
    "to": "2026-04-28T00:00:00",
    "pageSize": 5,                       # 取得件数
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
    # URLが取れなかったら、エラーメッセージを出してプログラムを終了させる
    raise ValueError("エラー：.envファイルに SLACK_WEBHOOK_URL が設定されていません。")

slack_response = requests.post(SLACK_WEBHOOK_URL, json=slack_payload)