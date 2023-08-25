from PyQt5.QtWidgets import *
import sys
import tkinter as tk
import requests
import json

api_url = "https://localhost:7180/customer/"
#Define action event for when the test button is clicked
def testButtonAction():
    #Send a get request to the API to get all customers, if the API is running and responds appropriately
    #we should receive a 200 response
    response = requests.get(api_url + "GetAllCustomers", verify=False)
    #if an OK response is received, show the rest of the controls
    if(response.status_code == 200):
        print(f'API running, show buttons')
        testButton.setVisible(False)
        getAllButton.setVisible(True)
        textbox.setVisible(True)
        nameInputBox.setVisible(True)
        getByNameButton.setVisible(True)
        numberInputBox.setVisible(True)
        getByNumberButton.setVisible(True)
        loginText.setVisible(True)
        loginButton.setVisible(True)

#Function to call get all request when the get all button is clicked        
def getAllButtonAction():
    response = requests.get(api_url + "GetAllCustomers", verify=False)
    if(response.status_code == 200):
        response = response.json()
        textbox.append(f"{response}")

#Function to call a get by name request when the get by name button is clicked    
def getByNameAction():
    response = requests.get(api_url + "GetCustomerByName/" + nameInputBox.text(), verify=False)
    if(response.status_code == 200):
        response = response.json()
        textbox.append(f"{response}")
        #Rob was here

#Function to call a get by number request when the get by number button is clicked
def getByNumberAction():
    response = requests.get(api_url + "GetCustomerById/" + numberInputBox.text(), verify=False)
    if(response.status_code == 200):
        response = response.json()
        textbox.append(f"{response}")
    else:
        textbox.append(f"No data found, or a bad request was sent. Please try again")

#Function to call a login request when the log in button is clicked
#this is done by sending a get request with a guid
def loginButtonAction():
    response = requests.get(api_url + "Login/" + loginText.text(), verify=False)
    if(response.status_code == 204):
        textbox.append(f"Login successful")
        loginButton.setVisible(False)
        loginText.setVisible(False)
        showMasterControls()
    elif(response.status_code == 404):
        textbox.append(f"Login failed")

#Function that makes all update related fields visible
def showControls():
    toggledNameLabel.setVisible(True)
    toggledNameText.setVisible(True)
    toggledNumberLabel.setVisible(True)
    toggledNumberText.setVisible(True)
    toggledAgeLabel.setVisible(True)
    toggledAgeText.setVisible(True)
    toggledPizzaLabel.setVisible(True)
    toggledPizzaText.setVisible(True)
 
#Function that hides all update related fields   
def hideControls():
    toggledNameLabel.setVisible(False)
    toggledNameText.setVisible(False)
    toggledNumberLabel.setVisible(False)
    toggledNumberText.setVisible(False)
    toggledAgeLabel.setVisible(False)
    toggledAgeText.setVisible(False)
    toggledPizzaLabel.setVisible(False)
    toggledPizzaText.setVisible(False)

#Function that shows "master" controls such as update by name, number, etc..
def showMasterControls():
    #TODO make method show all update related controls i.e. user logs in to see update add delete toggles
    updateByNameButton.setVisible(True)
    updateByNumberButton.setVisible(True)
    addCustomerButton.setVisible(True)
    deleteCustomerButton.setVisible(True)

#Function to make update by name related fields visible for the user to make requests with  
def updateByNameAction():
    hideToggledControls()
    showControls()
    toggledUpdateByNameButton.setVisible(True)

#Function to make update by number related fields visible for the user to make requests with
def updateByNumberAction():
    hideToggledControls()
    showControls()
    toggledUpdateByNumberButton.setVisible(True)

#Function to make add user related fields visible for the user to make requests with
def addUserAction():
    hideToggledControls()
    showControls()
    toggledAddButton.setVisible(True)

#Function to make delete user related fields visible for the user to make requests with
def deleteUserAction():
    hideToggledControls()
    toggledNameLabel.setVisible(True)
    toggledNameText.setVisible(True)
    toggledDeleteButton.setVisible(True)

#Function to gather data from update related fields into json format then send a put request
#if it is successful (204 -- No Content) then it lets the user know an update was performed
def toggledUpdateByNameAction():
    topost = {
        "Name": toggledNameText.text(),
        "PhoneNumber": int(toggledNumberText.text()),
        "Age": int(toggledAgeText.text()),
        "FavoritePizza": toggledPizzaText.text()
        }
    headers =  {"Content-Type":"application/json"}
    response = requests.put(api_url + "UpdateByNameFromMVC/" + toggledNameText.text(), json=topost, verify=False)
    #If we are returned no content, then the update SHOULD have applied
    if(response.status_code == 204):
        textbox.append("Updated")
        hideControls()
        toggledUpdateByNameButton.setVisible(False)
        clearToggledText()

#Function to gather data from update related fields into json format then send a put request
#if it is successful (204 -- No Content) then it lets the user know an update was performed     
def toggledUpdateByNumberAction():
    topost = {
        "Name": toggledNameText.text(),
        "PhoneNumber": int(toggledNumberText.text()),
        "Age": int(toggledAgeText.text()),
        "FavoritePizza": toggledPizzaText.text()
        }
    headers =  {"Content-Type":"application/json"}
    response = requests.put(api_url + "UpdateByIdFromApp/" + toggledNumberText.text(), json=topost, verify=False)
    #If we are returned no content, then the update SHOULD have applied
    if(response.status_code == 204):
        textbox.append("Updated")
        hideControls()
        toggledUpdateByNumberButton.setVisible(False)
        clearToggledText()

#Function to gather data from update related fields into json format then send a post request
#if it is successful (201 -- Created) then it lets the user know an update was performed
def toggledAddAction():
    topost = {
        "Name": toggledNameText.text(),
        "PhoneNumber": int(toggledNumberText.text()),
        "Age": int(toggledAgeText.text()),
        "FavoritePizza": toggledPizzaText.text()
        }
    headers =  {"Content-Type":"application/json"}
    response = requests.post(api_url + "NewCustomer", json=topost, verify=False)
    #If we are returned 201, that means the content was created
    if(response.status_code == 201):
        textbox.append("Added")
        hideControls()
        toggledAddButton.setVisible(False)
        clearToggledText()

#Function to send a delete request after gathering which name to delete
def toggledDeleteAction():
    response = requests.delete(api_url + "DeleteByName/" + toggledNameText.text(), verify=False)
    if(response.status_code == 204):
        textbox.append("Deleted")
        hideControls()
        toggledDeleteButton.setVisible(False)
        clearToggledText()

#Function to clear the text boxes for the update related areas, this is generally called after
#a function is performed so that next time it is used it looks new again
def clearToggledText():
    toggledNameText.setText("")
    toggledNumberText.setText("")
    toggledAgeText.setText("")
    toggledPizzaText.setText("")

#Function to make update related fields not visible to the user anymore    
def hideToggledControls():
    toggledUpdateByNameButton.setVisible(False)
    toggledUpdateByNumberButton.setVisible(False)
    toggledAddButton.setVisible(False)
    toggledDeleteButton.setVisible(False)
    
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
#Get all controls
getAllButton = QPushButton(mainMenu)
getAllButton.setText("Get all customers")
getAllButton.move(10,10)
getAllButton.setVisible(False)
getAllButton.clicked.connect(getAllButtonAction)
#Get by name controls
nameInputBox = QLineEdit(mainMenu)
nameInputBox.move(10,70)
nameInputBox.setVisible(False)
#text boxes and buttons arent the same, tried resizing them several times and they just look worse lol
getByNameButton = QPushButton(mainMenu)
getByNameButton.move((nameInputBox.size().width() * 2) + 30,70)
getByNameButton.setText("Get by name")
getByNameButton.setVisible(False)
getByNameButton.clicked.connect(getByNameAction)
#Get by phone number controls
numberInputBox = QLineEdit(mainMenu)
numberInputBox.move(10,120)
numberInputBox.setVisible(False)
getByNumberButton = QPushButton(mainMenu)
getByNumberButton.move((numberInputBox.size().width() * 2) + 30,120)
getByNumberButton.setText("Get by number")
getByNumberButton.setVisible(False)
getByNumberButton.clicked.connect(getByNumberAction)
#Log in controls
loginText = QLineEdit(mainMenu)
loginText.move(200,12)
loginText.resize(300,30)
loginText.setVisible(False)
loginButton = QPushButton(mainMenu)
loginButton.move(500,10)
loginButton.setText("Log in")
loginButton.setVisible(False)
loginButton.clicked.connect(loginButtonAction)
#Update by name controls
updateByNameButton = QPushButton(mainMenu)
updateByNameButton.move(10,180)
updateByNameButton.setText("Update by name")
updateByNameButton.setVisible(False)
updateByNameButton.clicked.connect(updateByNameAction)
#Update by number controls
updateByNumberButton = QPushButton(mainMenu)
updateByNumberButton.move(updateByNameButton.size().width() * 2 - 20,180)
updateByNumberButton.setText("Update by number")
updateByNumberButton.setVisible(False)
updateByNumberButton.clicked.connect(updateByNumberAction)
#Add customer button controls
addCustomerButton = QPushButton(mainMenu)
addCustomerButton.move(updateByNameButton.size().width() * 4 - 30,180)
addCustomerButton.setText("Add customer")
addCustomerButton.setVisible(False)
addCustomerButton.clicked.connect(addUserAction)
#Delete customer button controls
deleteCustomerButton = QPushButton(mainMenu)
deleteCustomerButton.move(updateByNameButton.size().width() * 5 + 20,180)
deleteCustomerButton.setText("Delete")
deleteCustomerButton.setVisible(False)
deleteCustomerButton.clicked.connect(deleteUserAction)
#General toggled update controls
toggledNameText = QLineEdit(mainMenu)
toggledNameText.move((nameInputBox.size().width() * 2) + 30, 300)
toggledNameText.setVisible(False)
toggledNumberText = QLineEdit(mainMenu)
toggledNumberText.move((nameInputBox.size().width() * 2) + 30, 340)
toggledNumberText.setVisible(False)
toggledAgeText = QLineEdit(mainMenu)
toggledAgeText.move((nameInputBox.size().width() * 2) + 30, 380)
toggledAgeText.setVisible(False)
toggledPizzaText = QLineEdit(mainMenu)
toggledPizzaText.move((nameInputBox.size().width() * 2) + 30, 420)
toggledPizzaText.setVisible(False)
toggledNameLabel = QLabel(mainMenu)
toggledNameLabel.setText("Name:")
toggledNameLabel.move((nameInputBox.size().width()) + 60, 300)
toggledNameLabel.setVisible(False)
toggledNumberLabel = QLabel(mainMenu)
toggledNumberLabel.setText("Phone Number:")
toggledNumberLabel.move((nameInputBox.size().width()) - 26, 340)
toggledNumberLabel.setVisible(False)
toggledAgeLabel = QLabel(mainMenu)
toggledAgeLabel.move((nameInputBox.size().width()) + 78, 380)
toggledAgeLabel.setText("Age:")
toggledAgeLabel.setVisible(False)
toggledPizzaLabel = QLabel(mainMenu)
toggledPizzaLabel.setText("Favorite pizza:")
toggledPizzaLabel.move((nameInputBox.size().width()) - 13, 420)
toggledPizzaLabel.setVisible(False)
toggledUpdateByNameButton = QPushButton(mainMenu)
toggledUpdateByNameButton.setText("Update by name")
toggledUpdateByNameButton.move((nameInputBox.size().width()) + 60, 460)
toggledUpdateByNameButton.setVisible(False)
toggledUpdateByNameButton.clicked.connect(toggledUpdateByNameAction)
toggledUpdateByNumberButton = QPushButton(mainMenu)
toggledUpdateByNumberButton.setText("Update by number")
toggledUpdateByNumberButton.move((nameInputBox.size().width()) + 60, 460)
toggledUpdateByNumberButton.setVisible(False)
toggledUpdateByNumberButton.clicked.connect(toggledUpdateByNumberAction)
toggledAddButton = QPushButton(mainMenu)
toggledAddButton.setText("Add new user")
toggledAddButton.move((nameInputBox.size().width()) + 60, 460)
toggledAddButton.setVisible(False)
toggledAddButton.clicked.connect(toggledAddAction)
toggledDeleteButton = QPushButton(mainMenu)
toggledDeleteButton.setText("Delete (serious)")
toggledDeleteButton.move((nameInputBox.size().width() * 2) + 30, 340)
toggledDeleteButton.setVisible(False)
toggledDeleteButton.clicked.connect(toggledDeleteAction)
#Create text box to display text in
textbox = QTextEdit(mainMenu)
textbox.move(int(1280/2),0)
textbox.resize((int(1280/2) - 10),960 - 10)
textbox.setVisible(False)
textbox.setReadOnly(True)
#Add widget to window for display
window.addWidget(mainMenu)
window.setCurrentWidget(mainMenu)
sys.exit(app.exec())