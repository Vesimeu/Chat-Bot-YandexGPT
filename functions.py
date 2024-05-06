from text_vectorizer import get_embedding
from data import doc_texts
from scipy.spatial.distance import cosine, cdist
from token_loader import read_tokens_from_file
from get_parameter import get_parameter
from gpt_request import get_gpt_response
import numpy as np

tokens = read_tokens_from_file("token.txt")
telegram_token = tokens["token_bot"]
folder_id = tokens["FOLDER_ID"]
api_key = tokens["SecretKey"]
iam_token = tokens["IAM_token"]


#Функция которая находит наиболее похожие тексты
def find_most_similar_text(query_text):
    query_embedding = get_embedding(query_text, folder_id, iam_token, text_type="query")
    min_distance = float('inf')
    most_similar_text = None

    if query_embedding is not None:
        for text in doc_texts:
            text_embedding = get_embedding(text, folder_id, iam_token)
            if text_embedding is not None:
                distance = cosine(query_embedding, text_embedding)
                if distance < min_distance:
                    min_distance = distance
                    most_similar_text = text
    else:
        print("Ошибка при получении вектора запроса.")

    return most_similar_text

#Функция которая возращает в числовом значении косинусное расстояние между векторами query_embedding и каждым элементом docs_embedding
def find_cosine_similarity(query_text, doc_texts):
    query_embedding = get_embedding(query_text, folder_id, iam_token, text_type="query")
    docs_embedding = np.array([get_embedding(doc_text, folder_id, iam_token) for doc_text in doc_texts])
    dist = cdist(query_embedding[None, :], docs_embedding, metric="cosine")[0]
    return dist

# Загрузка данных о днях рождения из файла
def load_birthdays(file_path):
    birthdays = {}
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            date, names = line.strip().split(":")
            birthdays[date.strip()] = [name.strip() for name in names.split(",")]
    return birthdays


birthdays_data = load_birthdays("data.txt")

names_and_dates = {}
for date, names in birthdays_data.items():
    for name in names:
        if date in names_and_dates:
            names_and_dates[date].append(name)
        else:
            names_and_dates[date] = [name]

# Извлекает параметр из строки.
def extract_parameter(input_string):
    lines = input_string.split('\n')  # Разделение строки на строки по символу новой строки
    for line in lines:
        key, value = line.split(':')  # Разделение строки на ключ и значение по символу ":"
        if value.strip() != '0':  # Проверка, что значение не равно "0"
            return value.strip()  # Возвращаем значение без пробелов по краям
    return 0  # Возвращаем 0, если ни один параметр не был передан

# Эта функция ищет нужные нам вещи.
def find_info(birthdays_data, target_data):
    if '.' in target_data:  # Проверка наличия точки в строке (если есть, это дата)
        if target_data in birthdays_data:  # Проверка наличия даты в словаре
            names = birthdays_data[target_data]  # Получение имен по дате
            return names if names else f"В день {target_data} нет дней рождения"
        else:
            return f"День {target_data} не найден в базе данных"
    else:  # Если точки нет, то это имя
        for date, names in birthdays_data.items():
            if target_data in names:  # Проверка наличия имени в списке имен для каждой даты
                return date
        return f"Имя {target_data} не найдено в базе данных"

# Функция которая выводит готовое сообщение в зависимости от того что пришло на вход.
def process_input(birthdays_data, target_data):
    if '.' in target_data:  # Проверка наличия точки в строке (если есть, это дата)
        if target_data in birthdays_data:  # Проверка наличия даты в словаре
            names = birthdays_data[target_data]  # Получение имен по дате
            if names:
                return f"{target_data} День рождение у {', '.join(names)}"
            else:
                return f"В день {target_data} нет дней рождения"
        else:
            return f"День {target_data} не найден в базе данных"
    else:  # Если точки нет, то это имя
        date = find_info(birthdays_data, target_data)  # Получение даты рождения для имени
        if date:
            return f"{date} день рождения у {target_data}"
        else:
            return f"Имя {target_data} не найдено в базе данных"

# print(process_input(birthdays_data, "06.06"))

def output_answer(query_text):
    print("Вопрос: " + query_text)

    parametr = extract_parameter(get_parameter(query_text))  # Получаем параметры из запроса
    # print(parametr)
    if parametr != 0:
        return (process_input(birthdays_data, parametr)) #Вот тут надо что-то придумать, потому что может ошибочно вывезти блок else из process_input
    else:
        gpt_response = get_gpt_response(query_text)
        print("Ответ от YandexGPT:")
        return gpt_response