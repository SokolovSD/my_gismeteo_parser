from engine_weather_web_parser import WeatherMaker
from engine_database import InteractorWithDB
from engine_database import Weather
from engine_image_maker import ImageMaker
from datetime import date


class WeatherAPP:
    main_menu = """
    1. Запрос погоды
    2. Работа с базой данных
    3. Выход
    """
    
    data_base_menu = """
    1. Вывести полученные прогнозы в консоль
    2. Создать открытки из полученных прогнозов
    """
    
    def weather_request(self, days_count):
        parsing = WeatherMaker(days_count)
        parsing_data = parsing.data.copy()
        parsing.data.clear()
        return parsing_data
    
    def saver_into_db(self, data_parsing):
        saver = InteractorWithDB(Weather)
        saver.save(data_parsing)
        print('\nДанные сохранены в базу данных\n')

    def get_data_from_db(self, start, finish, first=True):
        getter = InteractorWithDB(Weather)
        return getter.get_from_db(start, finish, first)
    
    def show_data_from_db(self, data):
        print()
        if not data:
            print("Данных нет")
        for day in data:
            print(f"""Дата: {day.get('day')}
                  Осадки: {day.get('rainfall')}
                  Температура ночью: {day.get('night_t')}
                  Температура днем: {day.get('day_t')}""")
            print("***\n")
    
    def draw_postcard(self, data_from_db):
        painter = ImageMaker(data_from_db)
        painter.test()
        
    def main(self):
        print("Приветствую в программе с прогнозами погоды!")
        today = date.today()
        today = f"{today.year}-{today.month}-{today.day}"
        last_week = self.get_data_from_db(start=today, finish=today)
        self.show_data_from_db(last_week)
        while True:
            print(self.main_menu)
            answer = input("Выберите пункт меню: ")
            if answer == '1':
                days_count = int(input("\nВведите количество дней, для которых нужны данные (max. = 10): "))
                parsing_data = self.weather_request(days_count)
                print("Данные получены\n")
                step_2 = input("Сохранить данные в базу данных? (Y/N): ")
                if step_2.upper() == 'Y':
                    self.saver_into_db(parsing_data)
                else:
                    print('\nДанные не сохранены\n')

            if answer == '2':
                print("Введите начальную и конечную дату в формате: ")

                a = f"{input('введите год: ')}-{input('введите месяц: ')}-{input('введите день: ')}"
                b = f"{input('введите год: ')}-{input('введите месяц: ')}-{input('введите день: ')}"

                data_db = self.get_data_from_db(a, b, first=False)
                print(self.data_base_menu)
                answer = input("Выберите пункт меню: ")
                
                if answer == '1':
                    self.show_data_from_db(data_db)
                
                if answer == '2':
                    self.draw_postcard(data_db)
            
            if answer == '3':
                print("Пока!")
                break
