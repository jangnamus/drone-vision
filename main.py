from djitellopy import tello
import time
from time import sleep
import key_press_module as kp
import cv2
import yolo
import ctypes
import multiprocessing
import speech





def get_keyboard_input():
    lr, fb, ud, yv = 0, 0, 0, 0
    halt, land, takeoff = False, False, False
    speed = 50

    if kp.get_key("LEFT"): lr = -speed
    elif kp.get_key("RIGHT"): lr = speed

    if kp.get_key("UP"): fb = speed
    elif kp.get_key("DOWN"): fb = -speed

    if kp.get_key("w"): ud = -speed
    elif kp.get_key("s"): ud = speed

    if kp.get_key("a"): yv = -speed
    elif kp.get_key("d"): yv = speed

    if kp.get_key("h"):
        halt = True
    else:
        halt = False

    if kp.get_key("q"): 
        land = True
    else:
        land = False
        
    if kp.get_key("l"): 
        takeoff = True
    else:
        takeoff = False

    if kp.get_key("t"): 
        lr *= 2
        fb *= 2
        ud *= 2
        yv *= 2
    
    return [lr, fb, ud, yv], [halt, land, takeoff]



def control(tookoff, landed, started_filming):
    kp.init()
    me = tello.Tello()
    me.connect()
    print("battery: ", me.get_battery())
    me.streamon()
    print("stream on")
    print("OK to fly")
    print("Takeoff in 5 seconds")
    sleep(5)
    me.takeoff()
    sleep(0.5)
    tookoff.value = True
    while True:
        values, commands = get_keyboard_input()
        halt, land, takeoff = commands
        me.send_rc_control(values[0], values[1], values[2], values[3])
        if halt:
            me.send_rc_control(0, 0, 0,0 )
        if land:
            if tookoff.value:
                me.send_rc_control(0, 0, 0, 0)
                me.land()
            landed.value = True
            kp.destroy_py_game_window()
            sleep(5)
            me.streamoff()
            return
        if takeoff:
            me.takeoff()
        
        img = me.get_frame_read().frame
        cas = time.time()
        cas = str(round(cas))
        full_path_photos_folder = "C:\\Users\\jangn\\Documents\\Tello\\drone_project\\photos\\"
        file_name = full_path_photos_folder + cas + ".jpg"
        cv2.imwrite(file_name, img)
        started_filming.value = True
        cv2.waitKey(1)
        sleep(0.1)
        print("battery: ", me.get_battery())



def process_photos(tookoff, landed, started_filming):
    delay = 1
    while not (started_filming.value):
        sleep(1)
    sleep(delay)                  # necessary in order to ensure that control() function 
                                  # creates .jpg file before this function reads it
    while True: 
        if landed.value == True:
            print("LAND COMMAND -> quitting camera")
            sleep(0.1)
            return
        cas = time.time() - delay
        cas = str(round(cas))
        full_path_photos_folder = "C:\\Users\\jangn\\Documents\\Tello\\drone_project\\photos\\"
        file_name = full_path_photos_folder + cas
        filename_ext = file_name + ".jpg"
        processed_image, detected_objects = yolo.yolo(filename_ext)
        new_file = file_name + "processed" + ".jpg"
        cv2.imwrite(new_file, processed_image)
        speech_object = speech.Speech(detected_objects)
        sentence = speech_object.create_sentence("I see ")      # voice output, e.g. "I see a book, a chair and a person."
        speech_object.speak(sentence)







# Shared variables between processes
tookoff = multiprocessing.Value(ctypes.c_bool, False)
landed = multiprocessing.Value(ctypes.c_bool, False)
started_filming = multiprocessing.Value(ctypes.c_bool, False)



p1 = multiprocessing.Process(target=control, args=[tookoff, landed, started_filming])
p2 = multiprocessing.Process(target=process_photos, args=[tookoff, landed, started_filming])


if __name__ == '__main__':
    p1.start()
    p2.start()

    p1.join()
    p2.join()

    p1.terminate()
    p2.terminate()

    print("Both processes terminated")
