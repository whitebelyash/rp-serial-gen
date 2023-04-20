#!/bin/env python3


# ReProtect Serial Generator
import sys
import string
import random as rnd
import base64 as b64

# idk чё это
# вообще, начало строки, обфускатор её пропускает
# сама строка представляет собой Vn%строка%VUMDk=
# изначально: [RW-SERIAL] + base64 серийника (похоже что тоже обфусцирован)
# думаю, в этом плане не углублялись
PREF = "Vn"
SUFF = "VUMDk="
MAGIC = "PUT09"
PREFIX = "[RW-SERIAL]"
STRING_LEN = 27

# params
verbose = False
string_provided = False

def dprint(message):
    if verbose == True:
        print("VERBOSE: {:s}".format(message))
# random string
def gen_string(size) -> str:
    dprint("генерация строки...")
    ret = ""
    for i in range(0,size):
        ret += rnd.choice(string.ascii_letters + string.digits)
    dprint("создана строка " + ret)
    return ret
# убирает лишние символы
def strip_string(string) -> str:
    return string.replace(PREF, "", 1).replace(SUFF, "", 1) # Vn: 1 проход, т.к. в начале стоит
# возвращает строку в первоначальный вид
def make_string(string) -> str:
    return PREF + string + SUFF
# приводит строку к норм виду
def parse_string(string) -> str:
    str_len = len(string)
    if str_len < STRING_LEN:
        print("Недостаточно символов в строке, генерация дополнительных...")
        string += gen_string(STRING_LEN - str_len)
        return string
    if str_len > STRING_LEN:
        print("Слишком много символов в строке")
        return string[0:STRING_LEN]
    return string

# Обфускация строки
def obfuscate(string) -> str:
    dprint("обфускация строки " + string)
    dprint("len" + str(len(string)))
    old_string = None
    new_string = ""
    # указатель на символ в строке
    pointer_char = 0
    # то же самое, но скачет по строке
    pointer_pos = 0
    if verbose == True:
        old_string = string
    for l in string:
        dprint(f"символ #{pointer_pos} в строке {string}")
        if pointer_char - 1 > len(string):
            break
        if len(string) - pointer_pos < 3:
            for c in string[pointer_pos:len(string)]:
                            new_string += c
            break
        c1 = string[pointer_pos]
        dprint(f"{c1}, pointer {pointer_pos}, pointer char: {pointer_char}")
        pointer_pos += 1
        c2 = string[pointer_pos]
        dprint(f"{c2}, pointer {pointer_pos}, pointer char: {pointer_char}")
        pointer_pos += 1
        c3 = string[pointer_pos]
        dprint(f"{c3}, pointer {pointer_pos}. pointer char: {pointer_char}")
        pointer_pos += 2    
        new_string += c3 + c2 + c1 + string[pointer_pos - 1]
        dprint(f"проход завершён, {old_string} -> {new_string}")
        pointer_char += 1
    dprint("out len " + str(len(new_string)))
    return new_string
def enc_base64(string) -> str:
    dprint("input: " + string)
    byte_str = string.encode("UTF-8")
    enc_byte = b64.b64encode(byte_str)
    ret = enc_byte.decode("UTF-8")
    dprint("output: " + ret)
    return ret

# добавляет префикс и прогоняет base64 три раза
def prepare(string) -> str:
    if len(string) != STRING_LEN:
        string = parse_string(string)
    string = PREFIX + string + MAGIC
    dprint("toEncode: " + string)
    for x in range(0,3):
        string = enc_base64(string)
    dprint("encoded: " + string)
    return string
def help():
    print(f"{sys.argv[0]} [-v] [string]")
def args_handle():
    if "-h" in sys.argv or "--help" in sys.argv:
        help()
        exit(0)
    if "-v" in sys.argv or "--verbose" in sys.argv:
        global verbose
        verbose = True
        # shitty code
        if "-v" in sys.argv:
            sys.argv.remove("-v")
        if "--verbose" in sys.argv:
            sys.argv.remove("--verbose")
    if len(sys.argv) > 1:
        global string_provided
        string_provided = True
        return
def main():
    args_handle()
    dprint(f"run, argv: {sys.argv}")
    dprint(f"params: verbose - {verbose}, string_provided - {string_provided}") 
    if string_provided == True:
        string = sys.argv[1]
    else:
        string = gen_string(27)
    string = prepare(string)
    string = strip_string(string)
    string = obfuscate(string)
    string = make_string(string)
    print(string)
# Main
print("ReProtect serial generator v666")
main()














    

        

