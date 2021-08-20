#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 12 09:10:09 2021

@author: user
"""
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtCore
import sys
 
def display():
    global count
    count += 1
    if count > 5:
        print("Finished")
        timer.stop()
        return
    print("Hello World")
 
count = 0
app = QApplication(sys.argv)
#app = QCoreApplication::exec()
#win = QMainWindow()
#win.setGeometry(400,400,300,300)
#win.setWindowTitle("CodersLegacy")
  
timer = QtCore.QTimer()
timer.timeout.connect(display)
timer.start(1000)
 
 
#win.show()
#app.exec_()
sys.exit(app.exec_())

