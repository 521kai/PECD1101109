print ("你好")


import tkinter as tk
from tkinter import messagebox

def on_button_click():
    name = entry.get()
    if name.strip() == "":
        messagebox.showwarning("提醒", "請輸入名稱！")
    else:
        messagebox.showinfo("Hello", f"Hello, {name}！")

# 建立主視窗
window = tk.Tk()
window.title("Tkinter 範例")
window.geometry("500x300")

# 標籤
label = tk.Label(window, text="請輸入你的名字：", font=("Arial", 12))
label.pack(pady=10)

# 輸入框
entry = tk.Entry(window, font=("Arial", 12))
entry.pack(pady=5)

# 按鈕
button = tk.Button(window, text="打招呼", font=("Arial", 12), command=on_button_click)
button.pack(pady=10)

# 進入主迴圈
window.mainloop()