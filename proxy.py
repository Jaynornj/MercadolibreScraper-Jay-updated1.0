import requests

proxies = {
    'http': '34.171.77.246:80',
    'https': '34.171.77.246:80',
}

proxies_one = {
    'http': '34.139.101.153:80',
    'https': '34.139.101.153:80',
}

proxies_two = {
    'http': '35.236.45.217:80',
    'https': '35.236.45.217:80',
}

proxies_three = {
    'http': '35.236.213.209:80',
    'https': '35.236.213.209:80',
}

def fetch_proxies(url:str):
    try:
        response = requests.get(url, proxies=proxies)
        #print("Fetch.. fetch_proxies", url)
        return response
    except Exception as error:
        print("Error fetch", error)

def fetch_proxies_one(url:str):
    try:
        response = requests.get(url, proxies=proxies_one, timeout=5)
        #print("Fetch.. fetch_proxies_one", url)
        return response
    except Exception as error:
        print("Error fetch", error)

def fetch_proxies_two(url:str):
    try:
        response = requests.get(url, proxies=proxies_two, timeout=5)
        #print("Fetch.. fetch_proxies_two", url)
        return response
    except Exception as error:
        print("Error fetch", error)

def fetch_proxies_three(url:str):
    try:
        response = requests.get(url, proxies=proxies_three, timeout=5)
        #print("Fetch.. fetch_proxies_three", url)
        return response
    
    except Exception as error:
        print("Error fetch", error)