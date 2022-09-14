""" Калькулятор """
import decimal


def _calc_sum(op1: complex, op2: complex) -> complex:
    return op1 + op2


def _calc_diff(op1: complex, op2: complex) -> complex:
    return op1 - op2


OPERATORS = {
    '+': _calc_sum,
    '-': _calc_diff
}


def get_help() -> str:
    res_str = 'Введите выражение в формате <операнд 1> <операция> <операнд 2>\n' \
              'Поддерживаемые операнды: числа и комплексные числа\n' \
              'Разделители: . - для дробной части, , - для мнимой части\n' \
              'Поддерживаемые операции: +, -\n' \
              'Например: 3,1 - 1.2\n'
    return res_str


def execute_command(command: str) -> str:
    cmd_list = command.split()
    if len(cmd_list) != 3:
        return 'Incorrect input'
    op1 = _get_operand(cmd_list[0])
    operation = cmd_list[1]
    op2 = _get_operand(cmd_list[2])
    func = OPERATORS.get(operation)
    if func:
        res = func(op1, op2)
    else:
        return 'Incorrect input'

    return f'{command} = {_convert_result_to_str(res)}'


def _get_operand(in_str: str):
    tmp_list = in_str.split(',')
    real = 0
    img = 0
    if len(tmp_list) == 1:
        if tmp_list[0].replace('.', '', 1).isdigit() and tmp_list[0].count('.') < 2:
            real = decimal.Decimal(tmp_list[0])
        else:
            return None
    elif tmp_list[0].replace('.', '', 1).isdigit() and tmp_list[0].count('.') < 2:
        if tmp_list[0].isdecimal():
            real = decimal.Decimal(tmp_list[0])
        else:
            return None
        if tmp_list[1].replace('.', '', 1).isdigit() and tmp_list[1].count('.') < 2:
            img = decimal.Decimal(tmp_list[1])
        else:
            return None
    else:
        return None
    return complex(f'{real}+{img}j')


def _convert_result_to_str(number: complex) -> str:
    real = int(number.real) if number.real == int(number.real) else number.real
    imag = int(number.imag) if number.imag == int(number.imag) else number.imag

    if imag == 0:
        res_str = str(real)
    else:
        res_str = ','.join([str(real), str(imag)])
    return res_str


if __name__ == '__main__':
    print(get_help())
    print(execute_command('3.1 + 1'))
    print(execute_command('3 - 1'))
    print(execute_command('3,1 - 1.21'))
