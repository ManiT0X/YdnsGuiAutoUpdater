from tkinter import *
import requests
import math

# this endpoint is provided by ydns and will get your current ip
IP = requests.get("https://ydns.io/api/v1/ip").text

# time to count down in seconds starts a 0
time_in_sec = 0

# this is a way to turn off the timer between functions.
# time start when you click the button.
# if the response is not "OK", this will turn to False and timer won't start
is_ok = True


# this function will send a request ith your credentials and update your ip
def update_ip():
    global status_text, is_ok
    host = host_input.get()
    email = email_input.get()
    password = passwrd_input.get()
    response = requests.get(f"https://ydns.io/api/v1/update/?host={host}&ip={IP}", auth=(email, password))
    status_text.delete('1.0', END)
    status_text.insert(END, f"status: [{response.text}]")
    if response.text != "ok":
        is_ok = False


# this function will do the countdown
def timer():
    global time_in_sec
    seconds = time_in_sec % 60
    minutes = math.floor(time_in_sec / 60)
    if 0 <= seconds <= 10:
        seconds = f"0{seconds}"
    if minutes < 10:
        minutes = f"0{minutes}"
    countdown.config(text=f"{minutes}:{seconds}")
    window.update()
    time_in_sec -= 1
    if is_ok:
        count = window.after(1000, timer)
        if int(minutes) < 1 and int(seconds) < 1:
            update_ip()
            window.after_cancel(count)
            start_timer()


# this function will update the ip and start the countdown
def start_timer():
    global time_in_sec, is_ok
    is_ok = True
    update_ip()
    # if the length of the input == 0 , it means the field is empty
    if len(email_input.get()) == 0 or len(passwrd_input.get()) == 0 or len(host_input.get()) == 0:
        status_text.delete('1.0', END)
        status_text.insert(END, "make sure you don't leave any fields empty")
        is_ok = False
    time_in_sec = int(current_value.get()) * 60
    timer()


# Tkinter form
window = Tk()
window.title("Ydns Updater")
window.config(padx=20, pady=10)

label_host = Label(text="Ydns Host:", width=10, anchor="w", pady=10)
label_host.grid(row=0, column=0)

host_input = Entry()
host_input.grid(row=0, column=1, columnspan=2)

label_email = Label(text="Email:", width=10, anchor="w", pady=10)
label_email.grid(row=1, column=0)

email_input = Entry()
email_input.grid(row=1, column=1, columnspan=2)

label_passwrd = Label(text="Password:", width=10, anchor="w", pady=10)
label_passwrd.grid(row=2, column=0)

passwrd_input = Entry()
passwrd_input.grid(row=2, column=1, columnspan=2)

your_ip_label = Label(text="Your IP:", width=10, anchor="w", pady=10)
your_ip_label.grid(row=3, column=0)

ip_label = Label(text=f"{IP}", pady=10)
ip_label.grid(row=3, column=1)

update_every_label = Label(text="Update every: ", width=10, anchor="w", pady=10)
update_every_label.grid(row=4, column=0)

current_value = StringVar(value=0)
update = Spinbox(window, from_=1, to=60, textvariable=current_value, wrap=True, width=12, justify=CENTER)
update.grid(row=4, column=1)

min_label = Label(text="min")
min_label.grid(row=4, column=2)

confirm = Button(text="Confirm", command=start_timer, width=22)
confirm.grid(row=5, column=0, columnspan=3, pady=10)

countdown_label = Label(text="Update in: ")
countdown_label.grid(row=6, column=0)

countdown = Label(text="00:00", pady=10)
countdown.grid(row=6, column=1)

status_text = Text(width=25, height=3)
status_text.grid(row=7, column=0, columnspan=3)
window.mainloop()
