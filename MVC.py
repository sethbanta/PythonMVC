from PyQt5.QtWidgets import *
import sys
import tkinter as tk
import requests

api_url = "https://localhost:7180/customer"

def testButtonAction():
    #Send a get request to the API to get all customers, if the API is running and responds appropriately
    #we should receive a 200 response
    response = requests.get("https://localhost:7180/customer/GetAllCustomers", verify=False)
    #if an OK response is received, show the rest of the controls
    if(response.status_code == 200):
        print(f'API running, show buttons')

#Create instance of QApplication
app = QApplication([])

#Create main widget for displaying controls
mainMenu = QWidget()

#Create a window
window = QStackedLayout()
#Set the title of our main menu widget
mainMenu.setWindowTitle("Customer data Python MVC")
#Grab resolution of monitor in order to try and place the window in the center of the screen
root = tk.Tk()
screen_width = root.winfo_screenwidth() / 2
screen_height = root.winfo_screenheight() / 2
#Use the grabbed width of the monitor and subtract half the width of the window size in order to offset
#the starting area to be close enough to the center of the screen
#same method is used for height as well
mainMenu.setGeometry((int(screen_width) - 640),(int(screen_height) - 480),1280,960)

#Create a new button for testing connectivity to the API
#using this button to server as an initial test for users to run to make sure the API is running, once the test
#is completed, other controls will display accordingly, this is to avoid sending requests to an offline API
testButton = QPushButton(mainMenu)
testButton.setText("Test API connectivity")
#move the starting point to the center of the screen then subtract the width and height of the button
testButton.move(int(1280/2) - testButton.size().width(), int(960/2) - testButton.size().height())
testButton.clicked.connect(testButtonAction)

#Add widget to window for display
window.addWidget(mainMenu)
window.setCurrentWidget(mainMenu)
sys.exit(app.exec())