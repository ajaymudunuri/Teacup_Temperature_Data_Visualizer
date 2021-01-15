'''
File Handler Module
This module handles all folder selection and read/write operations to csv files
'''

import os
import random
import pandas
from datetime import datetime
from PyQt5.QtWidgets import QFileDialog

# Empty list to hold the list of csv files in the selected folder
csvFileList = []


'''
loadData function is used to select the folder containing
csv files with the temperature data

This functions pops up a open folder dialog and lets the user
select a folder. Once the folder is selected, the function
looks for csv files and populates a list with all the csv file names

This function returns the absolute path of the selected folder and the
list of csv file names in that folder
'''
def loadData():
    #Clear the list
    csvFileList.clear()
    # Open a dialog box for the user to select a desired folder
    # Configure the dialog box to display only folders and no files
    dataDir = QFileDialog.getExistingDirectory(None, 'Select data folder', os.path.join(os.path.dirname(__file__), '..'))
    
    # Look through all the files in the selected directory 
    # and add all the csv files to the list
    for item in os.listdir(dataDir):
        if(os.path.isfile(os.path.join(dataDir, item))):
            if item.endswith(".csv"):
                csvFileList.append(item)

    # Return the absolute path of the 
    # selected folder and the list of csv files
    return dataDir, csvFileList


'''
selectDirectory function is used to select the folder in which the
input temperature data shall be saved

This functions pops up a open folder dialog and lets the user
select a folder.

This function returns the absolute path of the selected folder
'''
def selectDirectory():
    # Open a dialog box for the user to select a desired folder
    # Configure the dialog box to display only folders and no files
    dataDir = QFileDialog.getExistingDirectory(None, 'Select data folder', os.path.join(os.path.dirname(__file__), '..'))
    
    # Return the absolute path of the selected folder
    return dataDir


'''
readCSVData function takes a file path as an input (assuming csv file) and reads
the file as a Pandas data frame
This function reads the first column into a temporary list and converts it into
a list of time deltas (in minutes) relative to the first time element in the csv file
The second column (temperature) is read directly into a different list

This function returns the time delta list as xData and temperature list as yData
'''
def readCSVData(filePath):
    # Open the csv file using pandas
    dataFrame = pandas.read_csv(os.path.normpath(filePath))
    
    # Create an empty list for time data
    xData = list()
    # Copy the temperature data (second column) into a list
    yData = dataFrame.temp

    # Read the first column in a date time format
    timeData = pandas.to_datetime(dataFrame.time)
    # Iterate through each time element in the first columm
    for time in timeData:
        # Calculate the time delta in minutes (hence /60) for each
        # entry compared to the first entry and add it to the time
        # data list
        xData.append((pandas.Timedelta(time - timeData[0]).seconds)/60)
    
    # Return the relative time and temperature data lists
    return xData, yData


'''
writeCSVData function takes file path, time data and temperature data as
input parameters and writes that data into a csv file
'''
def writeCSVData(filePath, timeData, tempData):
    # Create a dictionary with time and temperature data lists
    csvData = {'time': timeData,
                'temp': tempData
                }
    
    # Convert that dictionary into a pandas data frame in csv format
    dataFrame = pandas.DataFrame(csvData, columns=['time', 'temp'])
    # Write to csv file
    dataFrame.to_csv(filePath, index = False, header=True)
    
    

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    guiApp = QApplication([])
    loadData()

