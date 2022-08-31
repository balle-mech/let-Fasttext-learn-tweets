import tweepy
import MeCab

# 認証に必要なキーとトークン
API_KEY = 'IR2CAa7c3w5OqzilT5iCPIAbg'
API_SECRET = 'swUFZpyRUnzfYWOnRkfAbSRa2xZycAUTot5ype3j6czTU17dHY'
ACCESS_TOKEN = '911457413865152512-kzcZi6uMkK8LHHxbCSXz5D23hPiNKv3'
ACCESS_TOKEN_SECRET = '7CuJBoA7FtHdngpAzUQpaTLTEkPRhf4Td73WWRwzXtCwb'

# APIの認証
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api=tweepy.API(auth)  #APIインスタンスの作成

COUNT = 10
KEYWORD = 'ゲーム'
CLASS_LABEL = "__label__1"

def main():
    get_tweet()      #ツイートを取得
    #surfaces = get_surfaces(tweets)     #ツイートを分かち書き
    #write_txt(surfaces)        #ツイートを書き込み

# TwitterからKEYWORDに関連するツイートを取得
def get_tweet():
    tweets = api.search_tweets(q=KEYWORD,count=COUNT)
    for tweet in tweets:
        print('-------------')
        print(tweet.text)

if __name__ == '__main__':
    main()

