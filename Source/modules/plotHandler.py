'''
Plot Handler Module
This module handles all operations related to plotting the time vs. temperature
graphs on the GUI
'''

import matplotlib
from modules import fileHandler
matplotlib.use('Qt5Agg')

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# Default plot option is configured as Single Plot
plotOption = 'Single Plot'

# Matplot lib figure with a single plot1 is defined
fig = Figure(figsize=(10, 8), dpi=100)
temperaturePlot = fig.add_subplot(111)
        
'''
plotCanvas class defines all the functionality required to plot
the time vs. temperature data
'''
class plotCanvas(FigureCanvas):

    '''
    plotCanvas class constructor initializes the figure
    by defining the plot title and axes labels
    '''
    def __init__(self):
        fig.suptitle('Temperature Decay Curve')
        temperaturePlot.set_xlabel('Time (minutes)')
        temperaturePlot.set_ylabel('Temperature (deg Celcius)')
        super(plotCanvas, self).__init__(fig)

    '''
    updatePlot function is responsible for updating the plot with new data
    This function takes the folder path and file name of the csv file which
    contains the data. This data is read into xData and yData lists which are
    then plotted on the figure

    If the plot option is selected as single plot, this function clears any
    previous plots before drawing the new data

    This function also updates the legend with the file name of the plot that
    is being drawn
    '''
    def updatePlot(folderPath, fileName):
        if 'Single Plot' == plotOption:
            temperaturePlot.cla()
        
        filePath = folderPath + "/" + fileName

        xData, yData = fileHandler.readCSVData(filePath)

        temperaturePlot.set_xlabel('Time (minutes)')
        temperaturePlot.set_ylabel('Temperature (deg Celcius)')
        temperaturePlot.plot(xData, yData, 'o-', label=fileName)
        temperaturePlot.legend()
        fig.canvas.draw_idle()

    '''
    clearPlot function is responsible for clearing all the plots on the figure
    The funtion resets the axes labels after clearing the plot
    '''
    def clearPlot():
        temperaturePlot.cla()
        temperaturePlot.set_xlabel('Time (minutes)')
        temperaturePlot.set_ylabel('Temperature (deg Celcius)')
        
        fig.canvas.draw_idle()

    '''
    setPlotOption function reads the text from the radio button selection
    and updates the plot option variable.
    This is used to select Single Plot or Combine Plot options
    '''
    def setPlotOption(radioButtonText):
        global plotOption
        plotOption = radioButtonText
