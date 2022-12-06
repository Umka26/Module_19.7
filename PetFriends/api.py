import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import json
class PetFriends:
    def __init__(self):
        self.base_url = "https://petfriends.skillfactory.ru"
#--------------------------------------------------------------------------------------------------
# Получение идентификационного ключа зарегестрированного пользователя
    def get_api_key(self, email, password):
        headers = {
            'email' : email,
            'password' : password
        }
        res = requests.get(self.base_url + "/api/key", headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

#--------------------------------------------------------------------------------------------------
# Получение списка всех питомцев
    def get_list_of_pets(self, auth_key, filter):
        headers = {
            'auth_key' : auth_key['key']
        }
        filter = {'filter' : filter}

        res = requests.get(self.base_url+'/api/pets', headers=headers, params=filter)

        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

#------------------------------------------------------------------------------------------------
# Добавление нового питомца без фото
    def create_pet_simple_with_valid_data(self, auth_key, name: str, animal_type: str, age: str)-> json:
        headers = {'auth_key': auth_key['key']}
        data = {
            'name' : name,
            'animal_type' : animal_type,
            'age' : age
        }
        res = requests.post(self.base_url + '/api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

# ------------------------------------------------------------------------------------------------
#Добавление фото к существующему питомцу
    def add_new_photo_pet(self, auth_key: json, pet_id: str, pet_photo: str) -> json:
        data = MultipartEncoder(
            fields={
                 'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        res = requests.post(self.base_url + '/api/pets/set_photo/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result


# ------------------------------------------------------------------------------------------------
# Добавление нового питомца с фото
    def add_new_pet(self, auth_key: json, name: str, animal_type: str, age: str, pet_photo: str) -> json:
        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        res = requests.post(self.base_url + '/api/pets', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result

# ------------------------------------------------------------------------------------------------
#Обновление данных о питомце

    def update_info_about_pet(self, auth_key: json, pet_id: str, name: str,  animal_type: str, age: str) -> json:
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }
        headers = {'auth_key': auth_key['key']}
        res = requests.put(self.base_url + '/api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

# ------------------------------------------------------------------------------------------------
#Удаление питомца
    def delete_pet(self, auth_key: json, pet_id: str) -> json:
        headers = {'auth_key': auth_key['key']}
        res = requests.delete(self.base_url + '/api/pets/' + pet_id, headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result


