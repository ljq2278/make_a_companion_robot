from fastapi import FastAPI, Form
from pydantic import BaseModel
import queue
import threading
import tkinter as tk

app = FastAPI()
messages = queue.Queue()




def start_tkinter():
    window = tk.Tk()
    window.geometry("1280x960")
    window.title("Network Messages")
    scrollbar = tk.Scrollbar(window)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    # label = tk.Label(window, text="", font=("Arial", 24))
    text_box = tk.Text(window, font=("Arial", 24), yscrollcommand=scrollbar.set)
    scrollbar.config(command=text_box.yview)
    # label.place(x=50, y=0)
    text_box.pack(side="top", padx=10, pady=10)

    # label.pack()

    def update_label():
        if not messages.empty():
            # label.config(text=label.cget('text') + messages.get())
            text_box.insert(tk.END, messages.get())
        window.after(1000, update_label)

    window.after(1000, update_label)
    window.mainloop()


@app.post("/message")
async def receive_message(content: str = Form(...)):
    print("get message: ", content)
    messages.put(content)


threading.Thread(target=start_tkinter).start()
