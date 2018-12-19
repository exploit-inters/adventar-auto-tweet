import urllib.request
import feedparser
import config

def tweet(entry, category='記事') -> None:
    calendar_title = entry['title']
    url = entry['link']
    text = '{}の{}です！ {}'.format(calendar_title, category, url)
    print(text)

def parse_and_tweet(url):
    rss = feedparser.parse(url)
    for entry in rss['entries']:
        tweet(entry)

def main():
    for url in config.FEED_URLS:
        parse_and_tweet(url)

if __name__ == '__main__':
    main()
