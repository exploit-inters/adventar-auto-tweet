import os
import time
from datetime import datetime
import sqlite3
import feedparser
import config

def id_of_guid(guid: str) -> int:
    # guidがURLの形式になっているので末尾のみを取り出す
    return int(os.path.basename(guid))

def datetime_of_struct_time(struct_time: time.struct_time) -> datetime:
    return datetime.fromtimestamp(time.mktime(struct_time))

def get_category(entry) -> str:
    '''
    お絵描き が含まれてたらイラスト
    そうでない場合は記事
    '''
    if 'お絵描き' in entry['title']:
        return 'イラスト'
    else:
        return '記事'

def register_db(conn, entry):
    published_parsed = datetime_of_struct_time(entry['published_parsed'])
    now = datetime.now()
    id = id_of_guid(entry['guid'])
    with conn as cursor:
        cursor.execute('insert into entry values (?, ?, ?)',
                       [id, published_parsed, now])

def tweet(entry):
    calendar_title = entry['title']
    url = entry['link']
    category = get_category(entry)
    text = '{}の{}です！ {}'.format(calendar_title, category, url)
    print(text)

def parse_and_tweet(url: str):
    rss = feedparser.parse(url)

    # 前の日程から順になめる
    for entry in reversed(rss['entries']):
        conn = sqlite3.connect(config.DB_FILE)
        try:
            register_db(conn, entry)
            tweet(entry)
        except sqlite3.IntegrityError as e:
            print('already tweeted:', entry['title'])
        finally:
            conn.close()

def main():
    for url in config.FEED_URLS:
        parse_and_tweet(url)

if __name__ == '__main__':
    main()
