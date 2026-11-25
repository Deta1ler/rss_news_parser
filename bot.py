from httpx import AsyncClient
import feedparser
import asyncio

#Тут подгружаем процедуры из наших модулей
from parse import parselink
from sql import create_table, save_to_db, select_for_db

async def main():
    rss_link = 'https://habr.com/ru/rss/articles/?fl=ru&limit=10'

    #создаем БД, если ее нет
    await create_table()

    #создаем экземпляр класса AsyncClient() и посылаем асинхронный get 
    httpx_client = AsyncClient()

    rss_text = await httpx_client.get(rss_link) #Загружаем RSS-ленту
    rss = feedparser.parse(rss_text.text)#Парсим RSS ленту


    for news in rss.entries[::-1]:   #rss.entries по сути это список словарей 
                                      #где каждый элемент представляет одну запись (новость, статью, эпизод подкаста) из RSS
         news_id = parselink(news['link'])

         if news_id is not None:
             #Если записи нет в базе данных:
            if await select_for_db(news_id, 'news_id') is None: 
                #Добавляем запись в базу данных:
                await save_to_db(news_id, news['title'], news['link'])

                print (f"Новость ID {news_id} добавлена в БД")

                # - спим 4 секунды, можно больше после каждой итерации с новой записью.
                await asyncio.sleep(4)

            else:
                #Если запись уже есть - пропускаем
                continue

if __name__ == '__main__':
    asyncio.run(main())