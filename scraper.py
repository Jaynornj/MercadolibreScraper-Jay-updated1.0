from proxy import fetch_proxies, fetch_proxies_one, fetch_proxies_two, fetch_proxies_three
from bs4 import BeautifulSoup
import requests
import concurrent.futures
import pandas as pd
import datetime

NUM_THREADS = 10

custId = '176165485'
CategoriesWithSub = []
CategoriesWithOutSub = []
products_data = []


def getMoreCategory(link):
    try:
        responseCategory = fetch_proxies(link)
        if not responseCategory:
            responseCategory = fetch_proxies_one(link)
            if not responseCategory:
                responseCategory = fetch_proxies_two(link)
                if not responseCategory:
                    responseCategory = fetch_proxies_three(link)

        CategorySoup = BeautifulSoup(responseCategory.content, 'html.parser')
        CategoriesWithSub.remove(link)
        getLinkByCategory(CategorySoup)
    except:
        print("No more subcategories")

def getTotalSold(name):
    try:
        response = fetch_proxies(f'https://www.mercadolibre.com.co/perfil/{name}')
        if not response:
            response = fetch_proxies_one(f'https://www.mercadolibre.com.co/perfil/{name}')
            if not response:
                response = fetch_proxies_two(f'https://www.mercadolibre.com.co/perfil/{name}')
                if not response:
                    response = fetch_proxies_three(f'https://www.mercadolibre.com.co/perfil/{name}')
        
        SellerProfilesoup = BeautifulSoup(response.content, 'html.parser')
        infoSeller = SellerProfilesoup.find('p', {'class': 'seller-info__subtitle-sales'}).text
        products_data.append({'seller_info':infoSeller})

    except:
        print("Error on looking info")

def getLinkByCategory(pageSoup:BeautifulSoup):

    titleCategory = pageSoup.find('div', {'class': 'ui-search-filter-dt-title shops-custom-primary-font'})
    title = titleCategory.get_text()
    if title == 'Categorías':

        listCategories = titleCategory.find_previous('div', {'class': 'ui-search-filter-dl shops__filter-items'})
        categories = listCategories.find_all('li', {'class': 'ui-search-filter-container shops__container-lists'})
        
        if (len(categories) > 9):
            linkMoreCategories = listCategories.find('a', {'class': 'ui-search-modal__link ui-search-modal--default ui-search-link'})['href']  
            try:
                res = fetch_proxies(linkMoreCategories)
                if res == None:
                    res = fetch_proxies_one(linkMoreCategories)
                    if res == None:
                        res = fetch_proxies_two(linkMoreCategories)
                        if res == None:
                            res = fetch_proxies_three(linkMoreCategories)
            except:
                print('Error to get Link categories')

            CategoryPage = BeautifulSoup(res.content, 'html.parser')
            linkCategories = CategoryPage.find('div', {'class': 'ui-search-search-modal-grid-columns'})
            links = linkCategories.find_all('a', {'class': 'ui-search-search-modal-filter ui-search-link'})

            for linkCategory in links:
                try:

                    res = fetch_proxies(linkCategory.get('href'))
                    if not res:
                        res = fetch_proxies_one(linkCategory.get('href'))
                        if not res:
                            res = fetch_proxies_two(linkCategory.get('href'))
                            if not res:
                                res = fetch_proxies_three(linkCategory.get('href'))


                    page = BeautifulSoup(res.content, 'html.parser')
                    itemsResult = int(page.find('span',{'class':'ui-search-search-result__quantity-results shops-custom-secondary-font'}).text.replace(' resultados', '').replace('.', ''))
                    
                    if itemsResult > 2000:
                        CategoriesWithSub.append(linkCategories.get('href'))
                    else:
                        CategoriesWithOutSub.append(linkCategory.get('href'))

                except:
                    print("Error to search link category")
        else:
            for category in categories:
                linkCategory = category.find('a', {'class': 'ui-search-link'})['href']
                try:
                    res = fetch_proxies(linkCategory)
                    if not res:
                        res = fetch_proxies_one(linkCategory)
                        if not res:
                            res = fetch_proxies_two(linkCategory)
                            if not res:
                                res = fetch_proxies_three(linkCategory)

                    page = BeautifulSoup(res.content, 'html.parser')
                    itemsResult = int(page.find('span',{'class':'ui-search-search-result__quantity-results shops-custom-secondary-font'}).text.replace(' resultados', '').replace('.', ''))
                    if itemsResult > 2000:
                        CategoriesWithSub.append(linkCategory)
                    else:
                        CategoriesWithOutSub.append(linkCategory)
                except Exception as e:
                    print("Error to search link category 2", e)

    if title == 'Precio':
        listCategories = titleCategory.find_previous('div', {'class': 'ui-search-filter-dl shops__filter-items'})
        categoriesByPrice = listCategories.find_all('li', {'class': 'ui-search-filter-container shops__container-lists'})
        
        for category in categoriesByPrice:
            listPrice = category.find('a', {'class': 'ui-search-link'})['href']
            try:
                res = fetch_proxies(listPrice)
                if not res:
                    res = fetch_proxies_one(listPrice)
                    if not res:
                        res = fetch_proxies_two(listPrice)
                        if not res:
                            res = fetch_proxies_three(listPrice)
                            
                page = BeautifulSoup(res.content, 'html.parser')
                itemsResult = int(page.find('span',{'class':'ui-search-search-result__quantity-results shops-custom-secondary-font'}).text.replace(' resultados', '').replace('.', ''))

                if itemsResult > 2000:
                    CategoriesWithSub.append(listPrice)
                else:
                    CategoriesWithOutSub.append(listPrice)
            except:
                print("Error to search link category")
    if len(CategoriesWithSub) > 0:
        with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
            executor.map(getMoreCategory, CategoriesWithSub)

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
            try:
                with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
                    executor.submit(
                        products_data.append({
                            'titles': item.find('h2', {'class': 'ui-search-item__title'}).text,
                            'prices': item.find('span', {'class': 'price-tag-fraction'}).text.replace(',', ''),
                            'urls': item.find('a', {'class': 'ui-search-item__group__element'})['href'],
                            'id_product': get_id(item.find('a', {'class': 'ui-search-item__group__element'})['href']),
                            'main_image': item.find('img', {'class': 'ui-search-result-image__element'})["data-src"]
                            })
                        )
            except Exception as r:
                print(r)

    except Exception as e:
        print("Error get element Ol", e)

def getInformation(soup: BeautifulSoup) -> None:
    try:
        rawItemList = soup.find_all('li', {'class': 'ui-search-layout__item'})

        for item in rawItemList:
            try:
                with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
                    executor.submit(
                        products_data.append({
                            'titles': item.find('h2', {'class': 'ui-search-item__title'}).text,
                            'prices': item.find('span', {'class': 'price-tag-fraction'}).text.replace(',', ''),
                            'urls': item.find('a', {'class': 'ui-search-item__group__element'})['href'],
                            'id_product': get_id(item.find('a', {'class': 'ui-search-item__group__element'})['href']),
                            'main_image': item.find('img', {'class': 'ui-search-result-image__element'})["data-src"]
                            })
                        )
                
            except Exception as r:
                print(r)
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
            responseNextPage = fetch_proxies(nextPage)
            if not responseNextPage:
                responseNextPage = fetch_proxies_one(nextPage)
                if not responseNextPage:
                    responseNextPage = fetch_proxies_two(nextPage)
                    if not responseNextPage:
                        responseNextPage = fetch_proxies_three(nextPage)

            soupNextPage = BeautifulSoup(responseNextPage.content, 'html.parser')
            getInformation(soupNextPage)

            nextPageResult = soupNextPage.find('a', {'class': 'andes-pagination__link', 'title': 'Siguiente'})['href']
            isNextPageResult = soupNextPage.find('a', {'class': 'andes-pagination__link', 'title': 'Siguiente'})['title']
            if nextPageResult and isNextPageResult:
                pagination(nextPageResult, isNextPageResult, '0', soupNextPage)
        except:
            print("end code")

def searchItems(link):
    try:
        responseCategory = fetch_proxies(link)
        if not responseCategory:
            responseCategory = fetch_proxies_one(link)
            if not responseCategory:
                responseCategory = fetch_proxies_two(link)
                if not responseCategory:
                    responseCategory = fetch_proxies_three(link)

        CategorySoup = BeautifulSoup(responseCategory.content, 'html.parser')
        try:
            nextPage = CategorySoup.find('a', {'class': 'andes-pagination__link'})['href']
            isNextPage = CategorySoup.find('a', {'class': 'andes-pagination__link'})['title']
            isFirstPage = CategorySoup.find('span', {'class':'andes-pagination__link'}).text

            if nextPage and isNextPage:
                pagination(nextPage, isNextPage, isFirstPage, CategorySoup)
        except:
            getInformation(CategorySoup)
            
    except:
        print("Error to get items")

def get_info(product):
    try:
        res = fetch_proxies(product['urls'])
        if not res:
            res = fetch_proxies_one(product['urls'])
            if not res:
                res = fetch_proxies_two(product['urls'])
                if not res:
                    res = fetch_proxies_three(product['urls'])

        ItemSoup = BeautifulSoup(res.content, 'html.parser')
        try:
            countSold = ItemSoup.find('span', {'class': 'ui-pdp-subtitle'}).text
            product['sold'] = countSold[10:]
        except:
            pass
        
        try:
            descriptionContent = ItemSoup.find('p', {'class': 'ui-pdp-description__content'})
            description = descriptionContent.get_text()

            if len(description) >= 100:
                product['description'] = description[:99]
            else:
                product['description'] = description
        except:
            pass
        
        try:
            imagesContent = ItemSoup.find_all('div', {'class': 'ui-pdp-thumbnail__picture'})
            
            for item in imagesContent:
                images = item.find('img', {'class': 'ui-pdp-image'})
                desc = ''
                for num in images['alt']:
                    images = item.find('img', {'class': 'ui-pdp-image'})
                    desc += num

                    first = images['data-src']
                    if desc == 'Imagen 1':
                        pass
                    if desc == 'Imagen 2':
                        product['second_image'] = first
                    if desc == 'Imagen 3':
                        product['third_image'] = first
        except:
            pass
                
    except Exception as e:
        pass


def main():
    y = datetime.datetime.now()
    print(y)
    print("Start scraping... please wait...")
    try:
        response = fetch_proxies('https://listado.mercadolibre.com.co/_CustId_'+custId)

        soup = BeautifulSoup(response.content, 'html.parser')
        name_seler = soup.find('h1', {'class': 'ui-search-breadcrumb__title'}).text[17::].replace(' ', '+')

        getLinkByCategory(soup)
        getTotalSold(name_seler)
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
                executor.map(searchItems, CategoriesWithOutSub)
        products_data.sort(reverse=True, key=lambda x:(len(x), repr(x)))
        
        for i in range(0, len(products_data)):
            try:
                if products_data[i+1]['id_product'] == products_data[i]['id_product']:
                        products_data.remove(products_data[i])
            except:
                continue

        if len(products_data) % 5000 == 0:
            time_queries = int(len(products_data) / 5000)
        else:
            time_queries = int((len(products_data) // 5000) + 1)
        
        for i in range(0, time_queries):
            with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
                    executor.map(get_info, products_data[0:4999])
        
        frame = pd.DataFrame(products_data)
        frame.to_excel(f'{name_seler}.xlsx', index=False)

    except Exception as E:
        print(E)

    x = datetime.datetime.now()
    print(x)
if __name__ == '__main__':
    main()