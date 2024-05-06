import numpy as np
from functions import *
from text_vectorizer import get_embedding
from data import *
from get_parameter import get_parameter
from gpt_request import get_gpt_response
from token_loader import read_tokens_from_file

tokens = read_tokens_from_file("token.txt")
folder_id = tokens["FOLDER_ID"]
api_key = tokens["SecretKey"]
iam_token = tokens["IAM_token"]



query_text = "А когда у Пети день рождение?"
print("Вопрос: " + query_text)

parametr = extract_parameter(get_parameter(query_text)) # Получаем параметры из запроса
# print(parametr)
if parametr != 0:
    print(process_input(birthdays_data, parametr))
else:
    gpt_response = get_gpt_response(query_text)
    print("Ответ от YandexGPT:")
    print(gpt_response)

# # Вычисляем косинусное расстояние между векторами query_embedding и каждым элементом docs_embedding
# dist = find_cosine_similarity(query_text, doc_texts)
# print(dist)
# if np.any(dist < 0.6):
#     print("Текст найден в базе данных.")
#     most_similar_text = find_most_similar_text(query_text)
#     print(most_similar_text)
# else:
#     # Если семантическая близость меньше порога, обращаемся к YandexGPT
#     gpt_response = get_gpt_response(query_text)
#     print("Ответ от YandexGPT:")
#     print(gpt_response)