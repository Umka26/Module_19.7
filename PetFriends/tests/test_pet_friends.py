from api import PetFriends
from settings import valid_email, valid_password, not_valid_email, not_valid_password, not_valid_key
import json
import os
pf = PetFriends()

#-------------------------------------------------------------------------------------
#Получение идентификационного ключа с кореектными данными почты и пароля
def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

#-------------------------------------------------------------------------------------
#Получение списка всех питомцев
def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

#-------------------------------------------------------------------------------------
#Добавление нового питомца без фото
def test_create_pet_simple_with_valid_data(name="Мурмяус", animal_type="Кошка", age='5'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple_with_valid_data(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name

#-------------------------------------------------------------------------------------
#Добавление фото к питомцу
def test_add_new_photo_pet(pet_photo='image/3.jpg') -> json:
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) == 0:
        pf.create_pet_simple_with_valid_data(auth_key, "Test_name", "Test_type", "Test_age")
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.add_new_photo_pet(auth_key, pet_id, pet_photo)
    assert status == 200
    assert result['pet_photo'] is not None

#-------------------------------------------------------------------------------------
#Добавление нового питомца с фото
def test_add_new_pet(name='Джульбарс', animal_type='дворняга', age='4', pet_photo='image/1.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == age

#-------------------------------------------------------------------------------------
#Обновление данных о питомце при предположении что список питомцев не пустой
def test_update_info_about_pet(name='Пунька', animal_type='Кошка', age="2"):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.update_info_about_pet(auth_key, my_pets['pets'][1]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("Невозможно обновить информацию о питомце. \nСписок питомцев пуст!")

# --------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------
#Обновление данных о питомце
def test_update_info_about_pet_1(name='Пунька', animal_type='Кошка', age="2"):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) == 0:
        pf.create_pet_simple_with_valid_data(auth_key, "Test_name", "Test_type", "Test_age")
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    status, result = pf.update_info_about_pet(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
    assert status == 200
    assert result['name'] == name
#-------------------------------------------------------------------------------------
#Удаление питомца если хотя бы один питомец присутствует в списке
def test_delete_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        pet_id = my_pets['pets'][0]['id']
        status, result = pf.delete_pet(auth_key, pet_id)
        assert status == 200
        assert pet_id not in my_pets.values()
    else:
        raise IndexError("Невозможно удалить несуществующего питомца. \nСписок питомцев пуст!")

# --------------------------------------------------------------------------------------
#Удаление питомца если питомцы отсутствуют в списке
def test_delete_pet_if_list_of_pets_is_null():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.create_pet_simple_with_valid_data(auth_key, "Test_name", "Test_type", "Test_age")
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.delete_pet(auth_key, pet_id)
    assert status == 200
    assert pet_id not in my_pets.values()

# --------------------------------------------------------------------------------------
#Удаление питомца при помощи неверного идентификационного ключа пользователя
def test_delete_pet_with_not_valid_key():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.create_pet_simple_with_valid_data(auth_key, "Test_name", "Test_type", "Test_age")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    auth_key = not_valid_key
    status, result = pf.delete_pet(auth_key, pet_id)
    assert status == 403
    assert len(my_pets['pets']) > 0

# --------------------------------------------------------------------------------------
#Попытка получения идентификационного ключа незарегистрированным пользователем
def test_get_api_key_for_not_valid_user(email=not_valid_email, password=not_valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result


# --------------------------------------------------------------------------------------
#Попытка получения идентификационного ключа с некорректными данными почты
def test_get_api_key_for_not_valid_email(email=not_valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

# --------------------------------------------------------------------------------------
#Попытка получения идентификационного ключа при вводе неверного пароля
def test_get_api_key_for_not_valid_password(email=valid_email, password=not_valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

# --------------------------------------------------------------------------------------
#Попытка получения списка всех питомцев при помощи неверного идентификационного ключа пользователя
def test_get_all_pets_with_not_valid_key(filter=''):
    auth_key = not_valid_key
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 403

# --------------------------------------------------------------------------------------
#Попытка добавления нового питомца без фото с некорректными данными
def test_create_pet_simple_with_invalid_data(name="%,.", animal_type=".,%", age= "%,.;:"):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple_with_valid_data(auth_key, name, animal_type, age)

    if status == 400:
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
        pet_id = my_pets['pets'][0]['id']
        assert pet_id not in my_pets.values()
    else:
        raise AssertionError("При вводе некорректных данных произошло добавление питомца в список!!!")

# --------------------------------------------------------------------------------------
#Попытка добавления нового питомца без фото при помощи неверного идентификационного ключа пользователя
def test_create_pet_simple_with_invalid_key(name="Шарик", animal_type="Дворняга", age= '3'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    auth_key = not_valid_key
    status, result = pf.create_pet_simple_with_valid_data(auth_key, name, animal_type, age)
    assert status == 403

# --------------------------------------------------------------------------------------
#Обновление данных о питомце при помощи неверного идентификационного ключа пользователя
def test_update_info_about_pet_with_not_valid_key(name='Пунька', animal_type='Кошка', age='2'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) == 0:
        pf.create_pet_simple_with_valid_data(auth_key, "Test_name", "Test_type", "Test_age")
    auth_key = not_valid_key
    status, result = pf.update_info_about_pet(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
    assert status == 403

#Удаление питомца при помощи неверного идентификационного ключа пользователя
def test_delete_pet_with_not_valid_key_1():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    a = len(my_pets['pets'])

    if len(my_pets['pets']) == 0:
        pf.create_pet_simple_with_valid_data(auth_key, "Test_name", "Test_type", "Test_age")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
        pet_id = my_pets['pets'][0]['id']
        auth_key = not_valid_key
        status, result = pf.delete_pet(auth_key, pet_id)
        assert status == 403
        assert len(my_pets['pets']) == a + 1
    else:
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
        pet_id = my_pets['pets'][0]['id']
        auth_key = not_valid_key
        status, result = pf.delete_pet(auth_key, pet_id)
        assert status == 403