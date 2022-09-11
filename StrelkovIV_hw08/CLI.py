"""
Модуль интерфейса командной строки:
- вывод справки
- обработка команд
"""
import record_manager

INPUT_OPERATIONS = \
    {'qа': "Выйти без сохранения",
     'qw': 'Сохранить результат и выйти',
     'add': 'Добавить запись <Поля>',
     'upd': 'Изменить запись <Табельный №>  <Поля>',
     'del': 'Удалить запись <Табельный №>',
     'dis': 'Показать список сотрудников'}


def go():
    record_manager.init()
    print(f"Инициализация базы: {len(record_manager.get_record_list())} записей.")
    field_list = record_manager.get_record_field_list()

    print_init_help = True
    while True:
        if print_init_help:
            print("Введите операцию с параметрами через пробел, доступные операции:")
            for key, value in INPUT_OPERATIONS.items():
                print(f"  {key}: {value}")
            print("Последовательность полей при добавлении:")
            for field, spec in field_list:
                print(spec[0], end='; ')
            print('')
            print_init_help = False
            print("Пример добавления: add 2022-02-02 2099-12-31 Иванов Иван Иванович 35")
            print("Пример корректировки: upd 2 2022-02-02 2022-12-31 Иванов Иван Иванович 35")
            print("Пример удаления: del 2")

        input_list = input("Введите операцию с параметрами через пробел:").split()
        if len(input_list) == 0:
            continue

        command = input_list[0]
        params = input_list[1:]
        if command == 'qa':
            break
        elif command == 'qw':
            record_manager.save()
            print(f"Сохранено ({len(record_manager.get_record_list())} записей).")
            break
        elif command == 'add':
            if len(params) > 0:
                record = {field_list[i+1][0]: params[i] for i in range(len(params))}
                record_id, error_txt = record_manager.add_record_from_cli(record)
                if record_id > 0:
                    print(f"Сотрудник добавлен с номером {record_id}.")
                else:
                    print(error_txt)
            else:
                print("Некорректный ввод")
                print_init_help = True
        elif command == 'upd':
            if len(params) > 0:
                record = {field_list[i][0]: params[i] for i in range(len(params))}
                record_id, error_txt = record_manager.update_record_from_cli(record)
                if record_id > 0:
                    print(f"Данные обновлены для сотрудника с номером {record_id}.")
                else:
                    print(error_txt)
            else:
                print("Некорректный ввод")
                print_init_help = True
        elif command == 'dis':
            for record in record_manager.get_record_list():
                print(record)
        elif command == 'del':
            if len(params) > 0:
                print(f"Запись удалена: {record_manager.delete_record(int(params[0]))}")
            else:
                print("Некорректный ввод")
                print_init_help = True
