# token_loader.py
#Отсюда я беру необходимые данные из файла
def read_tokens_from_file(file_path: str) -> dict:
    tokens = {}
    with open(file_path, 'r') as file:
        for line in file:
            key, value = line.strip().split(" = ")
            tokens[key.strip()] = value.strip()
    return tokens
