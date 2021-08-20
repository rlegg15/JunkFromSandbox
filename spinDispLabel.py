#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 13 08:54:17 2021

@author: user
"""

from pydm import Display
from PyQt5.QtGui import QStandardItem
from PyQt5.QtWidgets import (QWidgetItem, QCheckBox, QPushButton, QLineEdit,
                             QGroupBox, QHBoxLayout, QMessageBox, QWidget,
                             QLabel, QFrame, QComboBox, QRadioButton)
from os import path, pardir
from datetime import datetime, timedelta
import sys



class SelFlt(Display):
  def __init__(self, parent=None, args=None, ui_filename="sel.ui"):
    super(SelFlt, self).__init__(parent=parent, args=args, ui_filename=ui_filename)
    self.pathHere = path.dirname(sys.modules[self.__module__].__file__)
    spinner = self.ui.spinBox_2.value()
    self.ui.spinBox_2.valueChanged.connect(self.show_result)
  def show_result(self):
    dispOptions = ['Display selector', 'Flt Counts', 'Flt Statistics', 'XFEL Display']  
    spinVal = self.spinBox_2.value()
    dispVal = dispOptions[spinVal]
    self.ui.lab_1.setText(dispVal)

        