#!/usr/bin/python
# -*- coding:utf-8 -*-

from waveshare_epd import epd7in5b_V2
epdModule = epd7in5b_V2
import math

from PIL import Image,ImageDraw,ImageFont
import traceback
import sys
import gpiozero 
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

from signal import pause

from time import localtime, strftime
import time

import calendar
curr_dir = __file__.split(__file__.split("/")[-1])[0]

from datetime import datetime
from datetime import timedelta

from gcal_getEvents import main

tomatoes = [0,0,0,0]
start = time.time()
tomato = -1
inited = -1
started = -1

import threading

def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

def handleButton(button):
    global start
    global started
    start = time.time()
    tomatoes[0] = 0
    tomatoes[1] = 0
    tomatoes[2] = 0
    tomatoes[3] = 0
    global tomato
    print(button)
    started = 0
    print(button.pin.number)
    if button.pin.number == 5:
      tomato = 0
    elif button.pin.number == 6:
      tomato = 1
    elif button.pin.number == 13:
      tomato = 2      
    elif button.pin.number == 19:
      tomato = 3 
    refreshScreen()

def merge_two_dicts(x, y):
    z = x.copy()   # start with keys and values of x
    z.update(y)    # modifies z with keys and values of y
    return z

def refreshScreen():

  processedEvents = main(curr_dir + "token_guerrerocarlos.json", curr_dir + "credentials.json")

  epd = epdModule.EPD()
  epd.init()

  screenWidth = epdModule.EPD_WIDTH
  screenHeight = epdModule.EPD_HEIGHT

  Himage = Image.new('1', (epdModule.EPD_WIDTH, epdModule.EPD_HEIGHT), 255)  # 255: clear the frame
  HimageRed = Image.new('1', (epdModule.EPD_WIDTH, epdModule.EPD_HEIGHT), 255)  # 255: clear the frame
  screenWidth = epdModule.EPD_WIDTH
  screenHeight = epdModule.EPD_HEIGHT -1

  print(sys.argv)

  draw = ImageDraw.Draw(Himage)
  drawRed = ImageDraw.Draw(HimageRed)

  font = ImageFont.truetype(curr_dir + 'font.ttc', 20)
  fontSmall = ImageFont.truetype(curr_dir + 'font.ttc', 16)
  fontTiny = ImageFont.truetype(curr_dir + 'font.ttc', 11)

  today = datetime.today()
  todayWeekday = today.weekday() + 1

  firstDayOfMonth = today - timedelta(days = today.day)

  year = today.year
  month = today.month
  day = today.day

  dow = calendar.day_name[today.weekday()]

  print(today - timedelta(days = (todayWeekday)))

  showWeeks = 6
  vSpan = screenHeight / showWeeks / 7 * 7
  hSpan = screenWidth / 7

  lines = []

  shown_months = []

  for dayCount in range(0, 7 * showWeeks):
    drawDay = today + timedelta(days = (+ dayCount - (today.day + firstDayOfMonth.weekday() + 1)))

    lines = []
    for eventDate in processedEvents: 
      if eventDate.find(drawDay.isoformat()[:10]) != -1:
          print(processedEvents[eventDate]['summary'])
          lines.append((eventDate[11:16] + " "+processedEvents[eventDate]['summary']))
    lines.sort()

    if drawDay.month == today.month: 
      draw.rectangle((
        (dayCount % 7) * hSpan, 
        math.floor(dayCount / 7) * vSpan, 
        # (dayCount % 7) * hSpan + hSpan + (4 if dayCount % 7 == 6 else 0) , 
        (dayCount % 7) * hSpan + hSpan, 
        math.floor(dayCount / 7) * vSpan + vSpan), 
        fill = 255,
        outline = 0)   

      for l in range(0, len(lines)):
        drawRed.text(((dayCount % 7) * hSpan + 3,  vSpan * math.floor(dayCount / 7) + 20 + l * 10), lines[l], font = fontTiny, fill = (0 if drawDay.day == today.day else 255), align = "left")

      for l in range(0, len(lines)):
        draw.text(((dayCount % 7) * hSpan + 3,  vSpan * math.floor(dayCount / 7) + 20 + l * 10), lines[l], font = fontTiny, fill = (0 if not drawDay.day == today.day else 255), align = "left")

      if(drawDay.day == today.day):   
        drawRed.rectangle((
          (dayCount % 7) * hSpan, 
          math.floor(dayCount / 7) * vSpan , 
          (dayCount % 7) * hSpan + hSpan , 
          math.floor(dayCount / 7) * vSpan + vSpan), 
          fill = 0,
          outline = 0)  

        for l in range(0, len(lines)):
          drawRed.text(((dayCount % 7) * hSpan + 3, vSpan * math.floor(dayCount / 7) + 20 + l * 10), lines[l], font = fontTiny, fill = (0 if not drawDay.day == today.day else 255), align = "left")

      label = str(drawDay.day)
      if(drawDay.day == 1 or drawDay.day == today.day):
        label = str(drawDay.day) + "º " + calendar.month_name[drawDay.month]

      drawRed.text(((dayCount % 7) * hSpan + 3, vSpan * math.floor(dayCount / 7)), label, font = font, fill = (0 if not drawDay.day == today.day else 255), align = "left")
      shown_months.append(drawDay.month)
    else:
      draw.rectangle((
        (dayCount % 7) * hSpan, 
        math.floor(dayCount / 7) * vSpan, 
        (dayCount % 7) * hSpan + hSpan, 
        math.floor(dayCount / 7) * vSpan + vSpan), 
        fill = 255,
        outline = 0) 

      label = str(drawDay.day)
      if(drawDay.day == 1):
        label = str(drawDay.day) + "º " + calendar.month_name[drawDay.month]

      draw.text(((dayCount % 7) * hSpan + 3, vSpan * math.floor(dayCount / 7)), label, font = font, fill = 0, align = "left")
      shown_months.append(drawDay.month)

      for l in range(0, len(lines)):
        draw.text(((dayCount % 7) * hSpan + 3, vSpan * math.floor(dayCount / 7) + 20 + l * 10), lines[l], font = fontTiny, fill = 0, align = "left")


  # draw.text((10, screenHeight / 2 + 5), "chao", font = font, fill = 255)

  epd.display(epd.getbuffer(Himage), epd.getbuffer(HimageRed))
      
  epd.sleep()

try:
  refreshScreen()
  # set_interval(refreshScreen, 60)
  # pause()
except:
  print('traceback.format_exc():\n%s' % traceback.format_exc())
  exit()


