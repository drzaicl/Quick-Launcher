import tkinter as tk
from tkinter import filedialog, simpledialog
import os
import json

# ==== STYLE ====
BG = "#1e1e1e"
BTN = "#2d2d2d"
TXT = "white"
ACCENT = "#4CAF50"

# ==== LOAD ====
try:
    with open("profiles.json", "r") as f:
        profiles = json.load(f)
except:
    profiles = {"Work": [], "Gaming": []}

current_profile = list(profiles.keys())[0]

# ==== LOGIC ====
def save_profiles():
    with open("profiles.json", "w") as f:
        json.dump(profiles, f)

def refresh_profiles():
    profile_list.delete(0, tk.END)
    for p in profiles:
        profile_list.insert(tk.END, p)

def refresh_apps():
    listbox.delete(0, tk.END)
    for app in profiles[current_profile]:
        listbox.insert(tk.END, os.path.basename(app))

def select_profile(event):
    global current_profile
    sel = profile_list.curselection()
    if sel:
        current_profile = profile_list.get(sel[0])
        refresh_apps()
        label_status.config(text=f"Selected: {current_profile}")

def add_profile():
    name = simpledialog.askstring("New Profile", "Enter profile name:")
    if not name:
        return
    if name in profiles:
        label_status.config(text="Profile exists!")
        return

    profiles[name] = []
    save_profiles()
    refresh_profiles()
    label_status.config(text=f"Added profile: {name}")

def rename_profile():
    global current_profile
    new = simpledialog.askstring("Rename", "New name:")
    if not new:
        return

    profiles[new] = profiles.pop(current_profile)
    current_profile = new

    save_profiles()
    refresh_profiles()
    refresh_apps()
    label_status.config(text=f"Renamed to: {new}")

def delete_profile():
    global current_profile

    if len(profiles) <= 1:
        label_status.config(text="Need at least 1 profile")
        return

    sel = profile_list.curselection()
    if not sel:
        return

    name = profile_list.get(sel[0])

    confirm = simpledialog.askstring("Confirm", f"Type '{name}' to delete:")
    if confirm != name:
        return

    profiles.pop(name)
    current_profile = list(profiles.keys())[0]

    save_profiles()
    refresh_profiles()
    refresh_apps()
    label_status.config(text=f"Deleted: {name}")

def add_app():
    path = filedialog.askopenfilename()
    if path:
        profiles[current_profile].append(path)
        save_profiles()
        refresh_apps()
        label_status.config(text=f"Added app")

def delete_app():
    sel = listbox.curselection()
    if sel:
        profiles[current_profile].pop(sel[0])
        save_profiles()
        refresh_apps()
        label_status.config(text="App deleted")

def run_apps():
    apps = profiles[current_profile]

    if not apps:
        label_status.config(text="No apps in profile!")
        return

    count = 0
    for app in apps:
        if os.path.exists(app):
            os.startfile(app)
            count += 1

    label_status.config(text=f"{count} apps started!")

def close_app():
    root.destroy()

# ==== GUI ====
root = tk.Tk()
root.title("Quick Launcher")
root.geometry("600x400")
root.configure(bg=BG)

# TITLE
tk.Label(root, text="Quick Launcher",
         font=("Arial", 18, "bold"),
         fg=TXT, bg=BG).pack(pady=10)

# MAIN FRAME
main = tk.Frame(root, bg=BG)
main.pack()

# LEFT (PROFILES)
frame_profiles = tk.Frame(main, bg=BG)
frame_profiles.grid(row=0, column=0, padx=20)

tk.Label(frame_profiles, text="Profiles", fg=TXT, bg=BG).pack()

profile_list = tk.Listbox(frame_profiles, bg=BTN, fg=TXT, width=20)
profile_list.pack(pady=5)
profile_list.bind("<<ListboxSelect>>", select_profile)
profile_list.config(selectbackground=ACCENT)

tk.Button(frame_profiles, text="Add", command=add_profile,
          bg=BTN, fg=TXT, width=18).pack(pady=2)

tk.Button(frame_profiles, text="Rename", command=rename_profile,
          bg=BTN, fg=TXT, width=18).pack(pady=2)

tk.Button(frame_profiles, text="Delete", command=delete_profile,
          bg=BTN, fg=TXT, width=18).pack(pady=2)

# RIGHT (APPS)
frame_apps = tk.Frame(main, bg=BG)
frame_apps.grid(row=0, column=1, padx=20)

tk.Label(frame_apps, text="Apps", fg=TXT, bg=BG).pack()

listbox = tk.Listbox(frame_apps, bg=BTN, fg=TXT, width=35)
listbox.pack(pady=5)
listbox.config(selectbackground=ACCENT)

tk.Button(frame_apps, text="Add App", command=add_app,
          bg=BTN, fg=TXT, width=25).pack(pady=2)

tk.Button(frame_apps, text="Delete App", command=delete_app,
          bg=BTN, fg=TXT, width=25).pack(pady=2)

tk.Button(frame_apps, text="Run Apps", command=run_apps,
          bg=ACCENT, fg="black", width=25).pack(pady=5)

# STATUS
label_status = tk.Label(root, text="Ready",
                        fg=ACCENT, bg=BG)
label_status.pack(pady=10)

# EXIT
tk.Button(root, text="Exit", command=close_app,
          bg=BTN, fg=TXT, width=20).pack()

# INIT
refresh_profiles()
refresh_apps()

root.mainloop()