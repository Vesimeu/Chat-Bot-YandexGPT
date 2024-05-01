# import requests
# import numpy as np
# from scipy.spatial.distance import cdist
#
# FOLDER_ID = "b1gcfcn8598cvatrhm8j"
# IAM_TOKEN = "t1.9euelZqelJOWj86KyseTiZvOl46Vme3rnpWak8jKkJWVyYqUmp2SnJOUkczl8_dYQjVO-e8DdA9a_d3z9xhxMk757wN0D1r9zef1656VmpHOlp2NiZCZlZCKlpmPjYuc7_zF656VmpHOlp2NiZCZlZCKlpmPjYuc.zCrtZHjEr123kXcLnudLQ2V0iReQJdC-OqV_Ry9ax3t1yU3azYNUAzm-MLnnVljSsMMsGE6TUA8t0saqKxC_AA"
#
# doc_uri = f"emb://{FOLDER_ID}/text-search-doc/latest"
# query_uri = f"emb://{FOLDER_ID}/text-search-query/latest"
#
# embed_url = "https://llm.api.cloud.yandex.net:443/foundationModels/v1/textEmbedding"
# headers = {"Content-Type": "application/json", "Authorization": f"Bearer {IAM_TOKEN}", "x-folder-id": f"{FOLDER_ID}"}
#
# doc_texts = [
#   """2+2 = 5""",
#   """Python - это низкоуровневый язык программирования для разработки чат-ботов для геликона """
# ]
#
# query_text = "И для чего испольщуется Python?"
#
# def get_embedding(text: str, text_type: str = "doc") -> np.array:
#     query_data = {
#         "modelUri": doc_uri if text_type == "doc" else query_uri,
#         "text": text,
#     }
#
#     return np.array(
#         requests.post(embed_url, json=query_data, headers=headers).json()["embedding"]
#     )
#
#
# query_embedding = get_embedding(query_text, text_type="query")
# docs_embedding = [get_embedding(doc_text) for doc_text in doc_texts]
#
# # Вычисляем косинусное расстояние
# dist = cdist(query_embedding[None, :], docs_embedding, metric="cosine")
#
# # Вычисляем косинусное сходство
# sim = 1 - dist
#
# # most similar doc text
# print(doc_texts[np.argmax(sim)])
