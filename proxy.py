import requests 

proxies = {
  'http': '34.72.94.38:80',
  'https': '34.72.94.38:80',
}
proxies_one = {
  'http': '35.184.53.123:80',
  'https': '35.184.53.123:80',
}
proxies_two = {
  'http': '34.171.23.191:80',
  'https': '34.171.23.191:80',
}


def fetch(url:str): 
    try:
        response = requests.get(url, proxies=proxies,timeout=5)
        print("fetch....", url)
        return response
    except Exception as e:
        print("Error fetch", e)

def fetch_one(url:str): 
    try:
        response = requests.get(url, proxies=proxies_one,timeout=5)
        print("fetch....", url)
        return response
    except Exception as e:
        print("Error fetch", e)

def fetch_two(url:str): 
    try:
        response = requests.get(url, proxies=proxies_two,timeout=5)
        print("fetch....", url)
        return response
    except Exception as e:
        print("Error fetch", e)
