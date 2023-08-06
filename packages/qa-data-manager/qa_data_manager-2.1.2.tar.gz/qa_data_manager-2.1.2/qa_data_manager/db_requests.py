from datetime import datetime

from qa_data_manager.data_base_model import SlotsDoctors, ConfirmationCodes, Users, DoctorPatient, Chats, ClinicUser, \
    Clinics


class Slot_doctor:
    # Вся строка из таблицы по id слота
    def slot_info_by_id(slot_id):
        return SlotsDoctors.select().where(SlotsDoctors.id == slot_id).get()

    # Дата и время начала определенного слота по id
    def start_at_by_id(slot_id):
        return datetime.strptime(str(SlotsDoctors.select().where(SlotsDoctors.id == slot_id).get().start_at),
                                 "%Y-%m-%d %H:%M:%S")


class User:
    # Вся строка из таблицы по номеру телефона пользователя
    def get_info_by_phone(person):
        return Users.select().where(Users.phone == person.get('phone')).get()
    # Код по номеру телефона пользователя
    def get_code_by_phone(person):
        return Users.select().where(Users.phone == person.get('phone')).get().code


class Confirmation_codes:
    # Код по id пользователя
    def get_code_by_id(person):
        return ConfirmationCodes.select().where(ConfirmationCodes.user_id == person.id).get()


class Doctor_patient:
    # Кол-во записей между id двух пользователей
    def count_of_value_by_ids(doctor, patient):
        return DoctorPatient.select().where(
            (DoctorPatient.doctor == doctor.get('id')) & (DoctorPatient.patient == patient.id)).count()


class Chat:
    # Кол-во записей между id двух пользователей
    def count_of_value_by_ids(doctor, patient):
        return Chats.select().where(
            (Chats.doctor == doctor.get('id')) & (Chats.patient == patient.id)).count()


class Clinic_User:
    # id клиники по id привязанного пользователя
    def clinic_id_by_user_id(person):
        return ClinicUser.select().where(ClinicUser.user == person.get("id")).get().clinic


class Clinic:
    # Название клиники по id клиники
    def name_by_clinic_id(clinic_id):
        return Clinics.select().where(Clinics.id == clinic_id).get().name
    # Город и улица клиники по id клиники
    def address_by_clinic_id(clinic_id):
        info = Clinics.select().where(Clinics.id == clinic_id).get()
        return info.city + ", " + info.street
