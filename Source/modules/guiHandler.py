'''
GUI Handler Module
This module defines and handles all the GUI elements and operations
'''

import os
import sys
from datetime import datetime

from modules import fileHandler
from modules import plotHandler

from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QRadioButton
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QListWidget
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem


'''
fileSelectGroup class defines all the GUI elements and operations
related to the csv file selection section of the application window
'''
class fileSelectGroup(QGroupBox):

    '''
    fileSelectGroup class constructor initializes the file selection
    section of the application window
    This function sets the group title and adds the required GUI elements
    in a vertical layout
    '''
    def __init__(self):
        super(fileSelectGroup, self).__init__()

        # Set the title and vertical layout
        self.setTitle('Select Folder')
        self.groupElements = QVBoxLayout()
        self.setLayout(self.groupElements)

        # Add a push button to select the folder and attach 
        # a function to handle the folder selection
        self.folderSelectButton = QPushButton('Select Folder')
        self.folderSelectButton.clicked.connect(self.openFolderHandler)
        self.groupElements.addWidget(self.folderSelectButton)

        # Add a list box to display the list of csv files and
        # attach a function to process the selected file
        self.fileListBox = QListWidget()
        self.fileListBox.itemClicked.connect(self.fileSelectHandler)
        self.groupElements.addWidget(self.fileListBox)

        # Add a spacer at the bottom to ensure all the GUI elements
        # will be aligned to the top even when the window is resized
        self.groupElements.addStretch(1)


    '''
    openFolderHandler function is responsible for collecting the
    absolute path and the list of csv file in that location
    This function calls the loadData function in the file handler
    module to read the path and file list
    If the file list is not empty, it populates the list box with
    the list of csv file names in the selected folder
    This function resizes the width of the group box based on the
    maximum characters in the longest file name
    This function also resizes the height of the file list based on 
    the total number of csv files in the folder
    '''
    def openFolderHandler(self):
        # Read the folder path and file list from the file handler
        self.folderpath, self.fileList = fileHandler.loadData()
        # Clear any existing items in the file list box
        self.fileListBox.clear()

        # If the file list is empty
        if not self.fileList:
            # Show a message saying no CSV files in the folder
            self.fileListBox.addItem('CSV Files not found in the selected folder')
        # If the file list is not empty
        else:
            # Add each file name to the file list box
            for file in self.fileList:
                self.fileListBox.addItem(file)
        
        self.setMinimumWidth(self.fileListBox.sizeHintForColumn(0) + (20 * self.fileListBox.frameWidth()))
        self.fileListBox.setMinimumHeight((self.fileListBox.sizeHintForRow(0) * self.fileListBox.count()) + (2 * self.fileListBox.frameWidth()))
    
    '''
    fileSelectHandler function reads the line time in the list box and passes the
    text (assuming csv file name) along with the absolute path of the folder to the
    plot handler
    '''
    def fileSelectHandler(self, item):
        if (item.text() != 'CSV Files not found in the selected folder'):
            plotHandler.plotCanvas.updatePlot(self.folderpath, item.text())




'''
plotSelectButtonGroup class defines all the GUI elements and operations
related to the plot select sub group within the plot section of the application window
'''
class plotSelectButtonGroup(QGroupBox):

    '''
    plotSelectButtonGroup class constructor initializes the plot select
    sub group of the plotting section of the application window
    This function sets the group title and adds the required GUI elements
    in a horizontal layout
    '''
    def __init__(self):
        super(plotSelectButtonGroup, self).__init__()

        # Set the title and horizontal layout
        self.setTitle('Select Plot Style')    
        self.groupElements = QHBoxLayout()
        self.setLayout(self.groupElements)

        # Add radio button for "Single Plot" option 
        # and select it by default
        self.singlePlotRadioButton = QRadioButton("Single Plot")
        self.singlePlotRadioButton.setChecked(True)
        # Connect this button to a function which handles the radio button selection
        self.singlePlotRadioButton.toggled.connect(self.selectPlotOption)
        self.groupElements.addWidget(self.singlePlotRadioButton)

        # Add radio button for "Combine Plot" option 
        self.combinePlotRadioButton = QRadioButton("Combine Plot")
        # Connect this button to a function which handles the radio button selection
        self.combinePlotRadioButton.toggled.connect(self.selectPlotOption)
        self.groupElements.addWidget(self.combinePlotRadioButton)

        # Add a spacer to push the two radio buttons to the left and the
        # push button to the right
        self.groupElements.addStretch(1)

        # Add a button to clear the plot area and connect it to a 
        # function which handles the clear plot operation
        self.clearPlotButton = QPushButton("Clear Plot")
        self.clearPlotButton.clicked.connect(plotHandler.plotCanvas.clearPlot)
        self.groupElements.addWidget(self.clearPlotButton) 

    '''
    selectPlotOption function reads the text from the radio button that is
    selected and sends that data to the plot handler module to set the
    plot option
    '''
    def selectPlotOption(self):
        # Read the text of the radio button that triggered this function
        radioButton = self.sender()
        # If the button is checked
        if radioButton.isChecked():
            # Pass that text to the plot handler
            plotHandler.plotCanvas.setPlotOption(radioButton.text())

'''
plotGroup class defines all the GUI elements and operations
related to the plotting section of the application window
'''
class plotGroup(QGroupBox):

    '''
    plotGroup class constructor initializes the plotting
    section of the application window and arranges all the 
    sub groups in a vertical layout.
    This function also sets the group title
    '''
    def __init__(self):
        super(plotGroup, self).__init__()

        # Set title and vertical layout
        self.setTitle('Data Visualizer')
        self.groupElements = QVBoxLayout()
        self.setLayout(self.groupElements)

        # Add the plot select group
        self.groupElements.addWidget(plotSelectButtonGroup())
        # Add the plot handler group (from plot handler module)
        self.groupElements.addWidget(plotHandler.plotCanvas())
        

'''
dataLoggerGroup class defines all the GUI elements and operations
related to the data logging section of the application window
'''
class dataLoggerGroup(QGroupBox):

    '''
    dataLoggerGroup class constructor initializes the data logging
    section of the application window and arranges all the GUI elements
    in a vertical layout.
    This function also sets the group title
    '''
    def __init__(self):
        super(dataLoggerGroup, self).__init__()

        # Empty lists to hold time and temperature data
        self.timeData = list()
        self.temperatureData = list()

        # Set the title, minimum width and vertical layout
        self.setTitle('Data Logger')
        self.setMinimumWidth(500)
        self.groupElements = QVBoxLayout()
        self.setLayout(self.groupElements)

        # Add button to select the target folder and 
        # connect it to the function which handles that operation
        self.folderSelectButton = QPushButton('Select Folder')
        self.folderSelectButton.clicked.connect(self.selectFolderHandler)
        self.groupElements.addWidget(self.folderSelectButton)

        # Add an empty text box to display the selected folder
        self.folderPathTextBox = QLabel(self)
        # Set the alignment to right to show the lowest folder if
        # the absolute path is longer than the text box
        self.folderPathTextBox.setAlignment(Qt.AlignRight)
        self.groupElements.addWidget(self.folderPathTextBox)

        # Add a spacer
        self.groupElements.addStretch(1)

        # Add a label with a prompt to enter file name 
        # and set it to invisible. This shall be visible 
        # only if the target folder is selected
        self.fileNamePrompt = QLabel('Enter file name. Leave Empty to use default')
        self.fileNamePrompt.setVisible(False)
        self.groupElements.addWidget(self.fileNamePrompt)

        # Add a text box to capture the file name 
        # and set it to invisible. This shall be visible 
        # only if the target folder is selected
        self.fileNameTextBox = QLineEdit(self)
        self.fileNameTextBox.setVisible(False)
        self.groupElements.addWidget(self.fileNameTextBox)

        # Add a button to trigger the log file 
        # and set it to invisible. This shall be visible 
        # only if the target folder is selected
        # This button is connected to the function which handles
        # the start of the data logging operation
        self.startLoggingButton = QPushButton('Start Logging')
        self.startLoggingButton.setVisible(False)
        self.startLoggingButton.clicked.connect(self.startLoggingHandler)
        self.groupElements.addWidget(self.startLoggingButton)

        # Add a spacer
        self.groupElements.addStretch(1)

        # Add a label with a prompt to enter temperature 
        # and set it to invisible. This shall be visible 
        # only if the data logging is started
        self.temperaturePrompt = QLabel('Enter the temperature (in deg. C)')
        self.temperaturePrompt.setVisible(False)
        self.groupElements.addWidget(self.temperaturePrompt)

        # Add a text box to enter temperature 
        # and set it to invisible. This shall be visible 
        # only if the data logging is started
        # The text box is connected to a function which captures
        # the new data when a return key is pressed
        self.temperatureTextBox = QLineEdit(self)
        self.temperatureTextBox.setVisible(False)
        self.temperatureTextBox.returnPressed.connect(self.enterTemperatureData)
        self.groupElements.addWidget(self.temperatureTextBox)

        # Add a spacer
        self.groupElements.addStretch(1)

        # Add a table to display the data during the logging operation
        self.dataTable = QTableWidget()
        # Enable alternate row colors to improve visibility between rows
        self.dataTable.setAlternatingRowColors(True)
        # Hide vertical headers
        self.dataTable.verticalHeader().hide()
        # Set the horizontal size to stretch to the available space 
        # and the vertical size to stay fixed to the initial size and enable
        # the scrolling option
        self.dataTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.dataTable.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.dataTable.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        # Set the table to 2 columns and 10 rows
        self.dataTable.setColumnCount(2)
        self.dataTable.setRowCount(10)
        # Set table header text and font
        self.dataTable.setHorizontalHeaderLabels(['Time', 'Temperature'])
        stylesheet = "::section{font-size: 10pt;border-radius:4px;padding: 10px}"
        self.dataTable.horizontalHeader().setStyleSheet(stylesheet)
        # Set the table invisible. This shall be visibile 
        # only after the logging operation is started
        self.dataTable.setVisible(False)
        self.groupElements.addWidget(self.dataTable)

        # Add a spacer
        self.groupElements.addStretch(1)

        # Add a button to trigger the save file operation
        # and set it to invisible. This shall be visible 
        # only after the logging operation is started
        # This button is connected to the function which handles
        # the save file operation
        self.saveDataButton = QPushButton('Save Data')
        self.saveDataButton.setVisible(False)
        self.saveDataButton.clicked.connect(self.saveDataHandler)
        self.groupElements.addWidget(self.saveDataButton)


    '''
    selectFolderHandler function is responsible for collecting the target folder
    path to save the temperature data

    This function calls the selectDirectory function from the file handler module
    and reads the absolute path of the selected folder
    This function displays the selected folder in a text box and sets the
    file name text boxes and start logging button to visible
    '''
    def selectFolderHandler(self):
        # Read the absolute path of the target folder
        self.folderpath = fileHandler.selectDirectory()
        # Display the absolute path in the text box
        self.folderPathTextBox.setText(self.folderpath)
        # Set the file name text boxes and the start logging button to visible
        self.fileNamePrompt.setVisible(True)
        self.fileNameTextBox.setVisible(True)
        self.startLoggingButton.setVisible(True)


    '''
    startLoggingHandler function is responsible for starting the
    data logging process
    This function reads the file name from the text box and adds the
    current time stamp to the file name and saves the absolute path for the file name

    This function then makes the temperature entry boxes, table and save button visible
    and makes the file name boxes invisible

    This function also clears the data arrays to make sure any old data cleared before
    starting a new temperature log
    '''    
    def startLoggingHandler(self):
        # Read the file name from the text box
        fileName = self.fileNameTextBox.text()
        # Capture the current timestamp
        now = datetime.now()
        # Format the time stamp to YYYY_MM_DD_hh_mm_ss
        timeStamp = now.strftime("%Y_%m_%d_%H_%M_%S_")

        # If the file name is empty
        if not fileName:
            # Set the default file name
            fileName = 'TemperatureLog'

        # Set the absolute path and file name for the csv file
        self.filePath = self.folderpath + '/' + timeStamp + fileName + '.csv'    

        # Set temperature entry text boxes to visible
        self.temperaturePrompt.setVisible(True)
        self.temperatureTextBox.setVisible(True)
        # Set data table to visible
        self.dataTable.setVisible(True)
        # Set save button to visible
        self.saveDataButton.setVisible(True)
        # Set file name text boxes to invisible
        self.fileNamePrompt.setVisible(False)
        self.fileNameTextBox.setVisible(False)

        # Clear data arrays
        self.timeData.clear()
        self.temperatureData.clear()
        
    '''
    enterTemperatureData function reads the input temperature
    string from the text box and adds the current time stamp
    and the temperature value to the data lists and the table
    if the entered data is a number
    This function also clears the text in the text box to get
    it ready for the next entry
    '''
    def enterTemperatureData(self):
        # Read the string from the text box
        temperature = self.temperatureTextBox.text()
        # Capture current data & time stamp
        now = datetime.now()
        # Format the time stamp into HH:MM:SS format
        timeStamp = now.strftime("%H:%M:%S")

        # If the input string from the text box is a digit
        if temperature.isdigit():
            # Add the time stamp and temperature data to the lists
            self.timeData.append(timeStamp)
            self.temperatureData.append(temperature)
            # Add the time stamp and temperature data to the table
            self.updateTable(timeStamp, temperature)
        
        # Clear the text box to get it ready for next entry
        self.temperatureTextBox.clear()

    '''
    updateTable function is responsible for showing the entered data
    in a table format
    This function updates the table with time and temperature data
    The first 9 rows of data are added to the next available empty
    row
    If the data exceeds 9 rows, new row is added to the table and the
    data is added to the next available empty row
    '''
    def updateTable(self, timeData, temperatureData):
        # Read the current number of rows in the table
        totalRows = self.dataTable.rowCount()
        # For every row in the table
        for currentRow in range(totalRows):
            # If the current row is the last row
            if currentRow >= (totalRows - 1):
                # Add a new row
                self.dataTable.setRowCount(totalRows + 1)
                # Scroll to the bottom to make the latest data visible
                self.dataTable.scrollToBottom()
            
            # Read the data from the first column in the current row
            timeCellData = self.dataTable.item(currentRow, 0)
            # If the data in current row is empty
            if not timeCellData:
                # Write time data in the first column
                self.dataTable.setItem(currentRow, 0, QtWidgets.QTableWidgetItem(timeData))
                # Write temperature data in the second column
                self.dataTable.setItem(currentRow, 1, QtWidgets.QTableWidgetItem(temperatureData))
                # Break out of the for loop after writing to the last empty row
                break
            
    '''
    saveDataHandler function calls the writeCSVData function from the file handler module
    to save the temperture data to a csv file in a format that can be plotted
    This function also calls the resetData function to clear all the data and reset
    the GUI once the data is saved
    '''
    def saveDataHandler(self):
        # Write the data to CSV file
        fileHandler.writeCSVData(self.filePath, self.timeData, self.temperatureData)
        # Reset the data and GUI
        self.resetData()

    '''
    resetData function clears and resets the data and the table 
    and hides the data table, save button and temperature entry text boxes
    This is done to hide old data once it is saved and force the user
    to enter a new file name if they need to enter new data
    '''
    def resetData(self):
        # Clear the data lists
        self.timeData.clear()
        self.temperatureData.clear()
        # Clear the data in the table
        self.dataTable.clear()
        # Reset the data table to 10 rows
        self.dataTable.setRowCount(10)
        # Reset the table headers. Clearing the table also clears the headers
        self.dataTable.setHorizontalHeaderLabels(['Time', 'Temperature'])
        # Hide the data table
        self.dataTable.setVisible(False)
        # Hide the temperature entry text boxes and prompts
        self.temperaturePrompt.setVisible(False)
        self.temperatureTextBox.setVisible(False)
        # Hid the save button
        self.saveDataButton.setVisible(False)
        
        
        
        

               
'''
mainWindow class defines the main application window and adds the
required sections of the GUI
'''
class mainWindow(QMainWindow):

    '''
    mainWindow class constructor initializes the application window
    and arranges the different groups in a horizontal layout.
    This function also sets the window title and icon
    '''
    def __init__(self):
        super(mainWindow, self).__init__()

        self.main_widget = QWidget(self)

        self.main_layout = QHBoxLayout(self.main_widget)

        self.main_layout.addWidget(fileSelectGroup())
        self.main_layout.addWidget(plotGroup())
        self.main_layout.addWidget(dataLoggerGroup())


        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

        self.setWindowTitle('Teacup Temperature Data Visualizer')

        scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.setWindowIcon(QtGui.QIcon(scriptDir + os.path.sep + 'icon.png'))

        self.show()
