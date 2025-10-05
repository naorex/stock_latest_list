import requests
from bs4 import BeautifulSoup

# リンクからデータを取得する関数
def get_data(url):

    # User-Agent設定（2023/08/16）
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    header = {
        'User-Agent': user_agent
    }

    r = requests.get(url, headers=header)  # User-Agentsを設定
    soup = BeautifulSoup(r.content, "html.parser")

    return soup

if __name__ == '__main__':
    url = input('URLを入力: ')
    soup = get_data(url)
    print(soup)
