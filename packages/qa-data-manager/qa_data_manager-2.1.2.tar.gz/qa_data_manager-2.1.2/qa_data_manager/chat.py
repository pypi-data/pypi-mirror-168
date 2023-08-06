import datetime

from playhouse.shortcuts import model_to_dict

from qa_data_manager.data_base_model import Chats

"""
Генерация чата.
    Поля:
        * doctor_id - Идентификатор доктора; Обязательное поле, устанавливается при инициализации класса из параметра doctor.
        * patient_id - Идентификатор пациента; Обязательное поле, устанавливается при инициализации класса из параметра patient.
    
    Методы 
    - is_active - Устанавливает признак активности чата.
    - generate(): 
        -Сохраняет объект GenerateChat в базу данных
        -Возвращает модель таблицы Chats с данными сгенерированного чата.
"""


class GenerateChat:

    def __init__(self, doctor, patient):
        self._doctor_id = doctor.get('id')
        self._patient_id = patient.get('id')
        self._active = 0

    def is_active(self):
        self._active = 1
        return self

    def generate(self):
        chat = Chats(doctor=self._doctor_id,
                     patient=self._patient_id,
                     active=self._active,
                     created_at=datetime.datetime.now(),
                     updated_at=datetime.datetime.now())
        chat.save()
        return model_to_dict(chat)
