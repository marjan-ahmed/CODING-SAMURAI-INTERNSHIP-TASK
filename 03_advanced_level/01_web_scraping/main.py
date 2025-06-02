import requests as re
from bs4 import BeautifulSoup

bbc_news_url = "https://www.bbc.com/news/topics/crem2zr2vmqt"

def main(url):
    response = re.get(url)
    content = BeautifulSoup(response.content, "html.parser")
    titles = content.find_all("h2")

    with open('data.csv', 'w') as f:
        count = 1
        for title in titles:
            line = f"{count}, {title.text}\n"
            f.write(line)
            count += 1


if __name__ == '__main__':
    main(bbc_news_url)