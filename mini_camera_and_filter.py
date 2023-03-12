import cv2 as cv
import numpy as np
import time

video = cv.VideoCapture(0)

def mouse_event_handler(event, x, y, flags, param):
    # Change 'mouse_state' (given as 'param') according to the mouse 'event'
    if event == cv.EVENT_LBUTTONDOWN:
        param[0] = True
        param[1] = (x, y)
    elif event == cv.EVENT_LBUTTONUP:
        param[0] = False
    elif event == cv.EVENT_MOUSEMOVE and param[0]:
        param[1] = (x, y)


if video.isOpened():
    # Get FPS and calculate the waiting time in millisecond
    fps = video.get(cv.CAP_PROP_FPS)
    wait_msec = int(1 / fps * 1000)

    while True:
        # Read an image from WebCam
        valid, img = video.read()
        if not valid:
            print("No Camera Data")
            break

        # Show the image
        cv.putText(img, 'Press "enter" to capture', (8, 20), cv.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 0), thickness=2)
        cv.putText(img, 'Press "enter" to capture', (8, 20), cv.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), thickness=1)
        cv.imshow('Step1: Capture', img)

        # Terminate if the given key is ESC
        key = cv.waitKey(wait_msec)
        
        if key == 27: # ESC
            break
        elif key == 13: # Enter
            cv.imwrite('img/captured_image.png', img)
            break
        
    video.release()
    cv.destroyAllWindows()
    
    first_point = (0,0)
    last_point = (0,0)
    
    mouse_state = [False, (-1, -1)] # Note) [mouse_left_button_click, mouse_xy]
    mouse_click_count = 0
    saved_img = cv.imread('img/captured_image.png')

    contrast = 1
    contrast_step = 0.01
    brightness = 0
    brightness_step = 1
    
    while True:
        if saved_img is not None:
            saved_img = contrast * saved_img + brightness # Alternative) cv.equalizeHist(), cv.intensity_transform
            saved_img[saved_img < 0] = 0
            saved_img[saved_img > 255] = 255 # Saturate values
            saved_img = saved_img.astype(np.uint8)

            cv.imshow('Step2: Edit Image', saved_img)
            cv.setMouseCallback('Step2: Edit Image', mouse_event_handler, mouse_state)
            mouse_left_button_click, mouse_xy = mouse_state
            
            if (mouse_left_button_click == True) and (mouse_click_count==0):
                first_point = mouse_xy
                mouse_click_count = 1
                time.sleep(0.1)
                
            elif (mouse_left_button_click == True) and (mouse_click_count==1):
                last_point = mouse_xy
                mouse_click_count = 2

            elif (mouse_click_count==2):
                sliced_img = saved_img[first_point[1]:last_point[1], first_point[0]:last_point[0]]
                cv.imwrite('img/edited_image.png', sliced_img)
                mouse_click_count = 0
                cv.destroyAllWindows()
                break

            elif key == ord('r'): # if you want restore click state, press r to make first_point and last_point (0,0)
                first_point = (0,0)
                last_point = (0,0)
                mouse_click_count = 0
                cv.destroyAllWindows()

            elif key == ord('i'): # at the photoshop, this option key is 'ctrl+i'
                saved_img = 255 - saved_img # Alternative) cv.bitwise_xor()
                cv.imwrite('img/edited_image.png', saved_img)
            
            elif key == ord('+') or key == ord('='):
                contrast += contrast_step

            elif key == ord('-') or key == ord('_'):
                contrast -= contrast_step

            elif key == ord(']') or key == ord('}'):
                brightness += brightness_step

            elif key == ord('[') or key == ord('{'):
                brightness -= brightness_step

            elif key == 27: # ESC
                break

            key = cv.waitKey(wait_msec)