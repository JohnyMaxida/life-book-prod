# TeslaGen lib modules WAY-MOD MODULE v1.7
import os, random, shutil, base64, json, requests
import time, re
from gradio_client import Client # AI_GEN2
from telegram.ext import ContextTypes
from fre0lib import SEX, SEFoB, Gechate
# from way_lib import GetUid, GetCid, replace_emojis, SEX, SEFoB, GetVAR, GetVar, SetVar
# from deep_translator import GoogleTranslator as Translator
# tra2ru = Translator(source='en', target='ru')
# tra2en = Translator(source='ru', target='en')
# from googletrans import Translator  
# from way_gen import *    
# КОНСТАНТЫ!!!!!!!!!!!!!!!!!!!!!!!!!
PIGEN = 'AI_GEN.png'
PIJEN = 'AI_GEN.jpg'
# CHAT_ID = None
WIC_RML = 1  # модель
WIC_ARM = not True # модель
WIC_AINUM = 3 # Предельное число моделей для бота
# {dirr}/{prom.split('.')[0]} _ {r(0, 100000)}.jpg


api_key = 'ABEF3E23DD3534E344A913A7B2A3E2E2'  # Замените на ваш ключ
sec_key = '6F50E3353C32988344A898B90693076E'  # Замените на ваш секретный ключ
base_url = "https://api-key.fusionbrain.ai/key/api/v1"
headers = {
        'X-Key': f'Key {api_key}',
        'X-Secret': f'Secret {sec_key}',
}


def fuse_get_pipeline_id(): 
    response = requests.get(f"{base_url}/pipelines", headers=headers)
    pipelines = response.json()
    if pipelines and len(pipelines) > 0:
        return pipelines[0]['id']
    else:
        print("Не удалось получить pipeline_id. Проверьте API ключи.")
        return None

        
def Gef_Aijpg(RML) -> bool:    
    return (RML==3) 

def Set_Aim(modex:int):
    global WIC_RML
    WIC_RML = modex    
    
def contains_digit(s: str) -> bool:
    return bool(re.search(r'\d', s))     
 
def TuneGenPath(user_id):
    global PIGEN, PIJEN
    # InitFreogen(user_id)
    # Upchate(user_id, context)
    print("TuneGenPath > ")
    user_path = './data-pigen/'
    os.makedirs(user_path, exist_ok=True)  # Создание папки, если она не существует
    pig1, pig2 = PIGEN.split('.')[0], PIGEN.split('.')[-1]
    pij1, pij2 = PIJEN.split('.')[0], PIJEN.split('.')[-1]
    if not contains_digit(PIGEN):
        PIGEN = os.path.join(user_path, f'{pig1}_{user_id}.{pig2}') 
        print(f" > PIGEN: {PIGEN}")
    if not contains_digit(PIJEN):
        PIJEN = os.path.join(user_path, f'{pij1}_{user_id}.{pij2}')  
        print(f" > PIJEN: {PIJEN}")

async def Make_Pic(promt: str, context: ContextTypes.DEFAULT_TYPE, MODEL:int=WIC_RML):
    CHAT_ID = Gechate(context)
    Temple_STX = 'CAACAgEAAxkBAAENBqlnHxhwdSSpMxllY5KZ_FqsCWla9QAC3AIAAhIG2EYCNm2_qSkoETYE'
    print(f"Рисоваю...{promt}...", end='', flush=True)
    print(f"WIC_RML={WIC_RML}")
    MSG = await context.bot.send_sticker(CHAT_ID, sticker=Temple_STX) 
    if MODEL == 0:
        for model in [3, 1, 2]:  # Порядок смены моделей: 2, 3, 1
            print(f"> Model={model}")
            pigen = await try_gen_pic(promt, model, MSG, CHAT_ID, context)
            if pigen:
                return pigen
            await SEX(f'Ошибка малявации (модель {model}), попробую другую...', context)
        await SEX('Ошибка малявации, все модели затупили 🥺', context)
    else:
        pigen = await try_gen_pic(promt, MODEL, MSG, CHAT_ID, context)
        if pigen:
            return pigen
        await SEX('Ошибка малявации 🥺 сбой генератора', context)
            
    
async def try_gen_pic(promt: str, model: int, msg, chat_id, context: ContextTypes.DEFAULT_TYPE):
    pigen, status = await Gen_Pic(promt, model, context)
    if pigen:
        try:  # Удаляем сообщение пользователя
            await context.bot.delete_message(chat_id, message_id=msg.message_id)
        except Exception as e:
            print(f"Make_Pic: Ошибка удаления сообщения: {e}")
        return await Print_Pic(promt, model, context)
    return None  
 

async def Gen_Pic(promt: str, numod:int, context: ContextTypes.DEFAULT_TYPE): 
    if promt is None:
        promt = 'pink cat'    
        print("No Prompt, set def > ", promt)
    return await Get_Aimfunc(numod, promt)  # def

async def Get_Aimfunc(num: int, promt: str):
    aimfunc_name = f'AI_GEN{num}'    
    aimfunc = globals().get(aimfunc_name)    
    if aimfunc and callable(aimfunc):
        return aimfunc(promt)  # Предполагаем, что функции AI_GEN принимают 
    else:
        print(f"Ошибка: Функция {aimfunc_name} не найдена или не является вызываемым объектом.")
        raise ValueError(f"Ошибка: функция {aimfunc_name} не найдена.")  # Генерируем исключение


async def Print_Pic(promt:str, numod:int, context: ContextTypes.DEFAULT_TYPE):
    CHAT_ID = Gechate(context)
    PIC = PIJEN if Gef_Aijpg(numod) else PIGEN
    print("Print_Pic: ", PIC)    
    if os.path.exists(PIC):
        text = f'Вот картинка: {promt}'
        await SEFoB(CHAT_ID, PIC, text, context) 
        return True    
    else:
        await SEX('Сбой файла картинки', context)
        return False 

   
def Get_AI_style(Flang:bool=False):
    STYLE_RU = ["Абстрактный", "Винтажный", "Минимализм", "Природа", "Киберпанк", "Ретро", "Графический", "Мультфильм", "Морской", "Готический"]
    STYLE_EN = ["Abstract", "Vintage", "Minimalism", "Nature", "Cyber", "Retro", "Graphic", "Cartoon", "Marine", "Gothic"]
    BACKGROUND = ["cosmic", "simple", "classroom", "jungle", "forest", "space", "city", "lake", "ocean", "beach", "ship", "gradient", "office", "factory", "roman city", "medieval village", "fantasy city", "cyberpunk city", "war", "fire", "kitchen", "bathroom", "bedroom", "dungeon", "prison", "valley", "field of flowers", "field of wheat", "Alphonse Mucha", "swimming pool", "mountain", "desert", "vatican city", "jewish temple", "colosseum", "space station", "lunar base", "cave", "slums", "sunset", "infernal palace", "frozen lakeside", "winter", "bouncy castle", "chicken coop", "hen house", "autumn", "fall", "summer", "spring", "airport", "barn", "farm", "library", "haunted library", "camp", "capitol building", "corn maze", "night sky", "moon", "gothic", "alleyway", "court", "ramen shop", "pagoda", "wrestling ring", "mushroom forest"]
    # STYLE = random.choice(STYLE_RU) if Flang else random.choice(STYLE_EN)
    STYLE = random.choice(BACKGROUND)
    print(f"Get_AI_style > Получен стайл {STYLE}")  
    return STYLE
    

def AI_GEN1(prompt: str):    # 5. Pollinations AI API 
    print("A1_GEN1 > ", end='', flush=True)
    picture = PIGEN
    ok = "OK"
    url = f"https://image.pollinations.ai/prompt/{prompt}?width=512&height=512"
    try:
        r = requests.get(url)
        if r:
            with open(picture, 'wb') as f:
                f.write(r.content)
            print(f"Успешно.{picture}...", flush=True)
            return True, ok  # Возвращаем True при успешной операции
        else:
            ok = "Ошибка - нет картинки" 
            print(ok)
    except requests.exceptions.RequestException as e:
        ok = f"Ошибка API запроса: {e}" 
        print(ok)
    except Exception as e:
        ok = f"Ошибка операции: {e}" 
        print(ok)
    return False, ok
    
def AI_GEN2(prompt: str):
    print("AI2_GEN2 > ", end='', flush=True)
    picture = PIGEN
    ok = "OK"
    lurl = "lalashechka/FLUX_1"
    task = "FLUX.1 [schnell]" 
    # task = "FLUX.1 [dev]" 
    api_name = "/flip_text"
    try:
        client = Client(lurl)
        result = client.predict(
            prompt=prompt,    
            task=task,
            api_name=api_name
        )
        # Если result является строкой, предполагаем, что это путь к файлу
        print(f"Пришел резалт: {result}...", flush=True)
        if isinstance(result, dict):
            image_path = result[path]  # Локальный путь к изображению
        else:
            image_path = result
        # Проверяем, существует ли файл по указанному пути
        if os.path.isfile(image_path):
            # Копируем изображение в новое место
            shutil.copy(image_path, picture)
            print(f"Успешно: {picture}...")
            return True, ok  # Возвращаем True при успешной операции
        else:
            ok = f"Ошибка - файл не найден по пути: {image_path}" 
            print(ok)
            # return False, ok
        # else:
            # ok = "Ошибка - результат не словарь." 
            # print(ok)
            # return False, ok
    except Exception as e:
        ok = f"Ошибка операции: {e}" 
        print(ok)
    return False, ok 
    
    
def AI_GEN3(prompt: str):
    """Generate an image from a text prompt using the FusionBrain API."""
    print("AI_GEN3 > Request to pipeline", flush=True)
    picture = PIJEN    
    params = {
        "type": "GENERATE",
        "numImages": 1,
        "width": 1024,
        "height": 1024,
        "generateParams": {"query": prompt}
    }
    try:
        pipeline_id = fuse_get_pipeline_id()
        files = {
            'params': (None, json.dumps(params), 'application/json'),
            'pipeline_id': (None, str(pipeline_id))
        }    
        response = requests.post(f"{base_url}/pipeline/run", files=files, headers=headers)
        uuid = response.json()['uuid']

        while True:
            status_response = requests.get(f"{base_url}/pipeline/status/{uuid}", headers=headers)
            status_data = status_response.json()
            if status_data['status'] == 'DONE':
                image_data = base64.b64decode(status_data['result']['files'][0])
                with open(picture, 'wb') as f:
                    f.write(image_data)
                print(f"AI_GEN3 > OK: сохранено как {picture}")
                return True, "OK"
            time.sleep(3)            

    except Exception as e:
        print(f"AI_GEN3 > Error: {str(e)}")
        return False, f"Error: {str(e)}" 



    
    
    
# def AI_GEN3(prompt: str):  # 5. Kandinsky AI API
    # print("AI3_GEN3 > ", end='', flush=True)
    # picture = PIJEN
    # status = "OK"    
    # Актуальный URL (проверено по ссылке из веб-поиска) [[3]]
    # url = 'https://api.fusionbrain.ai'
    # api_key = ''  # Замените на ваш ключ
    # sec_key = ''  # Замените на ваш секретный ключ
    # try:
        # api = Text2ImageAPI(url, api_key, sec_key)
        # model_id = api.get_model()
        # uuid = api.generate(prompt, model_id)
        # images = api.check_generation(uuid)
        # image_base64 = images[0]
        # image_data = base64.b64decode(image_base64)
        # with open(picture, 'wb') as f:
            # f.write(image_data)
        # return True, status
    # except Exception as e:
        # status = f"Ошибка операции: {e}"
    # print(status)
    # return False, status      
    
    
# def AI_GEN3(prompt: str):    # 5. Kandinsky AI API 
    # print("AI3_GEN3 > ", end='', flush=True)
    # picture = PIJEN 
    # status = "OK"
    # url = 'https://api-key.fusionbrain.ai/'
    # api_key = ''
    # sec_key = ''
    # try:
        # api = Text2ImageAPI(url, api_key, sec_key)
        # model_id = api.get_model()
        # uuid = api.generate(prompt, model_id)
        # images = api.check_generation(uuid)
        # print(f"Сгенерированное изображение: {images}")
        # image_base64 = images[0]
        # Декодируем строку base64 в бинарные данные
        # image_data = base64.b64decode(image_base64)
        # with open(picture, 'wb') as f:
            # f.write(image_data)
        # return True, status
    # except Exception as e:
        # status = f"Ошибка операции: {e}"   
    # print(status)    
    # return False, status
  
  
  


# def Show_Pic():
    # if os.path.exists(PIGEN):
        # print("Картинка: ", PIGEN)
        # os.system (f"start {PIGEN}")
        # return TEX('wic_ai_ok') # "Картинка Вам как ПОДСКАЗКА"
    # else:
        # return "Картинки нету! Ошибка сохранения файла"


  
  
  
# from gradio_client import Client

# client = Client("lalashechka/FLUX_1")
# result = client.predict(
		# prompt="Hello!!",
		# task="FLUX.1 [schnell]",
		# api_name="/flip_text"
# )
# print(result)
# Accepts 2 parameters:
# prompt str Required

# The input value that is provided in the "Описание изображения:" Textbox component.

# task Literal['FLUX.1 [schnell]', 'FLUX.1 [dev]'] Default: "FLUX.1 [schnell]"

# The input value that is provided in the "Версия нейросети:" Radio component.

# Returns 1 element
# Dict(path: str | None (Path to a local file), url: str | None (Publicly available url or base64 encoded image), size: int | None (Size of image in bytes), orig_name: str | None (Original filename), mime_type: str | None (mime type of image), is_stream: bool (Can always be set to False), meta: Dict())  
    # path
    # url
    # size
    # orig_name
    
    
   
    