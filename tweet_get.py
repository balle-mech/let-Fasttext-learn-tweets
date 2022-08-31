import tweepy

# 認証に必要なキーとトークン
API_KEY = 'IR2CAa7c3w5OqzilT5iCPIAbg'
API_SECRET = 'swUFZpyRUnzfYWOnRkfAbSRa2xZycAUTot5ype3j6czTU17dHY'
ACCESS_TOKEN = '911457413865152512-kzcZi6uMkK8LHHxbCSXz5D23hPiNKv3'
ACCESS_TOKEN_SECRET = '7CuJBoA7FtHdngpAzUQpaTLTEkPRhf4Td73WWRwzXtCwb'

# APIの認証
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

#APIインスタンスの作成
api=tweepy.API(auth)

#アカウント指定
id = '@Suzu_Mg'
tweets = tweepy.Cursor(api.user_timeline, screen_name=id).items(20)

i = 0

for tweet in tweets:
    if (list(tweet.text)[:2]!=['R', 'T']) & (list(tweet.text)[0]!='@'):
        i += 1
        print('-------------------------')
        print(i)
        print(tweet.text)
