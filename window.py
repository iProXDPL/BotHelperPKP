import requests
import tkinter as tk
from tkinter import scrolledtext
import subprocess
import os
import time
import json
import uuid

random_id = str(uuid.uuid4())  
VENV_PATH = r".\venv\Scripts\activate.bat"
checking_status = True  # Flaga do kontrolowania pętli sprawdzania statusu

def check_rasa_status():
    global checking_status
    if not checking_status:
        return
    
    try:
        response = requests.get("http://localhost:5005")
        if response.status_code == 200:
            update_status("BOT Online", "green")
            checking_status = False  # Zatrzymanie dalszego sprawdzania statusu
            return
        else:
            update_status("BOT Offline", "red")
    except requests.exceptions.RequestException:
        update_status("BOT Offline", "red")
    
    root.after(5000, check_rasa_status)  # Kontynuacja sprawdzania jeśli bot jest offline

def update_status(status_text, color):
    status_label.config(text=status_text, fg=color)

def start_rasa():
    global rasa_process, actions_process
    rasa_process = subprocess.Popen(
        ['cmd.exe', '/K', f'{VENV_PATH} && rasa run'], creationflags=subprocess.CREATE_NEW_CONSOLE
    )
    actions_process = subprocess.Popen(
        ['cmd.exe', '/K', f'{VENV_PATH} && rasa run actions'], creationflags=subprocess.CREATE_NEW_CONSOLE
    )

def stop_rasa():
    global checking_status
    checking_status = False  # Zatrzymanie sprawdzania statusu
    if rasa_process:
        subprocess.call(['taskkill', '/F', '/T', '/PID', str(rasa_process.pid)])
    if actions_process:
        subprocess.call(['taskkill', '/F', '/T', '/PID', str(actions_process.pid)])

def send_message():
    user_message = user_input.get()
    if not user_message.strip():
        return
    
    chat_window.insert(tk.END, f"You: {user_message}\n", "user")
    user_input.delete(0, tk.END)
    
    response = requests.post(
        "http://localhost:5005/webhooks/rest/webhook",
        json={"sender": random_id, "message": user_message}
    )
    
    bot_response = ""
    suggestions = []
    if response.status_code == 200:
        messages = response.json()
        for message in messages:
            if "text" in message:
                bot_response += message["text"] + "\n"
            if "buttons" in message:
                suggestions = [button["title"] for button in message["buttons"]]
    else:
        bot_response = "Błąd połączenia z API."
    
    chat_window.insert(tk.END, f"Bot: {bot_response}\n", "bot")
    chat_window.yview(tk.END)
    update_suggestions(suggestions)

def insert_suggestion(suggestion):
    user_input.delete(0, tk.END)
    user_input.insert(0, suggestion)

def update_suggestions(new_suggestions):
    for widget in suggestions_frame.winfo_children():
        widget.destroy()
    
    if not new_suggestions:
        new_suggestions = ["Witam", "Szukam połaczenia"]
    
    for suggestion in new_suggestions:
        btn = tk.Button(suggestions_frame, text=suggestion, command=lambda s=suggestion: insert_suggestion(s))
        btn.pack(side=tk.LEFT, padx=2)

start_rasa()

# Tworzenie GUI
root = tk.Tk()
root.title("Chatbot Rasa")
root.protocol("WM_DELETE_WINDOW", lambda: (root.destroy(), stop_rasa()))  # Zamknięcie Rasa i GUI

status_label = tk.Label(root, text="BOT Offline", fg="red")
status_label.pack(pady=5)

chat_window = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=15)
chat_window.pack(padx=10, pady=10)
chat_window.tag_config("user", foreground="blue")
chat_window.tag_config("bot", foreground="green")

user_input = tk.Entry(root, width=40)
user_input.pack(pady=5)

send_button = tk.Button(root, text="Wyślij", command=send_message)
send_button.pack()

suggestions_frame = tk.Frame(root)
suggestions_frame.pack(pady=5)

check_rasa_status()
update_suggestions([]) 

root.mainloop()
