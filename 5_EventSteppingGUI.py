light_color = "red"
green_time = 15
yellow_time = 5
red_time = 60

time = 0

from heapq import heappop, heappush
import sys

q = []

        

class Event:
    def __init__(self, trigger_time, color):
        self.t_time = trigger_time
        self.color = color
    def __lt__(self, other):
        return self.t_time < other.t_time
    def process(self):
        global q
        global light_color
        print("time: ", time, ": light turns ", self.color)
        light_color = self.color
        if(self.color == "red") :
            heappush(q, Event(time + red_time, "green"))
        elif(self.color == "green"):
            heappush(q, Event(time + green_time, "yellow"))
        elif(self.color == "yellow"):
            heappush(q, Event(time + yellow_time, "red"))


heappush(q, Event(time, "red"))

#simulation
def advance():
    global time
    global q
    nextEvent = heappop(q)
    time = nextEvent.t_time
    nextEvent.process()

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        global light_color
        self.setMinimumSize(QSize(800, 600))
        self.setWindowTitle("Red Light Simulation")

        self.time_disp = QLabel("time: "+str(time), self)
        self.time_disp.move(50, 100)
        self.light_disp = QLabel(light_color, self)
        self.light_disp.setStyleSheet("color: "+light_color)
        self.light_disp.move(300, 100)
        self.time_disp.adjustSize()
        self.light_disp.adjustSize()

        pybutton = QPushButton("advance", self)
        pybutton.clicked.connect(self.handleClick)
        pybutton.resize(100, 32)
        pybutton.move(100, 300)
    
    def handleClick(self):
        global light_color
        advance()
        self.time_disp.setText("time: "+str(time))
        self.light_disp.setText("light: "+light_color)
        self.light_disp.setStyleSheet("color: "+light_color)
        self.time_disp.adjustSize()
        self.light_disp.adjustSize()


app = QtWidgets.QApplication(sys.argv)
myFont = QFont()
myFont.setWeight(60)
myFont.setPointSize(24)
app.setFont(myFont, 'QLabel')
mainWin = MainWindow()
mainWin.handleClick() #advance one time
mainWin.show()

sys.exit(app.exec_())
