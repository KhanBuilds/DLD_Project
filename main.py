import cv2
import serial
import time
FRAME_WIDTH=640
FRAME_HEIGHT= 480
FOV_X = 60
FOV_Y = 48
degrees_per_pixelx= FOV_X/FRAME_WIDTH
degrees_per_pixely= FOV_Y/FRAME_HEIGHT
servo_pos_x=90
servo_pos_y=90
arduino = serial.Serial('COM3', 115200, timeout=0.1)
time.sleep(2)
cascade_path= cv2.data.haarcascades
face_cascade_path= cascade_path + 'haarcascade_frontalface_default.xml'

face_cascade=cv2.CascadeClassifier(face_cascade_path)
cap= cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

if face_cascade.empty():
    print("Error could not load cascade file")

else:
    print("Loaded xml file successfully")
    while cap.isOpened():
        ret, frame=cap.read()
        if ret:


            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x,y), (x+w, y+h), (255, 0, 0), 2)
                cv2.imshow('Frame', frame)
                if len(faces) > 0:

                    (x, y, w, h) = faces[0]
                    face_center_x= x + (w // 2)
                    center_face_y = y + (h // 2)

                    screen_center_x= FRAME_WIDTH // 2
                    screen_center_y = FRAME_HEIGHT // 2

                    pixel_error_x=face_center_x - screen_center_x
                    pixel_error_y=center_face_y- screen_center_y

                    angle_offset_x= pixel_error_x * degrees_per_pixelx
                    angle_offset_y= pixel_error_y * degrees_per_pixely

                    new_servo_pos_x= 90 - angle_offset_x
                    new_servo_pos_y=90 - angle_offset_y



                    if new_servo_pos_x > 180: new_servo_pos_x = 180
                    if new_servo_pos_x < 0: new_servo_pos_x = 0

                    if new_servo_pos_y > 180: new_servo_pos_y = 180
                    if new_servo_pos_y < 0: new_servo_pos_y = 0
                    #print(f"Face center:{face_center_x}, X angle: {int(new_servo_pos_x)}")
                    servo_pos_x = new_servo_pos_x
                    servo_pos_y = new_servo_pos_y
                    #print(f"X Angle: {int(servo_pos_x)}, Y Angle: {int(servo_pos_y)}")
                    arduino.write(bytes([int(new_servo_pos_x), int(new_servo_pos_y)]))
                    cv2.waitKey(1)


        else:
            print('Video not loaded check for errors!')
    cap.release()
    cv2.destroyAllWindows()