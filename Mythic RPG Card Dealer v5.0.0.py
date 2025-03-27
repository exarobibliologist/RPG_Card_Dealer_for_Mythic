import os
import random
import tkinter as tk
from tkinter import filedialog, scrolledtext
from PIL import Image, ImageTk

# Get the script directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FATE_CHART_FILE = os.path.join(SCRIPT_DIR, "FateChart.png")  # Path to FateChart.png

# Load images from a selected folder
def load_images(folder_path):
    return [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.lower().endswith((".png", ".jpg", ".jpeg"))]

# Load the last used folder path
def load_last_folder():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            folder_path = f.read().strip()
            return folder_path if os.path.isdir(folder_path) else None
    return None

def save_last_folder(folder_path):
    with open(SAVE_FILE, "w") as f:
        f.write(folder_path)

# Select folder containing card images
def select_folder():
    global card_images
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        card_images = load_images(folder_selected)
        result_label.config(text=f"Loaded {len(card_images)} cards." if card_images else "No images found.")
        save_last_folder(folder_selected)  # Save folder path after selection

# Shuffle and deal cards
def deal_cards(num_cards=None):
    if not card_images:
        result_label.config(text="No folder selected. Please load images first.")
        return
    
    if num_cards is None:
        try:
            num_cards = int(entry.get())
        except ValueError:
            result_label.config(text="Enter a valid number.")
            return
    
    if num_cards <= 0 or num_cards > len(card_images):
        result_label.config(text="Invalid number of cards.")
        return
    
    random.shuffle(card_images)
    selected_cards = card_images[:num_cards]
    show_cards(selected_cards, rotate=True)

# Display cards in a new window
def show_cards(selected_cards, rotate=False):
    card_window = tk.Toplevel(root)
    card_window.title("Dealt Cards")
    
    for idx, card in enumerate(selected_cards):
        img = Image.open(card).resize((250, 350))
        
        if rotate and random.choice([True, False]):  # Randomly rotate some cards
            img = img.rotate(180)
        
        photo = ImageTk.PhotoImage(img)
        label = tk.Label(card_window, image=photo)
        label.image = photo
        label.grid(row=idx // 5, column=idx % 5, padx=10, pady=10)

# Function to show the Fate Chart (always upright)
def show_fate_chart():
    if not os.path.exists(FATE_CHART_FILE):
        result_label.config(text="FateChart.png not found.")
        return
    show_cards([FATE_CHART_FILE], rotate=False)

# Function to create a new game (clear all fields)
def new_game():
    threads_list.delete("1.0", tk.END)
    characters_list.delete("1.0", tk.END)
    storyline_box.delete("1.0", tk.END)
    chaos_slider.set(5)

# Function to save data with file dialog
def save_data():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "w") as f:
            f.write("Threads List:\n" + threads_list.get("1.0", tk.END))
            f.write("Characters List:\n" + characters_list.get("1.0", tk.END))
            f.write("Chaos Factor:\n" + str(chaos_slider.get()) + "\n")
            f.write("Storyline:\n" + storyline_box.get("1.0", tk.END))

# Function to load data with file dialog
def load_data():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path and os.path.exists(file_path):
        with open(file_path, "r") as f:
            data = f.read().split("\n")
        try:
            threads_list.delete("1.0", tk.END)
            characters_list.delete("1.0", tk.END)
            storyline_box.delete("1.0", tk.END)
            
            threads_index = data.index("Threads List:") + 1
            characters_index = data.index("Characters List:") + 1
            chaos_index = data.index("Chaos Factor:") + 1
            storyline_index = data.index("Storyline:") + 1
            
            threads_list.insert("1.0", "\n".join(data[threads_index:characters_index-1]))
            characters_list.insert("1.0", "\n".join(data[characters_index:chaos_index-1]))
            chaos_slider.set(int(data[chaos_index]))
            storyline_box.insert("1.0", "\n".join(data[storyline_index:]))
        except ValueError:
            pass

# GUI Setup
root = tk.Tk()
root.title("Mythic RPG Card Dealer v5.1.5")
root.geometry("700x300")

# Game State Window
game_state_window = tk.Toplevel(root)
game_state_window.title("Game State")
game_state_window.geometry("700x600")
game_state_window.transient(root)  # Keeps it tied to main window
game_state_window.protocol("WM_DELETE_WINDOW", lambda: None)  # Disable closing
root.protocol("WM_DELETE_WINDOW", lambda: [game_state_window.destroy(), root.destroy()])

# Buttons
button_frame = tk.Frame(root)
button_frame.pack()
tk.Button(button_frame, text="New", command=new_game).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Save", command=save_data).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Load", command=load_data).pack(side=tk.LEFT, padx=5)
tk.Button(root, text="Select Card Folder", command=select_folder).pack(pady=5)

result_label = tk.Label(root, text="No folder selected.")
result_label.pack()

# Horizontal Rule
separator = tk.Frame(root, height=2, bd=1, relief="sunken", bg="black")
separator.pack(fill="x", padx=5, pady=5)

tk.Button(root, text="Show Fate Chart", command=show_fate_chart).pack(pady=5)

# Horizontal Rule
separator = tk.Frame(root, height=2, bd=1, relief="sunken", bg="black")
separator.pack(fill="x", padx=5, pady=5)

# Quick Deal Cards
tk.Label(root, text="Quickly Draw Cards").pack()
quick_draw_frame = tk.Frame(root)
quick_draw_frame.pack()
for i in range(1, 11):
    tk.Button(quick_draw_frame, text=f"Draw {i}", command=lambda i=i: deal_cards(i)).pack(side=tk.LEFT, padx=5)

# Deal Cards Section
tk.Label(root, text="Enter number of cards to deal:").pack()
entry = tk.Entry(root)
entry.pack()
tk.Button(root, text="Deal Cards", command=deal_cards).pack(pady=5)

# Game State Window Elements
text_frame = tk.Frame(game_state_window)
text_frame.pack(pady=10)

def create_scrollable_text(parent, label):
    frame = tk.Frame(parent)
    tk.Label(frame, text=label).pack()
    text_box = scrolledtext.ScrolledText(frame, width=30, height=20, wrap=tk.WORD)
    text_box.pack()
    frame.pack(side=tk.LEFT, padx=10)
    return text_box

threads_list = create_scrollable_text(text_frame, "Threads List")
chaos_slider = tk.Scale(text_frame, from_=9, to=1, orient=tk.VERTICAL, label="Chaos Factor")
chaos_slider.pack(side=tk.LEFT, padx=10)
characters_list = create_scrollable_text(text_frame, "Characters List")

tk.Label(game_state_window, text="Storyline").pack()
storyline_box = scrolledtext.ScrolledText(game_state_window, width=80, height=10, wrap=tk.WORD)
storyline_box.pack(pady=10)

root.mainloop()
