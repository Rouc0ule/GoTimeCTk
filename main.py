import sys
import os
from customtkinter import *
from tkinter import messagebox
from CTkMenuBar import *
from datetime import datetime
from json import load, dump
from pygame import mixer

def validate_numeric_input(text):
    return text.isdigit() or text == ""

def update_clock():
    current_time = datetime.now().strftime("%X")
    clockLabel.configure(text=current_time)
    app.after(500, update_clock)

def start_timer():

    if clickSound_value == "on":
        btn_click_sound.play()

    global remaining_time, paused
    minutes = int(minuteEntry.get())
    seconds = int(secondEntry.get())
    total_seconds = minutes * 60 + seconds
    remaining_time = total_seconds
    paused = False
    update_timer()

def update_timer():
    global remaining_time, paused
    if not paused:
        if remaining_time > 0:
            minutes = remaining_time // 60
            seconds = remaining_time % 60
            timeLabel.configure(text=f"{minutes:02}:{seconds:02}")
            remaining_time -= 1
            app.after(1000, update_timer)
        else:
            timeLabel.configure(text="Time's up!")
            if alarm_value == "on":
                alarm_sound.play()
    else:
        timeLabel.configure(text="Paused")

def pause_resume_timer():

    if clickSound_value == "on":
        btn_click_sound.play()

    global paused
    paused = not paused
    if paused:
        pauseBtn.configure(text="Resume")
    else:
        pauseBtn.configure(text="Pause")
        update_timer()

def stop_timer():

    if clickSound_value == "on":
        btn_click_sound.play()
    global remaining_time
    remaining_time = 0
    timeLabel.configure(text="00:00")

def clear_entry():

    if clickSound_value == "on":
        btn_click_sound.play()

    minuteEntry.delete(0, END)
    secondEntry.delete(0, END)

def open_settings():
    
    global themeApp, alarmType, alarm_value, clickSound_value, gray_1, gray_2
        
    def doneBtnCommand():
        global alarmType, themeApp, alarm_value

        set_appearance_mode(themeApp)

        data["theme"] = themeMenu.get()
        themeApp = data["theme"]
        save_config(data)

        data["click-sounds"] = clickSoundSwitch.get()
        clickSound_value = data["click-sounds"]
        save_config(data)

        data["alarm-sounds"] = alarmSoundSwitch.get()
        alarm_value = data["alarm-sounds"]
        save_config(data)

        data["alarm-type"] = alarmSoundMenu.get()
        alarmType = data["alarm-type"]
        save_config(data)

        if clickSound_value == "on":
            btn_click_sound.play()

        settings_window.destroy()
        restart_program()

    def toggle_alarm_sound_menu():
        
        if alarmSoundSwitch_var.get() == "on":
            alarmSoundMenu.place(x=37.5, y=110)
        else:
            alarmSoundMenu.place_forget()

    themeList = [
        "Dark",
        "Light"
    ]

    themeValue = StringVar()
    themeValue.set(data["theme"])

    alarmSoundList = [
        "Classic Alarm", 
        "Digital Clock", 
        "Cowing Alarm", 
        "Security Alarm"
    ]

    alarmSoundvalue = StringVar()
    alarmSoundvalue.set(data["alarm-type"])

    settings_window = CTk()
    settings_window.geometry("300x200")

    optionsFrame = CTkFrame(settings_window, width=275, height=160, fg_color=gray_1, border_color=gray_2, border_width=2)
    optionsFrame.place(x=12.5,y=0)

    themeMenu = CTkOptionMenu(optionsFrame, width=200, fg_color=btn_color_1, button_color=btn_color_2, text_color=btn_text_color,
                              variable=themeValue,
                              values=themeList)
    themeMenu.place(x=37.5, y=20)

    clickSoundSwitch_var = StringVar()
    clickSoundSwitch_var.set(data["click-sounds"])

    clickSoundSwitch = CTkSwitch(optionsFrame, width=200, text="Click sounds", font=("", 15, "bold"), fg_color=btn_color_1, progress_color=btn_color_2, text_color=btn_text_color,
                                 variable=clickSoundSwitch_var, onvalue="on", offvalue="off")
    clickSoundSwitch.place(x=37.5,y=50)

    alarmSoundSwitch_var = StringVar()
    alarmSoundSwitch_var.set(data["alarm-sounds"])

    alarmSoundSwitch = CTkSwitch(optionsFrame, width=200, text="Alarm sounds", font=("", 15, "bold"), fg_color=btn_color_1, progress_color=btn_color_2, text_color=btn_text_color,
                                 variable=alarmSoundSwitch_var, onvalue="on", offvalue="off",
                                 command=toggle_alarm_sound_menu)
    alarmSoundSwitch.place(x=37.5,y=80)

    alarmSoundMenu = CTkOptionMenu(optionsFrame, variable=alarmSoundvalue, width=200, fg_color=btn_color_1, button_color=btn_color_2, text_color=btn_text_color,
                              values=alarmSoundList)
    alarmSoundMenu.place(x=37.5, y=110)

    doneBtn = CTkButton(settings_window, text="Done", width=100, command=doneBtnCommand, fg_color=btn_color_1, hover_color=btn_color_2, border_color=btn_color_3, border_width=3, text_color=btn_text_color,)
    doneBtn.place(x=193, y=165)

    settings_window.mainloop()

def restart_program():
    app.destroy()
    os.startfile("main.py")

def load_config():
    try:
        with open("settings.json", 'r') as file:
            config = load(file)
        return config
    except FileNotFoundError:
        messagebox.showerror(title=f"Erreur", message=f"Le fichier de paramètre de GoTime n'a pas été trouvé pour lecture.")
        return None; exit()
        
def save_config(config):
    try:
        with open("settings.json", 'w') as file:
            dump(config, file, indent=4)
    except FileNotFoundError:
        messagebox.showerror(title=f"Erreur", message=f"Le fichier de paramètre de GoTime n'a pas été trouvé pour écriture.")
        return None; exit()

data = load_config()

themeApp = data["theme"]
clickSound_value = data["click-sounds"]
alarm_value = data["alarm-sounds"]
alarmType = data["alarm-type"]

if themeApp == "Dark" :

    green_1 = "#418D3A"
    green_2 = "#7CFF70"

    orange_1 = "#8d633a"
    orange_2 = "#ffb870"

    purple_1 = "#563a8d"
    purple_2 = "#a070ff"

    gray_1 = "#4d4d4d"
    gray_2 = "#808080"

    btn_text_color = "white"

    btn_color_1 = "#444444"
    btn_color_2 = "#333333"
    btn_color_3 = "#404040"

    entry_color = "#303030"

elif themeApp == "Light":

    green_1 = "#7CFF70"
    green_2 = "#418D3A"

    orange_1 = "#ffb870"
    orange_2 = "#8d633a"

    purple_1 = "#a070ff"
    purple_2 = "#563a8d"

    gray_1 = "#808080"
    gray_2 = "#4d4d4d"

    btn_text_color = "black"

    btn_color_1 = "#bfbfbf"
    btn_color_2 = "#cccccc"
    btn_color_3 = "#bbbbbb"

    entry_color = "#cfcfcf"

mixer.init()

if alarmType == "Classic Alarm":
    alarm_sound= mixer.Sound("sounds/alarms/classic-alarm.wav")
elif alarmType == "Digital Clock":
    alarm_sound= mixer.Sound("sounds/alarms/digital-clock-alarm.wav")
elif alarmType == "Cowing Alarm":
    alarm_sound= mixer.Sound("sounds/alarms/rooster-crowing-morning-alarm.wav")
elif alarmType == "Security Alarm":
    alarm_sound= mixer.Sound("sounds/alarms/security-alarm.wav")

btn_click_sound= mixer.Sound("sounds/clicks/interface-click.wav")
check_box_sound= mixer.Sound("sounds/clicks/box-check-click.wav")


app = CTk()
app.geometry("515x320")
app.title("GoTime")
app.resizable(False, False)
set_appearance_mode(themeApp)

menu = CTkTitleMenu(app)

window = menu.add_cascade("Window")
commands = menu.add_cascade("Commands")
about = menu.add_cascade("About")

dropdown1 = CustomDropdownMenu(widget=window)
dropdown1.add_option(option="Settings", command=open_settings)
dropdown1.add_separator()
dropdown1.add_option(option="Restart", command=restart_program)
dropdown1.add_option(option="Shutdown", command=quit)

dropdown2 = CustomDropdownMenu(widget=commands)
dropdown2.add_option(option="Clear entry", command=clear_entry)
dropdown2.add_separator()
dropdown2.add_option(option="Start", command=start_timer)
dropdown2.add_option(option="Pause", command=pause_resume_timer)
dropdown2.add_option(option="Stop", command=stop_timer)


clockFrame = CTkFrame(app, width=100, height=100, fg_color=green_1, border_color=green_2, border_width=2)
clockFrame.place(x=5, y=5)

timeFrame = CTkFrame(app, width=400, height=100, fg_color=orange_1, border_color=orange_2, border_width=2)
timeFrame.place(x=110, y=5)

entryFrame = CTkFrame(app, width=505, height=100, fg_color=purple_1, border_color=purple_2, border_width=2)
entryFrame.place(x=5, y=110)

btnFrame = CTkFrame(app, width=505, height=100, fg_color=gray_1, border_color=gray_2, border_width=2)
btnFrame.place(x=5, y=215)

clockLabel = CTkLabel(clockFrame, text="", width=95, height=95, font=("", 20, "bold"))
clockLabel.place(relx=0.5, rely=0.5, anchor="center")

timeLabel = CTkLabel(timeFrame, text="00:00", width=200, height=50, font=("", 20, "bold"))
timeLabel.place(relx=0.5, rely=0.5, anchor="center")

startBtn = CTkButton(btnFrame, text="Start", width=150, font=("", 20, "bold"), text_color=btn_text_color, fg_color=btn_color_1, hover_color=btn_color_2, border_color=btn_color_3, border_width=3, command=start_timer)
startBtn.place(x=15, rely=0.5, anchor="w")

pauseBtn = CTkButton(btnFrame, text="Pause", width=150, font=("", 20, "bold"), text_color=btn_text_color, fg_color=btn_color_1, hover_color=btn_color_2, border_color=btn_color_3, border_width=3, command=pause_resume_timer)
pauseBtn.place(x=175, rely=0.5, anchor="w")

stopBtn = CTkButton(btnFrame, text="Stop", width=150, font=("", 20, "bold"), text_color=btn_text_color, fg_color=btn_color_1, hover_color=btn_color_2, border_color=btn_color_3, border_width=3, command=stop_timer)
stopBtn.place(x=335, rely=0.5, anchor="w")

minuteLabel = CTkLabel(entryFrame, text="Minutes", font=("", 15, "bold", "italic"))
minuteLabel.place(x=20, y=10)

secondLabel = CTkLabel(entryFrame, text="Seconds", font=("", 15, "bold", "italic"))
secondLabel.place(x=180, y=10)

minuteEntry = CTkEntry(entryFrame, placeholder_text="", width=150, font=("", 20, "bold"), text_color=btn_text_color, fg_color=entry_color, border_color=btn_color_3, border_width=3)
minuteEntry.place(x=15, rely=0.5, anchor="w")
minuteEntry.configure(validate="key", validatecommand=(minuteEntry.register(validate_numeric_input), "%P"))

secondEntry = CTkEntry(entryFrame, placeholder_text="", width=150, font=("", 20, "bold"), text_color=btn_text_color, fg_color=entry_color, border_color=btn_color_3, border_width=3)
secondEntry.place(x=175, rely=0.5, anchor="w")
secondEntry.configure(validate="key", validatecommand=(secondEntry.register(validate_numeric_input), "%P"))

clearBtn = CTkButton(entryFrame, text="Clear", width=150, font=("", 20, "bold"), text_color=btn_text_color, fg_color=btn_color_1, hover_color=btn_color_2, border_color=btn_color_3, border_width=3, command=clear_entry)
clearBtn.place(x=335, rely=0.5, anchor="w")

update_clock()

app.mainloop()