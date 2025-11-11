import os, requests, json
from telegram import Update
from telegram.ext import ContextTypes

from passive import Adelay
from fre0lib import ASPLITTER, Parse_TeLinx, Parse_Linx, Pic_Find, Gechate, format_to_md, SEX, parse_website
from fre0gen import Make_Pic
# from dotenv import load_dotenv

# S0S = 'Вы являетесь полезным AI, который делится всем, что знает. Говорите на русском.'
Ring_STX = 'CAACAgEAAxkBAAENB8ZnIG6wpYSeyiuwy27Bjt62hys9aAACNgMAAhOiGEQpRM8rzoHLZDYE'
KEYDRAW = ["рисуй", "сгень", "t2i", "imagine"]


LLM = None
# DEWIAR_TOKEN = os.getenv('DEW_KEY') 
# DEWIAR_IDENT = os.getenv('DEW_IDB')  

DEWIAR_TOKEN='Dwr_6d373b6661fbb4a79183828142d1ea93983c4a327b86ed9e09c2ea180d9205f3'
DEWIAR_IDENT=1745403320

def AQnit():
    global LLM
    LLM = f'https://dewiar.com/dew_ai/api?key={DEWIAR_TOKEN}'  
    print(f"ИИ получение LLM-API-URL: {LLM}")
    return LLM    

# def AIQ(prom:str):
    # a,_ = AIQue (prom)   
    # return a



async def draw_image(prompt, context: ContextTypes.DEFAULT_TYPE):
    if isinstance(prompt, list):
        prompt = ' '.join(prompt)
    print("AI > draw_image ", prompt)
    cargo = prompt.replace(',','.')
    cargo = prompt.replace("'","")
    return await Make_Pic(cargo, context) 
     
     
async def INHA_TEX(Promt:str, name:str, context: ContextTypes.DEFAULT_TYPE) -> None:
    CHAT_ID = Gechate(context) 
    try:
        TLINX = Parse_TeLinx(Promt) # Ищем ссылки
        PLINX = Parse_Linx(Promt) # Ищем ссылки        
        if TLINX:
            chat_id, message_id = TLINX
            message = await context.bot.forward_message(chat_id=CHAT_ID,
                from_chat_id=chat_id, message_id=message_id)
            mext = message.text
            print(f"IHT: Пересылкой выделено сообщение, содержание: {mext}")
            if mext:
                await AHANDLER(mext, context)
            return    
        if PLINX:
            Parce_doc = parse_website(PLINX)
            if Parce_doc:
                Parce = '\n'.join(Parce_doc)
                print(f"IHT: содержание: {Parce}")
                Promt += Parce
                await AHANDLER(Promt, context)
            return
    except Exception as e:
        error = f"IH_T: Ошибка: {e}"
        print('Ошибка: ', error)
        # await SEX(error, context)            

    Pic_Promt = Pic_Find(Promt, KEYDRAW) # Ищем Директивный запрос на Генератор
    if Pic_Promt:
        print('IHT: Пошло в рисовалку', Pic_Promt)
        Pic_Pro = ' '.join(Pic_Promt)
        await draw_image(Pic_Promt, context)
    else:
        Promt += name
        await AHANDLER(Promt, context)



async def AHANDLER(ai_prom: str, context: ContextTypes.DEFAULT_TYPE):
    # chat_id = Get_Uid(context) 
    chat_id = Gechate(context)         
    MSG = await context.bot.send_sticker(chat_id, sticker=Ring_STX)     
    pro_num, answer = AIQue(ai_prom)
    # if '&amp;quot;' in answer:
        # answer = answer.replace('&amp;quot;','')
    try: # Удаляем сообьзователя
        await context.bot.delete_message(chat_id, message_id=MSG.message_id)
    except Exception as e:
        print(f"AI_HANDLER: Ошибка удаления стикера: {e}") 
    # if pro_num == 99: # Передаем ошибку в сплитер
        # ai_response = answer         
        # return   
    if answer is None:
        return await SEX('Нейросеть: СБОЙ!', context)           
    await ASPLITTER(answer, context)     
     
def AIQue(prompt: str):        
    try:
        data = {
            "data": {
                "message": prompt,
                "image": "",
                "idb": DEWIAR_IDENT,
                "session_id": "",
                "midnight_clear": "yes",
            }
        }
        headers = {"Content-Type": "application/json"}
        respons = requests.post(LLM, headers=headers, data=json.dumps(data))
        if respons.status_code == 402:
            print(f"API Balance Error: {respons.text}")
            return 99, "⚠️ Ошибка нейросети Фрея:\n⚠️ API ключ не активирован или закончился баланс. Обратитесь к администратору."
        
        response = respons.json()   
        print("Ответ от модели: ", response) 
        answer = response.get('response', '⚠️ Ошибка: пустой ответ от модели')
        print("Выделяем текст: ", answer) 
        return 0, answer  

    except requests.RequestException as e:
        return 99, f"ФРЕЯ: 🧑‍🎤 Ошибка сети ⚠️ Мне очень жаль.\nВидимо сломался сервер Dewiar где лежит моя нейросеть. Попробуйте в следующий раз 😢"
    except Exception as e:
        return 99, f"ФРЕЯ: 🧑‍🎤 Ошибка ⚠️ нейросети: {e}"

# async def ASPLITTER(response:str, context: ContextTypes.DEFAULT_TYPE):
    # parts = response.split('```')    
    # for index, part in enumerate(parts):
        # part = part.strip()        
        # if index % 2 == 1:  # Code block
            # code_chunks = ASPLIT(f"```{part}```")
            # for chunk in code_chunks:
                # print ('> ЧАНКИ КОДА: =====')
                # await SEX(chunk, context, FORMAT='B')
                # await asyncio.sleep(2)
        # else:  # Regular text
            # text_chunks = ASPLIT(part)
            # for chunk in text_chunks:
                # print ('> ЧАНКИ ТЕКСТА: ==md==')                  
                # print ("force format_to_md...") 
                # formad = format_to_md(chunk)
                # await SEX(formad, context, FORMAT='B')
                # else:                     
                    # formad = clearq(chunk) 
                    # await ZEX(chunk, context)
                # await Adelay(2)   
                
                
AQnit()                   