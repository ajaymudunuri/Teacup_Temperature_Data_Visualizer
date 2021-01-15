'''
Application main
This is the start point for the main application which launches
the GUI
'''
import sys
from PyQt5.QtWidgets import QApplication

from modules import guiHandler

# Define the application
guiApp = QApplication([])
# Setup the main application window
window = guiHandler.mainWindow()
# Execute the application
sys.exit(guiApp.exec_())

