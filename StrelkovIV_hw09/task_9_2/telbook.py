# Создать телефонный справочник с возможностью импорта и экспорта данных в нескольких форматах.
# • под форматами понимаем структуру файлов, например:в файле на одной строке хранится одна часть записи,
# пустая строка - разделитель
# Фамилия_1
# Имя_1
# Телефон_1
# Описание_1
#
# Фамилия_2
# Имя_2
# Телефон_2
# Описание_2
#
# и т.д.в файле на одной строке хранится все записи, символ разделитель - ;
# Фамилия_1,Имя_1,Телефон_1,Описание_1
# Фамилия_2,Имя_2,Телефон_2,Описание_2
# и т.д.

BASE_FILE_NAME = 'telbook_base.txt'
BASE_FIELD_SEPARATOR = '\t'
BASE_ROW_SEPARATOR = '\n'
BASE_ENCODING = 'utf-8'
UPDATE_RESULT_TXT = \
    {'e': 'Error', 'a': 'Added', 'u': 'Updated', 'd': 'Deleted', 'i': 'Ignored'}
INPUT_OPERATIONS = \
    {'qa': "Выйти без сохранения",
     'qw': 'Сохранить и выйти',
     'set_sep': "Сменить разделители",
     'i': 'Загрузить в память файл',
     'e': 'Выгрузить память в файл'}
INPUT_SEP_FOR_REPLACE = \
    {'tab': ['Табуляция', '\t'],
     'cr': ['Перенос строки', '\n']}
global_dict = dict()
user_separators = dict()


def _update_row_in_dict(row: list):
    """ Проверка элемента и возврат результата обновления (UPDATE_RESULT_TXT) """
    if len(row) == 1 and row[0] == '':
        update_result = 'i'
    elif len(row) < 2 or len(row) > 4:
        update_result = 'e'  # Error
    elif row[0] == '' or row[1] == '':
        update_result = 'e'  # Error
    else:
        dict_key = row[0] + '_' + row[1]
        if len(row) == 2:
            if global_dict.get(dict_key):
                global_dict.pop(dict_key)
                update_result = 'd'
            else:
                update_result = 'i'
        else:
            elem = global_dict.get(dict_key)
            new_row = row.copy()
            if len(new_row) == 3:
                new_row.append('')
            if elem:
                if BASE_FIELD_SEPARATOR.join(elem) == BASE_FIELD_SEPARATOR.join(new_row):
                    update_result = 'i'
                else:
                    global_dict[dict_key] = new_row
                    update_result = 'u'
            else:
                update_result = 'a'
                global_dict[dict_key] = new_row
    return update_result


def _import_from_file(file_name: str, row_sep=BASE_ROW_SEPARATOR, field_sep=BASE_FIELD_SEPARATOR):
    """ Парсинг и добавление данных в словарь, возврат статистики обновления"""
    update_statistics = {res: list() for res in list(UPDATE_RESULT_TXT.keys())}
    split_sep = field_sep + row_sep if field_sep == row_sep else row_sep
    with open(file_name, 'r') as in_file:
        row_counter = 1
        for line in in_file.read().split(sep=split_sep):
            row = line.split(sep=field_sep)
            res = _update_row_in_dict(row)
            update_statistics[res].append(row_counter)
            row_counter += 1
        if line == '' and res == 'i':
            update_statistics[res].pop()
    return update_statistics


def _export_to_file(file_name: str, row_sep=BASE_ROW_SEPARATOR, field_sep=BASE_FIELD_SEPARATOR):
    """ Экспорт словаря в файл """
    result = 0
    with open(file_name, 'w', encoding=BASE_ENCODING) as out_file:
        out_file.write(row_sep.join([field_sep.join(row) for row in global_dict.values()]))
        result = len(global_dict.keys())
    return result


def _convert_user_sep_to_internal(user_sep: str) -> str:
    return INPUT_SEP_FOR_REPLACE[user_separators['row_sep']][1] \
        if INPUT_SEP_FOR_REPLACE.get(user_separators['row_sep']) else user_separators['row_sep']


def get_help(command: str) -> str:
    if command == 'set_sep':
        help_str = 'Введите разделители через пробел\n'
        help_str += "При смене разделителя используйте следующие обозначения\n"
        for key, value in INPUT_SEP_FOR_REPLACE.items():
            help_str += f"  {key}: {value[0]}\n"
        help_str += "Например: cr tab\n"
    elif command == 'i':
        help_str = 'Отправьте файл в чат\n'
        help_str += "При импорте игнорируются пустые и существующие записи. Последний разделитель строк обязателен."
    else:
        help_str = ""
    return help_str


def get_separators_info() -> str:
    row_sep = INPUT_SEP_FOR_REPLACE[user_separators['row_sep']][0] \
        if INPUT_SEP_FOR_REPLACE.get(user_separators['row_sep']) else user_separators['row_sep']
    col_sep = INPUT_SEP_FOR_REPLACE[user_separators['row_sep']][0] \
        if INPUT_SEP_FOR_REPLACE.get(user_separators['row_sep']) else user_separators['row_sep']
    return f'Разделитель строк: {row_sep}, столбцов: {col_sep}\n'


def init() -> str:
    stats = _import_from_file(BASE_FILE_NAME)
    init_row_count = len(stats.get('a'))
    user_separators['row_sep'] = 'cr'
    user_separators['col_sep'] = ';'
    return f"Инициализация базы: {init_row_count} записей."


def set_separators(in_str: str) -> str:
    sep_list = in_str.split()
    if len(sep_list) == 2:
        user_separators['row_sep'] = 'cr'
        user_separators['col_sep'] = ';'
    return get_separators_info()


def abort() -> str:
    global_dict.clear()
    return "Выход без сохранения"


def commit() -> str:
    res = f"Сохранено ({_export_to_file(BASE_FILE_NAME)} записей)."
    global_dict.clear()
    return res


def import_file(file_name: str) -> str:
    result_str = 'Статистика импорта:\n'
    stats = _import_from_file(file_name,
                              row_sep=_convert_user_sep_to_internal(user_separators['row_sep']),
                              field_sep=_convert_user_sep_to_internal(user_separators['col_sep']))
    for stat, stat_txt in UPDATE_RESULT_TXT.items():
        if len(stats[stat]) > 0:
            result_str += f'{stat_txt}: {len(stats[stat])}\n'
            if stat == 'e':
                result_str += f"Ошибочные записи: {stats[stat]}\n"
    return result_str


def export_file(file_name: str) -> str:
    if file_name == BASE_FILE_NAME:
        return "Зарезервированное имя файла"
    record_cnt = _export_to_file(file_name,
                                 row_sep=_convert_user_sep_to_internal(user_separators['row_sep']),
                                 field_sep=_convert_user_sep_to_internal(user_separators['col_sep']))
    return f"Экспортировано {record_cnt} записей).\n"


if __name__ == '__main__':
    print(init())
    print(get_help(''))
    print(get_separators_info())
    # stats = import_from_file(BASE_FILE_NAME)
    # init_row_count = len(stats.get('a'))
    # print(f"Инициализация базы: {init_row_count} записей.")
    # print_init_help = True
    # while True:
    #     if print_init_help:
    #         print("Введите операцию с параметрами через пробел, доступные операции:")
    #         for key, value in INPUT_OPERATIONS.items():
    #             print(f"  {key}: {value}")
    #         print("Для указания спец.символов в качестве разделителей используйте следующие обозначения")
    #         for key, value in INPUT_SEP_FOR_REPLACE.items():
    #             print(f"  {key}: {value[0]}")
    #         print_init_help = False
    #         print("Пример импорта 1: i task_7_1_import1.txt cr cr")
    #         print("Пример импорта 2: i task_7_1_import2.csv cr ;")
    #         print("Пример экспорта: e task_7_1_export.txt cr tab")
    #         print("Пример импорта с удалением: i task_7_1_import3_with_deletion.csv cr ;")
    #         print("При импорте игнорируются пустые и существующие записи. Последний разделитель строк обязателен.")
    #
    #     input_list = input("Введите операцию с параметрами через пробел:").split()
    #     if len(input_list) == 0:
    #         continue
    #
    #     command = input_list[0]
    #     if command == 'qa':
    #         break
    #     elif command == 'qw':
    #         print(f"Сохранено ({export_to_file(BASE_FILE_NAME)} записей).")
    #         break
    #     elif command == 'i':
    #         if len(input_list) == 4:
    #             file_name = input_list[1]
    #             row_sep = input_list[2]
    #             col_sep = input_list[3]
    #             row_sep = INPUT_SEP_FOR_REPLACE[row_sep][1] if INPUT_SEP_FOR_REPLACE.get(row_sep) else row_sep
    #             col_sep = INPUT_SEP_FOR_REPLACE[col_sep][1] if INPUT_SEP_FOR_REPLACE.get(col_sep) else col_sep
    #             stats = import_from_file(file_name, row_sep=row_sep, field_sep=col_sep)
    #             for stat, stat_txt in UPDATE_RESULT_TXT.items():
    #                 if len(stats[stat]) > 0:
    #                     print(f'{stat_txt}: {len(stats[stat])}')
    #                     if stat == 'e':
    #                         print(f"Ошибочные записи: {stats[stat]}")
    #         else:
    #             print("Некорректный ввод")
    #             print_init_help = True
    #     elif command == 'e':
    #         if len(input_list) == 4:
    #             file_name = input_list[1]
    #             if file_name == BASE_FILE_NAME:
    #                 print("Зарезервированное имя файла")
    #                 continue
    #             row_sep = input_list[2]
    #             col_sep = input_list[3]
    #             row_sep = INPUT_SEP_FOR_REPLACE[row_sep][1] if INPUT_SEP_FOR_REPLACE.get(row_sep) else row_sep
    #             col_sep = INPUT_SEP_FOR_REPLACE[col_sep][1] if INPUT_SEP_FOR_REPLACE.get(col_sep) else col_sep
    #             print(f"Экспортировано ({export_to_file(file_name, row_sep=row_sep, field_sep=col_sep)} записей).")
    #         else:
    #             print("Некорректный ввод")
    #             print_init_help = True


