import math
import re
import copy


def count_text_in_quotes(text):  # считаем строковые константы
    amount = 0
    amount += len(re.findall(r'(".*?")', text))
    amount += len(re.findall(r"('.*?')", text))
    # print(amount)

    return {
        '" "': amount
    }


def remove_text_in_quotes(text):  # удаляем текст в кавычках
    amount = 0
    amount += len(re.findall(r'(".*?")', text))
    amount += len(re.findall(r"('.*?')", text))
    # print(amount)
    text = re.sub(r'(".*?")', '""', text)
    return re.sub(r"('.*?')", "''", text)


def remove_comments(text):  # удаляем комментарии
    return re.sub(r'#.*', '', text)


def count_binary_op(text): # считаем бинарные операторы
    binary_operators = {
        '+': len(re.findall(r'\+(?!=)', text)),
        '-': len(re.findall(r'-(?!=)', text)),
        '*': len(re.findall(r'(?<!\*)\*(?![*=])', text)),
        '/': len(re.findall(r'/(?!=)', text)),
        '%': len(re.findall(r'%(?!=)', text)),
        '**': len(re.findall(r'\*\*', text)),

        '<<': len(re.findall(r'<<', text)),
        '>>': len(re.findall(r'>>', text)),
        '>': len(re.findall(r'(?<![=>])>(?![>=])', text)),
        '<': len(re.findall(r'(?<!<)<(?![=<])', text)),

        '=': len(re.findall(r'(?<![=!><+\-*/%])=(?!=)', text)),
        '!=': len(re.findall(r'!=', text)),
        '==': len(re.findall(r'(?!=)==(?!=)', text)),
        '===': len(re.findall(r'===', text)),
        '<=>': len(re.findall(r'<=>', text)),
        '>=': len(re.findall(r'>=', text)),
        '<=': len(re.findall(r'<=(?!>)', text)),

        '&&': len(re.findall(r'&&', text)),
        '||': len(re.findall(r'\|\|', text)),
        '!': len(re.findall(r'!(?!=)', text)),

        '+=': len(re.findall(r'\+=', text)),
        '-=': len(re.findall(r'-=', text)),
        '*=': len(re.findall(r'\*=', text)),
        '/=': len(re.findall(r'/=', text)),
        '%=': len(re.findall(r'%=', text)),

        '&': len(re.findall(r'(?<!&)&(?!&)', text)),
        '|': len(re.findall(r'(?<!\|)\|(?!\|)', text)),
        '^': len(re.findall(r'\^', text)),
        '~': len(re.findall(r'~', text)),
        'and': len(re.findall(r'\band\b', text)),
        'not': len(re.findall(r'\bnot\b', text)),
        'or': len(re.findall(r'\bor\b', text)),
        '?:': len(re.findall(r'\?.+?:', text)),

        '.': len(re.findall(r'(?<!\.)\.(?!\.)', text)),
        '..': len(re.findall(r'(?<!\.)\.\.(?!\.)', text)),
        '...': len(re.findall(r'\.\.\.', text)),
        ',': len(re.findall(r',', text)),

        '()': len(re.findall(r'(?<!\w)(\s*\()', text)),
        '[]': len(re.findall(r'\[.*?]', text)),
        '::': len(re.findall(r'::', text))
    }
    return binary_operators


def count_key_words(text):   # считаем ключевые слова(операторы управления и функции)
    return {
            'in': len(re.findall(r'\bin\b', text)),
            'break': len(re.findall(r'\bbreak\b', text)),
            'next': len(re.findall(r'\bnext\b', text)),
            'if...(else)...end': len(re.findall(r'\bif\b', text)),
            'case...when...(else)...end': len(re.findall(r'\bcase\b', text)),
            'BEGIN...END': len(re.findall(r'\bBEGIN\b', text)),
            'begin...end': len(re.findall(r'\bbegin\b', text)),
            'until...end': len(re.findall(r'\buntil\b', text)),
            'while...end': len(re.findall(r'\bwhile\b', text)),
            'loop..do...end': len(re.findall(r'\bloop\b\s+\bdo\b', text)),
            'for...in...end': len(re.findall(r'\bfor\b', text)),
            'redo': len(re.findall(r'\bredo\b', text)),
            'retry': len(re.findall(r'\bretry\b', text)),
            'return': len(re.findall(r'\breturn\b', text)),

            'puts': len(re.findall(r'\bputs\b', text)),
            'print': len(re.findall(r'\bprint\b', text)),
            'gets': len(re.findall(r'\bgets\b', text)),

            'alias': len(re.findall(r'\balias\b', text)),  # псевдонимы
            'if...elsif...(else)...end': len(re.findall(r'\belsif\b', text)),
            'unless...end': len(re.findall(r'\bunless\b', text)),
            'module...end': len(re.findall(r'\bmodule\b', text)),  # создание групп
            'yield': len(re.findall(r'\byield\b', text))
        }


def count_operands(text): # считаем числовые константы
    const_list = re.findall(r'\b\d+\b', text)
    count_const = {}
    for const in const_list:
        count_const[const] = len(re.findall(fr'\b{const}\b', text))
    return count_const


def count_variables(text):  # считаем перемнные
    var_list = (re.findall(r'\w+(?:, *\w+)*? *= *(?!=)', text))
    naked_var = []
    count_var = {}

    for var_str in var_list:
        var_name = ""
        for char in var_str:
            if char.isalnum():
                var_name += char
            elif char == ',' or char == '=':
                if var_name:
                    naked_var.append(var_name)
                    var_name = ""

    for var in naked_var:
        count_var[var] = len(re.findall(fr'\b{var}\b', text))

    return count_var


def user_functions_as_operators(text):  # пользовательские функции(вспомогательная)
    list_of_functions = (re.findall(r'def\s+\w+', text))
    dict_func_count = {}
    for i in range(len(list_of_functions)):
        print(list_of_functions[i])
        list_of_functions[i] = list_of_functions[i].replace('def', ' ')
        list_of_functions[i] = list_of_functions[i].strip()
    for i in range(len(list_of_functions)):
        a = list_of_functions[i]
        flags = re.MULTILINE
        l = len(re.findall(fr'^\s*{re.escape(a)}.*?\)$', text, flags=re.MULTILINE))
        dict_func_count[a + "( )"] = l
    print(dict_func_count)
    return dict_func_count


def user_functions_operators(text):  # пользовательские функции как операторы
    list_of_functions = re.findall(r'def\s+\w+', text)
    dict_func_operators = user_functions_as_operators(text)
    dict_func_operands = {}
    for i in range(len(list_of_functions)):
        print(list_of_functions[i])
        list_of_functions[i] = list_of_functions[i].replace('def', ' ')
        list_of_functions[i] = list_of_functions[i].strip()
    for i in range(len(list_of_functions)):
        a = list_of_functions[i]
        l = len(re.findall(fr'(?<!def)\s+{a}', text))
        dict_func_operands[a + "( )"] = l - dict_func_operators[a + "( )"]
        dict_func_operators[a + "( )"] += dict_func_operands[a + "( )"]

    return dict_func_operators


def user_functions_operands(text):  # пользовательские функции как операнды
    list_of_functions = re.findall(r'def\s+\w+', text)
    dict_func_operators = user_functions_as_operators(text)
    dict_func_operands = {}
    for i in range(len(list_of_functions)):
        print(list_of_functions[i])
        list_of_functions[i] = list_of_functions[i].replace('def', ' ')
        list_of_functions[i] = list_of_functions[i].strip()
    for i in range(len(list_of_functions)):
        a = list_of_functions[i]
        l = len(re.findall(fr'(?<!def)\s+{a}', text))
        dict_func_operands[a + "( )"] = l - dict_func_operators[a + "( )"]
        dict_func_operators[a + "( )"] += dict_func_operands[a + "( )"]
    print(dict_func_operands)
    return dict_func_operands


def built_in_functions(text):  # операторы встроенных функций
    list_of_functions = re.findall(r'(?<!\.)\.\w+[ \n]', text)
    dict_built_in_func = {}
    for i in range(len(list_of_functions)):
        list_of_functions[i] = list_of_functions[i].replace('.', ' ')
        if list_of_functions[i].find('\n') != -1:
            list_of_functions[i] = list_of_functions[i].replace('\n', ' ')
        list_of_functions[i] = list_of_functions[i].strip()
    for i in range(len(list_of_functions)):
        a = list_of_functions[i]
        l = len(re.findall(fr'.{a}\b', text))
        dict_built_in_func[a] = l

    return dict_built_in_func


def remove_by_value(dictionary, value):
    keys_to_remove = []
    for key, val in dictionary.items():
        if val == value:
            keys_to_remove.append(key)
    for key in keys_to_remove:
        del dictionary[key]

def sum_dict_values(dictionary):
    total_sum = 0
    for value in dictionary.values():
        total_sum += value
    return total_sum


def metrics(text):
    operators_dict, operands_dict = copy.deepcopy(fill_the_table(text))
    operators_dict.popitem()
    operands_dict.popitem()
    sum_1 = sum_dict_values(operands_dict)
    sum_2 = sum_dict_values(operators_dict)
    length_pr = sum_1 + sum_2
    dict_pr = len(operands_dict) + len(operators_dict)
    volume_pr = length_pr * math.log2(dict_pr)
    volume_pr = int(volume_pr)
    str = f'Словарь = {dict_pr};\t' + f'Длина = {length_pr};\t' + f'Объём = {volume_pr};'
    return str


def fill_the_table(text):
    operators_dict = {}
    operands_dict = {}

    operands_dict = count_text_in_quotes(text)
    text = remove_text_in_quotes(text)
    text = remove_comments(text)

    operands_dict.update(count_operands(text))
    operands_dict.update(count_variables(text))
    operands_dict.update(user_functions_operands(text))
    remove_by_value(operands_dict, 0)

    operators_dict = count_binary_op(text)
    operators_dict.update(count_key_words(text))
    operators_dict.update(user_functions_operators(text))
    operators_dict.update(built_in_functions(text))
    remove_by_value(operators_dict, 0)

    sum_1 = sum_dict_values(operands_dict)
    operands_dict.update({'Итого': sum_1})
    sum_2 = sum_dict_values(operators_dict)
    operators_dict.update({'Итого': sum_2})

    length_pr = sum_1 + sum_2
    dict_pr = len(operands_dict) + len(operators_dict)
    volume_pr = length_pr * math.log2(dict_pr)

    return operands_dict, operators_dict
