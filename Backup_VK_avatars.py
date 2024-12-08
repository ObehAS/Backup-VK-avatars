import requests
import json
import time
from tqdm import tqdm

# Константы
VK_API_VERSION = '5.131'
VK_API_URL = 'https://api.vk.com/method/'
YANDEX_API_URL = 'https://cloud-api.yandex.net/v1/disk/'

def get_vk_photos(user_id, access_token, count=5):
    """Получает фотографии с профиля ВКонтакте."""
    params = {
        'owner_id': user_id,
        'album_id': 'profile',
        'extended': 1,
        'photo_sizes': 1,
        'count': count,
        'access_token': access_token,
        'v': VK_API_VERSION
    }
    response = requests.get(f'{VK_API_URL}photos.get', params=params)
    response.raise_for_status()
    
    # Добавляем вывод ответа для отладки
    print(f"VK API Response: {response.json()}")
    
    return response.json()['response']['items']

def get_max_size_photo(photo):
    """Возвращает URL фотографии максимального размера."""
    sizes = photo['sizes']
    max_size = max(sizes, key=lambda size: size['width'] * size['height'])
    return max_size['url'], max_size['type']

def create_yandex_folder(folder_name, yandex_token):
    """Создает папку на Яндекс.Диске."""
    headers = {'Authorization': f'OAuth {yandex_token}'}
    params = {'path': folder_name}
    response = requests.put(f'{YANDEX_API_URL}resources', headers=headers, params=params)
    response.raise_for_status()

def upload_photo_to_yandex(file_url, file_path, yandex_token):
    """Загружает фотографию на Яндекс.Диск."""
    headers = {'Authorization': f'OAuth {yandex_token}'}
    params = {'path': file_path, 'url': file_url}
    response = requests.post(f'{YANDEX_API_URL}resources/upload', headers=headers, params=params)
    response.raise_for_status()

def backup_photos(user_id, vk_token, yandex_token, count=5):
    """Создает резервную копию фотографий с профиля ВКонтакте на Яндекс.Диск."""
    try:
        photos = get_vk_photos(user_id, vk_token, count)
    except KeyError as e:
        print(f"Ошибка при получении фотографий: {e}")
        return
    
    folder_name = f'VK_Backup_{user_id}'
    create_yandex_folder(folder_name, yandex_token)
    
    backup_info = []
    
    for photo in tqdm(photos, desc='Загрузка фотографий'):
        photo_url, size_type = get_max_size_photo(photo)
        likes_count = photo['likes']['count']
        upload_date = time.strftime('%Y-%m-%d', time.localtime(photo['date']))
        file_name = f'{likes_count}.jpg'
        
        if any(info['file_name'] == file_name for info in backup_info):
            file_name = f'{likes_count}_{upload_date}.jpg'
        
        file_path = f'{folder_name}/{file_name}'
        upload_photo_to_yandex(photo_url, file_path, yandex_token)
        
        backup_info.append({
            'file_name': file_name,
            'size': size_type
        })
    
    with open('backup_info.json', 'w') as f:
        json.dump(backup_info, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    user_id = input('Введите id пользователя ВКонтакте: ')
    vk_token = input('Введите токен ВКонтакте: ')
    yandex_token = input('Введите токен Яндекс.Диска: ')
    
    backup_photos(user_id, vk_token, yandex_token)
    print('Резервное копирование завершено.')