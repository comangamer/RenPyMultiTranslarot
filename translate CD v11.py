# MIT License
# 
# Copyright (c) 2024 Mikhail Ivanov
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import time
from datetime import datetime
from googletrans import Translator
import re

def translate_text(text, target_language, translator):
    """Безопасный перевод с обработкой ошибок"""
    try:
        translation = translator.translate(text, dest=target_language)
        return translation.text
    except Exception as e:
        print(f"Ошибка перевода: {e}")
        return text

def process_translation(input_file_name, output_file_name, target_language='french', replace_translate=False):
    start_time = time.time()
    
    if not os.path.exists(input_file_name):
        print(f"Файл {input_file_name} не найден!")
        return 0, 0, 0

    with open(input_file_name, 'r', encoding='utf-8') as input_file:
        lines = input_file.readlines()

    total_lines = len(lines)
    translated_count = 0
    total_source_chars = 0
    total_translation_chars = 0
    translator = Translator()

    with open(output_file_name, 'w', encoding='utf-8') as output_file:
        for line in lines:
            # Обработка строк с "translate english"
            if replace_translate and 'translate english' in line:
                line = line.replace('translate english', f'translate {target_language}')

            # Обработка строк old и new
            old_match = re.match(r'^(\s*)old\s*(".*")', line)
            new_match = re.match(r'^(\s*)new\s*(".*")', line)
            
            # Обработка реплик персонажей
            character_line_match = re.match(r'^(\s*)(\w+)\s*(".*")', line)
            
            # Пропускаем замену текста в квадратных скобках (переменные)
            if re.search(r'\[.*?\]', line):
                output_file.write(line)
                continue

            if old_match:
                # Строки old остаются без изменений
                output_file.write(line)
            elif new_match:
                indent = new_match.group(1)
                new_text = new_match.group(2)
                
                # Проверяем, есть ли русский текст
                if not re.search(r'[а-яА-Я]', new_text):
                    # Переводим
                    translated_text = translate_text(new_text.strip('"'), target_language, translator)
                    
                    # Подсчет символов
                    total_source_chars += len(new_text.strip('"'))
                    total_translation_chars += len(translated_text)
                    
                    # Комментируем оригинальную строку new
                    output_file.write(f'{indent}# {line.strip()}\n')
                    
                    # Добавляем перевод с сохранением отступов и ключевого слова new
                    output_file.write(f'{indent}new "{translated_text}"\n')
                    
                    translated_count += 1
                    print(f"Перевел new: {new_text} -> {translated_text}")
                else:
                    # Если текст содержит русские символы, оставляем как есть
                    output_file.write(line)
            elif character_line_match:
                indent = character_line_match.group(1)
                character = character_line_match.group(2)
                text = character_line_match.group(3)
                
                # Проверяем, есть ли русский текст
                if not re.search(r'[а-яА-Я]', text):
                    # Переводим
                    translated_text = translate_text(text.strip('"'), target_language, translator)
                    
                    # Подсчет символов
                    total_source_chars += len(text.strip('"'))
                    total_translation_chars += len(translated_text)
                    
                    # Комментируем оригинальную строку
                    output_file.write(f'{indent}# {character} {text.strip()}\n')
                    
                    # Добавляем перевод с сохранением отступов и имени персонажа
                    output_file.write(f'{indent}{character} "{translated_text}"\n')
                    
                    translated_count += 1
                    print(f"Перевел реплику {character}: {text} -> {translated_text}")
                else:
                    # Если текст содержит русские символы, оставляем как есть
                    output_file.write(line)
            else:
                # Стандартная обработка других строк
                match = re.search(r'^(\s*).*?"([^"]+)"', line)
                if match and not re.search(r'[а-яА-Я]', match.group(2)):
                    # Захватываем отступы
                    indent = match.group(1)
                    english_text = match.group(2)
                    
                    # Перевод
                    translated_text = translate_text(english_text, target_language, translator)
                    
                    # Подсчет символов
                    total_source_chars += len(english_text)
                    total_translation_chars += len(translated_text)
                    
                    # Комментируем оригинальную строку
                    output_file.write(f'{indent}# {line.strip()}\n')
                    
                    # Добавляем перевод с сохранением отступов
                    output_file.write(f'{indent}"{translated_text}"\n')
                    
                    translated_count += 1
                    print(f"Перевел: {english_text} -> {translated_text}")
                else:
                    # Если строка не подлежит переводу, пишем как есть
                    output_file.write(line)

    total_time = time.time() - start_time
    print(f"\nПеревод завершен за {total_time:.2f} секунд")
    print(f"Переведено строк: {translated_count}")
    print(f"Символов в исходных текстах: {total_source_chars}")
    print(f"Символов в переведенных текстах: {total_translation_chars}")

    return translated_count, total_source_chars, total_translation_chars

def translate_all_rpy_files(target_language, replace_translate):
    """Перевод всех .rpy файлов в текущей директории с сохранением в папку перевода"""
    output_directory = target_language
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    input_files = [f for f in os.listdir('.') if f.endswith('.rpy')]
    total_translated_lines = 0
    total_source_chars = 0
    total_translation_chars = 0

    for input_file_name in input_files:
        output_file_name = os.path.join(output_directory, input_file_name)
        
        print(f"\n🌍 Перевод файла: {input_file_name}")
        translated_count, source_chars, translation_chars = process_translation(input_file_name, output_file_name, target_language, replace_translate)
        
        total_translated_lines += translated_count
        total_source_chars += source_chars
        total_translation_chars += translation_chars

    print(f"\n✨ Массовый перевод завершен.")
    print(f"Всего переведено строк: {total_translated_lines}")
    print(f"Суммарное количество символов в исходных файлах: {total_source_chars}")
    print(f"Суммарное количество символов в переведенных файлах: {total_translation_chars}")

    return total_translated_lines, total_source_chars, total_translation_chars

def main():
    print("🌍 Универсальный скрипт перевода текстовых файлов 🌐")
    
    languages = {
        '1': 'arabic',
        '2': 'zh-CN',
        '3': 'dutch',
        '4': 'finnish',
        '5': 'french',
        '6': 'german',
        '7': 'hindi',
        '8': 'italian',
        '9': 'japanese',
        '10': 'korean',
        '11': 'norwegian',
        '12': 'portuguese', 
        '13': 'spanish',
        '14': 'swedish',
        '15': 'turkish',
        '16': 'ukrainian'
    }
    
    print("\nВыберите целевой язык:")
    for key, lang in languages.items():
        print(f"{key}. {lang}")
    
    lang_choice = input("Введите номер языка: ")
    target_language = languages.get(lang_choice, 'french')
    
    replace_translate = input("Заменять 'translate english' на название языка перевода? (y/n): ").lower() == 'y'
    
    translation_mode = input("\nВыберите режим перевода:\n1. Перевод одного файла\n2. Перевод всех .rpy файлов\nВведите номер: ")
    
    if translation_mode == '2':
        translate_all_rpy_files(target_language, replace_translate)
    else:
        input_file_name = input("Введите имя входного файла (например, script.rpy): ")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file_name = f"translated_{target_language}_{timestamp}.rpy"
        
        process_translation(input_file_name, output_file_name, target_language, replace_translate)

if __name__ == "__main__":
    main()
