import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, UnidentifiedImageError
import cv2
import threading
import time
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# -------------------- MAIN WINDOW --------------------
root = tk.Tk()
root.title("AI Interview Bot")
root.geometry("1100x750")
root.configure(bg="#e8f1f2")

# -------------------- GLOBAL VARIABLES --------------------
current_user = ""
carousel_index = 0
carousel_images = [
    "a.jpg",
    "b.jpg",
    "c.jpg",
    "d.jpg"
]
carousel_photo = []
camera_stream = None

# -------------------- FRAME SWITCHER --------------------
def switch_frame(frame):
    for f in frames.values():
        f.pack_forget()
    frame.pack(fill="both", expand=True)

# -------------------- LOGIN --------------------
def login():
    global current_user
    user = username_entry.get()
    password = password_entry.get()
    if user == "admin" and password == "1234":
        current_user = user
        user_label.config(text=f"👤 {user}")
        switch_frame(home_frame)
        start_carousel()
    else:
        messagebox.showerror("Login Failed", "Invalid login! Use admin / 1234")

def logout():
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    switch_frame(login_frame)

# -------------------- RESUME UPLOAD --------------------
def upload_resume():
    file_path = filedialog.askopenfilename(filetypes=[("Documents", "*.pdf *.doc *.docx")])
    if file_path:
        resume_status.config(text=f"📄 Uploaded: {os.path.basename(file_path)}")
    else:
        messagebox.showwarning("No File", "Please select a file first!")

# -------------------- ROUND 1 --------------------
def submit_round1():
    messagebox.showinfo("Round 1", "✅ Round 1 Submitted Successfully!")
    switch_frame(round2_frame)

# -------------------- ROUND 2 --------------------
def submit_round2():
    messagebox.showinfo("Round 2", "✅ Round 2 Submitted Successfully!")
    switch_frame(round3_frame)

# -------------------- ROUND 3 --------------------
def start_camera():
    def camera_loop():
        global camera_stream
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror("Camera Error", "Could not access the camera!")
            return
        camera_stream = True
        while camera_stream:
            ret, frame = cap.read()
            if ret:
                cv2.imshow("Camera", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
        camera_stream = False

    threading.Thread(target=camera_loop).start()

def finish_interview():
    if camera_stream:
        messagebox.showwarning("Camera Running", "Close camera window first!")
    else:
        switch_frame(report_frame)
        show_report_chart()

# -------------------- IMAGE CAROUSEL --------------------
def start_carousel():
    def carousel_loop():
        global carousel_index
        while True:
            if carousel_photo:
                img_label.config(image=carousel_photo[carousel_index])
                carousel_index = (carousel_index + 1) % len(carousel_photo)
            else:
                img_label.config(text="⚠ No images found", fg="#ff3333", font=("Segoe UI", 18))
            time.sleep(3)
    threading.Thread(target=carousel_loop, daemon=True).start()

# -------------------- FRAMES --------------------
frames = {}

# -------------------- LOGIN FRAME --------------------
login_frame = tk.Frame(root, bg="white")

# Modern gradient header
header = tk.Frame(login_frame, bg="#0d6efd", height=150)
header.pack(fill="x")
tk.Label(header, text="🤖 AI Interview Bot", font=("Segoe UI", 38, "bold"), bg="#0d6efd", fg="white").pack(pady=30)

# Login box
login_box = tk.Frame(login_frame, bg="#f8f9fa", bd=2, relief="groove")
login_box.pack(pady=60, ipadx=20, ipady=20)

tk.Label(login_box, text="Welcome Back!", font=("Segoe UI", 22, "bold"), bg="#f8f9fa", fg="#0d6efd").pack(pady=10)
tk.Label(login_box, text="Login to Continue", font=("Segoe UI", 14), bg="#f8f9fa", fg="#495057").pack(pady=5)

# Username field
user_frame = tk.Frame(login_box, bg="white", bd=1, relief="solid")
user_frame.pack(pady=10)
tk.Label(user_frame, text="👤", bg="white", font=("Segoe UI", 16)).pack(side="left", padx=10)
username_entry = tk.Entry(user_frame, font=("Segoe UI", 14), width=25, bd=0)
username_entry.insert(0, "admin")
username_entry.pack(side="left", padx=5, pady=5)

# Password field
pass_frame = tk.Frame(login_box, bg="white", bd=1, relief="solid")
pass_frame.pack(pady=10)
tk.Label(pass_frame, text="🔒", bg="white", font=("Segoe UI", 16)).pack(side="left", padx=10)
password_entry = tk.Entry(pass_frame, font=("Segoe UI", 14), show="*", width=25, bd=0)
password_entry.insert(0, "1234")
password_entry.pack(side="left", padx=5, pady=5)

# Login button
tk.Button(login_box, text="LOGIN", font=("Segoe UI", 16, "bold"), bg="#00bfa5", fg="white",
          width=25, height=2, bd=0, command=login, activebackground="#009688").pack(pady=20)

frames["login"] = login_frame

# -------------------- HOME FRAME --------------------
home_frame = tk.Frame(root, bg="#e8f1f2")

top_nav = tk.Frame(home_frame, bg="#212529")
top_nav.pack(fill="x")

nav_buttons = [
    ("🏠 Home", lambda: switch_frame(home_frame)),
    ("📄 Resume Upload", lambda: switch_frame(resume_frame)),
    ("🧩 Round 1", lambda: switch_frame(round1_frame)),
    ("✏ Round 2", lambda: switch_frame(round2_frame)),
    ("🎥 Round 3", lambda: switch_frame(round3_frame)),
    ("📊 Report", lambda: switch_frame(report_frame)),
]
for txt, cmd in nav_buttons:
    tk.Button(top_nav, text=txt, bg="#00bfa5", fg="white", font=("Segoe UI", 12, "bold"),
              activebackground="#0d6efd", activeforeground="white", command=cmd).pack(side="left", padx=5, pady=5)

tk.Button(top_nav, text="🚪 Logout", bg="#dc3545", fg="white", font=("Segoe UI", 12, "bold"),
          command=logout).pack(side="right", padx=10, pady=5)

user_label = tk.Label(home_frame, text="", font=("Segoe UI", 20, "bold"), bg="#e8f1f2", fg="#0d6efd")
user_label.pack(pady=20)

tk.Label(home_frame, text="Welcome to AI Interview Bot! Prepare, Practice, and Excel.",
         font=("Segoe UI", 18), bg="#e8f1f2", fg="#333333").pack(pady=10)

img_label = tk.Label(home_frame, bg="#e8f1f2")
img_label.pack(pady=20)

# Load carousel images safely
for img_path in carousel_images:
    if os.path.exists(img_path):
        try:
            img = Image.open(img_path).resize((850, 350))
            carousel_photo.append(ImageTk.PhotoImage(img))
        except UnidentifiedImageError:
            print(f"Skipping invalid image: {img_path}")
    else:
        print(f"Image not found: {img_path}")

frames["home"] = home_frame

# -------------------- RESUME FRAME --------------------
resume_frame = tk.Frame(root, bg="#f8f9fa")
tk.Label(resume_frame, text="📁 Upload Your Resume", font=("Segoe UI", 28, "bold"), bg="#f8f9fa", fg="#0d6efd").pack(pady=20)
tk.Button(resume_frame, text="Choose File", bg="#00bfa5", fg="white", font=("Segoe UI", 14), command=upload_resume).pack(pady=10)
resume_status = tk.Label(resume_frame, text="", font=("Segoe UI", 14), bg="#f8f9fa", fg="#333333")
resume_status.pack(pady=10)
tk.Button(resume_frame, text="Next → Round 1", bg="#0d6efd", fg="white", font=("Segoe UI", 14),
          command=lambda: switch_frame(round1_frame)).pack(pady=20)
frames["resume"] = resume_frame

# -------------------- ROUND 1 FRAME --------------------
round1_frame = tk.Frame(root, bg="#eaf4f4")
tk.Label(round1_frame, text="🧩 Round 1: Multiple Choice Questions", font=("Segoe UI", 28, "bold"),
         bg="#eaf4f4", fg="#0d6efd").pack(pady=20)
quiz_questions = [
    ("What is AI?", ["Machine Learning", "Human Intelligence", "Artificial Intelligence", "Automation"]),
    ("HTML stands for?", ["Hyper Trainer Marking Language", "Hyper Text Markup Language", "High Text Machine Language", "None"])
]
quiz_vars = []
for i, (q, options) in enumerate(quiz_questions):
    tk.Label(round1_frame, text=f"{i+1}. {q}", font=("Segoe UI", 16), bg="#eaf4f4", fg="#333333").pack(anchor="w", padx=40)
    var = tk.IntVar()
    quiz_vars.append(var)
    for j, opt in enumerate(options):
        tk.Radiobutton(round1_frame, text=opt, variable=var, value=j, font=("Segoe UI", 14),
                       bg="#eaf4f4", fg="#212529", selectcolor="#bde0fe").pack(anchor="w", padx=60)
tk.Button(round1_frame, text="Submit Round 1", bg="#00bfa5", fg="white", font=("Segoe UI", 14), command=submit_round1).pack(pady=20)
frames["round1"] = round1_frame

# -------------------- ROUND 2 FRAME --------------------
round2_frame = tk.Frame(root, bg="#f1faee")
tk.Label(round2_frame, text="✏ Round 2: Short Answers", font=("Segoe UI", 28, "bold"), bg="#f1faee", fg="#0d6efd").pack(pady=20)
short_questions = [
    "Explain your strengths in 2-3 lines.",
    "What inspired you to pursue this field?",
    "Describe your biggest achievement briefly."
]
short_entries = []
for i, q in enumerate(short_questions):
    tk.Label(round2_frame, text=f"{i+1}. {q}", font=("Segoe UI", 16), bg="#f1faee", fg="#333333").pack(anchor="w", padx=40)
    entry = tk.Text(round2_frame, height=3, width=80, font=("Segoe UI", 12))
    entry.pack(padx=40, pady=5)
    short_entries.append(entry)
tk.Button(round2_frame, text="Submit Round 2", bg="#00bfa5", fg="white", font=("Segoe UI", 14), command=submit_round2).pack(pady=20)
frames["round2"] = round2_frame

# -------------------- ROUND 3 FRAME --------------------
round3_frame = tk.Frame(root, bg="#edf2fb")
tk.Label(round3_frame, text="🎥 Round 3: Live Camera Interview", font=("Segoe UI", 28, "bold"), bg="#edf2fb", fg="#0d6efd").pack(pady=20)
tk.Button(round3_frame, text="Start Camera", bg="#00bfa5", fg="white", font=("Segoe UI", 14), command=start_camera).pack(pady=10)
tk.Button(round3_frame, text="Finish Interview", bg="#0d6efd", fg="white", font=("Segoe UI", 14), command=finish_interview).pack(pady=10)
frames["round3"] = round3_frame

# -------------------- REPORT FRAME --------------------
report_frame = tk.Frame(root, bg="#e9ecef")
tk.Label(report_frame, text="📊 Final Report", font=("Segoe UI", 28, "bold"), bg="#e9ecef", fg="#0d6efd").pack(pady=20)

# Function to show chart
def show_report_chart():
    for widget in report_frame.winfo_children()[1:]:
        widget.destroy()
    scores = [85, 90, 80]
    labels = ['Round 1', 'Round 2', 'Round 3']
    fig, ax = plt.subplots(figsize=(6, 3), facecolor="#e9ecef")
    bars = ax.bar(labels, scores, color=['#0d6efd', '#00bfa5', '#6c757d'])
    ax.set_ylim(0, 100)
    ax.set_ylabel("Score (%)")
    ax.set_title("Performance Analysis")
    for bar, score in zip(bars, scores):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, f"{score}%", ha='center', fontsize=12)
    canvas = FigureCanvasTkAgg(fig, master=report_frame)
    canvas.get_tk_widget().pack()
    canvas.draw()
    tk.Label(report_frame, text="Overall Result: ✅ Selected", font=("Segoe UI", 20, "bold"), bg="#e9ecef", fg="#198754").pack(pady=20)
    tk.Button(report_frame, text="Back to Home", bg="#0d6efd", fg="white", font=("Segoe UI", 14),
              command=lambda: switch_frame(home_frame)).pack(pady=10)

frames["report"] = report_frame

# -------------------- START APP --------------------
switch_frame(login_frame)
root.mainloop()
