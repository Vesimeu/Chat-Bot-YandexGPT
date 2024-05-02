import numpy as np
from scipy.spatial.distance import cosine, cdist
from text_vectorizer import get_embedding
from gpt_request import get_gpt_response
from token_loader import read_tokens_from_file

tokens = read_tokens_from_file("token.txt")
folder_id = tokens["FOLDER_ID"]
api_key = tokens["SecretKey"]
iam_token = tokens["IAM_token"]

# Загрузка doc_texts
doc_texts = [
    """Александр Сергеевич Пушкин (26 мая [6 июня] 1799, Москва — 29 января [10 февраля] 1837, Санкт-Петербург) — русский поэт, драматург и прозаик, заложивший основы русского реалистического направления, литературный критик и теоретик литературы, историк, публицист, журналист.""",
    """Ромашка — род однолетних цветковых растений семейства астровые, или сложноцветные, по современной классификации объединяет около 70 видов невысоких пахучих трав, цветущих с первого года жизни."""
]

# Загрузка данных о днях рождения из файла
def load_birthdays(file_path):
    birthdays = {}
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            date, names = line.strip().split(":")
            birthdays[date.strip()] = [name.strip() for name in names.split(",")]
    return birthdays

birthdays_data = load_birthdays("data.txt")
# print(birthdays_data)

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

query_text = "Когда именины у Петра Полякова?"
print(query_text)
most_similar_text = find_most_similar_text(query_text)

# Вычисляем косинусное расстояние между векторами query_embedding и каждым элементом docs_embedding
query_embedding = get_embedding(query_text, folder_id, iam_token, text_type="query")
docs_embedding = np.array([get_embedding(doc_text, folder_id, iam_token) for doc_text in doc_texts])

# # Словарь, в котором ключи - имена, значения - векторы дат рождения
# names_and_dates = {name: birthdays_data[date] for date, names in birthdays_data.items() for name in names}
# print(names_and_dates)
names_and_dates = {}
for date, names in birthdays_data.items():
    for name in names:
        if date in names_and_dates:
            names_and_dates[date].append(name)
        else:
            names_and_dates[date] = [name]

# Проверяем ближайшую дату рождения
min_distance = float('inf')
closest_date = None
closest_name = None
for date, names in names_and_dates.items():
    for name in names:
        name_embedding = get_embedding(name, folder_id, iam_token)
        date_embedding = get_embedding(date, folder_id, iam_token)
        if name_embedding is not None and date_embedding is not None:
            distance_name = cosine(query_embedding, name_embedding)
            distance_date = cosine(query_embedding, date_embedding)
            if distance_name < min_distance:
                min_distance = distance_name
                closest_name = name
                closest_date = date

if closest_date is not None and closest_name is not None:
    print(f"Самая близкая дата из базы: {closest_date}")

    if query_text.startswith("Когда именины у "):
        print(f"Именины у {query_text.split()[-1]} - {closest_date}")
    elif query_text.startswith("У кого именины "):
        print(f"Именины {closest_date} у {', '.join(names_and_dates[closest_date])}")
    else:
        gpt_response = get_gpt_response(query_text)
        print("Ответ от YandexGPT:")
        print(gpt_response)
else:
    # Если не удалось найти подходящую дату рождения в базе данных, обращаемся к YandexGPT
    gpt_response = get_gpt_response(query_text)
    print("Ответ от YandexGPT:")
    print(gpt_response)