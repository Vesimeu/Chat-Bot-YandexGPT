import requests
import numpy as np

def get_embedding(text: str, folder_id: str, iam_token: str, text_type: str = "doc") -> np.array:
    doc_uri = f"emb://{folder_id}/text-search-doc/latest"
    query_uri = f"emb://{folder_id}/text-search-query/latest"
    embed_url = "https://llm.api.cloud.yandex.net:443/foundationModels/v1/textEmbedding"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {iam_token}", "x-folder-id": f"{folder_id}"}

    query_data = {
        "modelUri": doc_uri if text_type == "doc" else query_uri,
        "text": text,
    }

    response = requests.post(embed_url, json=query_data, headers=headers)
    if response.status_code == 200:
        try:
            return np.array(response.json()["embedding"])
        except KeyError:
            print("Ошибка: Не удалось получить эмбеддинг из ответа.")
            return None
    else:
        print("Ошибка при выполнении запроса к API.")
        return None
