import re
import tweepy
import MeCab

COUNT = 200
KEYWORD = 'ゲーム'
CLASS_LABEL = "__label__ゲーム"

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
    tweets = get_tweet()      #ツイートを取得
    separate = to_separate(tweets)     #ツイートを分かち書き
    write_txt(separate)        #ツイートをファイルに書き込み

# TwitterからKEYWORDに関連するツイートを取得
def get_tweet():
    api = authTwitter() # 認証
    tweets = api.search_tweets(q=KEYWORD,count=COUNT)
    return tweets

# 正規表現を使ってツイートから不要な情報を削除
def format_text(text):
    text=re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+', "", text)  # 外部リンクURL
    text=re.sub(r'@[\w/:%#\$&\?\(\)~\.=\+\-…]+', "", text)  #リプライ先のユーザーID
    text=re.sub(r'＼', "", text)  
    text=re.sub('／', "", text)
    text=re.sub('RT', "", text)
    text=re.sub('\n', "", text) # 改行文字
    return text

# 文書を分かち書きし単語単位に分割
def to_separate(tweets):
    results = []
    tagger = MeCab.Tagger('-Owakati')

    for tweet in tweets:
        content = format_text(tweet.text)
        wakati = tagger.parse(content)
        results.append(' , '.join([CLASS_LABEL, wakati])) # ツイートごとにラベルを付与
    return results

# 学習モデル用のテキストファイルを作成    
def write_txt(results):
    with open(CLASS_LABEL + '.txt', 'a') as f:
        for result in results:
            f.write(result)
        print(str(len(results))+"行を書き込み")

if __name__ == '__main__':
    main()
