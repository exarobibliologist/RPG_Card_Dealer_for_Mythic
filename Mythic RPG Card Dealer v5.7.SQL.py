import os
import random
import sys
import sqlite3
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
from PIL import Image, ImageTk

# Window Initialization
root = tk.Tk()
root.title("Mythic RPG Card Dealer v5.7.SQL")
root.geometry("700x250")

# Track open character windows to prevent duplicates
open_windows = {}

game_state_window = tk.Toplevel(root)
game_state_window.title("Mythic Game Notes")
game_state_window.geometry("700x650")
game_state_window.attributes("-topmost", True)
game_state_window.after(500, lambda: game_state_window.attributes("-topmost", False))

def lower_game_state():
    root.lift()
    root.focus_force()
game_state_window.after(1000, lower_game_state)

game_state_window.protocol("WM_DELETE_WINDOW", lambda: None)

# Paths and Save Logic
if getattr(sys, 'frozen', False):
    SCRIPT_DIR = os.path.dirname(sys.executable)
else:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

FATE_CHART_FILE = os.path.join(SCRIPT_DIR, "FateChart.png")
CONFIG_FILE = os.path.join(SCRIPT_DIR, "config.txt")
DB_FILE = os.path.join(SCRIPT_DIR, "characters.db")

# --- DATABASE LOGIC ---

def init_db():
    """Initialize the SQLite database and create the table if needed."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS characters (
            name TEXT PRIMARY KEY,
            strength TEXT,
            agility TEXT,
            reflex TEXT,
            iq TEXT,
            intuition TEXT,
            willpower TEXT,
            toughness TEXT,
            feats TEXT
        )
    """)
    conn.commit()
    conn.close()

def get_character_from_db(name):
    """Retrieve character details by name."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM characters WHERE name=?", (name,))
    data = c.fetchone()
    conn.close()
    return data

def get_all_character_names():
    """Retrieve all character names sorted alphabetically."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT name FROM characters ORDER BY name")
    rows = c.fetchall()
    conn.close()
    return [row[0] for row in rows]

def delete_character_from_db(name):
    """Delete a character from the database."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM characters WHERE name=?", (name,))
    conn.commit()
    conn.close()

def save_character_to_db(original_name, data):
    """Save, Update, or Rename character details."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Check if the character exists under the ORIGINAL name
    exists = None
    if original_name:
        c.execute("SELECT 1 FROM characters WHERE name=?", (original_name,))
        exists = c.fetchone()

    if exists:
        # If it exists, UPDATE the existing row (this handles renaming too)
        c.execute("""
            UPDATE characters 
            SET name=?, strength=?, agility=?, reflex=?, iq=?, intuition=?, willpower=?, toughness=?, feats=?
            WHERE name=?
        """, (*data, original_name))
    else:
        # If it's a brand new character (original_name was empty or not found), INSERT new
        c.execute("""
            INSERT OR REPLACE INTO characters 
            (name, strength, agility, reflex, iq, intuition, willpower, toughness, feats)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, data)

    conn.commit()
    conn.close()

# Initialize DB on startup
init_db()

# --- IMAGE LOADING LOGIC ---

def load_images(folder_path):
    return [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.lower().endswith((".png", ".jpg", ".jpeg"))]

def select_folder():
    global card_images
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        card_images = load_images(folder_selected)
        result_label.config(text=f"Loaded {len(card_images)} cards from {folder_selected}." if card_images else "No images found.")
        with open(CONFIG_FILE, "w") as f:
            f.write(folder_selected)

def load_last_folder():
    global card_images
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            last_folder = f.read().strip()
            if os.path.isdir(last_folder):
                card_images = load_images(last_folder)
                result_label.config(text=f"Auto-loaded {len(card_images)} cards from {last_folder}." if card_images else "No images found.")

# --- CARD DEALING LOGIC ---

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
        img = Image.open(card).resize((214, 300))
        if not force_upright and random.choice([True, False]):
            img = img.rotate(180)
        
        photo = ImageTk.PhotoImage(img)
        label = tk.Label(card_window, image=photo)
        label.image = photo
        label.grid(row=idx // columns, column=idx % columns, padx=10, pady=10)

def show_fate_chart():
    if not os.path.exists(FATE_CHART_FILE):
        result_label.config(text="FateChart.png not found in the application folder.")
        return
    show_cards([FATE_CHART_FILE], force_upright=True)

# --- SAVE/LOAD CAMPAIGN LOGIC ---

def save_data():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if not file_path:
        return
    with open(file_path, "w") as f:
        f.write("Threads List:\n" + threads_list.get("1.0", tk.END))
        f.write("Characters List:\n" + characters_list.get("1.0", tk.END))
        f.write("Chaos Factor:\n" + str(chaos_slider.get()) + "\n")
        f.write("Storyline:\n" + storyline_box.get("1.0", tk.END))

def load_data():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if not file_path:
        return
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

def new_game():
    threads_list.delete("1.0", tk.END)
    characters_list.delete("1.0", tk.END)
    storyline_box.delete("1.0", tk.END)
    chaos_slider.set(5)

# --- CHARACTER DETAIL EDITOR ---

def open_character_editor(name_from_list):
    name_stripped = name_from_list.strip()
    if not name_stripped:
        return

    # --- DUPLICATE CHECK ---
    if name_stripped in open_windows:
        window = open_windows[name_stripped]
        if window.winfo_exists():
            window.lift()
            window.focus_force()
            return
        else:
            del open_windows[name_stripped]

    editor = tk.Toplevel(root)
    editor.title(f"Character: {name_stripped}")
    # ADJUSTED SIZE HERE (Wider and Shorter)
    editor.geometry("420x450")
    
    open_windows[name_stripped] = editor

    # Store the original name locally
    original_name = name_stripped

    # Grid Setup
    fields = ["Strength", "Agility", "Reflex", "IQ", "Intuition", "Willpower", "Toughness"]
    entries = {}

    # Name Field
    tk.Label(editor, text="Name:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
    name_entry = tk.Entry(editor, width=30)
    name_entry.insert(0, name_stripped)
    name_entry.grid(row=0, column=1, pady=5)
    
    # Stat Fields
    for i, field in enumerate(fields):
        tk.Label(editor, text=f"{field}:").grid(row=i+1, column=0, sticky="e", padx=5, pady=2)
        entry = tk.Entry(editor, width=30)
        entry.grid(row=i+1, column=1, pady=2)
        entries[field] = entry

    # Feats Field
    tk.Label(editor, text="Feats and Abilities:").grid(row=len(fields)+1, column=0, sticky="nw", padx=5, pady=5)
    feats_box = scrolledtext.ScrolledText(editor, width=35, height=10)
    feats_box.grid(row=len(fields)+1, column=1, pady=5)

    # Load Data if exists
    db_data = get_character_from_db(name_stripped)
    if db_data:
        entries["Strength"].insert(0, db_data[1])
        entries["Agility"].insert(0, db_data[2])
        entries["Reflex"].insert(0, db_data[3])
        entries["IQ"].insert(0, db_data[4])
        entries["Intuition"].insert(0, db_data[5])
        entries["Willpower"].insert(0, db_data[6])
        entries["Toughness"].insert(0, db_data[7])
        feats_box.insert("1.0", db_data[8])
    else:
        original_name = None

    def save_char_internal():
        nonlocal original_name
        data = (
            name_entry.get(),
            entries["Strength"].get(),
            entries["Agility"].get(),
            entries["Reflex"].get(),
            entries["IQ"].get(),
            entries["Intuition"].get(),
            entries["Willpower"].get(),
            entries["Toughness"].get(),
            feats_box.get("1.0", tk.END)
        )
        
        save_character_to_db(original_name, data)
        
        # Handle renaming logic for window tracking
        new_name = name_entry.get()
        if original_name and original_name != new_name:
             if original_name in open_windows:
                 del open_windows[original_name]
             open_windows[new_name] = editor
        
        # Update original_name to the new name so subsequent saves work
        original_name = new_name

        messagebox.showinfo("Saved", f"{name_entry.get()} saved to database!")
        editor.destroy()
        
        if name_stripped in open_windows:
            del open_windows[name_stripped]
        if name_entry.get() in open_windows:
            del open_windows[name_entry.get()]

    def delete_char_internal():
        nonlocal original_name
        if not original_name:
            return 
        
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {original_name} from the database?")
        if confirm:
            delete_character_from_db(original_name)
            
            # Remove from tracking since the DB record is gone
            if original_name in open_windows:
                del open_windows[original_name]

            # Set original_name to None so the next Save acts as a NEW INSERT
            original_name = None
            
            messagebox.showinfo("Deleted", "Character deleted from database.\n\nThe window is still open. You can edit the name/stats and click Save to create a NEW character based on this one.")

    # Buttons (Added padx=10 to ensure Save button isn't cut off)
    delete_btn = tk.Button(editor, text="Delete", command=delete_char_internal, bg="#ffdddd")
    delete_btn.grid(row=len(fields)+2, column=0, pady=10, sticky="w", padx=10)

    save_btn = tk.Button(editor, text="Save Character", command=save_char_internal, bg="#ddffdd")
    save_btn.grid(row=len(fields)+2, column=1, pady=10, sticky="e", padx=10)
    
    def on_close():
        if name_stripped in open_windows:
            del open_windows[name_stripped]
        editor.destroy()
        
    editor.protocol("WM_DELETE_WINDOW", on_close)

# --- RIGHT CLICK HANDLER ---

def on_right_click_char(event):
    try:
        index = characters_list.index(f"@{event.x},{event.y}")
        line_start = f"{index.split('.')[0]}.0"
        line_end = f"{index.split('.')[0]}.end"
        selected_text = characters_list.get(line_start, line_end)
        
        if selected_text.strip():
            open_character_editor(selected_text)
    except Exception as e:
        print(e)

# --- MAIN UI SETUP ---

folder_button = tk.Button(root, text="Select Card Folder", command=select_folder)
folder_button.pack(pady=5)

result_label = tk.Label(root, text="No folder selected.")
result_label.pack()

separator = tk.Frame(root, height=2, bd=1, relief="sunken", bg="black")
separator.pack(fill="x", padx=5, pady=5)

tk.Button(root, text="Show Fate Chart", command=show_fate_chart).pack(pady=5)

separator = tk.Frame(root, height=2, bd=1, relief="sunken", bg="black")
separator.pack(fill="x", padx=5, pady=5)

tk.Label(root, text="Quickly Draw Cards").pack()
quick_draw_frame = tk.Frame(root)
quick_draw_frame.pack()
for i in range(1, 11):
    tk.Button(quick_draw_frame, text=f"Draw {i}", command=lambda i=i: deal_cards(i)).pack(side=tk.LEFT, padx=5)

tk.Label(root, text="Enter number of cards to deal:").pack()
entry = tk.Entry(root)
entry.pack()

deal_button = tk.Button(root, text="Deal Cards", command=deal_cards)
deal_button.pack(pady=5)

# Game State UI
top_frame = tk.Frame(game_state_window)
top_frame.pack()

new_button = tk.Button(top_frame, text="New", command=new_game)
new_button.pack(side=tk.LEFT, padx=5, pady=5)

save_button = tk.Button(top_frame, text="Save", command=save_data)
save_button.pack(side=tk.LEFT, padx=5, pady=5)

load_button = tk.Button(top_frame, text="Load", command=load_data)
load_button.pack(side=tk.LEFT, padx=5, pady=5)

# --- NEW MENU BAR FOR GAME STATE WINDOW ---
menu_bar = tk.Menu(game_state_window)
game_state_window.config(menu=menu_bar)

char_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Database", menu=char_menu)

def populate_char_list():
    names = get_all_character_names()
    if not names:
        messagebox.showinfo("Database Empty", "No characters found in database.")
        return
    
    # Confirm overwrite if there is text present
    if characters_list.get("1.0", tk.END).strip():
         if not messagebox.askyesno("Overwrite?", "This will replace the current Characters List with the full database.\nContinue?"):
             return

    characters_list.delete("1.0", tk.END)
    characters_list.insert("1.0", "\n".join(names))

char_menu.add_command(label="Import All Characters to List", command=populate_char_list)
# ------------------------------------------

separator = tk.Frame(game_state_window, height=2, bd=1, relief="sunken", bg="black")
separator.pack(fill="x", padx=5, pady=5)

text_frame = tk.Frame(game_state_window)
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

def select_random_entry(text_box):
    lines = text_box.get("1.0", tk.END).strip().split("\n")
    lines = [line for line in lines if line.strip()]
    if lines:
        selected = random.choice(lines)
        text_box.tag_remove("highlight", "1.0", tk.END)
        for i, line in enumerate(lines, start=1):
            if line == selected:
                text_box.tag_add("highlight", f"{i}.0", f"{i}.end")
                game_state_window.after(60000, lambda: text_box.tag_remove("highlight", "1.0", tk.END))
                break

threads_list = create_scrollable_text(text_frame, "Threads List")

chaos_frame = tk.Frame(text_frame)
tk.Label(chaos_frame, text="Chaos Factor").pack()
chaos_slider = tk.Scale(chaos_frame, from_=9, to=1, orient=tk.VERTICAL)
chaos_slider.pack()
chaos_frame.pack(side=tk.LEFT, padx=10)

characters_list = create_scrollable_text(text_frame, "Characters List")

# BIND RIGHT CLICK TO CHARACTERS
characters_list.bind("<Button-3>", on_right_click_char) 

tk.Label(game_state_window, text="Storyline").pack()
storyline_box = scrolledtext.ScrolledText(game_state_window, width=80, height=10, wrap=tk.WORD)
storyline_box.pack(pady=10)

load_last_folder()
root.mainloop()