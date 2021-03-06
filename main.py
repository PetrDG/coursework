import requests
import datetime
from pprint import pprint


class VK:
    def __init__(self, token_list, vers='5.131'):
        self.token = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
        self.id = '552934290'
        self.vers = vers
        self.params = {'access_token': self.token, 'v': self.vers}
        self.json, self.export_dict = self.sort_info()

    def photo_get(self):
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': self.id,
                  'album_id': 'profile',
                  'photo_sizes': 1,
                  'extended': 1}
        photo_det = requests.get(url, params={**self.params, **params}).json()['response']
        return photo_det['count'], photo_det['items']

    def likes_log(self):
        photo_count, photo_items = self.photo_get()
        result = {}
        for like in range(photo_count):
            likes_count = photo_items[like]['likes']['count']
            url_dl, photo_size = dpi_max(photo_items[like]['sizes'])
            time_load = date(photo_items[like]['date'])
            List_pp = result.get(likes_count, [])
            List_pp.append({'add_name': time_load,
                            'url_picture': url_dl,
                            'size': photo_size})
            result[likes_count] = List_pp
        return result

    def sort_info(self):
        json_list = []
        sorted_dict = {}
        photo_dict = self.likes_log()
        for elem in photo_dict.keys():
            for v in photo_dict[elem]:
                if len(photo_dict[elem]) == 1:
                    file_name = f'{elem}.jpeg'
                else:
                    file_name = f'{elem} {v["add_name"]}.jpeg'
                json_list.append({'file name': file_name, 'size': v["size"]})
                sorted_dict[file_name] = photo_dict[elem][0]['url_picture']
        return json_list, sorted_dict


class YAD:
    def __init__(self, name_folder, token_list):
        self.token = '~~~ТУТ ТОКЕН ОТ ЯНДЕКС ДИСКА~~~'
        self.url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        self.headers = {'Authorization': self.token}
        self.folder = self.create_folder(name_folder)

    def create_folder(self, name_folder):
        url = "https://cloud-api.yandex.net/v1/disk/resources"
        params = {'path': name_folder}
        if requests.get(url, headers=self.headers, params=params).status_code != 200:
            requests.put(url, headers=self.headers, params=params)
        else:
            print(f'\nПапка  {name_folder} уже существует')
        return name_folder

    def put_folder(self, name_folder):
        url = "https://cloud-api.yandex.net/v1/disk/resources"
        params = {'path': name_folder}
        resource = requests.get(url, headers=self.headers, params=params).json()['_embedded']['items']
        list_folder = []
        for t in resource:
            list_folder.append(t['name'])
        return list_folder

    def copy_photo(self, dict_files):
        photo_folder = self.put_folder(self.folder)
        num_files = 0
        for key in dict_files.keys():
            if key not in photo_folder:
                params = {'path': f'{self.folder}/{key}',
                          'url': dict_files[key],
                          'overwrite': 'false'}
                requests.post(self.url, headers=self.headers, params=params)
                num_files += 1
            else:
                print(f'Фото {key} уже загружено ранее')
        print(f'\nЗагружено {num_files} файлов.')


def dpi_max(dict_search):
    dpi_max = 0
    for d in range(len(dict_search)):
        dpi_file = dict_search[d].get('width') * dict_search[d].get('height')
        if dpi_file > dpi_max:
            dpi_max = dpi_file
            max_elem = d
    return dict_search[max_elem].get('url'), dict_search[max_elem].get('type')


def date(time):
    date_time = datetime.datetime.fromtimestamp(time)
    list_time = date_time.strftime('%Y-%m-%d time %H-%M-%S')
    return list_time


if __name__ == '__main__':
    tokenVK = ''
    json_VK = VK(tokenVK)
    pprint(json_VK.json)
    main = YAD('VK photo', '')
    main.copy_photo(json_VK.export_dict)
