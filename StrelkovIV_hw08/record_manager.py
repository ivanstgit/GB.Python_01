"""
Модуль обработки данных:
- взаимодействия с интерфейсом пользователя и модулем хранения
- проверка корректности
"""
import datetime
import database

PARAMS = {
    'db_id': 'people_record_list',
    'key_field': 'id',
    'del_field': 'deleted'}

# Описание модели- поле: описание, функция преобр из CLI, функция преобр из DB, функция преобр в DB
MODEL = {
    'id': ('Табельный номер', int, int, int),
    'valid_from': ('Запись действительна с',
                   datetime.date.fromisoformat, datetime.date.fromisoformat, str),
    'valid_to': ('Запись действительна с',
                   datetime.date.fromisoformat, datetime.date.fromisoformat, str),
    'last_name': ('Фамилия', str, str, str),
    'first_name': ('Имя', str, str, str),
    'second_name': ('Отчество', str, str, str),
    'comment': ('Комментарий', str, str, str),
    'deleted': ('Архивировано', bool, bool, bool)
}

__records = dict()


def init():
    __records.clear()
    for record in map(_convert_record_db_to_internal, database.load(PARAMS['db_id'])):
        __records[record['id']] = record


def save():
    database.save(PARAMS['db_id'], list(map(_convert_record_internal_to_db, __records.values())))


def get_id_field() -> str:
    return PARAMS.get('key_field')


def get_record_field_list() -> list:
    return list(MODEL.items())


def add_record_from_cli(cli_row: dict) -> (int, str):
    """ return id of new record or error string"""
    return _add_record(_convert_record_cli_to_internal(cli_row))


def update_record_from_cli(cli_row: dict) -> (int, str):
    """ return id of changed record or error string"""
    return _modify_record(_convert_record_cli_to_internal(cli_row))


def delete_record(record_id: int):
    record = __records.get(record_id)
    if record:
        record['deleted'] = True
        __records[record_id] = record
        return record_id
    else:
        return -1


def get_record_list(on_date=datetime.date.today(), with_deleted=False) -> list:
    if with_deleted:
        result = list([{record_id: list(map(str,
                                            [value for key, value in record.items()
                                             if key != 'id']))}
                       for record_id, record in __records.items()
                       if record['valid_from'] <= on_date <= record['valid_to']])
    else:
        result = list([{record_id: list(map(str,
                                            [value for key, value in record.items()
                                             if key != 'id' and key != 'deleted']))}
                       for record_id, record in __records.items()
                       if record['valid_from'] <= on_date <= record['valid_to'] and not record['deleted']])
    return result


def _check_record(row: dict) -> str:
    error_desc = ''
    return error_desc


def _add_record(row: dict) -> (int, str):
    """ return id of new record or error string"""
    if row.get(get_id_field()):
        return -1, 'error: id found'
    if row.get(PARAMS['del_field']):
        return -1, 'error: deletion indicator found'
    # generate id
    if len(__records.keys()) > 0:
        new_id = max(__records.keys()) + 1
    else:
        new_id = 1
    row[get_id_field()] = new_id
    row[PARAMS['del_field']] = False

    check_result = _check_record(row)
    if check_result == '':
        __records[new_id] = row
        return new_id, ''
    else:
        return -1, check_result


def _modify_record(row: dict) -> (int, str):
    """ return id of new record or error string"""
    existing_id = row.get(get_id_field())
    if not existing_id:
        return -1, 'error: id not found'

    row[PARAMS['del_field']] = False

    check_result = _check_record(row)
    if check_result == '':
        __records[existing_id] = row
        return existing_id, ''
    else:
        return -1, check_result


def _convert_record_cli_to_internal(row: dict) -> dict:
    # Convert external record to model structure
    if len(row) == 0:
        return {}
    res = dict.fromkeys(MODEL)
    for field, value in row.items():
        model_field = MODEL.get(field)
        if not model_field:
            return {}
        func = model_field[1]
        res[field] = func(value)
    return res


def _convert_record_db_to_internal(row: dict) -> dict:
    # Convert model structure to db-compatible format
    res = dict.fromkeys(MODEL)
    for field, value in row.items():
        model_field = MODEL.get(field)
        func = model_field[2]
        res[field] = func(value)
    return res


def _convert_record_internal_to_db(row: dict) -> dict:
    # Convert model structure to db-compatible format
    res = dict.fromkeys(MODEL)
    for field, value in row.items():
        model_field = MODEL.get(field)
        func = model_field[3]
        res[field] = func(value)
    return res


if __name__ == '__main__':
    test_record_cli = {
        'valid_from': str(datetime.date(2020, 7, 1)),
        'valid_to': str(datetime.date(2099, 7, 1)),
        'last_name': 'Фамилия',
        'first_name': 'Имя',
        'second_name': 'Отчество',
        'comment': 'Комментарий'
    }
    print(test_record_cli)
    print(add_record_from_cli(test_record_cli))
    print(get_record_list())
    print(delete_record(1))
    print(add_record_from_cli(test_record_cli))
    print(get_record_list())
    print(get_record_list(with_deleted=True))
    print(list(map(_convert_record_internal_to_db, __records.values())))
    save()
    init()
    print(get_record_list())
    print(__records)

