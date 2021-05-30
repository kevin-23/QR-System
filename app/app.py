from PIL import Image
from tkinter import *
import tkinter.messagebox
import pymongo
import secrets
import pyqrcode

#Creating and connecting with the database
client = pymongo.MongoClient("mongodb://172.16.0.3:27017/")
database = client["users"]
collection = database["user_data"]

#The main window is initialized with its options
root = Tk()
root.resizable(0,0)
root.title('QR System')
root.geometry('900x550')

#Destroy all widgets from frame
def clear():
    for widget in qr_frame.winfo_children():
       widget.destroy()

#Creating the QR code
def data():
    clear()
    result = collection.find_one({ "identification" : identification.get()})
    empty_message = 'You must type a value in the First Name, Identification and Phone Number fields.'
    int_message = 'You must type a interger values in the Identification and Phone Number fields.'

    user_id = secrets.token_hex(5)
    qr_code = pyqrcode.create(user_id)
    qr_code.png(f'./qr-codes/{user_id}.png', scale=10)

    if (len(first_name.get()) == 0 or len(identification.get()) == 0 or len(phone_number.get()) == 0):
        tkinter.messagebox.showerror(title='ERROR!', message=empty_message)
    else:
        int_identification = identification.get()
        int_phone = phone_number.get()
        if not int_identification.isdigit() or not int_phone.isdigit():
            tkinter.messagebox.showerror(title='ERROR!', message=int_message)
        elif result == None:
            data = { "_id" : user_id, "first_name" : first_name.get(),
            "last_name" : last_name.get(), "identification" : int_identification,
            "email" : email.get(), "phone_number" : int_phone }
            collection.insert_one(data)

            qr_frame.place(relx=0.2, rely=0.2,
                     height=250,
                     width=220)
            qrimage = PhotoImage(file=f'./qr-codes/{user_id}.png')
            qrimage_resize = qrimage.subsample(2,2)
            label = Label(qr_frame, image=qrimage_resize)
            label.image = qrimage_resize
            label.place(x=10, y=1,
                  height=200,
                  width=200)
            Label(qr_frame, text=f'QR Code Value: \n{user_id}',
            font='arial 10 bold').place(relx=0.2, rely=0.74)
        elif result['identification'] == int_identification:
            tkinter.messagebox.showerror(title='ERROR!', message='The user identification already exists!')

def consult(value1):
    clear()
    result = collection.find_one({ "identification" : value1 })

    qr_frame.place(relx=0.09, rely=0,
             height=460,
             width=300)

    if result == None:
        label = Label(qr_frame, text='The user does not exist!',
                font='arial 14 bold').place(relx=.5, rely=.5, anchor="center")
    else:
        qrimage = PhotoImage(file=f'./qr-codes/{result["_id"]}.png')
        qrimage_resize = qrimage.subsample(2,2)
        label = Label(qr_frame, image=qrimage_resize)
        label.image = qrimage_resize
        label.place(x=60, y=10)
        Label(qr_frame, text=f'QR Code Value: \n{result["_id"]}',
        font='arial 10 bold').place(relx=0.28, rely=0.4)

        Label(qr_frame, text=f"First name: {result['first_name']}",
        font="arial 10 bold").place(relx=0.2, rely=0.55)
        Label(qr_frame, text=f"Last name: {result['last_name']}",
        font="arial 10 bold").place(relx=0.2, rely=0.65)
        Label(qr_frame, text=f"Identification: {result['identification']}",
        font="arial 10 bold").place(relx=0.2, rely=0.75)
        Label(qr_frame, text=f"Email: {result['email']}",
        font="arial 10 bold").place(relx=0.2, rely=0.85)
        Label(qr_frame, text=f"Phone Number: {result['phone_number']}",
        font="arial 10 bold").place(relx=0.2, rely=0.95)


def consult_window():
    consult_window = Tk()
    consult_window.resizable(0,0)
    consult_window.title('Consult a user')
    consult_window.geometry('420x140')

    Label(consult_window, text="Write the user identification",
    font='arial 10 bold').place(relx=0.23, rely=0.15)
    registry = Entry(consult_window, highlightbackground="red",
               bd=1,
               width=30,
               justify=CENTER)
    registry.place(relx=0.2, rely=0.38)

    find_user = Button(consult_window, text='Search the user',
                font='arial 10 bold',
                command=lambda:[consult(registry.get()),
                consult_window.destroy()])
    find_user.place(relx=0.32, rely=0.63)


#This frame conatais the user's input values
input_values = LabelFrame(root, text="The user input values",
               font="arial 10 bold",
               height=360,
               width=420)
input_values.place(relx=0.5, rely=0.03)

name = Label(input_values, text="First name",
       font="arial 10 bold",
       height=2,
       width=10).place(x=42, y=20)
first_name = Entry(input_values, bd=1,
             width=30,
             justify=CENTER)
first_name.place(x=150, y=30)

lastname = Label(input_values, text="Last name",
           font="arial 10 bold",
           height=2,
           width=10).place(x=43, y=80)
last_name = Entry(input_values, bd=1,
            width=30,
            justify=CENTER)
last_name.place(x=150, y=90)

id = Label(input_values, text="Identification",
     font="arial 10 bold",
     height=2,
     width=15).place(x=25, y=140)
identification = Entry(input_values, bd=1,
                 width=30,
                 justify=CENTER)
identification.place(x=150, y=150)

e_mail = Label(input_values, text="Email",
         font="arial 10 bold",
         height=2,
         width=10).place(x=45, y=200)
email = Entry(input_values, bd=1,
        width=30,
        justify=CENTER)
email.place(x=150, y=210)

number = Label(input_values, text="Phone number",
         font="arial 10 bold",
         height=2,
         width=15).place(x=20, y=260)
phone_number = Entry(input_values, bd=1,
               width=30,
               justify=CENTER)
phone_number.place(x=150, y=270)

#This frame are the buttons
buttons_frame = Frame(root, height=180, width=420)
buttons_frame.place(relx=0.5, rely=0.7)

qr_generator_button = Button(buttons_frame, text="Generate QR Code",
                      bd=10,
                      border=1,
                      font="arial 10 bold",
                      height=2,
                      width=15,
                      command=data).place(x=30, y=10)
consult_user_button = Button(buttons_frame, text="Consult a user",
                      bd=1,
                      font="arial 10 bold",
                      height=2,
                      width=15,
                      command=consult_window).place(x=225, y=10)
clear_button = Button(buttons_frame, text="Clear the results",
               bd=1,
               font="arial 10 bold",
               height=2,
               width=15,
               command=clear).place(x=120, y=80)

#This frame contains the results
result_frame = LabelFrame(root, text="Results", font="arial 10 bold")
result_frame.place(relx=0.03, rely=0.03,
             height=500,
             width=370)

qr_frame = Frame(result_frame)

root.mainloop()
