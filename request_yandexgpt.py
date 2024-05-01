import requests
import json

def get_tokens(file_path):
    """
    Читает API ключ и токены из файла и возвращает их в виде словаря.
    """
    with open(file_path, "r") as file:
        lines = file.readlines()
        tokens = {}
        for line in lines:
            key, value = line.strip().split("=")
            tokens[key.strip()] = value.strip()
    return tokens

def send_gpt_request(prompt_data, url, api_key):
    """
    Отправляет запрос к YandexGPT API и возвращает ответ.
    """
    # Преобразуем данные в JSON
    prompt_data_json = json.dumps(prompt_data)

    # Отправляем запрос к YandexGPT API
    response = requests.post(
        url,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Api-Key {api_key}",
        },
        data=prompt_data_json
    )

    return response

def main():
    # Загружаем токены из файла
    tokens = get_tokens("token.txt")
    token_bot = tokens.get("token_bot")
    SecretKey = tokens.get("SecretKey")
    FOLDER_ID = tokens.get("FOLDER_ID")

    # Тело запроса к YandexGPT API
    prompt_data = {
        "modelUri": f"gpt://{FOLDER_ID}/yandexgpt-lite",
        "completionOptions": {
            "stream": False,
            "temperature": 0.6,
            "maxTokens": "2000"
        },
        "messages": [
            {
                "role": "system",
                "text": "Представь что ты программист"
            },
            {
                "role": "user",
                "text": "Как мне написать программу на Python которая бы работала?"
            }
        ]
    }

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

    # Отправляем запрос к YandexGPT API
    response = send_gpt_request(prompt_data, url, SecretKey)

    # Проверяем статус код ответа
    if response.status_code == 200:
        # Выводим ответ от API
        print(response.json())
    else:
        # Выводим статус код ответа
        print(f"Error: {response.status_code}")


if __name__ == "__main__":
    main()
