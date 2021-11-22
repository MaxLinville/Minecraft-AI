import keyboard
import pynput
import time
import math
import sys
import numpy as np
import pyautogui
import pydirectinput as pyd
import threading
import cv2
import pytesseract

from threading import Thread
from random import seed
from random import random
from pynput.keyboard import Key, Listener, Controller as KeyboardController
from pynput.mouse import Button, Controller as MouseController
from PIL import Image, ImageDraw, ImageGrab

keyb = KeyboardController()
mouse = MouseController()
Active = False

event = threading.Event()

x = abs(np.random.normal(0.25,0.1,None))
div = 4

#Boolean variables
isInInventory = False

def get_color_at_pixel(i_x, i_y):
    import PIL.ImageGrab
    return PIL.ImageGrab.grab().load()[i_x, i_y]

def press_left():
    pyd.keyDown('a')

def release_left():
    pyd.keyUp('a')

def press_right():
    pyd.keyDown('d')

def release_right():
    pyd.keyUp('d')

def press_forward():
    pyd.keyDown('w')

def release_forward():
    pyd.keyUp('w')

def press_backward():
    pyd.keyDown('s')

def release_backward():
    pyd.keyUp('s')

def press_crouch():
    pyd.keyDown('shift')

def release_crouch():
    pyd.keyUp('shift')

def hold_jump():
    pyd.keyDown('space')

def stop_jump():
    pyd.keyUp('space')

def jump():
    pyd.keyDown('space')
    event.wait(abs(np.random.normal(0.07896,0.02,None)))
    pyd.keyUp('space')

def toggleDebug():
    pyd.keyDown('f3')
    wait_until(abs(np.random.normal(0.07896,0.02,None)))
    pyd.keyUp('f3')

def click():
    pyd.mouseDown()
    z = np.random.normal(0.07,0.02,None)
    print(z)
    time.sleep(z)
    pyd.mouseUp()

def mine():
    pyd.mouseDown()

def stop_mine():
    pyd.mouseUp()

def place():
    pyd.mouseDown(button='right')

def stop_place():
    pyd.mouseUp(button='right')

def rotate(x, y):
    wait_until(1/60)
    mouse.move(x,y)

def smoothAccel(degrees, rotatedirection = "+", axis = "x"):
    px = 10*degrees
    if rotatedirection == "+" and axis == "x":
        n = 0
        totalinc = 0
        inc = 0
        final_inc = 0
        rotation_time = np.random.normal(0.5,0.075,None)
        interval = int(rotation_time*60)
        if interval%2 == 1:
            interval += -1
        for i in range(interval):
            diff = px-totalinc
            if i < interval/2:
                inc = int((px*(-1*math.cos(2*math.pi*((i+1)/interval))+1))/interval)
                totalinc += inc
                mouse.move(inc,0)
                time.sleep(1/60)
            elif i < interval-4:
                inc = int((px*(-1*math.cos(2*math.pi*((i+1)/interval))+1))/interval)
                if inc > 4:
                    mouse.move(inc,0)
                    final_inc = inc
                    totalinc += inc
                else:
                    continue
                time.sleep(1/60)
        while diff > 0:
            if final_inc == 0:
                final_inc = 1
            if diff % final_inc == 0:
                mouse.move(final_inc,0)
                time.sleep(1/60)
                totalinc += final_inc
            elif diff > final_inc: 
                mouse.move(final_inc,0)
                time.sleep(1/60)
                totalinc += final_inc
            else:
                mouse.move(diff % final_inc,0)
                time.sleep(1/60)
                totalinc += diff % final_inc
            diff = px - totalinc
    elif rotatedirection == "-" and axis == "x":
        n = 0
        totalinc = 0
        inc = 0
        final_inc = 0
        rotation_time = np.random.normal(0.5,0.075,None)
        interval = int(rotation_time*60)
        if interval%2 == 1:
            interval += -1
        for i in range(interval):
            diff = px-totalinc
            if i < interval/2:
                inc = int((px*(-1*math.cos(2*math.pi*((i+1)/interval))+1))/interval)
                totalinc += inc
                mouse.move(-inc,0)
                time.sleep(1/60)
            elif i < interval-4:
                inc = int((px*(-1*math.cos(2*math.pi*((i+1)/interval))+1))/interval)
                if inc > 4:
                    mouse.move(-inc,0)
                    final_inc = inc
                    totalinc += inc
                else:
                    continue
                time.sleep(1/60)
        while diff > 0:
            if final_inc == 0:
                final_inc = 1
            if diff % final_inc == 0:
                mouse.move(-final_inc,0)
                time.sleep(1/60)
                totalinc += final_inc
            elif diff > final_inc: 
                mouse.move(-final_inc,0)
                time.sleep(1/60)
                totalinc += final_inc
            else:
                mouse.move(-1*(diff % final_inc),0)
                time.sleep(1/60)
                totalinc += diff % final_inc
            diff = px - totalinc
    if rotatedirection == "-" and axis == "y":
        n = 0
        totalinc = 0
        inc = 0
        final_inc = 0
        rotation_time = np.random.normal(0.5,0.075,None)
        interval = int(rotation_time*60)
        if interval%2 == 1:
            interval += -1
        for i in range(interval):
            diff = px-totalinc
            if i < interval/2:
                inc = int((px*(-1*math.cos(2*math.pi*((i+1)/interval))+1))/interval)
                totalinc += inc
                mouse.move(0,inc)
                time.sleep(1/60)
            elif i < interval-4:
                inc = int((px*(-1*math.cos(2*math.pi*((i+1)/interval))+1))/interval)
                if inc > 4:
                    mouse.move(0,inc)
                    final_inc = inc
                    totalinc += inc
                else:
                    continue
                time.sleep(1/60)
        while diff > 0:
            if final_inc == 0:
                final_inc = 1
            if diff % final_inc == 0:
                mouse.move(0,final_inc)
                time.sleep(1/60)
                totalinc += final_inc
            elif diff > final_inc: 
                mouse.move(0,final_inc)
                time.sleep(1/60)
                totalinc += final_inc
            else:
                mouse.move(0,diff % final_inc)
                time.sleep(1/60)
                totalinc += diff % final_inc
            diff = px - totalinc
    elif rotatedirection == "+" and axis == "y":
        n = 0
        totalinc = 0
        inc = 0
        final_inc = 0
        rotation_time = np.random.normal(0.5,0.075,None)
        interval = int(rotation_time*60)
        if interval%2 == 1:
            interval += -1
        for i in range(interval):
            diff = px-totalinc
            if i < interval/2:
                inc = int((px*(-1*math.cos(2*math.pi*((i+1)/interval))+1))/interval)
                totalinc += inc
                mouse.move(0,-inc)
                time.sleep(1/60)
            elif i < interval-4:
                inc = int((px*(-1*math.cos(2*math.pi*((i+1)/interval))+1))/interval)
                if inc > 4:
                    mouse.move(0,-inc)
                    final_inc = inc
                    totalinc += inc
                else:
                    continue
                time.sleep(1/60)
        while diff > 0:
            if final_inc == 0:
                final_inc = 1
            if diff % final_inc == 0:
                mouse.move(0,-final_inc)
                time.sleep(1/60)
                totalinc += final_inc
            elif diff > final_inc: 
                mouse.move(0,-final_inc)
                time.sleep(1/60)
                totalinc += final_inc
            else:
                mouse.move(0,-1*(diff % final_inc))
                time.sleep(1/60)
                totalinc += diff % final_inc
            diff = px - totalinc

def wait_until(time_in_seconds: float):
    interval = time_in_seconds*div

    iterations = round(interval - (interval % 1))
    for i in range(iterations):
        if keyboard.is_pressed(']') == False:
            event.wait(1/div)
        elif keyboard.is_pressed(']') == True:
            sys.exit()
    event.wait(interval % 1)

#while Active == False:
 #   if keyboard.is_pressed('['):
 #       Active = True
  #      print("Activated")
   # else:
    #    pass

def locate_block():
    block = text_map()[0]
    info = block.split()
    block_coords = []
    try: 
        block_coords = [int(info[3]), int(info[4]), int(info[5])]
    except IndexError:
        block_coords = []
    except ValueError:
        block_coords = [int(info[3].replace('Block=', '')), int(info[4]), int(info[5])]
    return(block_coords)

def text_map():
    # Path of tesseract executable
    #pytesseract.pytesseract.tesseract_cmd ='C:\Program Files\Tesseract-OCR\tesseract'
    # ImageGrab-To capture the screen image in a loop. 
    # Bbox used to capture a specific area.
    cap = ImageGrab.grab(bbox = (1920, 600, 3840, 1200))
    cap2 = cv2.cvtColor(np.array(cap), cv2.COLOR_BGR2GRAY)
    (irrelevant, blocksimagepre) = cv2.threshold(cap2, 220, 255, cv2.THRESH_TOZERO)
    (irrelevant, blocksimage) = cv2.threshold(blocksimagepre, 221, 255, cv2.THRESH_TOZERO_INV)

    cap3 = ImageGrab.grab(bbox = (0, 630, 1920, 740))
    cap4 = cv2.cvtColor(np.array(cap3), cv2.COLOR_BGR2GRAY)
    (irrelevant, coordsimagepre) = cv2.threshold(cap4, 220, 255, cv2.THRESH_TOZERO)
    (irrelevant, coordsimage) = cv2.threshold(coordsimagepre, 221, 255, cv2.THRESH_TOZERO_INV)

    #ADD A THRESHOLD TO CONVERT ALL PIXELS LOWER THAN 220 TO 0 BLACK FOLLOWED BY PIXELS BRIGHTER THAN 220 TO 0 BLACK

    cap5 = ImageGrab.grab(bbox = (0, 680, 1920, 740))
    cap6 = cv2.cvtColor(np.array(cap5), cv2.COLOR_BGR2GRAY)
    (irrelevant, dirimagepre) = cv2.threshold(cap6, 220, 255, cv2.THRESH_TOZERO)
    (irrelevant, directionimage) = cv2.threshold(dirimagepre, 221, 255, cv2.THRESH_TOZERO_INV)
    #cv2.imshow('ooga', blocksimage)
    #cv2.waitKey(0)
    # Converted the image to monochrome for it to be easily 
    # read by the OCR and obtained the output String.

    blocks = pytesseract.image_to_string(blocksimage, lang ='mc')
    coords = pytesseract.image_to_string(coordsimage, lang = 'mc')
    direction = pytesseract.image_to_string(directionimage, lang = 'mc')

    coords = coords.replace(',', '.')
    direction = direction.replace(',', '.')

    return(blocks, coords, direction)

def find_log():
    total_rotation = 0
    while total_rotation <= 190:
        blocks = text_map()[0]
        if blocks.find("log") != -1 or blocks.find("leaves") != -1:
            print("there be logs here")
            break
        else:
            #print("no logs in these here parts")
            smoothAccel(20, "+")
            #print(text_map()[0])
            total_rotation = total_rotation + 1
            print(total_rotation)
    if total_rotation >= 190:
        press_forward()
        wait_until(10)
        release_forward()
    else:
        print("here ye here ye")
        target = locate_block()
        go_to(target[0], target[1], target[2])
        collect_tree()

def collect_tree():
    mine()
    wait_until(5)
    stop_mine()
    smoothAccelY(80, '-')
    mine()
    wait_until(3.5)
    stop_mine()
    smoothAccelY(80, '+')
    smoothAccelY(100, '+')
    mine()
    wait_until(3.5)
    stop_mine()
    smoothAccelY(100, '-')

def get_coords():
    randomjunk = text_map()[1].split()
    coord_list = [randomjunk[1], randomjunk[2], randomjunk[3]]
    for i in range(3):
        try: 
            coord_list[i] = coord_list[i].replace('S', '5')
        except ValueError:
            print("Here is the string that broke the program: ")
            print(coord_list)
        except IndexError:
            print("Comglom")
            print(coord_list)
    return(coord_list)

def get_rotation():
    morerandomjunk = text_map()[2].split()
    print(morerandomjunk)
    angle_list = [morerandomjunk[4].replace('(', ''), (morerandomjunk[6].replace(')', '')).rstrip('.')]
    cardinal = morerandomjunk[1]

    return(angle_list, cardinal)

def go_to(x_target, y_target, z_target):
    pos = (int(get_coords()[0]), int(get_coords()[2]))
    difference = (0, 0)
    try:
        difference = ((pos[0]-x_target), (pos[1]-z_target))
    except TypeError:
        print(get_coords())
    distance = (difference[0]**2 + difference[1]**2)**(1/2)
    angle = 0
    if difference[0] > 0:
        angle = (math.atan(difference[1]/difference[0]))*(57.3) + 90
    elif difference[0] < 0:
        angle = (math.atan(difference[1]/difference[0]))*(57.3) - 90
    elif difference[1] > 0: #for some reason confirming that the x distance is 0 just skips these, probably type thing idk
        angle = 180
    elif difference[1] < 0:
        angle = 0
    else: #this has some mystical mumbo jumbo but triggers when at destination block now
        pass

    yaw = int(round(float(get_rotation()[0][0])))
    rotation_difference = yaw-angle
    while abs(rotation_difference) >= 1.5:
        rotation_difference = int(round(float(get_rotation()[0][0]))) - angle
        if rotation_difference >= 1.5:
            smoothAccel(round(math.log(rotation_difference))*28, "-")
        elif -358.5 <= rotation_difference <= -1.5:
            smoothAccel(round(math.log(abs(rotation_difference)))*28, "+")
    if distance > 10:
        press_forward()
        wait_until(distance/5)
        release_forward()
    elif 10 > distance > 0:
        press_forward()
        wait_until(distance/20)
        release_forward()
    else:
        pass

    return(distance, angle, yaw)

def home_axes():
    for i in range(5):
        yaw = (float(get_rotation()[0][0]))
        if yaw < 0:
            smoothAccel(abs(yaw),"+")
        else:
            smoothAccel(abs(yaw), "-")
    for i in range(5):
        pitch = (float(get_rotation()[0][1]))
        if pitch < 0:
            smoothAccel(abs(pitch),"-", "y")
        else:
            smoothAccel(abs(pitch), "+", "y")
    '''pyd.keyDown("t")
    time.sleep(1/60)
    pyd.keyUp("t")'''

def add(x,y):
    x+=str(y)
    return x

def add_2(x,y):
    if y % 20000 == 0:
        z=[]
        for q in range(0,400000):
            z.append(q)

def build_nxn_platform(n):
    home_axes()
    press_crouch()
    press_backward()
    press_right()
    time.sleep(1)
    release_right()
    release_backward()
    press_left()
    half_time()
    release_left()
    smoothAccel(80, "-",  "y")
    for i in range(n):
        if i%2 == 0:
            build_line(n)
            smoothAccel(90, "-")
            build_line(1)
            smoothAccel(90, "-")
        else:
            build_line(n)
            smoothAccel(90)
            build_line(1)
            smoothAccel(90)
    release_crouch()


def build_line(n):
    press_backward()
    place()
    if 1 < n <= 3:
        time.sleep(((n-1)-0.129819)/1.30142)
    elif n == 1:
        time.sleep(0.61)
    else:
        time.sleep((n*0.774-0.127)/(1/((-0.673318/n)+1.03125)))
    release_backward()
    stop_place()

def testline(n):
    home_axes()
    press_crouch()
    press_backward()
    press_right()
    time.sleep(1)
    release_right()
    release_backward()
    press_left()
    half_time()
    release_left()
    smoothAccel(80, "-",  "y")
    build_line(n)
    release_crouch()

def half_time():
    time.sleep(0.5)

def main():
    minutes = 4
    for i in range(minutes):
        press_right()
        press_forward()
        mine()
        time.sleep(60+np.random.normal(5,1,None))
        stop_mine()
        release_right()
        release_forward()

if __name__ == '__main__':
    #import cProfile
    #cProfile.run('main()')
    wait_until(3)
    main()