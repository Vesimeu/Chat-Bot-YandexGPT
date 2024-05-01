import numpy as np

from text_vectorizer import get_embedding
from scipy.spatial.distance import cdist
from gpt_request import get_gpt_response

# Загрузка IAM токена из файла token.txt
with open("token.txt", "r") as token_file:
    token_data = token_file.readlines()
    folder_id = token_data[2].strip()
    iam_token = token_data[3].strip()

# Загрузка doc_texts
doc_texts = [
    """Александр Сергеевич Пушкин (26 мая [6 июня] 1799, Москва — 29 января [10 февраля] 1837, Санкт-Петербург) — русский поэт, драматург и прозаик, заложивший основы русского реалистического направления, литературный критик и теоретик литературы, историк, публицист, журналист.""",
    """Ромашка — род однолетних цветковых растений семейства астровые, или сложноцветные, по современной классификации объединяет около 70 видов невысоких пахучих трав, цветущих с первого года жизни."""
]


def find_in_doc_texts(query_text):
    for idx, text in enumerate(doc_texts):
        if query_text in text:
            return text
    return None

query_text = "когда день рождения Пушкина?"

# Проверяем, есть ли запрос в базе doc_texts
found_in_doc_texts = find_in_doc_texts(query_text)
print(found_in_doc_texts)
if query_text in doc_texts:
    query_embedding = get_embedding(query_text, folder_id, iam_token, text_type="doc")
    docs_embedding = [get_embedding(doc_text, folder_id, iam_token) for doc_text in doc_texts]

    if query_embedding is not None:
        # Вычисляем косинусное расстояние
        dist = cdist(query_embedding[None, :], docs_embedding, metric="cosine")

        # Вычисляем косинусное сходство
        sim = 1 - dist

        # Находим наиболее близкий документ
        most_similar_doc = doc_texts[np.argmax(sim)]
        print("Наиболее близкий документ:")
        print(most_similar_doc)
    else:
        print("Ошибка при векторизации текста.")
else:
    # Если запрос не найден, обращаемся к YandexGPT
    gpt_response = get_gpt_response(query_text)
    print("Ответ от YandexGPT:")
    print(gpt_response)
