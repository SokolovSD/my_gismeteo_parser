import requests
from bs4 import BeautifulSoup
import lxml
from datetime import datetime


class WeatherMaker:
    HOST = "https://www.gismeteo.ru"
    URL = "https://www.gismeteo.ru/weather-saratov-5032/2-weeks/"
    HEADERS = {
        "accept": "*/*",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
    }
    
    months_converter = {'янв': 1,
                        'фев': 2,
                        'мар': 3,
                        'апр': 4,
                        'май': 5,
                        'июн': 6,
                        'июл': 7,
                        'авг': 8,
                        'сен': 9,
                        'окт': 10,
                        'ноя': 11,
                        'дек': 12
                        }
    
    day_id = 0
    data = []
    
    def __init__(self, days):
        self.days = days
        self.__get_url_for_user()
        
    def __get_response(self, url):
        return requests.get(url, headers=WeatherMaker.HEADERS)
    
    def get_info_about_day(self):
        soup = BeautifulSoup(self.response.text, "lxml")
        date = soup.find("div", class_="tab tooltip").find("div", class_="date").text.strip()[4:].split()
        date = f'{date[0]} {WeatherMaker.months_converter.get(date[1])} {datetime.now().year}'
        date = datetime.strptime(date, '%d %m %Y')
        rainfall = soup.find("div", class_="tab tooltip").get("data-text")
        if '&nbsp;' in rainfall:
            rainfall = rainfall.replace('&nbsp;', ' ')
        
        temp_night = soup.find("div", class_="tab tooltip").find("div", class_="tab-content"). \
            find("div", class_="values").find("div", class_="value").find("span").text
        
        temp_day = soup.find("div", class_="tab tooltip").find("div", class_="tab-content"). \
            find("div", class_="values").find("div", class_="value"). \
            find_next(class_="value").find("span").text

        self.data.append({"day": date, "rainfall": rainfall, "night_t": temp_night,
                                       "day_t": temp_day})
        
    def __get_url_for_user(self):
        self.response = self.__get_response(self.URL)
        
        with open("top_page.html", "w", encoding="utf-8") as file:
            file.write(self.response.text)
        
        with open("top_page.html", encoding="utf-8") as file:
            src = file.read()
            soup = BeautifulSoup(src, "lxml")
            for i in range(self.days):
                day_link = soup.find("div", {"class": "widget__item", "data-item": f"{i}"}).find("a").get("href")
                self.response = self.__get_response(url=self.HOST + day_link)
                self.get_info_about_day()
                