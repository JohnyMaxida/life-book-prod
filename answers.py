import os
import json
from datetime import datetime
from lifeman import get_rate

numtask = 3
maxdays = 28        
user_id = None
user_path = None

questions = {
    1: "Как ты описываешь себя в трёх словах?",
    2: "А как бы тебя описал кто-то, кто хорошо тебя знает?",
    3: "Какой вопрос ты чаще всего задаёшь себе в голове?",
    4: "За что ты себя уважаешь?",
    5: "За что — критикуешь (даже если не вслух)?",
    6: "Как ты понимаешь, что ты «на своём месте»?",
    7: "Когда ты чувствуешь себя максимально живым? Что тогда происходит?",
    8: "Когда у тебя есть выбор — ты выбираешь то, что хочется или то, что правильно?",
    9: "Что ты чаще делаешь: действуешь по импульсу или по плану?",
    10: "Назови последнее решение, которое далось тебе трудно. Почему?",
    11: "Что тебе нужно, чтобы решиться начать новое?",
    12: "Когда ты достигаешь цели — что чувствуешь? Как долго длится это чувство?",
    13: "Что ты делаешь, когда тебе больно? А когда стыдно?",
    14: "Тебе легче говорить о своих чувствах или о своих мыслях?",
    15: "Кто может увидеть тебя настоящего — без роли?",
    16: "Что ты стараешься не чувствовать? Почему?",
    17: "Ты бы хотел плакать на людях — или это неприемлемо?",
    18: "Как ты понимаешь, что тебе комфортно с человеком?",
    19: "Ты умеешь просить о помощи? Легко ли тебе отказывать?",
    20: "Что ты терпишь в отношениях (дружбе, любви, семье), но на самом деле не хочешь?",
    21: "Ты чаще открываешься — или наблюдаешь?",
    22: "Кого ты не можешь отпустить до конца?",
    23: "Что будет, если ты полностью остановишься на неделю — без пользы, без целей?",
    24: "Как ты понимаешь, что ты молодец?",
    25: "Чего ты хочешь «на самом деле», но не говоришь вслух — даже себе?",
    26: "Что в тебе никто не понимает, как бы ты ни объяснял?",
    27: "Кто ты — если убрать твою профессию, знания, проекты и миссию?"
}

progress_levels = {
    1: "Новичок",
    2: "Стажер",
    3: "Ученик",
    4: "Специалист",
    5: "Профессионал",
    6: "Эксперт",
    7: "Мастер",
    8: "Гуру",
    9: "Виртуоз",
    10: "Магистр",
    11: "Академик",
    12: "Наставник",
    13: "Умелец",
    14: "Инженер",
    15: "Архитектор",
    16: "Технолог",
    17: "Ветеран",
    18: "Легенда",
    19: "Гений",
    20: "Мегамозг",
    21: "Волшебник",
    22: "Хакер",
    23: "Программист",
    24: "Разработчик",
    25: "Аналитик",
    26: "Командор",
    27: "Артист",
    28: "Ментор",
    29: "Виртуальный гений",
    30: "Разведчик",
    31: "Кибергений",
    32: "Технический маг",
    33: "Инноватор",
    34: "Капитан",
    35: "Цифровой властелин",
    36: "Технократ"
}

def Set_UP(uid, path): 
    global user_id, user_path
    user_id = uid
    user_path = path  


def get_rating():
    return get_prolevel(get_rate())

def get_prolevel(index: int) -> str:
    try: # Проверяем, есть ли индекс в словаре        
        if index in progress_levels:
            return progress_levels[index]
        else:
            return f"Ошибка индекса - нет уровня с номером {index}"
    except Exception as e:
        return f"Непредвиденная ошибка: {str(e)}"
        

def get_question(index: int) -> str:
    try: # Проверяем, есть ли индекс в словаре        
        if index in questions:
            return questions[index]
        else:
            return f"Ошибка индекса - нет вопроса с номером {index}"
    except Exception as e:
        return f"Непредвиденная ошибка: {str(e)}"


    
def Getask_day(day):
    mtask = numtask   
    print (f"Распорядок > день {day} по > {mtask} задач")
    return mtask  

    

def get_LAB_file(q_num: int, user_id:int) -> str:
    labook_file = f"USERLAB-{user_id}-Q{q_num}.json"
    file_path = os.path.join(user_path, labook_file)
    return file_path


def Init_Answers(user = None):
    if user is None: user = user_id    
    print(" > Init_Answers > Форматируем ОТВЕТЫ")
    # zero = {str(day): "" for day in range(1, maxdays)}  # Create dict with days as keys    
    tasks = ["Радость дня", "Благодарность дня", "Особый вопрос дня"]
    # zero = {"": "anything"}  # Create dict with days as keys       
    for task_index in range(1, numtask+1): 
        file_path = get_LAB_file(task_index, user)
        zero = {"": tasks[task_index-1]}  # Create dict with days as keys  
        Set_user_red(zero, task_index, user) 

def Get_user_re(q_num: int, user: int):
    try:
        file_path = get_LAB_file(q_num, user)
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    except Exception as e:
        print(f"Error reading user responses: {e}")
        return None
        
        
def Get_all_responses(user = None):
    if user is None: user = user_id
    block_respo = []
    for task_index in range(1, numtask+1): 
        file_path = get_LAB_file(task_index, user)
        if os.path.exists(file_path):
            responses = Get_user_re(task_index, user)  # читаем из текущего файла
            if responses:
                responsess = str(responses)
                block_respo.append(responsess)
    all_responses = '\n'.join(block_respo)
    return all_responses        
        

    
def Set_user_red(responses, q_num: int, user: int, day: str = None):
    try:
        file_path = get_LAB_file(q_num, user)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)        
        # Load existing data if file exists
        existing_data = {}
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                try:
                    existing_data = json.load(f)
                    if not isinstance(existing_data, dict):
                        existing_data = {}
                except json.JSONDecodeError:
                    existing_data = {}
        
        # Update with new responses
        if day is not None:
            # Update specific day's response
            existing_data[day] = responses
        else:
            # Update all responses
            existing_data.update(responses)
        
        # Save back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Ошибка при сохранении ответа: {e}")
        return False
        
        
# Get_user_responses        
        
    
   
def Get_day_responses(day, user = None):
    if user is None: user = user_id
    day_respo = []
    for task_index in range(1, numtask+1): 
        file_path = get_LAB_file(task_index, user)
        if os.path.exists(file_path):
            responses = Get_user_re(task_index, user)  # читаем из текущего файла
            if responses:
                response = responses.get(str(day))
                day_respo.append(response)
    return day_respo

def Get_task_response(task_index, day, user=None):
    if user is None: 
        user = user_id
    task_index += 1    
    file_path = get_LAB_file(task_index, user)  # +1 to match Update_task_response
    if os.path.exists(file_path):
        responses = Get_user_re(task_index, user)
        if responses:
            return responses.get(str(day))
    return None   
    
    
    
    
def Update_task_response(task_index, day, response_text):
    day = str(day) if day else "1"
    task_index += 1
    print(f"Update_task_response ПРИШЛО ~ Tindex->{task_index}  День->{day}")
    try:
        ok = Set_user_red(response_text, task_index, user_id, day=day)
        if ok:
            print(f"Ответ для задачи {task_index} день {day} обновлен: {response_text}")
            return True
        else:
            print(f"Ошибка в Set_user_red {task_index} день {day} обновлен: {response_text}")
            return False
    except Exception as e:
        print(f"Ошибка при обновлении ответа: {str(e)}")
        return False


def delete_user_responses(user = None):
    Init_Answers(user)
    
    
    
    
    
    
    
    
    