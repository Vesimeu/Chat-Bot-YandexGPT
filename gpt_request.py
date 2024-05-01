import requests
from token_loader import read_tokens_from_file

def send_gpt_request(prompt_data: dict, url: str, api_key: str, folder_id: str) -> dict:
    headers = {"Content-Type": "application/json", "Authorization": f"Api-Key {api_key}", "x-folder-id": folder_id}

    response = requests.post(url, json=prompt_data, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None


def get_gpt_response(query_text: str) -> str:
    tokens = read_tokens_from_file("token.txt")
    folder_id = tokens["FOLDER_ID"]
    api_key = tokens["SecretKey"]
    print(api_key , " ", folder_id)

    model_uri = f"gpt://{folder_id}/yandexgpt-lite"
    completion_options = {
        "stream": False,
        "temperature": 0.6,
        "maxTokens": "2000"
    }

    prompt_data = {
        "modelUri": model_uri,
        "completionOptions": completion_options,
        "messages": [
            {
                "role": "system",
                "text": "Представь что ты программист"
            },
            {
                "role": "user",
                "text": query_text
            }
        ]
    }

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

    response = send_gpt_request(prompt_data, url, api_key, folder_id)

    if response:
        return response["result"]["alternatives"][0]["message"]["text"]
    else:
        return "Ошибка при обращении к YandexGPT"
