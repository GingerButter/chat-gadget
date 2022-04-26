import random
import numpy as np
import cv2



class Stream:
    def randPic(self):
        num = random.randint(1,3)
        return "./static/dwitter/flowers"+str(num)

    def toBinary(self):
        path = "/home/andyj/Desktop/SLED/chat/dwitter/ss.png"
        img = cv2.imread(path)
        cv2.imshow("img",img)
        _, jpeg = cv2.imencode('.png', img)
        return jpeg.tobytes()

    def test(self):
        with open("/home/andyj/Desktop/SLED/chat/dwitter/ss.png") as image:
            f= image.read()
            image = np.asarray(bytearray(f))
            image = cv2.imdecode(image, 0)
            cv2.imshow("output", image)


def gen(stream):
    while True:
        binary = stream.toBinary(stream.randPic())
        yield (b'--binary\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + binary + b'\r\n\r\n')

info = "3821393298403598403825984239234035484998422132392134400098233821334639353449983536984038259825214940"
sum = 0
original = ""
for i in range(0, len(info), 2):
    ask = ((int(info[i])+4)%10)*10 + ((int(info[i+1])+4)%10)
    print(chr(ask), end='')
    # sum += ((int(i)+4)%10)
    # original += str((int(i)+4)%10)
# print(original)
