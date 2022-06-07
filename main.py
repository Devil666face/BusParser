import time, sqlite3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

if __name__ == '__main__':
    driver = webdriver.Chrome('/usr/bin/chromedriver')
    urls = []
    with open('allurls.txt','r') as file:
        urls=file.read().split('\n')
    for url in urls:
        driver.get(url=url)
        print(driver.current_url)
        bus = driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div[2]/div[2]/div/div[1]/div/div/div/div/div[1]/div[2]/div[3]/div[2]/h1/span/span').text.replace('Автобус ','')
        name = driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div[2]/div[2]/div/div[1]/div/div/div/div/div[1]/div[2]/div[3]/div[2]/div/span').text.replace('→','-')
        area = driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div[2]/div[2]/div/div[1]/div/div/div/div/div[2]/div/div[1]/div[3]/div[2]/div/div[1]/div[2]')
        area.click()

        temp_list = []
        station_list = []
        stations = driver.find_elements(By.CLASS_NAME,'_tqhgas')
        print(bus, name)

        with sqlite3.connect('database.db') as DB:

            insert_query = f"INSERT INTO bus VALUES ({bus},'{name}');"
            cursor = DB.cursor()
            cursor.execute(insert_query)
            DB.commit()

            create_query = f"CREATE TABLE bus{bus} (station TEXT);"
            cursor = DB.cursor()
            cursor.execute(create_query)
            DB.commit()

        for station in stations:
            try:
                temp_list.append(station.text)
            except Exception as ex:
                print(ex)

        [station_list.append(x) for x in temp_list if x not in station_list]

        for station in station_list:
            print(station)
            with sqlite3.connect('database.db') as DB:
                insert_query = f"INSERT INTO bus{bus} VALUES ('{station}');"
                cursor = DB.cursor()
                cursor.execute(insert_query)
                DB.commit()
    # hrefs = [#'https://2gis.ru/tver/search/0%20%D0%B0%D0%B2%D1%82%D0%BE%D0%B1%D1%83%D1%81/route/6615267543089177?m=35.901982%2C56.845734%2F12.02',
    #          # 'https://2gis.ru/tver/search/0%20%D0%B0%D0%B2%D1%82%D0%BE%D0%B1%D1%83%D1%81/page/2/route/6615267543089177?m=35.901982%2C56.845734%2F12.02',
    #          # 'https://2gis.ru/tver/search/0%20%D0%B0%D0%B2%D1%82%D0%BE%D0%B1%D1%83%D1%81/page/3/route/6615267543089177?m=35.901982%2C56.845734%2F12.02',
    #          # 'https://2gis.ru/tver/search/0%20%D0%B0%D0%B2%D1%82%D0%BE%D0%B1%D1%83%D1%81/page/4/route/6615267543089177?m=35.901982%2C56.845734%2F12.02',
    #          # 'https://2gis.ru/tver/search/0%20%D0%B0%D0%B2%D1%82%D0%BE%D0%B1%D1%83%D1%81/page/5/route/6615267543089177?m=35.901982%2C56.845734%2F12.02',]
    #          'https://2gis.ru/tver/search/0%20%D0%B0%D0%B2%D1%82%D0%BE%D0%B1%D1%83%D1%81/page/6/route/6615267543089262?m=35.91908%2C56.815636%2F15.62',
    #          'https://2gis.ru/tver/search/0%20%D0%B0%D0%B2%D1%82%D0%BE%D0%B1%D1%83%D1%81/page/7/route/6615267543089245?m=35.91908%2C56.815636%2F15.62',]
    # url_list = []
    # for url in hrefs:
    #     driver.get(url=url)
    #     time.sleep(3)
    #     print(driver.current_url)
    #     cards = driver.find_elements(By.XPATH,'/html/body/div[2]/div/div/div[1]/div[1]/div[2]/div[1]/div/div[2]/div/div/div/div[2]/div[2]/div[1]/div/div/div/div[3]')
    #     cards_str = str(cards[0].text).split('\n')
    #
    #     elements = driver.find_elements(By.TAG_NAME,'a')
    #     for element in elements:
    #         try:
    #             if element.get_attribute('href').find('https://2gis.ru/tver/route/')>=0:
    #                 href = str(element.get_attribute('href'))
    #                 url_list.append(href)
    #                 print(href)
    #         except Exception as ex:
    #             print(ex)
    #
    # with open('urls.txt','w') as file:
    #     for line in url_list:
    #         file.write(f'{line}\n')
    #     # with sqlite3.connect('database.db') as DB:
    #     #     print("База подключена")
    #     #     bus_list = []
    #     #     for i in range (0,len(cards_str),2):
    #     #         try:
    #     #             list = []
    #     #             list.append(cards_str[i])
    #     #             list.append(cards_str[i+1])
    #     #             bus_list.append(list)
    #     #         except Exception as ex:
    #     #             print(ex)
    #     #
    #     #     for list in bus_list:
    #     #         if (list[0].find('Автобус ')>=0):
    #     #             bus = int(list[0].replace('Автобус ',''))
    #     #             name = list[1].replace('→','-')
    #     #             # insert_query = f"INSERT INTO bus VALUES ({bus},'{name}');"
    #     #             # cursor = DB.cursor()
    #     #             # cursor.execute(insert_query)
    #     #             # DB.commit()
    #     #             print(bus, name)

    driver.quit()