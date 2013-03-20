import sys
import xml.etree.ElementTree as xml
import serial
import cv


class drilleye():

    def __init__(self, camno):
        self.camera = camno
        self.capture = None
        self.image = None
        self.cvfont = cv.InitFont(cv.CV_FONT_HERSHEY_DUPLEX, 0.5, 0.5)
        self.xoffset = 0
        self.yoffset = 0
        self.dia = 10
        self.stretch = 0
        self.stroke = 1
        self.serial = None#serial.Serial("/dev/ttyACM0")
        # key code assignment to function
        self.keys = {   1048603 : self.quit,        # ESC
                        1048608 : self.drill,       # SPACE
                        1048690 : self.reset,       # r
                        1376084 : self.strokeminus, #
                        1376082 : self.strokeplus,
                        1179476 : self.stretchminus,
                        1179474 : self.stretchplus,
                        1048621 : self.diaminus,
                        1114155 : self.diaplus,
                        1113938 : self.crossup, 
                        1113940 : self.crossdown, 
                        1113939 : self.crossright,
                        1113937 : self.crossleft
                    }

    def init_cam(self):
        try:
            cv.NamedWindow("drillEye", 1)
            cv.MoveWindow("drillEye", 288, 0)
            self.capture = cv.CreateCameraCapture(self.camera)
        except Exception, e:
            print("Error: %s" % e)
            exit(0)


    def get_frame(self):
        self.image = cv.QueryFrame(self.capture)
        if self.image == None:
            print("Error: Webcam not found!")
            exit(0)


    def update(self):
        target = cv.CreateImage((800,600), self.image.depth, self.image.nChannels)
        cv.Resize(self.image,target, cv.CV_INTER_AREA)
        cv.ShowImage("drillEye", target)   

           
    def handle_keys(self):
        key = cv.WaitKey(10)
        if key in self.keys:
            self.keys[key]()
        elif key != -1:
            print(key)

        
    def draw_info(self):    
        cv.PutText(self.image, "X-Offset: %s Y-Offset: %s Size: %s Stretch: %s" % (self.xoffset, self.yoffset, self.dia, self.stretch, ), (10,15), self.cvfont, cv.RGB(255, 255, 255))
        

    def draw_crosshair(self):
        hcenter = self.image.width / 2 + self.yoffset
        vcenter = self.image.height / 2 + self.xoffset
        #draw horizontal Line
        cv.Line(self.image, (0, vcenter), (self.image.width, vcenter), cv.RGB(255, 0, 0), self.stroke, cv.CV_AA, 0)
        #draw vertical Line
        cv.Line(self.image, (hcenter, 30), (hcenter, self.image.height), cv.RGB(255, 0, 0), self.stroke, cv.CV_AA, 0)
        #draw upper half-circles
        for i in range(0,4):
            cv.Ellipse(self.image, (hcenter,vcenter - self.stretch), (self.dia * i,self.dia * i), 0, 180, 360, cv.RGB(255, 0, 0), self.stroke, cv.CV_AA, 0) 
        #draw connecting lines id streched
        if self.stretch > 0:
            for i in range(1,4):            
                cv.Line(self.image, (hcenter + self.dia * i, vcenter - self.stretch), (hcenter + self.dia * i, vcenter + self.stretch), cv.RGB(255, 0, 0), self.stroke, cv.CV_AA, 0)
                cv.Line(self.image, (hcenter - self.dia * i, vcenter - self.stretch), (hcenter - self.dia * i, vcenter + self.stretch), cv.RGB(255, 0, 0), self.stroke, cv.CV_AA, 0)
        #draw lower half-circles
        for i in range(0,4):
            cv.Ellipse(self.image, (hcenter,vcenter + self.stretch), (self.dia * i,self.dia * i), 180, 180, 360, cv.RGB(255, 0, 0), self.stroke, cv.CV_AA, 0) 


    def strokeplus(self):
        if self.stroke < 10:
            self.stroke = self.stroke + 1


    def strokeminus(self):
        if self.stroke > 1:
            self.stroke = self.stroke - 1
    

    def stretchplus(self):
        if self.stretch < 100:
            self.stretch = self.stretch + 1


    def stretchminus(self):
        if self.stretch > 0:
            self.stretch = self.stretch - 1
    

    def diaplus(self):
        if self.dia < 100:
            self.dia = self.dia + 1


    def diaminus(self):
        if self.dia > 5:
            self.dia = self.dia - 1


    def crossup(self):
        self.xoffset = self.xoffset - 1


    def crossdown(self):
        self.xoffset = self.xoffset + 1

    
    def crossleft(self):
        self.yoffset = self.yoffset - 1


    def crossright(self):
        self.yoffset = self.yoffset + 1

    def drill(self):
        self.serial.write("a")    
    
    def reset(self):
        self.xoffset = 0
        self.yoffset = 0
        self.dia = 10
        self.stretch = 0
        self.stroke = 1

    def quit(self):
        print("Bye :-)")
        exit(0)




if __name__ == "__main__":
    helpargs = ["h","H","-h","--h","-H","--H"]
    if len(sys.argv) > 1:
        if sys.argv[1] in helpargs:
            print(" -- drilleye help -- ")
            print(" usage: python drillEye.py <camera number> (camera number is optional, default is 0) ")
            print(" leftarrow          : adjust crosshair position to the left ")
            print(" rightarrow         : adjust crosshair position to the right ")
            print(" uparrow            : adjust crosshair position upwards ")
            print(" downarrow          : adjust crosshair position downwards ")
            print(" Shift + leftarrow  : increase crosshair diameter ")
            print(" Shift + rightarrow : decrease crosshair diameter ")
            print(" Shift + uparrow    : inkrease crosshair stretch ")
            print(" Shift + downarrow  : decrease crosshair stretch ")
            print(" r                  : reset all corrections to default ")
            print(" ESC                : Quit program ")
            exit(1) 
        elif sys.argv[1].isdigit:
            cam = int(sys.argv[1])
    else:
        cam = 0

    drilleye = drilleye(cam)
    drilleye.init_cam()

    while True:
        drilleye.get_frame()
        drilleye.draw_info()
        drilleye.draw_crosshair()
        drilleye.update()
        drilleye.handle_keys() 
