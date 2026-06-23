import asyncio
import json
from openai import AsyncOpenAI

from dotenv import load_dotenv

async def parse_text_with_ai(raw_text: str) -> list:
    """
    Отправляем сырой текст со страниц выписки в нейросеть,
    получаем в ответ список с нужными данными
    """

    load_dotenv() # Загрузка окружения
    client = AsyncOpenAI() # Инициализация

    # Отправка запроса 
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system",
            "content": "Ты - робот-парсер. Нужно достать данные из текста"
            "и вернуть их строго в JSON формате. Ключи структуры должны быть:"
            "1. 'date_and_time': string (дата и время)"
            "2. 'date_accounting': string (дата учёта)"
            "3. 'description_operation': string (описание операции)"
            "4. 'sum_value': string (сумма)"
            "5. 'remainder': string (остаток)."},

            {"role": "user",
            "content": raw_text},
        ],
        response_format={"type": "json_object"},
    )
    
    # Получение ответа в формате JSON
    answer = response.choices[0].message.content

    # Преобразовываем в обычный словарь, проверяя, что данные вернулись успешно
    if answer is not None:
        answer_dict = json.loads(answer)
        result = [answer_dict]
    else:
        raise ValueError("API вернул пустой ответ")

    return result


