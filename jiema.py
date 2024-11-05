import base64
import urllib.parse
import datetime
from colorama import Fore, Style
import re


class Ping:
    is_found = 0
    val_name = 'None'
    decoded_value = ' '


def detect_base64():
    try:
        Ping.decoded_value = base64.b64decode(value).decode('UTF-8').replace('\n', ' ').strip()
        if Ping.decoded_value == '':
            pass
        else:
            Ping.val_name = 'BASE64'
            Ping.is_found = 1
    except ValueError:
        pass


def detect_base32():
    try:
        Ping.decoded_value = base64.b32decode(value).decode('UTF-8').replace('\n', ' ').strip()
        if Ping.decoded_value == '':
            pass
        else:
            Ping.val_name = 'BASE32'
            Ping.is_found = 1
    except ValueError:
        pass


def detect_hexa():
    try:
        hex_value = value.replace(" ", "")
        if re.match('^[0-9a-fA-F]+$', hex_value):
            Ping.decoded_value = bytes.fromhex(hex_value).decode('UTF-8').strip()
            Ping.val_name = 'HEXADECIMAL'
            Ping.is_found = 1
    except ValueError:
        pass


def detect_ue():
    try:
        if re.search(r'\\u[0-9a-fA-F]{4}', value):
            Ping.decoded_value = value.encode('utf-8').decode('unicode-escape', errors='strict')
            Ping.val_name = 'UNICODE ESCAPE'
            Ping.is_found = 1
    except UnicodeDecodeError:
        pass


def detect_morse():
    morse_dict = {
        '-----': '0', '.----': '1', '..---': '2', '...--': '3', '....-': '4',
        '.....': '5', '-....': '6', '--...': '7', '---..': '8', '----.': '9',
        '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E',
        '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',
        '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O',
        '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
        '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',
        '--..': 'Z', '--..--': ',', '.-.-.-': '.', '..--..': '?',
        '-..-.': '/', '-....-': '-', '-.--.': '(', '-.--.-': ')',
        '/': ' '
    }

    separated = value.split(' ')
    for symbol in separated:
        if symbol in morse_dict:
            Ping.decoded_value += morse_dict[symbol]
            Ping.is_found = 1
            Ping.val_name = 'MORSE'


def detect_binary():
    clean_value = value.replace(" ", "")
    if clean_value and all(char in '01' for char in clean_value):
        binary_int = int(clean_value, 2)
        byte_number = (binary_int.bit_length() + 7) // 8
        binary_array = binary_int.to_bytes(byte_number, 'big')
        Ping.decoded_value = binary_array.decode()
        Ping.is_found = 1
        Ping.val_name = 'BINARY'


def detect_url():
    for char in value:
        if char in '%' and Ping.is_found == 0:
            Ping.decoded_value = urllib.parse.unquote(value, encoding='UTF-8')
            Ping.is_found = 1
            Ping.val_name = 'URL'


def save_results_to_txt(results_to_save):
    with open('results.txt', 'a', encoding='utf-8') as txt_file:
        for result in results_to_save:
            txt_file.write(result + '\n')


def save_results_to_csv(results_to_save):
        with open('results.csv', 'w', encoding='utf-8') as csv_file:
            csv_file.write("time,format,original,decoded\n")
            for result in results_to_save:
                current_time, val_name, original_value, decoded_value = result
                csv_file.write(f"{current_time},{val_name},{original_value},{decoded_value}\n")



def strip_ansi(text):
    return re.sub(r'\x1B\[[0-?]*[mK]', '', text)


def execute():
    Ping.decoded_value = ''
    Ping.is_found = 0
    detect_base64()
    detect_base32()
    detect_hexa()
    detect_ue()
    detect_morse()
    detect_binary()
    detect_url()


if __name__ == '__main__':
    print(f"""
    \t\t\t\t\t\t    {Style.BRIGHT}@jydae on github.com{Style.RESET_ALL}
    ┌─────── {Fore.RED}Jiema Decoder{Style.RESET_ALL} ─────────────────────────────────────────────┐
    │  请输入字符串进行解码。       Please enter a string for decoding. │
    │  输入 "csv" 保存为 CSV 文件。 Type "csv" to save as CSV.  \t│
    │  输入 "txt" 保存为文本文件。  Type "txt" to save as text. \t│
    │  输入 "file" 解码指定文件。   Type "file" to decode a file.\t│
    └───────────────────────────────────────────────────────────────────┘
    """)

    results = []

    try:
        while True:
            value = input(':')

            if value.strip() == '':
                continue

            if any(char in value for char in ','):
                print(f'\n\t检测到一个符号；请��在字符串中使用逗号。')
                print(f'\tA symbol has been detected; do not use commas within the string.')

            execute()


            def print_result():
                current_time = f'{Fore.RED + Style.BRIGHT}{datetime.datetime.now().strftime("%H:%M:%S")}{Style.RESET_ALL}'
                val_name = f'{Style.BRIGHT + Fore.GREEN}{Ping.val_name}{Style.RESET_ALL}'
                original_value = f'{Style.BRIGHT}{value}{Style.RESET_ALL}'
                output_string = f'[{current_time}] [{val_name}] [{original_value}] Decoded: {Ping.decoded_value}'

                print(output_string)
                results.append((strip_ansi(current_time), strip_ansi(val_name), strip_ansi(original_value), Ping.decoded_value))


            if Ping.is_found == 1:
                if value == 'file':
                    print(f'\n\t输入文件的名称或路径（例如，encodings.txt）。')
                    print(f'\tType the name or path of the file (i.e., encodings.txt).')
                    file_name = input('\t:')
                    with open(file_name, 'r') as file:
                        print()
                        for line in file:
                            value = line.strip()
                            execute()
                            if Ping.is_found == 1:
                                print_result()
                        print()
                else:
                    print()
                    print_result()
                    print()

            elif value == 'txt':
                save_results_to_txt(results)
                print("\n已保存到 results.txt. Saved to results.txt.")


            elif value == 'csv':
                save_results_to_csv(results)
                print("\n已保存到 results.csv. Saved to results.csv.")

            elif Ping.is_found == 0:
                print(f'\t\n未找到. Nothing Found.\n')


    except KeyboardInterrupt:
        print(f'\n')
