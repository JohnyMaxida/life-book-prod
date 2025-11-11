# Freon Lib 1.2
import asyncio
import os, io, re
from pydub import AudioSegment
import speech_recognition as sr
import subprocess
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ContextTypes
# , , InputTextMessageContent, InlineQueryResultArticle
import mistune
import pdfplumber
import html
markdown = mistune.create_markdown()
DEVELOPERS = {"Джон Тесла": 1087968824, "Джон Максида": 6794691889, "Алиса Тесла": 7442136328}
LANG_CODE = "ru-RU" # для распознавателя голоса 6794691889
CHAT_ID = None
# sirius_n='https://t.me/siriusdetindigo'
# sirius_c='-1002261936806'
    
    
    
class MarkdownFormatter:
    """Класс для форматирования текста в Markdown V2."""
    
    SPECIAL_CHARS = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    
    @staticmethod
    def escape_markdown(text: str) -> str:
        """Экранирование специальных символов."""
        for char in MarkdownFormatter.SPECIAL_CHARS:
            text = text.replace(char, f'\\{char}')
        return text
    
    @staticmethod
    def format_code_block(lang: str, code: str) -> str:
        """Форматирование блока кода."""
        escaped_code = code.replace('`', '\\`')
        return f"```{lang}\n{escaped_code}\n```"
    
    @staticmethod
    def format_text(text: str) -> str:
        """Форматирование обычного текста с поддержкой разметки."""
        # Обработка жирного текста и курсива
        text = re.sub(r'\*\*(.+?)\*\*', lambda m: f"*{m.group(1)}*", text)
        text = re.sub(r'\*(.+?)\*', lambda m: f"_{m.group(1)}_", text)
        
        # Экранирование остальных специальных символов
        for char in ['[', ']', '~', '>', '#',  '|', '{', '}']:
            text = text.replace(char, f'\\{char}')
        return text

class MessageFormatter:
    """Класс для форматирования сообщений."""
    
    @staticmethod
    def format_response(text: str) -> str:
        """Форматирование ответа с поддержкой кода и Markdown."""
        parts = re.split(r'(```[\w]*\n.*?```)', text, flags=re.DOTALL)
        formatted_parts = []
        
        for part in parts:
            if not part.strip():
                continue
                
            if part.startswith('```') and part.endswith('```'):
                match = re.match(r'```(\w*)\n(.*?)```', part, re.DOTALL)
                if match:
                    lang, code = match.groups()
                    formatted_parts.append(MarkdownFormatter.format_code_block(lang, code))
            else:
                formatted_parts.append(MarkdownFormatter.format_text(part))
        
        return ''.join(formatted_parts)    
    

    
def Pic_Find(promt:str, KEYDRAW): 
    promts = promt.lower().split()
    new_prom = []
    EQ_DRAW = False
    for word in promts:
        flag = True
        for sord in KEYDRAW:
            if sord in word:
                EQ_DRAW = True
                flag = False
        if flag:
            new_prom.append(word)
    if EQ_DRAW:
        return new_prom
    else:
        return None  

    


# import requests
# from bs4 import BeautifulSoup

def parse_website(urls):
    documents = []
    
    # Проверяем, является ли входной аргумент строкой или списком
    if isinstance(urls, str):
        urls = [urls]  # Преобразуем строку в список
    
    for url in urls:
        try:
            # Отправляем GET-запрос к сайту
            response = requests.get(url)
            # Проверяем статус ответа (выбросит исключение для 4xx/5xx кодов)
            response.raise_for_status()
            # Создаем объект BeautifulSoup для парсинга HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            # Ищем все текстовые блоки в тегах <p>
            text_blocks = soup.find_all('p')
            # Собираем непустые текстовые блоки
            document = ' '.join(
                block.get_text(strip=True)
                for block in text_blocks
                if block.get_text(strip=True)
            )
            documents.append(document)
        except requests.exceptions.RequestException as e:
            # Обработка ошибок сети/HTTP
            print(f"Ошибка запроса для {url}: {str(e)}")
        except Exception as e:
            # Общая обработка других исключений
            print(f"Неожиданная ошибка для {url}: {str(e)}")
    
    return documents

def Parse_Linx(text:str):
    print(f"Parse_Linx : Website")
    linx = contains_links(text)
    if linx:
        for link in linx:
            print(f"Link: {link}")            
        return linx[0] 
    else:
        return None
    
def Parse_TeLinx(text:str):
    print("Parse_Linx: Telegram")
    tlinx = contains_telegram_links(text)
    if tlinx:
        for chat_id, message_id in tlinx:
            print(f"Chat ID: {chat_id}, Message ID: {message_id}")            
        return tlinx[0]
    else:
        return None
  
  
      
def Parse_website_old(url):
    # Отправляем GET-запрос к сайту
    response = requests.get(url)
    # Проверяем, успешен ли запрос
    if response.status_code == 200:
        # Создаем объект BeautifulSoup для парсинга HTML
        soup = BeautifulSoup(response.text, 'html.parser')        
        # Ищем все текстовые блоки (например, в тегах <p>)
        text_blocks = soup.find_all('p')        
        # Формируем список документов
        documents_v2 = []
        for block in text_blocks:
            documents_v2.append(block.get_text(strip=True))
            # {
                # "data": {
                    # "text": block.get_text(strip=True)
                # }
            # })        
        return documents_v2
    else:
        print(f"Ошибка при запросе: {response.status_code}")
        return []   
  
  
  
    
def contains_telegram_links(text):
    pattern = r"(?:https?://)?t\.me/(?:c/(-?\d+)|([\w_]+))/(\d+)"
    matches = re.findall(pattern, text)
    links_data = []
    for match in matches:
        if match[0]:  # Ссылка с ID чата
            chat_id = f"-100{match[0]}"
        elif match[1]:  # Ссылка с username
            chat_id = match[1]
        else:
            continue
        message_id = int(match[2])
        if has_non_digit(chat_id):
            chat_id = '@' + chat_id
        links_data.append((chat_id, message_id))
    if not links_data:
        print("Не удалось найти подходящие ссылки в тексте.")
    return links_data
    
def has_non_digit(s):
    return any(not char.isdigit() for char in s)
    
def contains_links(text):
    # Регулярное выражение для поиска ссылок
    url_pattern = r'https?://[^\s]+'    
    # Поиск всех ссылок в тексте
    links = re.findall(url_pattern, text)    
    return links    
    
def extract_text_from_pdf(file_path):
    try:
        with pdfplumber.open(file_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() + "\n"
            return text.strip() if text else None
    except Exception as e:
        print(f"Ошибка при извлечении текста из PDF: {e}")
        return None  
   
def Find_User_Name(uid):
    if not isinstance(uid, int):
        uid = int(uid)
    for name, u_id in DEVELOPERS.items():
        if uid == u_id:
            return name
    return None  # Return None if user ID is not found in the dictionary
   
async def ALLOWED(context: ContextTypes.DEFAULT_TYPE):
    user_id = GetVar('user_id', context)
    print (f"ALLOWED > user_id = {user_id}")
    # update.effective_user.id
    # SetVar('user_id',USER_ID, context)
    dev_name = Find_User_Name(user_id)
    if dev_name:
        print (f">{dev_name} > ДОСТУП ОДОБРЕН")
        return True  
    else:       
        await SEX("❌ У Вас нет прав 🙅🏼 Модератора 🦹🏼 для этой команды", context)
        return False 
   
# def Upmodel(mod_id, context: ContextTypes.DEFAULT_TYPE):
    # global CHAT_ID
    # CHAT_ID = user_id
    # SetVar('last_mod', mod_id, context)    
     

def Upchate(user_id, context: ContextTypes.DEFAULT_TYPE):
    global CHAT_ID
    CHAT_ID = user_id
    SetVar('last_chat', user_id, context)

# def Gemodel(context: ContextTypes.DEFAULT_TYPE):
    # return CHAT_ID
    # return GetVar('last_mod', context) 

    
def Gechate(context: ContextTypes.DEFAULT_TYPE):
    chid = GetVar('last_chat', context)
    # CHAT_ID = chid if chid else CHAT_ID
    return chid if chid else CHAT_ID
    # return GetVar('last_chat', context)        

def ASPLIT(text, max_length=4096):
    chunks = []
    while len(text) > max_length:
        # Try to split at newline or space
        split_index = text.rfind('\n', 0, max_length)
        if split_index == -1:
            split_index = text.rfind(' ', 0, max_length)        
        if split_index == -1:
            split_index = max_length        
        chunks.append(text[:split_index])
        text = text[split_index:].lstrip()    
    if text:
        chunks.append(text)    
    return chunks    
    
    
async def ASPLITTER(response:str, context: ContextTypes.DEFAULT_TYPE):
    parts = response.split('```')    
    for index, part in enumerate(parts):
        part = part.strip()        
        if index % 2 == 1:  # Code block
            code_chunks = ASPLIT(f"```{part}```")
            for chunk in code_chunks:
                print ('> ЧАНКИ КОДА: =====')
                await ZEX(chunk, context)
                await asyncio.sleep(2)
        else:  # Regular text
            text_chunks = ASPLIT(part)
            for chunk in text_chunks:
                print ('> ЧАНКИ ТЕКСТА: =====')
                # if is_mark2(chunk):
                    # print ("Найден МД2 - pass")
                    ## formad = MarkdownFormatter.format_text(chunk)
                    # formad = ESUm2(chunk)                    
                    # await ZEY(formad, context)
                # el
                # if is_markdown_format(chunk):
                    # print ("Найден МД (1 или 2)")                    
                print ("force format_to_md...") 
                formad = format_to_md(chunk)
                await ZEX(formad, context)
                # else:                     
                    # formad = clearq(chunk) 
                    # await ZEX(chunk, context)
                await asyncio.sleep(2)

def clearq(text):
    return text.replace('&quot;','"')

def TuneOGGpath(user_name):
    k = 1  # Локальная переменная для счётчика файлов
    user_path = os.path.join(os.getcwd(), 'data-ogg')  # Директория для хранения файлов
        # user_path = './data-ogg/'  # Директория для хранения файлов
    os.makedirs(user_path, exist_ok=True)  # Создание папки, если она не существует
    while True:
        file_name = f"{user_name}_{k}.ogg"  # Формирование имени файла
        full_path = os.path.join(user_path, file_name)  # Полный путь к файлу
        if not os.path.isfile(full_path):  # Проверка, существует ли файл
            return full_path  # Возвращаем путь, если файл не существует
        k += 1  # Увеличиваем счётчик, если файл существует

async def Transcribe_audio(user_name: str, file_id: str, context) -> str:
    # Создание пути для сохранения OGG-файла
    # user_path = './data-ogg/'
    # os.makedirs(user_path, exist_ok=True)  # Создание папки, если она не существует
    # file_name = f"{user_name}_TEMP.ogg"
    # ogg_file_path = os.path.join(user_path, file_name)
    # wav_file_path = ogg_file_path.replace(".ogg", ".wav")
    ogg_file_path = TuneOGGpath(user_name)
    print("OGGPath > ", ogg_file_path)
    # print("WavPath > ", wav_file_path)
    # Скачивание файла
    try:
        file = await context.bot.get_file(file_id)
        await file.download_to_drive(ogg_file_path)
    except Exception as e:
        return f"err: Ошибка при скачивании аудио: {e}"
# Конвертация OGG в WAV с помощью FFmpeg
    # try:
        # subprocess.run(
            # ["ffmpeg", "-i", ogg_file_path, wav_file_path],
            # check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        # )
    # except subprocess.CalledProcessError as e:
        # return f"err: Ошибка при конвертации OGG в WAV: {e.stderr.decode()}"
    # Распознавание текста из WAV
    # try:
        # recognizer = sr.Recognizer()
        # with sr.AudioFile(wav_file_path) as source:    
# Чтение и конвертация файла
    try:    
        with open(ogg_file_path, 'rb') as f:
            voice_data = io.BytesIO(f.read())        
        audio = AudioSegment.from_ogg(voice_data)
        audio_data = io.BytesIO()
        audio.export(audio_data, format="wav")
        audio_data.seek(0)
    except Exception as e:
        return f"err: Ошибка при конвертации аудио: {e}"
    with sr.AudioFile(audio_data) as source:
        recognizer = sr.Recognizer()
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language=LANG_CODE)
            return text
        except sr.UnknownValueError:
            return(f"err: Неизвестная ошибка распознавателя Google Speech Recognition")
        except sr.RequestError as e:
            return(f"err: Ошибка распознавателя Google Speech Recognition: {e}")    
        finally:
            # Удаление временных файлов
            if os.path.exists(ogg_file_path):
                os.remove(ogg_file_path)
            # if os.path.exists(wav_file_path):
                # os.remove(wav_file_path)

# Markdown and Text Formatting Utilities
# def Ma2Htm(text): 
    # text = "# Заголовок\n\nЭто **жирный текст**."
    # html = markdown(text)
    # print(html)
    # return html
    
# def formakdown(text):    
    # text = text.replace('**', '*') # Replace ** with * for bold
    # return text


def is_mark2(text):
    return bool('**' in text)


def is_markdown_format(text):
    patterns = [        
        r'\*[^*\n]+\*',      # Проверка *одинарными* звездочками
        r'\*\*[^*\n]+\*\*',  # Проверка **Дабл** звездочками
        # Проверка заголовков
        r'^\*[^*\n]+\*$',  # Заголовок 1 уровня
        r'^`[^`\n]+`$',    # Заголовок 2 уровня
        r'^_[^_\n]+_$',    # Заголовок 3 уровня
        r'^# ',              # Заголовок с #
        r'^## ',             # Заголовок с ##
        r'^### ',            # Заголовок с ###
        # Проверка списков
        r'^\• .+'
    ]    
    # Проверяем наличие хотя бы одного из паттернов
    has_markdown_elements = False
    for pattern in patterns:
        if re.search(pattern, text, re.MULTILINE):
            has_markdown_elements = True
            break    
    return has_markdown_elements


# def format_for_telegram(text):
    # return text.strip()

    
# В прошлом запросе я использовал значение `max_tokens` равное 1024\.
def ESUm1(text): # Debug special characters '_', '*','`',
    # print ('ESUm1 вход: ', text, end='') 
    if text.startswith('```'):
        print (' обнаружен Код!', text)
        return text    
    text = text.replace('&amp;quot;','*')        
    special_chars = ['_', '*', '`']
    for char in special_chars:
        count = text.count(char)
        if count>0 and (count % 2 != 0):
            text += char 
    return text
    # print (' выход: ', text)            
    
    
    
    
    
    
    
def ESUm2(text): # Escape special characters EX: '_', '*','`',
    print ('ESUm2 вход: ', text)
    escape_chars = ['[', ']', '(', ')', '~', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    text = str(text)
    for char in escape_chars:
        text = text.replace(char, '\\' + char)   
    print ('ESUm2 выход: ', text)
    return text    
    
    


def format_to_md(input_text):
    # Декодируем HTML-сущности в обычный текст
    decoded_text = html.unescape(input_text)
    
    # Заменяем двойные звездочки на временный символ
    formatted_text = decoded_text.replace('**', '~~')
    
    # Разбиваем текст на строки
    lines = formatted_text.split('\n')    
    
    # Форматируем каждую строку
    formatted_lines = []
    for line in lines:
        # Если строка начинается с одиночной звездочки, преобразуем её в пункт
        if line.lstrip().startswith('*') and not line.lstrip().endswith('*'):
            indent = '    ' * (len(line) - len(line.lstrip()))  # Определяем отступ
            content = line.lstrip()[1:].strip()  # Убираем звездочку и пробелы
            formatted_lines.append(f"{indent}- {content}")
        else:
            formatted_lines.append(line) 
    # Соединяем строки обратно
    formatted_text = '\n'.join(formatted_lines) 
    # Заменяем звездочки на курсивный символ
    formatted_text = formatted_text.replace('*', '_') 
    # Восстанавливаем жирный стиль
    formatted_text = formatted_text.replace('~~', '*') 
    return formatted_text 
    

    
def GetVar(variable:str, context: ContextTypes.DEFAULT_TYPE):   
    return context.user_data.get(variable)
    
def GetVAR(variable:str, defvalue, context: ContextTypes.DEFAULT_TYPE): 
    return context.user_data.get(variable, defvalue)
    
def SetVar(variable:str, value, context: ContextTypes.DEFAULT_TYPE):  
    context.user_data[variable] = value
    
def replace_emojis(text, new_emoji):
    # Замена смайлов на новый смайл, используя генератор списка
    replaced_text = ''.join([new_emoji if emoji.is_emoji(char) else char for char in text])
    return replaced_text  



async def UMR(text:str, update: Update):
    return await update.message.reply_text(text)     
    
async def ZEX(text: str, context: ContextTypes.DEFAULT_TYPE, chat_id: int = None, reply_markup = None): 
    print ('ZEX до: ', text)
    text = ESUm1(text)
    print ('ZEX ESUm1: ', text)
    try: # 
        res = await SEX(text, context, chat_id=chat_id, parse_mode='Markdown', reply_markup=reply_markup)
    except Exception as e:
        print(f"ZEX: Ошибка формата: {e}")     
        error = "Ошибка формата X-Markdown"
        # res = await SEX(error, context, chat_id=chat_id)        
        res = await SEX(text, context, chat_id=chat_id, parse_mode=None, reply_markup=reply_markup)    
    await asyncio.sleep(1)
    return res     
    
async def ZEY(text: str, context: ContextTypes.DEFAULT_TYPE, chat_id: int = None, reply_markup = None): 
    print ('ZEY до: ', text)
    # text = ESUm2(text)
    # print ('ZEY ESUm1: ', text)
    try: # 
        res = await SEX(text, context, chat_id=chat_id, parse_mode='MarkdownV2', reply_markup=reply_markup)
    except Exception as e:
        print(f"ZEY: Ошибка формата: {e}")     
        error = "Ошибка формата Y, будет выдан неформат"
        return None
        # await SEX(error, context, chat_id=chat_id)
        # res  = await SEX(text, context, chat_id=chat_id, parse_mode=None, reply_markup=reply_markup)    
    return res        

async def SEX(text: str, context: ContextTypes.DEFAULT_TYPE, chat_id: int = None, parse_mode = None, reply_markup = None):
    text = clearq(text)
    if chat_id is None:
        chat_id = Gechate(context)
    params = {      # params["chat_id"] = chat_id
        "text": text,
        "chat_id": chat_id, }
    if reply_markup is not None:
        params["reply_markup"] = reply_markup    
    if parse_mode is not None:
        params["parse_mode"] = parse_mode  
    print ('SEX: ', text)    
    return await context.bot.send_message(**params) 
    

async def SEFoB(chat_id, picfile, cap_text:str, context: ContextTypes.DEFAULT_TYPE):  
    cap_text = ESUm1(cap_text)  
    print ('SEFoB отладка: ', cap_text)    
    if os.path.isfile(picfile):  # , parse_mode='Markdown'
        print ("SEFoB: Photo found, sending photo block")
        with open(picfile, 'rb') as photo:
            await context.bot.send_photo(chat_id=chat_id, photo=photo, caption=cap_text, parse_mode='Markdown') 
    else:
        print ("SEFoB: Photo not found, sending text")
        await context.bot.send_message(chat_id=chat_id, text=cap_text, parse_mode='Markdown') 


  
    
    
 
    


# Получаем значения переменных окружения
# M_LAMA_b = os.getenv('M_LAMA_b', 'НЕТ')
# M_GEMA_2b = os.getenv('M_GEMA_2b', 'НЕТ')
# M_QUIN_b5 = os.getenv('M_QUIN_b5', 'НЕТ')
# M_QUIN_3b = os.getenv('M_QUIN_3b', 'НЕТ')
# M_DSC2I_16b = os.getenv('M_DSC2I_16b', 'НЕТ')
# M_AYA_8b = os.getenv('M_AYA_8b', 'НЕТ')
# M_SCI_3b = os.getenv('M_SCI_3b', 'НЕТ')
# MODELS = [M_QUIN_b5, M_LAMA_b, M_GEMA_2b, M_QUIN_3b, M_SCI_3b, M_AYA_8b, M_DSC2I_16b]   

# """
# async def ai_process(context, query):    
    # paging = 4096
    # yot = '<|eot_id|>'
    # accumulated_text = ""    
    # Начальный запрос к модели    
    # response = ai_query(query)
    # if not response:
        # await SEX("УПС, не смог получить ответ от модели...", context)
        # return    
    # Проверка на наличие необходимости продолжения ответа
    # while not response.endswith(yot):  # Замените на ваш токен конца
        # additional_response = ai_query(query)
        # response += additional_response
    # Разделяем текст на части по коду
    # parts = response.split('```')  # Используем тройные кавычки как разделитель
    # for index, part in enumerate(parts):
        # part = part.strip()  # Убираем лишние пробелы 
        # Если это код и мы не на первой итерации, отправляем предыдущий текст
        # if index % 2 == 1:  # Код находится на нечетных индексах
            # if accumulated_text:
                # await SEX(cleb(accumulated_text), context)
                # accumulated_text = ""
            # Отправляем код в отдельном блоке
            # await ZEX(f"```{cleb(part)}```", context)
        # else:
            # accumulated_text += part + "\n"  # Накопление обычного текста
        # Проверяем, если накопленный текст превышает 4096 символов
        # while len(accumulated_text) > paging:
            # await SEX(cleb(accumulated_text[:paging]), context)
            # accumulated_text = accumulated_text[paging:]
    # Отправляем оставшийся текст, если он есть
    # if accumulated_text:
        # await SEX(cleb(accumulated_text), context)
    # return accumulated_text
# """        