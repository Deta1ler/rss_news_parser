import aiosqlite

#Создаем БД, если ее нет в каталоге
async def create_table(): #Создай асинхронную функцию — корутину, а не обычный вызов
    #«внутри этой функции возможны точки паузы и ожидания, и запускать её нужно в асинхронном режиме»

    async with aiosqlite.connect('storage.db') as db:  #Вход в блок (async with ...): открыть ресурс (подключиться к storage.db)   
                                                    #может занять время — это асинхронная операция. Интерпретатор дожидается её 
                                                    # завершения (как бы делает await на этапе входа) и кладёт готовое подключение в 
                                                    # переменную после as (здесь это db).

        await db.execute('CREATE TABLE IF NOT EXISTS habr '  #«Подожди, пока команда запишется в базу, дав другим задачам поработать».
                         '(id integer, news_id text, title text, link text, status text, date text, PRIMARY KEY(id AUTOINCREMENT))')
        await db.commit()

#Создаем запись с новостью, заголовком и ссылкой
async def save_to_db(news_id, title, link):
    async with aiosqlite.connect('storage.db') as db:
        await db.execute('INSERT INTO habr (news_id, title, link) VALUES (?, ?, ?)',
                         (news_id, title, link))
        await db.commit()

#Обновляем запись в БД по ИД
async def update_db(news_id, status, date):
    async with aiosqlite.connect('storage.db') as db:
        await db.execute('UPDATE habr SET status = ?, date = ? WHERE news_id = ?',
                         (status, date, news_id))
        await db.commit()

#Запрашиваем данные
async def select_for_db(news_id, column):
    async with aiosqlite.connect('storage.db') as db:
        cursor = await db.cursor()
        await cursor.execute(f'SELECT {column} FROM habr WHERE news_id = ?',(news_id,))
        return await cursor.fetchone()