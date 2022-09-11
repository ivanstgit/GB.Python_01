"""
Модуль хранения данных:
- параметры чтения и записи
- импорт из базы
- экпорт в базу
"""
import json

PARAMS = {
    'encoding': 'utf-8'
}

FILE_NAMES = {
    'people_record_list': 'people_record_list.json'
    }


def save(db_id: str, content):
    with open(FILE_NAMES[db_id], 'w', encoding=PARAMS['encoding']) as fw:
        json.dump(content, fw, ensure_ascii=False, indent=0)


def load(db_id: str):
    with open(FILE_NAMES[db_id], 'r', encoding=PARAMS['encoding']) as fr:
        return json.load(fr)
