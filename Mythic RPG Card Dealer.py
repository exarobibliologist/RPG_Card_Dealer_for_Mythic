import os
import random
import tkinter as tk
from tkinter import filedialog, scrolledtext, Canvas, Scrollbar, filedialog
from PIL import Image, ImageTk

# Get the script directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_FILE = os.path.join(SCRIPT_DIR, "last_folder.txt")  # File to store the last used folder
DATA_FILE = os.path.join(SCRIPT_DIR, "saved_data.txt")  # File to store text box contents
FATE_CHART_FILE = os.path.join(SCRIPT_DIR, "FateChart.png")  # Path to FateChart.png

# Function to clear all text boxes and reset the Chaos Factor slider
def new_game():
    threads_list.delete("1.0", tk.END)
    characters_list.delete("1.0", tk.END)
    storyline_box.delete("1.0", tk.END)
    chaos_slider.set(5)  # Reset Chaos Factor to default (middle value)

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

# Load images from a selected folder
def load_images(folder_path):
    return [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.lower().endswith((".png", ".jpg", ".jpeg"))]

# Select folder containing card images
def select_folder():
    global card_images
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        save_last_folder(folder_selected)
        card_images = load_images(folder_selected)
        result_label.config(text=f"Loaded {len(card_images)} cards from {folder_selected}." if card_images else "No images found.")

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
    show_cards(selected_cards)

def show_cards(selected_cards, force_upright=False):
    card_window = tk.Toplevel(root)
    card_window.title("Dealt Cards")

    num_cards = len(selected_cards)
    columns = 5 if num_cards > 5 else num_cards
    rows = (num_cards // 5) + (1 if num_cards % 5 else 0)

    for idx, card in enumerate(selected_cards):
        img = Image.open(card).resize((250, 350))
        
        # Randomly rotate only if force_upright is False
        if not force_upright and random.choice([True, False]):
            img = img.rotate(180)
        
        photo = ImageTk.PhotoImage(img)
        label = tk.Label(card_window, image=photo)
        label.image = photo
        label.grid(row=idx // columns, column=idx % columns, padx=10, pady=10)
        
# Function to randomly select an entry from a text box
def select_random_entry(text_box):
    lines = text_box.get("1.0", tk.END).strip().split("\n")
    lines = [line for line in lines if line.strip()]
    if lines:
        selected = random.choice(lines)
        text_box.tag_remove("highlight", "1.0", tk.END)
        for i, line in enumerate(lines, start=1):
            if line == selected:
                text_box.tag_add("highlight", f"{i}.0", f"{i}.end")
                root.after(60000, lambda: text_box.tag_remove("highlight", "1.0", tk.END))  # Remove highlight after 1 minute
                break

# Function to save data to a user-selected file
def save_data():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if not file_path:
        return  # User canceled

    with open(file_path, "w") as f:
        f.write("Threads List:\n" + threads_list.get("1.0", tk.END))
        f.write("Characters List:\n" + characters_list.get("1.0", tk.END))
        f.write("Chaos Factor:\n" + str(chaos_slider.get()) + "\n")
        f.write("Storyline:\n" + storyline_box.get("1.0", tk.END))

# Function to load data from a user-selected file
def load_data():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if not file_path:
        return  # User canceled

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
        pass  # Handle cases where file format is incorrect
        
# Update the show_fate_chart function to pass force_upright=True
def show_fate_chart():
    if not os.path.exists(FATE_CHART_FILE):
        result_label.config(text="FateChart.png not found in the application folder.")
        return
    
    show_cards([FATE_CHART_FILE], force_upright=True)
    
last_folder = load_last_folder()
card_images = load_images(last_folder) if last_folder else []

# GUI Setup
root = tk.Tk()
root.title("Card Dealer for Mythic Cards v4.2.1-beta")
root.geometry("700x900")

# Save and Load buttons
top_frame = tk.Frame(root)
top_frame.pack()

# Add "New" button next to Save and Load
new_button = tk.Button(top_frame, text="New", command=new_game)
new_button.pack(side=tk.LEFT, padx=5, pady=5)

save_button = tk.Button(top_frame, text="Save", command=save_data)
save_button.pack(side=tk.LEFT, padx=5, pady=5)

load_button = tk.Button(top_frame, text="Load", command=load_data)
load_button.pack(side=tk.LEFT, padx=5, pady=5)

folder_button = tk.Button(root, text="Select Card Folder", command=select_folder)
folder_button.pack(pady=5)

result_label = tk.Label(root, text=f"Loaded {len(card_images)} cards from {last_folder}." if last_folder else "No folder selected.")
result_label.pack()

# Horizontal Rule
separator = tk.Frame(root, height=2, bd=1, relief="sunken", bg="black")
separator.pack(fill="x", padx=5, pady=5)

# Fate Chart Button
tk.Button(root, text="Show Fate Chart", command=show_fate_chart).pack(pady=5)

# Quick Draw Buttons
tk.Label(root, text="Quickly Draw Cards").pack()

quick_draw_frame = tk.Frame(root)
quick_draw_frame.pack()
for i in range(1, 11):
    tk.Button(quick_draw_frame, text=f"Draw {i}", command=lambda i=i: deal_cards(i)).pack(side=tk.LEFT, padx=5)

# Horizontal Rule
separator = tk.Frame(root, height=2, bd=1, relief="sunken", bg="black")
separator.pack(fill="x", padx=5, pady=5)

# You shouldn't need more than 10 cards ever, but here is an entry box just in case...
tk.Label(root, text="Enter number of cards to deal:").pack()
entry = tk.Entry(root)
entry.pack()

deal_button = tk.Button(root, text="Deal Cards", command=deal_cards)
deal_button.pack(pady=5)

# Horizontal Rule
separator = tk.Frame(root, height=2, bd=1, relief="sunken", bg="black")
separator.pack(fill="x", padx=5, pady=5)

# Scrollable Text Boxes and Chaos Factor
text_frame = tk.Frame(root)
text_frame.pack(pady=10)

def create_scrollable_text(parent, label):
    frame = tk.Frame(parent)
    tk.Label(frame, text=label).pack()
    text_box = scrolledtext.ScrolledText(frame, width=30, height=20, wrap=tk.WORD)
    text_box.pack()
    text_box.tag_configure("highlight", background="yellow")
    button = tk.Button(frame, text=f"Select Random {label}", command=lambda: select_random_entry(text_box))
    button.pack(pady=5)
    frame.pack(side=tk.LEFT, padx=10)
    return text_box

threads_list = create_scrollable_text(text_frame, "Threads List")

# Chaos Factor Slider
chaos_frame = tk.Frame(text_frame)
tk.Label(chaos_frame, text="Chaos Factor").pack()
chaos_slider = tk.Scale(chaos_frame, from_=9, to=1, orient=tk.VERTICAL)
chaos_slider.pack()
chaos_frame.pack(side=tk.LEFT, padx=10)

characters_list = create_scrollable_text(text_frame, "Characters List")

# Storyline Box
tk.Label(root, text="Storyline").pack()
storyline_box = scrolledtext.ScrolledText(root, width=80, height=10, wrap=tk.WORD)
storyline_box.pack(pady=10)

root.mainloop()
