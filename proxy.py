import requests

proxies = {
    'http': '104.154.168.184:80',
    'https': '104.154.168.184:80',
}

proxies_one = {
    'http': '34.139.225.109:80',
    'https': '34.139.225.109:80',
}

proxies_two = {
    'http': '34.86.0.141:80',
    'https': '34.86.0.141:80',
}

proxies_three = {
    'http': '34.125.236.127:80',
    'https': '34.125.236.127:80',
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