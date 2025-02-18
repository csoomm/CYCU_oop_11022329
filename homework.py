import requests
from bs4 import BeautifulSoup

def fetch_tvbs_news():
    url = 'https://news.tvbs.com.tw/'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        headlines = soup.find_all('h2', class_='news_title')
        for headline in headlines:
            print(headline.text.strip())
    else:
        print('Failed to retrieve the news')

if __name__ == '__main__':
    fetch_tvbs_news()