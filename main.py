from bs4 import BeautifulSoup
from proxy import fetch, fetch_one, fetch_two
import pandas as pd
import concurrent.futures
import time

NUM_THREADS = 20

products_data = []

print(f'Start Scraping')

CategoriesWithOutSub=[]
CategoriesWithSub=[]

def getTotalSold(name):
    try:
        response = ''
        response = fetch(f'https://www.mercadolibre.com.co/perfil/{name}')
        if not response:
            response = fetch_one(f'https://www.mercadolibre.com.co/perfil/{name}')
        if not response:
            response = fetch_two(f'https://www.mercadolibre.com.co/perfil/{name}')
        SellerProfilesoup = BeautifulSoup(response.content, 'html.parser')
        infoSeller = SellerProfilesoup.find('p', {'class': 'seller-info__subtitle-sales'}).text
        products_data.append({'seller_info':infoSeller})
    except:
        print("Error on looking info")

def get_id(url:str) -> str:
    url_list = url.split('/')
    product_id = ''
    if 5 > len(url_list):
        product_id = url_list[3]
        product_id = product_id.split('-')
        product_id = product_id[0] + product_id[1]
    else:
        product_id = url_list[5]
        product_id = product_id.split('?')
        product_id = product_id[0]
    return product_id

def getInformationOlList(soup: BeautifulSoup):
    try:
        section = soup.find('section', {'class': 'ui-search-results ui-search-results--without-disclaimer shops__search-results'})
        rawItemList = section.find_all('li', {'class': 'ui-search-layout__item'})
        for item in rawItemList:
            products_data.append({
                'titles': item.find('h2', {'class': 'ui-search-item__title ui-search-item__group__element shops__items-group-details shops__item-title'}).text,
                'prices': item.find('span', {'class': 'price-tag-fraction'}).text.replace(',', ''),
                'urls': item.find('a', {'class': 'ui-search-result__content ui-search-link'})['href'],
                'id_product': get_id(item.find('a', {'class': 'ui-search-result__content ui-search-link'})['href'])
            })
    except:
        print("Error get element Ol")


def getInformation(soup: BeautifulSoup) -> None:
    try:
        rawItemList = soup.find_all('li', {'class': 'ui-search-layout__item'})
        for item in rawItemList:
            products_data.append({
                'titles': item.find('h2', {'class': 'ui-search-item__title'}).text,
                'prices': item.find('span', {'class': 'price-tag-fraction'}).text.replace(',', ''),
                'urls': item.find('a', {'class': 'ui-search-item__group__element'})['href'],
                'id_product': get_id(item.find('a', {'class': 'ui-search-item__group__element'})['href'])
            })
    except:
        getInformationOlList(soup)
        print("Error to get information")

def pagination(nextPage, isNextPage, isFirstPage, soup): 
    if not nextPage:
        return
    if isFirstPage == '1':
        getInformation(soup)
    if nextPage and isNextPage == 'Siguiente':
        try:
            responseNextPage = None
            responseNextPage = fetch(nextPage)
            if not responseNextPage:
                responseNextPage = fetch_one(nextPage)
            if not responseNextPage:
                responseNextPage = fetch_two(nextPage)
            soupNextPage = BeautifulSoup(responseNextPage.content, 'html.parser')
            getInformation(soupNextPage)
            nextPageResult = soupNextPage.find('a', {'class': 'andes-pagination__link', 'title': 'Siguiente'})['href']
            isNextPageResult = soupNextPage.find('a', {'class': 'andes-pagination__link', 'title': 'Siguiente'})['title']
            if nextPageResult and isNextPageResult:
                pagination(nextPageResult, isNextPageResult, '0', soupNextPage)
        except:
            print("end code")

def getMoreCategory(link):
    try:
        responseCategory = None
        responseCategory = fetch(link)
        if not responseCategory:
            responseCategory = fetch_one(link)
        if not responseCategory:
            responseCategory = fetch_two(link)
        CategorySoup = BeautifulSoup(responseCategory.content, 'html.parser')
        CategoriesWithSub.remove(link)
        getLinkByCategory(CategorySoup)
    except:
        print("No more subcategories")

def searchItems(link):
    try:
        responseCategory = None
        responseCategory = fetch(link)
        print("Response........... ", responseCategory)
        if not responseCategory:
            responseCategory = fetch_one(link)
        if not responseCategory:
            responseCategory = fetch_two(link)
        CategorySoup = BeautifulSoup(responseCategory.content, 'html.parser')
        itemsResult = CategorySoup.find('span',{'class':'ui-search-search-result__quantity-results shops-custom-secondary-font'}).text.replace(' resultados', '')
        print(itemsResult)
        try:
            nextPage = CategorySoup.find('a', {'class': 'andes-pagination__link'})['href']
            isNextPage = CategorySoup.find('a', {'class': 'andes-pagination__link'})['title']
            isFirstPage = CategorySoup.find('span', {'class':'andes-pagination__link'}).text
            if nextPage and isNextPage:
               pagination(nextPage, isNextPage, isFirstPage, CategorySoup)
        except:
            getInformation(CategorySoup)
            print("Doesn't pagination")
    except:
        print("Error to get items")

def getLinkByCategory(pageSoup:BeautifulSoup):
    titleCategory = pageSoup.find('div', {'class': 'ui-search-filter-dt-title shops-custom-primary-font'})
    title = titleCategory.get_text()
    if title == 'Categorías':
        listCategories = titleCategory.find_previous('div', {'class': 'ui-search-filter-dl shops__filter-items'})
        categories = listCategories.find_all('li', {'class': 'ui-search-filter-container shops__container-lists'})
        if(len(categories)>=9):
            linkMoreCategories = listCategories.find('a', {'class': 'ui-search-modal__link ui-search-modal--default ui-search-link'})['href']
            try:
                res = None
                res = fetch(linkMoreCategories)
                if not res:
                    res = fetch_one(linkMoreCategories)
                if not res:
                    res = fetch_two(linkMoreCategories)
            except:
                print('Error to get Link categories')
            CategoryPage = BeautifulSoup(res.content, 'html.parser')
            linkCategories = CategoryPage.find('div', {'class': 'ui-search-search-modal-grid-columns'})
            links = linkCategories.find_all('a', {'class': 'ui-search-search-modal-filter ui-search-link'})
            for linkCategory in links:
                try:
                    res = None
                    res = fetch(linkCategory.get('href'))
                    print("RESPONSE...........", res)
                    if not res:
                        res = fetch_one(linkCategory.get('href'))
                    if not res:
                        res = fetch_two(linkCategory.get('href'))
                    page = BeautifulSoup(res.content, 'html.parser')
                    itemsResult = page.find('span',{'class':'ui-search-search-result__quantity-results shops-custom-secondary-font'}).text.replace(' resultados', '')
                    numberItems = int(itemsResult.replace('.', ''))
                    if numberItems > 2000:
                        CategoriesWithSub.append(linkCategory.get('href'))
                    else:
                        CategoriesWithOutSub.append(linkCategory.get('href'))
                except:
                    print("Error to search link category")
        else:
            for category in categories:
                linkCategory = category.find('a', {'class': 'ui-search-link'})['href']
                try:
                    res = None
                    res = fetch(linkCategory)
                    print("RESPONSE...........", res)
                    if not res:
                        res = fetch_one(linkCategory)
                    if not res:
                        res = fetch_two(linkCategory)
                    page = BeautifulSoup(res.content, 'html.parser')
                    itemsResult = page.find('span',{'class':'ui-search-search-result__quantity-results shops-custom-secondary-font'}).text.replace(' resultados', '')
                    numberItems = int(itemsResult.replace('.', ''))
                    if numberItems > 2000:
                        CategoriesWithSub.append(linkCategory)
                    else:
                        CategoriesWithOutSub.append(linkCategory)
                except:
                    print("Error to search link category")
    if title == 'Precio':
        listCategories = titleCategory.find_previous('div', {'class': 'ui-search-filter-dl shops__filter-items'})
        categoriesByPrice = listCategories.find_all('li', {'class': 'ui-search-filter-container shops__container-lists'})
        for category in categoriesByPrice:
            listPrice = category.find('a', {'class': 'ui-search-link'})['href']
            try:
                res = None
                res = fetch(listPrice)
                if not res:
                    res = fetch_one(listPrice)
                if not res:
                    res = fetch_two(listPrice)
                page = BeautifulSoup(res.content, 'html.parser')
                itemsResult = page.find('span',{'class':'ui-search-search-result__quantity-results shops-custom-secondary-font'}).text.replace(' resultados', '')
                numberItems = int(itemsResult.replace('.', ''))
                if numberItems > 2000:
                    CategoriesWithSub.append(listPrice)
                else:
                    CategoriesWithOutSub.append(listPrice)
            except:
                print("Error to search link category")
    if len(CategoriesWithSub) > 0:
        with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
            executor.map(getMoreCategory, CategoriesWithSub)
        

def get_sold(product):
    try:
        res = ''
        res = fetch(product['urls'])
        if not res:
            res = fetch_one(product['urls'])
        if not res:
            res = fetch_two(product['urls'])
        ItemSoup = BeautifulSoup(res.content, 'html.parser')
        countSold = ItemSoup.find('span', {'class': 'ui-pdp-subtitle'}).text
        product['sold'] = countSold[10:]
    except:
        print("Error to get sold by product")


def main():
    try:
        time_start = time.time()
        response = fetch(f'https://listado.mercadolibre.com.co/_CustId_1055693607')
        soup = BeautifulSoup(response.content, 'html.parser')
        nameSeller = soup.find('h1', {'class': 'ui-search-breadcrumb__title'}).text
        name = nameSeller[17:].replace(' ', '+')
        getLinkByCategory(soup)
        getTotalSold(name)
        with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
            executor.map(searchItems, CategoriesWithOutSub)
        products_data.sort(reverse=True, key=lambda x:(len(x), repr(x)))
        for i in range(0, len(products_data)):
            try:
                if products_data[i+1]['id_product'] == products_data[i]['id_product']:
                    products_data.remove(products_data[i])
            except:
                pass
        frame = pd.DataFrame(products_data)
        frame.to_excel(f'{name}.xlsx', index=False)
        time_queries = None
        if len(products_data) % 5000 == 0: 
            time_queries = int(len(products_data) / 5000)
        else: 
            time_queries = int((len(products_data) // 5000) + 1)
        start = 0
        end = 4999
        for i in range(0, time_queries):
            time.sleep(300)
            with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
                executor.map(get_sold, products_data[start:end])
            frame = pd.DataFrame(products_data)
            frame.to_excel(f'{name}.xlsx', index=False)
            start = end + 1
            end = end + 5000
        total_time = time.time() - time_start
        print(total_time)
    except: 
        print("Error func main")

if __name__ == '__main__':
    main()