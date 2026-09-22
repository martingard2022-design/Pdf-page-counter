import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from pypdf import PdfReader


def start_counting():
    folder_path = folder_entry.get()
    if not folder_path or not os.path.isdir(folder_path):
        messagebox.showerror("ስህተት", "እባክዎን ትክክለኛ የፎልደር አድራሻ ይምረጡ!")
        return

    # ቁልፎቹን ለአፍታ ማገድ
    btn_count.config(state=tk.DISABLED)
    btn_browse.config(state=tk.DISABLED)
    status_label.config(text="እየቆጠረ ነው... እባክዎን ትንሽ ይጠብቁ...")
    root.update()

    total_pages = 0
    pdf_count = 0
    corrupted_count = 0

    try:
        files = os.listdir(folder_path)
        pdf_files = [f for f in files if f.lower().endswith(".pdf")]

        for file_name in pdf_files:
            pdf_path = os.path.join(folder_path, file_name)
            try:
                reader = PdfReader(pdf_path)
                total_pages += len(reader.pages)
                pdf_count += 1
            except Exception:
                corrupted_count += 1

        # ውጤቱን በስክሪኑ ላይ ማሳየት
        result_text = f"✅ ስራው ተጠናቋል!\n\n"
        result_text += f"▪ የተቆጠሩ PDF ፋይሎች: {pdf_count}\n"
        result_text += f"▪ ጠቅላላ የገጽ ብዛት: {total_pages} ገጾች\n"
        if corrupted_count > 0:
            result_text += f"⚠️ ማንበብ ያልተቻሉ ፋይሎች: {corrupted_count}"

        lbl_result.config(text=result_text, fg="green")
        status_label.config(text="ተጠናቋል!")

    except Exception as e:
        messagebox.showerror("ስህተት", f"ችግር አጋጥሟል: {str(e)}")
        status_label.config(text="")
    finally:
        btn_count.config(state=tk.NORMAL)
        btn_browse.config(state=tk.NORMAL)


def browse_folder():
    selected_dir = filedialog.askdirectory()
    if selected_dir:
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, selected_dir)


# GUI ማዘጋጀት
root = tk.Tk()
root.title("PDF Page Counter")
root.geometry("500x320")
root.resizable(False, False)

tk.Label(
    root, text="PDF Page Counter App", font=("Helvetica", 14, "bold")
).pack(pady=10)

frame = tk.Frame(root)
frame.pack(pady=10, fill="x", px=20)

folder_entry = tk.Entry(frame, width=40, font=("Helvetica", 10))
folder_entry.pack(side=tk.LEFT, px=5)

btn_browse = tk.Button(
    frame, text="Browse...", command=browse_folder, bg="#e1e1e1"
)
btn_browse.pack(side=tk.LEFT)

btn_count = tk.Button(
    root,
    text="ገጾችን ቆጥር (Calculate Pages)",
    command=start_count,
    bg="#4CAF50",
    fg="white",
    font=("Helvetica", 11, "bold"),
    pady=5,
)
btn_count.pack(pady=15)

status_label = tk.Label(root, text="", font=("Helvetica", 9, "italic"))
status_label.pack()

lbl_result = tk.Label(
    root, text="", font=("Helvetica", 11, "bold"), justify=tk.LEFT
)
lbl_result.pack(pady=10)

root.mainloop()
