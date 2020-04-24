import requests
import sys


def get_ayahs(surah_num, start_ayah, num_of_ayahs):
    ''' returns dict of specified ayahs with keys as ayah number '''
    res = {}

    url = f'''http://api.alquran.cloud/v1/surah/{surah_num}?offset={start_ayah-1}&limit={num_of_ayahs}'''

    response = requests.get(url)
    if response.status_code != 200:
        print(f"{response.status_code}: Error retrieving ayahs")
        sys.exit()

    ayahs = response.json()['data']['ayahs']
    for ayah in ayahs:
        num = ayah['numberInSurah']
        text = ayah['text']
        res[num] = text

    return res

def get_surahs(type="english"):
    ''' returns list of surah names '''
    url = 'http://api.alquran.cloud/v1/surah'
    response = requests.get(url)
    if response.status_code != 200:
        print(f"{response.status_code}: Error retrieving ayahs")
        sys.exit()

    surahs = response.json()['data']
    nums_of_ayahs = [""] + [surah['numberOfAyahs'] for surah in surahs]
    list_of_surahs = [""] + [surah['englishName'] for surah in surahs]
    return list_of_surahs, nums_of_ayahs

def inspect(obj, obj_name=None):
    if obj_name:
        print(f"inspecting {obj_name}")
    if isinstance(obj, dict):
        print("type: dict")
        print(f"length: {len(obj)}")
        print(f"keys: {obj.keys()}")
    elif isinstance(obj, list):
        print("type: list")
        print(f"length: {len(obj)}")

    else:
        print(f"type: {type(obj)}")
    # print(f)



if __name__ == '__main__':
    surah_num = 1  # al-fatiha
    start_ayah = 1  # second ayah
    end_ayah = 3  # fourth ayah
    num_of_ayahs = end_ayah - start_ayah + 1
    ayah_dict = get_ayahs(surah_num, start_ayah, num_of_ayahs)

    for key, val in ayah_dict.items():
        s = " ".join([c for c in val])
        print(f"{key}: {s}")