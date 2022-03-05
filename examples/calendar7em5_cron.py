#!/usr/bin/python
# -*- coding:utf-8 -*-

# import epd5in83bc as epdModule

import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd7in5b_V2
epdModule = epd7in5b_V2

from PIL import Image,ImageDraw,ImageFont
import traceback
import sys
from gpiozero import Button
from signal import pause

from time import localtime, strftime
import time

# from gcal.gcal import GcalHelper
import calendar
calendar.setfirstweekday(calendar.SUNDAY)
# get parent directory
curr_dir = __file__.split(__file__.split("/")[-1])[0]

from datetime import datetime
from datetime import timedelta

from gcal_getEvents import main

key1 = Button(5)
key2 = Button(6)
key3 = Button(13)
key4 = Button(19)

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

# def to_datetime(self, isoDatetime, localTZ):
#     # replace Z with +00:00 is a workaround until datetime library decides what to do with the Z notation
#     toDatetime = datetime.fromisoformat(isoDatetime.replace('Z', '+00:00'))
#     return toDatetime.astimezone(localTZ)

def merge_two_dicts(x, y):
    z = x.copy()   # start with keys and values of x
    z.update(y)    # modifies z with keys and values of y
    return z

def refreshScreen():

#   processedEvents = merge_two_dicts(main(curr_dir + "token_guerrerocarlos.json", curr_dir + "credentials.json"), main(curr_dir + "token_masterworks.json", curr_dir + "credentials.json"))
  processedEvents = main(curr_dir + "token_guerrerocarlos.json", curr_dir + "credentials.json")

  # global inited 
  # global started 
  # minutes = strftime("%M", localtime())
  # done = time.time()
  # elapsed = done - start

  # if int(inited) < 0 or int(started) < 0 or int(minutes) % 5 == 0 or int(elapsed) % 5 == 0:
  epd = epdModule.EPD()
  epd.init()
  epd.Clear()

  # epd.clear(0xFF)

  # inited = 0
  # print("\nelapsed" + str(elapsed))
  # if(tomato):
  #   print("\ntomato" + str(tomato))
  # print("\tomatoes" + str(tomatoes))

  # Drawing on the Horizontal image

  screenWidth = epdModule.EPD_WIDTH
  screenHeight = epdModule.EPD_HEIGHT

  Himage = Image.new('1', (epdModule.EPD_WIDTH, epdModule.EPD_HEIGHT), 255)  # 255: clear the frame
  HimageRed = Image.new('1', (epdModule.EPD_WIDTH, epdModule.EPD_HEIGHT), 255)  # 255: clear the frame
  # Drawing on the Vertical image
  # Limage = Image.new('1', (epdModule.EPD_WIDTH, epdModule.EPD_HEIGHT), 255)  # 255: clear the frame
  screenWidth = epdModule.EPD_WIDTH
  screenHeight = epdModule.EPD_HEIGHT

  print(sys.argv)

  # Horizontal
  draw = ImageDraw.Draw(Himage)
  drawRed = ImageDraw.Draw(HimageRed)
  # # Font: https://github.com/byrongibson/fonts/blob/master/truetype/wqy/wqy-microhei.ttc

  font = ImageFont.truetype(curr_dir + 'font.ttc', 18)
  fontSmall = ImageFont.truetype(curr_dir + 'font.ttc', 13)
  fontTiny = ImageFont.truetype(curr_dir + 'font.ttc', 10)
  # fontBig = ImageFont.truetype('font.ttc', 30)
  # fontMed = ImageFont.truetype('font.ttc', 20)
  # fontMedSmall = ImageFont.truetype('font.ttc', 18)
  # fontSmall = ImageFont.truetype('font.ttc', 15)
  # fontTiny = ImageFont.truetype('font.ttc', 10)

  # hour = strftime("%H", localtime())
  
  # # # DATE
  # # draw.text((0, 0), strftime("%a, %d %b %Y", localtime()), font = fontSmall, fill = 0)


  # titleUnderline = screenWidth
  # graphLineWidth = titleUnderline / 24

  # # DAY HOURS GRAPH
  # verticalSpace = 0
  # for h in range(1, 25):
  #   if h < int(hour):
  #     drawRed.rectangle(
  #       (0 + (int(h - 1) * graphLineWidth ), 
  #       verticalSpace , 
  #       0 + int(h - 1) * graphLineWidth + graphLineWidth - 3, 
  #       verticalSpace  + 24), 
  #       fill = 0,
  #       outline = 0)

  #   if h >= int(hour):
  #     drawRed.rectangle(
  #       (0 + (int(h - 1) * graphLineWidth ), 
  #       verticalSpace , 
  #       0 + int(h - 1) * graphLineWidth + graphLineWidth - 3, 
  #       verticalSpace  + 24), 
  #       fill = 255,
  #       outline = 0)

  #   if h == int(hour):
  #     # MINUTES PIE
  #     # piexy = {'x': int(h - 1) * graphLineWidth, 'y': verticalSpace , 'width': 20, 'height': 20}
  #     # draw.pieslice((piexy['x'], piexy['y'], piexy['x']+piexy['width'], piexy['y'] + piexy['height']), 270, 270 + (int(minutes) * 360 / 60), fill = 0, outline=0, width=1)

  #     drawRed.rectangle(
  #       (0 + (int(h - 1) * graphLineWidth ), 
  #       verticalSpace + (24 - int(minutes) * 24 / 60) , 
  #       0 + int(h - 1) * graphLineWidth + graphLineWidth - 3, 
  #       verticalSpace + 24), 
  #       fill = 0,
  #       outline = 0)

  # graphLineWidth = titleUnderline / 4

  # # POMODORO GRAPH
  # graphqlVerticalWidth = graphLineWidth / 2
  # for p in range(0, 4):
  #   if p < tomato:
  #     draw.rectangle((
  #       p * graphLineWidth, 
  #       30, 
  #       p * graphLineWidth + graphLineWidth - 3,
  #       30 + graphqlVerticalWidth), 
  #       fill = 0,
  #       outline = 0)

  #   if p >= tomato:
  #     draw.rectangle((
  #       p * graphLineWidth, 
  #       30, 
  #       p * graphLineWidth + graphLineWidth - 3,
  #       30 + graphqlVerticalWidth), 
  #       fill = 255,
  #       outline = 0)

  #   if p == tomato:
  #     draw.rectangle((
  #       p * graphLineWidth, 
  #       30, 
  #       p * graphLineWidth + ((graphLineWidth - 3) * elapsed / (25 * 60)) ,
  #       30 + graphqlVerticalWidth), 
  #       fill = 0,
  #       outline = 0)

  # # HOUR
  # hourSize = 40
  # fontHour = ImageFont.truetype('font.ttc', hourSize)
  # hourText = strftime("%H:%M", localtime())
  # draw.text((screenWidth - hourSize * len(hourText) / 2, screenHeight - hourSize), hourText, font = fontHour, fill = 0)

  # # Show parameter lines
  # lines = sys.argv[1].split("\n")

  # for i in range(0, len(lines)):
  #   draw.text((0, (screenHeight - len(lines) * 15) + (i * 15)), lines[i], font = fontTiny, fill = 0)

  # gcalService = GcalHelper()
  # eventList = gcalService.retrieve_events(calendars, calStartDatetime, calEndDatetime, displayTZ, thresholdHours)

  today = datetime.today()
  todayWeekday = today.weekday() + 1

  firstDayOfMonth = today - timedelta(days = today.day)

  year = today.year
  month = today.month
  day = today.day

  dow = calendar.day_name[today.weekday()]

  print(today - timedelta(days = (todayWeekday)))

  showWeeks = 6
  vSpan = screenHeight / showWeeks / 8 * 7
  hSpan = screenWidth / 7

  lines = []

  # Top Square
  drawRed.rectangle((
    0,
    0, 
    screenWidth, 
    vSpan - 20), 
    fill = 0,
    outline = 0) 

  drawRed.text((5,-1), today.strftime("%A, %d %B %Y"), font = ImageFont.truetype(curr_dir + 'font.ttc', 40), fill = 255, align = "left")

  for dayCount in range(0, 7 * showWeeks):
    drawDay = today + timedelta(days = (+ dayCount - (today.day + firstDayOfMonth.weekday() + 1)))

    lines = []
    for eventDate in processedEvents: 
      if eventDate.find(drawDay.isoformat()[:10]) != -1:
          # print(datetime.fromisoformat(eventDate))
          # print(event, processedEvents[eventDate])
          # print(eventDate, processedEvents[eventDate]['summary'].encode('utf-8'))
          lines.append((eventDate[11:13] + " "+processedEvents[eventDate]['summary'].encode("ascii","ignore")))
    lines.sort()

    # drawRed.text((30 * dayCount,20), today.strftime("%A"), font = ImageFont.truetype(curr_dir + 'font.ttc', 40), fill = 0, align = "left")
    # if dayCount < 7:
    #   draw.text(
    #     (hSpan * dayCount + 3,
    #       vSpan - 20), 
    #     drawDay.strftime("%A")[0:3], 
    #     # "DAY", 
    #     font = ImageFont.truetype(curr_dir + 'font.ttc', 16), 
    #     fill = 0)

    if drawDay.month == today.month: 
      draw.rectangle((
        (dayCount % 7) * hSpan, 
        (dayCount / 7) * vSpan + vSpan, 
        (dayCount % 7) * hSpan + hSpan + (4 if dayCount % 7 == 6 else 0) , 
        (dayCount / 7) * vSpan + vSpan + vSpan), 
        fill = 255,
        outline = 0)   

      for l in range(0, len(lines)):
        drawRed.text(((dayCount % 7) * hSpan + 3, vSpan + vSpan * (dayCount / 7) + 20 + l * 10), lines[l], font = fontTiny, fill = (0 if drawDay.day == today.day else 255), align = "left")

      for l in range(0, len(lines)):
        draw.text(((dayCount % 7) * hSpan + 3, vSpan + vSpan * (dayCount / 7) + 20 + l * 10), lines[l], font = fontTiny, fill = (0 if not drawDay.day == today.day else 255), align = "left")

      if(drawDay.day == today.day):   
        drawRed.rectangle((
          (dayCount % 7) * hSpan, 
          (dayCount / 7) * vSpan + vSpan, 
          (dayCount % 7) * hSpan + hSpan , 
          (dayCount / 7) * vSpan + vSpan + vSpan), 
          fill = 0,
          outline = 0)  

        for l in range(0, len(lines)):
          drawRed.text(((dayCount % 7) * hSpan + 3, vSpan + vSpan * (dayCount / 7) + 20 + l * 10), lines[l], font = fontTiny, fill = (0 if not drawDay.day == today.day else 255), align = "left")

        draw.rectangle(
          (0,
          vSpan - 20, 
          screenWidth, 
          vSpan), 
          fill = 0,
          outline = 0) 

        draw.text(
            (3,
            vSpan - 20), 
          " | ".join(lines), 
          # "DAY", 
          font = ImageFont.truetype(curr_dir + 'font.ttc', 16), 
          fill = 255)

      drawRed.text(((dayCount % 7) * hSpan + 3, vSpan + vSpan * (dayCount / 7)), str(drawDay.day), font = font, fill = (0 if not drawDay.day == today.day else 255), align = "left")

    else:
      draw.rectangle((
        (dayCount % 7) * hSpan + 1, 
        (dayCount / 7) * vSpan + vSpan + 1, 
        (dayCount % 7) * hSpan + hSpan - 1, 
        (dayCount / 7) * vSpan + vSpan + vSpan - 1), 
        fill = 255,
        outline = 255) 

      draw.text(((dayCount % 7) * hSpan + 3, vSpan + vSpan * (dayCount / 7)), str(drawDay.day), font = font, fill = 0, align = "left")

      for l in range(0, len(lines)):
        draw.text(((dayCount % 7) * hSpan + 3, vSpan + vSpan * (dayCount / 7) + 20 + l * 10), lines[l], font = fontTiny, fill = 0, align = "left")


  # draw.text((10, screenHeight / 2 + 5), "chao", font = font, fill = 255)

  epd.display(epd.getbuffer(Himage), epd.getbuffer(HimageRed))
      
  # logging.info("Clear...")
  # epd.init()
  # epd.Clear()

  # logging.info("Goto Sleep...")
  # epd.sleep()

  #   drawRed.rectangle((
  #   0, 
  #   0, 
  #   screenWidth, 
  #   screenHeight * 3 / 4), 
  #   fill = 0,
  #   outline = 0)

  # drawRed.text((10,10), "hola", font = font, fill = 255)
  # drawRed.text((10, screenHeight / 2 + 5), "hola", font = font, fill = 255)



# key1.when_pressed = handleButton
# key2.when_pressed = handleButton
# key3.when_pressed = handleButton
# key4.when_pressed = handleButton

try:
  refreshScreen()
  # set_interval(refreshScreen, 60)
  # pause()
except:
  print('traceback.format_exc():\n%s' % traceback.format_exc())
  exit()


