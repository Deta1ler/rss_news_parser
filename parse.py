import requests
from bs4 import BeautifulSoup as bs
import re


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}


def parse(link):
    page = requests.get(link, headers=headers) #создаем умный обьект page через запрос по линку
    print("Статус ответа:", page.status_code)  # должно быть 200
    soup = bs(page.text, "html.parser")  #парсим нашу страницу(извлекаем полносттю данные)

    title_tag = soup.find('h1', class_='tm-title_h1')#находим первый попавшийся обьект  
                                                     #по тегу h1 и возвращает его
    title = title_tag.get_text(strip=True) if title_tag else "" #если title_tag не None вызови title_tag.get_text
                                                                #который заберет с обьекта h1 строку 

    article_body = soup.find('div', class_='article-formatted-body')#находим первый попавшийся обьект  
                                                     #по тегу div и и возвращает его


    body = "\n".join([
    p.get_text(strip=True) #что кладем в список (что то что превращаем в строку)
    for p in (article_body.find_all('p') if article_body else []) #article_body.find_all('p') возврщает список найденых тегов
                                                                  #
    if p.get_text(strip=True)
])
    return title + "\n" + body

def parselink(link):
    # Парсим ID статьи из ссылки вида https://habr.com/ru/articles/1112152/
    match = re.search(r'/articles/(\d+)/?', link)
    return match.group(1) if match else None



def main():
    text = parse('https://habr.com/ru/articles/1112152/')
    print(text)
if __name__ == '__main__':
    main()
