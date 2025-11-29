import re

def clean_text(text: str) -> str:
    if not text:
        return ""
    # Удаляем лишние пробелы (включая \n, \t) и заменяем на одиночный пробел
    text = re.sub(r'\s+', ' ', text)
    # Убираем пробелы в начале и конце
    return text.strip()
