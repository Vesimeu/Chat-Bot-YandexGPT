from get_parameter import get_parameter
from functions import *
import time
print(get_parameter("У кого 6 июня день рождение?"))
str = get_parameter("У кого 6 июня день рождение?")
print(extract_parameter(str))

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
