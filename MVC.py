from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import tkinter as tk
import requests
import json
import csv
import ctypes

api_url = "https://localhost:7180/customer/"
letterRegEx = QRegExp("[a-z-A-Z_ ]*")
letterValidator = QRegExpValidator(letterRegEx)
numberRegEx = QRegExp("[0-9_]+")
numberValidator = QRegExpValidator(numberRegEx)
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
        clearConsoleButton.setVisible(True)
        
#Function to call get all request when the get all button is clicked        
def getAllButtonAction():
    response = requests.get(api_url + "GetAllCustomers", verify=False)
    if(response.status_code == 200):
        response = response.json()
        #for each customer in the response, split by ' then append to the text box the information
        #the phone number and age responses contain a : at the beginning and , at the end which is gets stripped
        for customer in response:
            strReal = str(customer)
            splitOutput = strReal.split("'")
            textbox.append(f"{splitOutput[3]}, {splitOutput[6].strip(': ,')}, {splitOutput[8].strip(': ,')}, {splitOutput[11]}")


#Function to call a get by name request when the get by name button is clicked    
def getByNameAction():
    response = requests.get(api_url + "GetCustomerByName/" + nameInputBox.text(), verify=False)
    if(response.status_code == 200):
        response = response.json()
        #turn the response to a string then split by ' and remove : and , from age and phone number then send to text box
        strReal = str(response)
        splitOutput = strReal.split("'")
        textbox.append(f"{splitOutput[3]}, {splitOutput[6].strip(': ,')}, {splitOutput[8].strip(': ,')}, {splitOutput[11]}")
        #Rob was here
    elif(response.status_code == 204):
        textbox.append("Customer not found")
        customers = []
        toDisplay = []
        isEmpty = True
        response = requests.get(api_url + "GetAllCustomers", verify=False)
        if(response.status_code == 200):
            response = response.json()
            #for each customer in the response, split by ' then append to the text box the information
            #the phone number and age responses contain a : at the beginning and , at the end which is gets stripped
            for customer in response:
                strReal = str(customer)
                splitOutput = strReal.split("'")
                customers.append(splitOutput[3])
                subbedName = splitOutput[3][0:len(nameInputBox.text())]
                if(subbedName == nameInputBox.text()):
                    #lolrob
                    isEmpty = False
                    toDisplay.append(splitOutput[3])
        if(isEmpty == False):
            #MessageBox = ctypes.windll.user32.MessageBoxW
            #MessageBox(None, str(toDisplay), 'Potential matches', 0)
            def copyFunc(text):
                clippy.clipboard_clear()
                clippy.clipboard_append(text)
                nameInputBox.setText(text)
                popup.close()
            root = tk.Tk()
            screen_width = root.winfo_screenwidth() / 2
            screen_height = root.winfo_screenheight() / 2
            clippy = tk.Tk()
            clippy.withdraw()
            popupWindow = QStackedLayout()
            popup = QMainWindow()
            popup.setGeometry(int(screen_width) - 400,int(screen_height) - 300,800,600)
            popup.setWindowTitle("Potential matches")
            i = 0
            for match in toDisplay:
                label = QLabel(popup)
                label.setText(f'{match}')
                label.move(50 + (100 * i),0)
                text = label.text()
                button = QPushButton(popup)
                button.setText('Copy')
                button.move(50 + (100 * i), 30)
                button.clicked.connect(lambda ch, text=text: copyFunc(text))
                i += 1
            popupWindow.addWidget(popup)
            popup.show()            
        else:
            MessageBox = ctypes.windll.user32.MessageBoxW
            MessageBox(None, 'No potential matches found', 'Potential matches', 0)

#Function to call a get by number request when the get by number button is clicked
def getByNumberAction():
    if(len(numberInputBox.text()) != 10):
        textbox.append('Phone number invalid, please try again')
    else:
        response = requests.get(api_url + "GetCustomerById/" + numberInputBox.text(), verify=False)
        if(response.status_code == 200):
            response = response.json()
            #turn the response to a string then split by ' and remove : and , from age and phone number then send to text box
            strReal = str(response)
            splitOutput = strReal.split("'")
            textbox.append(f"{splitOutput[3]}, {splitOutput[6].strip(': ,')}, {splitOutput[8].strip(': ,')}, {splitOutput[11]}")
        elif(response.status_code == 204):
            textbox.append("Customer not found")
            customers = []
            toDisplay = []
            isEmpty = True
            response = requests.get(api_url + "GetAllCustomers", verify=False)
            if(response.status_code == 200):
                response = response.json()
                #for each customer in the response, split by ' then append to the text box the information
                #the phone number and age responses contain a : at the beginning and , at the end which is gets stripped
                for customer in response:
                    strReal = str(customer)
                    splitOutput = strReal.split("'")
                    strippedNumber = splitOutput[6].strip(': ,')
                    customers.append(strippedNumber)
                    subbedNumber = strippedNumber[0:5]
                    if(subbedNumber == numberInputBox.text()[0:5]):
                        #lolrob
                        isEmpty = False
                        toDisplay.append(strippedNumber)
            if(isEmpty == False):
                def copyFunc(text):
                    clippy.clipboard_clear()
                    clippy.clipboard_append(text)
                    numberInputBox.setText(text)
                    popup.close()
                root = tk.Tk()
                screen_width = root.winfo_screenwidth() / 2
                screen_height = root.winfo_screenheight() / 2
                clippy = tk.Tk()
                clippy.withdraw()
                popupWindow = QStackedLayout()
                popup = QMainWindow()
                popup.setGeometry(int(screen_width) - 400,int(screen_height) - 300,800,600)
                popup.setWindowTitle("Potential matches")
                i = 0
                for match in toDisplay:
                    label = QLabel(popup)
                    label.setText(f'{match}')
                    label.move(50 + (150 * i),0)
                    text = label.text()
                    button = QPushButton(popup)
                    button.setText('Copy')
                    button.move(50 + (150 * i), 30)
                    button.clicked.connect(lambda ch, text=text: copyFunc(text))
                    i += 1
                popupWindow.addWidget(popup)
                popup.show()            
            else:
                MessageBox = ctypes.windll.user32.MessageBoxW
                MessageBox(None, 'No potential matches found', 'Potential matches', 0)

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
    toggledNameToUpdate.setVisible(False)
    toggledNameToUpdateLabel.setVisible(False)
    toggledNameLabel.setVisible(False)
    toggledNameText.setVisible(False)
    toggledNumberLabel.setVisible(False)
    toggledNumberText.setVisible(False)
    toggledAgeLabel.setVisible(False)
    toggledAgeText.setVisible(False)
    toggledPizzaLabel.setVisible(False)
    toggledPizzaText.setVisible(False)
    toggledNumberToUpdateLabel.setVisible(False)
    toggledNumberToUpdate.setVisible(False)
    toggledDeleteNumberButton.setVisible(False)
    toggledDeleteNumberLabel.setVisible(False)
    toggledNameToUpdate.setVisible(False)
    numberToUpdateGrabButton.setVisible(False)
    nameToUpdateGrabButton.setVisible(False)
    toggledDeleteNumberText.setVisible(False)

#Function that shows "master" controls such as update by name, number, etc..
def showMasterControls():
    updateByNameButton.setVisible(True)
    updateByNumberButton.setVisible(True)
    addCustomerButton.setVisible(True)
    deleteCustomerButton.setVisible(True)
    exportButton.setVisible(True)
    importButton.setVisible(True)

#Function to make update by name related fields visible for the user to make requests with  
def updateByNameAction():
    clearToggledText()
    hideToggledControls()
    hideControls()
    toggledNameToUpdate.setVisible(True)
    toggledNameToUpdateLabel.setVisible(True)
    nameToUpdateGrabButton.setVisible(True)

#Function to make update by number related fields visible for the user to make requests with
def updateByNumberAction():
    clearToggledText()
    hideToggledControls()
    hideControls()
    numberToUpdateGrabButton.setVisible(True)
    toggledNumberToUpdate.setVisible(True)
    toggledNumberToUpdateLabel.setVisible(True)

#Function to make add user related fields visible for the user to make requests with
def addUserAction():
    hideToggledControls()
    hideControls()
    clearToggledText()
    showControls()
    toggledAddButton.setVisible(True)

#Function to make delete user related fields visible for the user to make requests with
def deleteUserAction():
    hideToggledControls()
    hideControls()
    toggledNameLabel.setVisible(True)
    toggledNameText.setVisible(True)
    toggledDeleteButton.setVisible(True)
    toggledDeleteNumberText.setVisible(True)
    toggledDeleteNumberLabel.setVisible(True)
    toggledDeleteNumberButton.setVisible(True)

#Function to gather data from update related fields into json format then send a put request
#if it is successful (204 -- No Content) then it lets the user know an update was performed
def toggledUpdateByNameAction():
    if(len(toggledNumberText.text()) != 10):
        textbox.append('Phone number invalid, please try again')
    elif(len(toggledAgeText.text()) != 2):
        textbox.append('Age invalid, please try again')
    else:
        topost = {
            "Name": toggledNameText.text(),
            "PhoneNumber": int(toggledNumberText.text()),
            "Age": int(toggledAgeText.text()),
            "FavoritePizza": toggledPizzaText.text()
            }
        headers =  {"Content-Type":"application/json"}
        response = requests.put(api_url + "UpdateByNameFromMVC/" + toggledNameToUpdate.text(), json=topost, verify=False)
        #If we are returned no content, then the update SHOULD have applied
        if(response.status_code == 204):
            textbox.append("Updated")
            hideControls()
            toggledUpdateByNameButton.setVisible(False)
            clearToggledText()

#Function to gather data from update related fields into json format then send a put request
#if it is successful (204 -- No Content) then it lets the user know an update was performed     
def toggledUpdateByNumberAction():
    if(len(toggledNumberText.text()) != 10):
        textbox.append('Phone number invalid, please try again')
    elif(len(toggledAgeText.text()) != 2):
        textbox.append('Age invalid, please try again')
    else:
        topost = {
            "Name": toggledNameText.text(),
            "PhoneNumber": int(toggledNumberText.text()),
            "Age": int(toggledAgeText.text()),
            "FavoritePizza": toggledPizzaText.text()
            }
        headers =  {"Content-Type":"application/json"}
        response = requests.put(api_url + "UpdateByIdFromApp/" + toggledNumberToUpdate.text(), json=topost, verify=False)
        #If we are returned no content, then the update SHOULD have applied
        if(response.status_code == 204):
            textbox.append("Updated")
            hideControls()
            toggledUpdateByNumberButton.setVisible(False)
            clearToggledText()

#Function to gather data from update related fields into json format then send a post request
#if it is successful (201 -- Created) then it lets the user know an update was performed
def toggledAddAction():
    if(len(toggledNumberText.text()) != 10):
        textbox.append('Phone number invalid, please try again')
    elif(len(toggledAgeText.text()) != 2):
        textbox.append('Age invalid, please try again')
    else:
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
    else:
        textbox.append("Failed to delete customer")
        
#Function to send a delete request after gathering which number to delete
def toggledDeleteNumberAction():
    response = requests.delete(api_url + "DeleteById/" + toggledDeleteNumberText.text(), verify=False)
    if(response.status_code == 204):
        textbox.append("Deleted")
        hideControls()
        toggledDeleteButton.setVisible(False)
        toggledDeleteNumberText.setVisible(False)
        toggledDeleteNumberLabel.setVisible(False)
        toggledDeleteNumberButton.setVisible(False)
        clearToggledText()
    else:
        textbox.append("Failed to delete customer")

#Sends a request to the API to save information to JSON
#exports a json file in the local directory where this program runs and where the API runs
#basically server and client side
def exportAction():
    response = requests.get(api_url + "save", verify=False)
    if(response.status_code == 204):
        textbox.append("Exported")
    response = requests.get(api_url + "GetAllCustomers", verify=False)
    output = response.json()
    #BigRob was here also
    outputStr = str(output)
    outputStr = outputStr.replace("[", "[\n")  
    outputStr = outputStr.replace("{", "\t{\n")
    outputStr = outputStr.replace(",", ",\n")
    outputStr = outputStr.replace("}", "\n\t}")
    outputStr = outputStr.replace("]", "\n]\n")
    with open("SavedList.json", "w") as outfile:
        outfile.write(str(outputStr))
    
#Sends a request to the API to load information from JSON file into the API    
def importAction():
    response = requests.get(api_url + "import", verify=False)
    if(response.status_code == 204):
        textbox.append("Imported")

#Function to clear text in the console
def clearConsoleAction():
    textbox.setText("")
    
#Function to clear the text boxes for the update related areas, this is generally called after
#a function is performed so that next time it is used it looks new again
def clearToggledText():
    toggledNameText.setText("")
    toggledNumberText.setText("")
    toggledAgeText.setText("")
    toggledPizzaText.setText("")
    toggledNameToUpdate.setText("")
    toggledNumberToUpdate.setText("")
    toggledNameToUpdate.setText("")
    toggledDeleteNumberText.setText("")

#Function to make update related fields not visible to the user anymore    
def hideToggledControls():
    toggledUpdateByNameButton.setVisible(False)
    toggledUpdateByNumberButton.setVisible(False)
    toggledAddButton.setVisible(False)
    toggledDeleteButton.setVisible(False)
    toggledNameToUpdateLabel.setVisible(False)
    toggledNameToUpdate.setVisible(False)
    toggledNumberToUpdate.setVisible(False)
    toggledNumberToUpdateLabel.setVisible(False)
    
def nameGrabAction():
    response = requests.get(api_url + "GetCustomerByName/" + toggledNameToUpdate.text(), verify=False)
    if(response.status_code == 200):
        response = response.json()
        #turn the response to a string then split by ' and remove : and , from age and phone number then send to text box
        strReal = str(response)
        splitOutput = strReal.split("'")
        toggledNameText.setText(f'{splitOutput[3]}')
        toggledNumberText.setText(f"{splitOutput[6].strip(': ,')}")
        toggledAgeText.setText(f"{splitOutput[8].strip(': ,')}")
        toggledPizzaText.setText(f'{splitOutput[11]}')
        showControls()
        toggledUpdateByNameButton.setVisible(True)
        nameToUpdateGrabButton.setVisible(False)
        toggledNameToUpdate.setVisible(False)
        toggledNameToUpdateLabel.setVisible(False)
        #Rob was here
    else:
        textbox.append("No customer found")
        
def numberToUpdateAction():
    if(len(toggledNumberToUpdate.text()) != 10):
        textbox.append('Please enter a valid phone number')
    else:
        response = requests.get(api_url + "GetCustomerById/" + toggledNumberToUpdate.text(), verify=False)
        if(response.status_code == 200):
            response = response.json()
            #turn the response to a string then split by ' and remove : and , from age and phone number then send to text box
            strReal = str(response)
            splitOutput = strReal.split("'")
            toggledNameText.setText(f'{splitOutput[3]}')
            toggledNumberText.setText(f"{splitOutput[6].strip(': ,')}")
            toggledAgeText.setText(f"{splitOutput[8].strip(': ,')}")
            toggledPizzaText.setText(f'{splitOutput[11]}')
            showControls()
            toggledUpdateByNumberButton.setVisible(True)
            numberToUpdateGrabButton.setVisible(False)
            toggledNumberToUpdate.setVisible(False)
            toggledNumberToUpdateLabel.setVisible(False)
        else:
            textbox.append("No customer found")
    
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
nameInputBox.setValidator(letterValidator)
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
numberInputBox.setValidator(numberValidator)
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
toggledNameToUpdate = QLineEdit(mainMenu)
toggledNameToUpdate.move((nameInputBox.size().width() * 2) + 30, 260)
toggledNameToUpdate.setVisible(False)
toggledNameToUpdate.setValidator(letterValidator)
toggledNameToUpdateLabel = QLabel(mainMenu)
toggledNameToUpdateLabel.setText("Name to update:")
toggledNameToUpdateLabel.move((nameInputBox.size().width()) - 37, 260)
toggledNameToUpdateLabel.setVisible(False)
nameToUpdateGrabButton = QPushButton(mainMenu)
nameToUpdateGrabButton.setText("Grab")
nameToUpdateGrabButton.setVisible(False)
nameToUpdateGrabButton.move((nameInputBox.size().width() * 2) + 30, 300)
nameToUpdateGrabButton.clicked.connect(nameGrabAction)
toggledNumberToUpdate = QLineEdit(mainMenu)
toggledNumberToUpdate.move((nameInputBox.size().width() * 2) + 30, 260)
toggledNumberToUpdate.setVisible(False)
toggledNumberToUpdate.setValidator(numberValidator)
toggledNumberToUpdateLabel = QLabel(mainMenu)
toggledNumberToUpdateLabel.setText("Number to update:")
toggledNumberToUpdateLabel.move((nameInputBox.size().width()) - 58, 260)
toggledNumberToUpdateLabel.setVisible(False)
numberToUpdateGrabButton = QPushButton(mainMenu)
numberToUpdateGrabButton.setText("Grab")
numberToUpdateGrabButton.setVisible(False)
numberToUpdateGrabButton.move((nameInputBox.size().width() * 2) + 30, 300)
numberToUpdateGrabButton.clicked.connect(numberToUpdateAction)
toggledNameText = QLineEdit(mainMenu)
toggledNameText.move((nameInputBox.size().width() * 2) + 30, 300)
toggledNameText.setVisible(False)
toggledNameText.setValidator(letterValidator)
toggledNumberText = QLineEdit(mainMenu)
toggledNumberText.move((nameInputBox.size().width() * 2) + 30, 340)
toggledNumberText.setVisible(False)
toggledNumberText.setValidator(numberValidator)
toggledAgeText = QLineEdit(mainMenu)
toggledAgeText.move((nameInputBox.size().width() * 2) + 30, 380)
toggledAgeText.setVisible(False)
toggledAgeText.setValidator(numberValidator)
toggledPizzaText = QLineEdit(mainMenu)
toggledPizzaText.setValidator(letterValidator)
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
toggledDeleteNumberLabel = QLabel(mainMenu)
toggledDeleteNumberLabel.move((nameInputBox.size().width()) + 39, 390)
toggledDeleteNumberLabel.setText("Number:")
toggledDeleteNumberLabel.setVisible(False)
toggledDeleteNumberText = QLineEdit(mainMenu)
toggledDeleteNumberText.move((nameInputBox.size().width() * 2) + 30, 390)
toggledDeleteNumberText.setVisible(False)
toggledDeleteNumberText.setValidator(numberValidator)
toggledDeleteNumberButton = QPushButton(mainMenu)
toggledDeleteNumberButton.setText("Delete (serious)")
toggledDeleteNumberButton.move((nameInputBox.size().width() * 2) + 30, 430)
toggledDeleteNumberButton.setVisible(False)
toggledDeleteNumberButton.clicked.connect(toggledDeleteNumberAction)
#Import and export controls
exportButton = QPushButton(mainMenu)
exportButton.setText("Export")
exportButton.move((int(1280/2) - 150), 800)
exportButton.setVisible(False)
exportButton.clicked.connect(exportAction)
importButton = QPushButton(mainMenu)
importButton.setText("Import")
importButton.move((int(1280/2) - 150), 850)
importButton.setVisible(False)
importButton.clicked.connect(importAction)
#Clear console button
clearConsoleButton = QPushButton(mainMenu)
clearConsoleButton.setText("Clear")
clearConsoleButton.move((int(1280/2) - 150), 900)
clearConsoleButton.setVisible(False)
clearConsoleButton.clicked.connect(clearConsoleAction)
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