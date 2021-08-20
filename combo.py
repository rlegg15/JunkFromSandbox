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
  def __init__(self, parent=None, args=None, ui_filename="Combo.ui"):
    super(SelFlt, self).__init__(parent=parent, args=args, ui_filename=ui_filename)
    self.pathHere = path.dirname(sys.modules[self.__module__].__file__)
    self.ui.RfFltSel.addItems(["RF Faults over time", "Fault Stats over Time", "Faults per module by Day"])
#    dropDown = self.ui.RfFltSel.value()
    self.ui.RfFltSel.currentIndexChanged.connect(self.show_result)
        
  def show_result(self,i):
    print("current index",i,"selection changed ", self.ui.RfFltSel.currentText())
    print(self.ui.RfFltSel.currentIndex())   