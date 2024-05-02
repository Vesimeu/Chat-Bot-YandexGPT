def add_gender_suffix(name):
    if name.endswith("а") or name.endswith("я"):
        return name[:-1] + "е"
    elif name.endswith("й") or name.endswith("ь"):
        return name[:-1] + "ю"
    elif name.endswith("о") or name.endswith("е"):
        return name + "му"
    else:
        return name + "у"

# Пример использования:
names = ["Петя", "Валера", "Андрей", "Ольга", "Иван"]
for name in names:
    print(f"У {add_gender_suffix(name)} день рождения.")
