from pydm import Display
from PyQt5.QtGui import QStandardItem
from PyQt5.QtWidgets import (QWidgetItem, QCheckBox, QPushButton, QLineEdit,
                             QGroupBox, QHBoxLayout, QMessageBox, QWidget,
                             QLabel, QFrame, QComboBox)
from os import path, pardir
from qtpy.QtCore import Slot
#from pydm.widgets.template_repeater import PyDMTemplateRepeater
from typing import List, Dict
from functools import partial, reduce
from datetime import datetime, timedelta
from requests import post
from csv import reader
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

sys.path.insert(0, '..')

DEFAULT_AMPLITUDE = 16.608


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class Q0Measurement(Display):
    def __init__(self, parent=None, args=None, ui_filename="q0.ui"):

        super(Q0Measurement, self).__init__(parent=parent, args=args,
                                            ui_filename=ui_filename)

        self.pathHere = path.dirname(sys.modules[self.__module__].__file__)

        def getPath(fileName):
            return path.join(self.pathHere, fileName)

        sc = MplCanvas(self, width=5, height=4, dpi=100)
        # TODO get rid of meaningless test data
        sc.axes.plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])
        self.calibrationResultsWindow = Display(ui_filename=getPath("results.ui"),
                                                macros={"label": "dLL/dt Slope"})
        self.calibrationResultsWindow.ui.dataLayout.addWidget(sc)

        self.settingsWindow = Display(ui_filename=getPath("settings.ui"))
        self.setupSettingsWindow()

        self.liveSignalsWindow = Display(ui_filename=getPath("signals.ui"))
        self.ui.liveSignalsButton.clicked.connect(partial(self.showDisplay,
                                                          self.liveSignalsWindow))

        self.calibrationOptionsWindow = Display(ui_filename=getPath("options.ui"))
        self.calibrationOptionsWindow.ui.cryomoduleComboBox.activated.connect(self.populatecalibrationOptions)
        self.calibrationOptionsWindow.ui.optionTable.resizeColumnsToContents()

        self.setupButtons()

        self.calibrationStatus = None
        self.setupLabels()

        self.calibrationFrame = None
        self.rfFrame = None
        self.setupFrames()

        self.selectWindow = Display(ui_filename=getPath("cmSelection.ui"))
        self.ui.cmSelectButton.clicked.connect(partial(self.showDisplay,
                                                       self.selectWindow))

        self.pathToAmplitudeWindow = getPath("amplitude.ui")

        # maps cryomodule names to their checkboxes
        self.cryomoduleCheckboxes = {}  # type: Dict[str, QCheckBox]

        # maps cryomodule names to their buttons
        self.cryomoduleButtons = {}  # type: Dict[str, QPushButton]

        # maps checkboxes to their buttons
        self.cryomoduleCheckboxButtonMap = {}  # type: Dict[QCheckBox, QPushButton]

        # maps cryomodule names to the cavity display
        self.buttonDisplays = {}  # type: Dict[str, Display]

        # maps cyomodule names to desired cavity amplitudes
        self.desiredCavAmps = {}  # type: Dict[str, List[QLineEdit]]

        # maps cryomodule names to cavity groupboxes
        self.cavityGroupBoxes = {}  # type: Dict[str, List[QGroupBox]]

        # maps cryomodule names to select all cavities checkbox
        self.selectAllCavitiesCheckboxes = {}  # type: Dict[str, QCheckBox]

        self.selectedDisplayCMs = set()
        self._selectedFullCMs = set()

        self.sectors = [[], [], [], []]  # type: List[List[str]]
        self.selectAllCheckboxes = [self.selectWindow.ui.selectAllCheckboxL0B,
                                    self.selectWindow.ui.selectAllCheckboxL1B,
                                    self.selectWindow.ui.selectAllCheckboxL2B,
                                    self.selectWindow.ui.selectAllCheckboxL3B]  # type: List[QCheckBox]

        self.checkboxSectorMap = {}  # type: Dict[QCheckBox, int]

        #self.populateCheckboxes()

        for sector in self.sectors:
            self.calibrationOptionsWindow.ui.cryomoduleComboBox.addItems(sector)

        self.sanityCheck = QMessageBox()
        self.setupSanityCheck()

    def populatecalibrationOptions(self):
        self.calibrationOptionsWindow.ui.optionTable.clearContents()
        parent = path.abspath(path.join(self.pathHere, pardir))
        cmName = self.calibrationOptionsWindow.ui.cryomoduleComboBox.currentText()
        calFolderPath = path.join(path.join(parent, "calibrations"),
                                  "cm{NAME}".format(NAME=cmName))
        print(calFolderPath)
        baseFile = path.join(calFolderPath,
                             "calibrationsCM{NAME}.csv".format(NAME=cmName))

        with open(baseFile, "rb") as fileInput:
            for row in reader(fileInput):
                items = [QStandardItem(field) for field in row]
                self.model.appendRow(items)
        return

    def setupFrames(self):
        name2frame = {}  # type: Dict[str, QFrame]
        for frame in self.ui.dialogues.findChildren(QFrame):
            if frame.accessibleName():
                name2frame[frame.accessibleName()] = frame
        self.calibrationFrame = name2frame["calibrationFrame"]
        self.rfFrame = name2frame["rfFrame"]

    def setupLabels(self):
        name2label = {}  # type: Dict[str, QLabel]
        for label in self.ui.dialogues.findChildren(QLabel):
            name2label[label.accessibleName()] = label
        self.calibrationStatus = name2label["calibrationLabel"]

    def setupButtons(self):
        name2button = {}  # type: Dict[str, QPushButton]
        # Get all the buttons from my template repeater and figure out which
        # one's which with the accessible names (set in dialogues.json)
        for button in self.ui.dialogues.findChildren(QPushButton):
            name2button[button.accessibleName()] = button
        name2button["newCalibrationButton"].clicked.connect(self.takeNewCalibration)
        name2button["loadCalibrationButton"].clicked.connect(partial(self.showDisplay,
                                                                     self.calibrationOptionsWindow))
        name2button["calibrationDataButton"].clicked.connect(partial(self.showDisplay,
                                                                     self.calibrationResultsWindow))

    def setupSettingsWindow(self):
        self.settingsWindow.ui.valvePosSearchStart.setDateTime(datetime.now())
        self.settingsWindow.ui.valvePosSearchEnd.setDateTime(datetime.now()
                                                             - timedelta(hours=24))
        self.ui.settingsButton.clicked.connect(partial(self.showDisplay,
                                                       self.settingsWindow))

    #def populateCheckboxes(self):


    def setupSanityCheck(self):
        def takeMeasurement(decision):
            if "No" in decision.text():
                print("Measurement canceled")
                return
            else:
                print("Taking new measurement")
                self.showDisplay(self.liveSignalsWindow)
                self.calibrationStatus.setStyleSheet("color: blue;")
                self.calibrationStatus.setText("Starting Calibration")

        self.sanityCheck.setWindowTitle("Sanity Check")
        self.sanityCheck.setText("Are you sure? This will take multiple hours")
        self.sanityCheck.setIcon(QMessageBox.Warning)
        self.sanityCheck.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        self.sanityCheck.setDefaultButton(QMessageBox.No)
        self.sanityCheck.buttonClicked.connect(takeMeasurement)

    @Slot()
    def takeNewCalibration(self):
        self.sanityCheck.show()

    @Slot()
    def showDisplay(self, display):
        # type: (QWidget) -> None
        display.show()

        # brings the display to the front
        display.raise_()

        # gives the display focus
        display.activateWindow()

    @Slot()
    # TODO needs to check all cavities
    def cavityToggled(self, cm):
        # type: (str) -> None

        statusList = list(map(lambda groupbox: groupbox.isChecked(),
                              self.cavityGroupBoxes[cm]))
        allChecked = reduce((lambda isChecked1, isChecked2: isChecked1 and isChecked2),
                            statusList)

        if statusList.count(statusList[0]) != len(statusList):
            self.selectAllCavitiesCheckboxes[cm].setCheckState(1)

        else:
            self.selectAllCavitiesCheckboxes[cm].setCheckState(0 if not allChecked else 2)

        self.updateOutputBasedOnDefaultConfig(cm, allChecked)

    @Slot()
    # TODO use AMAX/ops limit
    def checkIfAllCavitiesAtDefault(self, cm, updateOutput=True):
        # type: (str, bool) -> bool

        isDefault = True

        for lineEdit in self.desiredCavAmps[cm]:
            if lineEdit.text():
                try:
                    amplitude = float(lineEdit.text())
                    if amplitude != DEFAULT_AMPLITUDE:
                        isDefault = False
                        break

                except ValueError:
                    lineEdit.clear()
                    isDefault = False
                    break
            else:
                isDefault = False
                break

        if updateOutput:
            self.updateOutputBasedOnDefaultConfig(cm, isDefault)

        return isDefault

    # TODO put sector logic in here
    def updateOutputBasedOnDefaultConfig(self, cm, isDefault):
        starredName = "{CM}*".format(CM=cm)

        if isDefault:
            if starredName in self.selectedDisplayCMs:
                self.selectedDisplayCMs.add(cm)
                self.selectedDisplayCMs.discard(starredName)
        else:
            if cm in self.selectedDisplayCMs:
                self.selectedDisplayCMs.discard(cm)
                self.selectedDisplayCMs.add(starredName)

        self.updateSelectedText()


    @Slot()
    def selectAllCavitiesToggled(self, cm):
        state = self.selectAllCavitiesCheckboxes[cm].checkState()

        if state == 0:
            for cavityGroupbox in self.cavityGroupBoxes[cm]:
                cavityGroupbox.setChecked(False)
        elif state == 2:
            for cavityGroupbox in self.cavityGroupBoxes[cm]:
                cavityGroupbox.setChecked(True)

    @Slot()
    # TODO use ops max
    def restoreDefault(self, desiredAmplitude):
        # type: (QLineEdit) -> None

        desiredAmplitude.setText(str(DEFAULT_AMPLITUDE))

    def updateSelectedText(self):
        if not self.selectedDisplayCMs:
            self.ui.cmSelectionLabel.setStyleSheet("color: red;")
            self.ui.cmSelectionLabel.setText("No Cryomodules Selected")
            self.calibrationFrame.setEnabled(False)
            self.rfFrame.setEnabled(False)

        else:
            self.ui.cmSelectionLabel.setStyleSheet("color: green;")
            self.ui.cmSelectionLabel.setText(str(sorted(self.selectedDisplayCMs))
                                             .replace("'", "").replace("[", "")
                                             .replace("]", ""))
            self.calibrationFrame.setEnabled(True)

    @Slot()
    # TODO check if all checkboxes in sector are clicked
    def cryomoduleCheckboxToggled(self, cryomodule):
        # type:  (str) -> None

        checkbox = self.cryomoduleCheckboxes[cryomodule]
        button = self.cryomoduleButtons[cryomodule]

        sector = self.checkboxSectorMap[checkbox]
        selectAllCheckbox = self.selectAllCheckboxes[sector]

        state = selectAllCheckbox.checkState()
        sectorLabel = "L{SECTOR}B*".format(SECTOR=sector)

        if checkbox.isChecked():
            self._selectedFullCMs.add(cryomodule)
            button.setEnabled(True)

            isDefault = (self.checkIfAllCavitiesAtDefault(cryomodule, False)
                         if cryomodule in self.desiredCavAmps else True)

            if state == 0:
                selectAllCheckbox.setCheckState(1)
                self.selectedDisplayCMs.add(cryomodule if isDefault
                                            else cryomodule + "*")

            elif state == 1:
                self.selectedDisplayCMs.add(cryomodule if isDefault
                                            else cryomodule + "*")

            else:
                if not isDefault:
                    self.selectedDisplayCMs.add(sectorLabel)

        else:
            self._selectedFullCMs.discard(cryomodule)
            button.setEnabled(False)

            if state == 2:
                selectAllCheckbox.setCheckState(1)
                self.selectedDisplayCMs.discard(sectorLabel)
                self.selectedDisplayCMs.discard("L{SECTOR}B".format(SECTOR=sector))

                for sectorCryomodule in self.sectors[sector]:
                    isDefault = (self.checkIfAllCavitiesAtDefault(sectorCryomodule, False)
                                 if sectorCryomodule in self.desiredCavAmps
                                 else True)
                    self.selectedDisplayCMs.add(sectorCryomodule
                                                if isDefault
                                                else (sectorCryomodule + "*"))

            self.selectedDisplayCMs.discard(cryomodule + "*")
            self.selectedDisplayCMs.discard(cryomodule)

        self.updateSelectedText()

    @Slot()
    def selectAllSectorCryomodules(self, selectAllCheckbox, sector):
        # type:  (QCheckBox, int) -> None

        sectorLabel = "L{SECTOR}B".format(SECTOR=sector)

        if selectAllCheckbox.checkState() == 2:

            for name in self.sectors[sector]:
                self.cryomoduleCheckboxes[name].setChecked(True)
                self.selectedDisplayCMs.discard(name)

            if (sectorLabel + "*") not in self.selectedDisplayCMs:
                self.selectedDisplayCMs.add(sectorLabel)

        elif selectAllCheckbox.checkState() == 0:
            for name in self.sectors[sector]:
                self.cryomoduleCheckboxes[name].setChecked(False)

            self.selectedDisplayCMs.discard(sectorLabel)
            self.selectedDisplayCMs.discard(sectorLabel + "*")

        self.updateSelectedText()
