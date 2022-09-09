import re
import tweepy
import fasttext as ft
import MeCab
from time import sleep

COUNT = 50    # ツイート取得数
SET = 1    # セット数×100件のツイートを取得

# 認証に必要なキーとトークン
API_KEY = 'IR2CAa7c3w5OqzilT5iCPIAbg'
API_SECRET = 'swUFZpyRUnzfYWOnRkfAbSRa2xZycAUTot5ype3j6czTU17dHY'
ACCESS_TOKEN = '911457413865152512-kzcZi6uMkK8LHHxbCSXz5D23hPiNKv3'
ACCESS_TOKEN_SECRET = '7CuJBoA7FtHdngpAzUQpaTLTEkPRhf4Td73WWRwzXtCwb'

# TwitterAPI認証用関数
def authTwitter():
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)  #APIインスタンスの作成
    return api

def main():
    tweets = get_tweet(id)      #ツイートを取得
    results = separate_tweet(tweets)     #ツイートを分かち書き
    categorize(results)        #ツイートを分類

# TwitterIDを取得
def get_id():
    id = input('Twitter IDを入力してください:')
    return id

# 指定したユーザーのツイートを取得
def get_tweet(id):
    api = authTwitter() # 認証
    tweets = [
        tweet
        for tweet in tweepy.Cursor(api.user_timeline, screen_name=id).items(COUNT)
        if list(tweet.text)[0] != '@'  # リプライを除外
        ]
    return tweets

# 正規表現を使ってツイートから不要な情報を削除
def format_text(text):
        text=re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+', "", text)  # 外部リンクURL
        text=re.sub(r'@[\w/:%#\$&\?\(\)~\.=\+\-…]+', "", text) # リツイート元のユーザーID
        text=re.sub(r'＼', "", text)
        text=re.sub('／', "", text)
        text=re.sub('RT', "", text)
        text=re.sub('\n', "", text)    # 改行文字
        return text

# 文書を分かち書きし単語単位に分割
def separate_tweet(tweets):
    results = []
    tagger = MeCab.Tagger('-Owakati')

    i = 1
    for tweet in tweets:
        content = format_text(tweet.text)
        wakati = tagger.parse(content)
        results.append(wakati)
    return results
    """
    print('------------------------')
    print(str(i) + '件目のツイート')
    print(result)
    i += 1
    """

# ツイートを学習モデルに分類させる関数
def categorize(results):
    for result in results:
        model = ft.train_supervised(input='train.txt')
        ret = model.predict(result)
        print(ret)

if __name__ == '__main__':
    id = get_id()
    main()

    """
    for i in range(SET):
        main()
    """
    