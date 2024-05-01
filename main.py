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


query_text = "ромашки"
most_similar_text = find_most_similar_text(query_text)

# Вычисляем косинусное расстояние между векторами query_embedding и каждым элементом docs_embedding
query_embedding = get_embedding(query_text, folder_id, iam_token, text_type="query")
docs_embedding = np.array([get_embedding(doc_text, folder_id, iam_token) for doc_text in doc_texts])
dist = cdist(query_embedding[None, :], docs_embedding, metric="cosine")[0]
print(dist)
if np.any(dist < 0.6):
    print("Текст найден в базе данных.")
    print(most_similar_text)
else:
    # Если семантическая близость меньше порога, обращаемся к YandexGPT
    gpt_response = get_gpt_response(query_text)
    print("Ответ от YandexGPT:")
    print(gpt_response)

