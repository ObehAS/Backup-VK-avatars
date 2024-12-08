import requests

class VK:
    def __init__(self, access_token, user_id, version='5.131'):
        self.token = access_token
        self.id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def users_info(self):
        url = 'https://api.vk.com/method/users.get'
        params = {'user_ids': self.id}
        response = requests.get(url, params={**self.params, **params})
        return response.json()

access_token = 'vk1.a.jn-_UjRW4tFjHR2wKlYUt6XWuet90PKHY0QVMD1WLpdWHtRJx6LTu_jp4trY6n57LmVKoRcVnpBtDZDCbMy6He2HG7AVTEjBTdGu-3NQ0TRaSHxl5YHHwt1FIb167uBmu0sAK-5s9YBJxbosag6FKm1T6-PdiIyAtwWkU02hredHgR4pcl_wKkDwpuJ8UCxw'
user_id = 'id23725029'
vk = VK(access_token, user_id)

print(vk.users_info())