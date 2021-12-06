import re
import requests
from bs4 import BeautifulSoup
import numpy as np
from cv2 import cv2
import datetime
import re


class ImageMaker:
    img = cv2.imread("pics/probe.jpg")
    count = 0
    
    def __init__(self, data_from_db):
        self.data = data_from_db
    
    def test(self):
        for day in self.data:
            day_name = day['day']
            rainfall = day['rainfall']
            back = 'pics/probe.jpg'

            if re.search(r'асмурно', rainfall) or re.search(r'блачно', rainfall):
                if re.search(r'нег', rainfall):
                    pic = "pics/snow.jpg"
                elif re.search(r'ожд', rainfall):
                    pic = "pics/rain.jpg"
                else:
                    pic = "pics/cloud.jpg"
                b, g, r = (128, 128, 128)
                step_b = 1
                step_g = 1
                step_r = 1

            elif re.search(r'олнечно', rainfall):
                pic = "pics/sun.jpg"
                b, g, r = (0, 255, 255)
                step_b = 2.5
                step_g, step_r = 0, 0
            elif re.search(r'нег', rainfall):
                pic = "pics/snow.jpg"
                b, g, r = (255, 200, 0)
                step_b = 0
                step_g = 0.5
                step_r = 2.5
            elif re.search(r'ожд', rainfall):
                pic = "pics/rain.jpg"
                b, g, r = (255, 0, 0)
                step_b = 0
                step_g, step_r = 2.5, 2.5

            background = self.draw_background(b, g, r, step_b, step_g, step_r, back)

            new_pic = self.add_img_on_background(pic, background)
            new_pic_2 = self.draw_text(new_pic, day)
            self.saver_pic(new_pic_2, day_name)
            
    def draw_background(self, b, g, r, step_b, step_g, step_r, back):
        w_start = 0
        w_next = 5
        for i in range(110):
            self.img[:, w_start:w_next] = b, g, r
            w_start, w_next = w_next, w_next + 5
            b += step_b
            g += step_g
            r += step_r

        return self.img
    
    def add_img_on_background(self, pic, back):
        img_pic = cv2.imread(pic)
        img_bg = back
        probe_h, probe_w, channels_bg = img_bg.shape
        img_pic_h, img_pic_w, channels = img_pic.shape
        roi = img_bg[:img_pic_h, probe_w - img_pic_w:]
        new = cv2.addWeighted(roi, 0.4, img_pic, 0.5, 0.3)
        img_bg[:img_pic_h, probe_w - img_pic_w:] = new

        return img_bg

    def draw_text(self, pic, day):
        day_t = day['day_t'].replace('-', "-")
        night_t = day['night_t'].replace('−', "-")
    
        final = cv2.putText(pic, f"{day['day'].day}/{day['day'].month} {day['rainfall']}", (0, 30),
                            cv2.FONT_HERSHEY_COMPLEX, 1.3, (0, 0, 0), 2)
    
        final = cv2.putText(pic, f"{day_t}/{night_t}", (0,200), cv2.FONT_HERSHEY_COMPLEX, 2.5, (0, 0, 0), 4)
        cv2.imshow('last', final)
        cv2.waitKey()
        return final
            
    def saver_pic(self, new_pic_2, day_name):
        cv2.imwrite(f"pics/postcards/{ImageMaker.count}_{day_name}.jpg", new_pic_2)
        print('открытка сохранена')
        ImageMaker.count += 1
        
    def show_img(self, img):
        a = cv2.imread(img)
        cv2.imshow("weather", a)
        cv2.waitKey()
