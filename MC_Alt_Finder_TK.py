import requests
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

antisniper_api_key = ''

FONT = 'Roboto'

def get_info(call):
    r = requests.get(call)
    return r.json()

def process_shop_data(shop_data):
    items = shop_data.split(',')
    f_items = []

    current_row = []
    for i, item in enumerate(items, start=1):

        item = item.replace('_', ' ')
        item = ' '.join(word.capitalize() for word in item.split())
        item = item.replace('Null', 'Empty')

        current_row.append(f"Slot {i} - {item}")

        if i % 7 == 0:
            f_items.append(f"Row {len(f_items) + 1}:\n{"\n".join(current_row)}")
            current_row = []

    if current_row:
        f_items.append(f"Row {len(f_items) + 1}:\n{"\n".join(current_row)}")

    return "\n\n".join(f_items)

def show_user_details(notebook, username):
    as_1 = f"https://api.antisniper.net/v2/convert/mojang?player={username}&key={antisniper_api_key}"
    data = get_info(as_1)

    frame = ttk.Frame(notebook)

    if 'uuid' in data and data['uuid']:
        notebook.add(frame, text=username)

        uuid = data["uuid"]

        alt_url = f"https://api.antisniper.net/v2/player/altfinder?player={uuid}&key={antisniper_api_key}"
        data_alt = get_info(alt_url)

        if 'data' in data_alt and data_alt['data']:
            found_usernames = []
            for user_data in data_alt['data']:
                ign = user_data['ign']
                shop = user_data['shop']
                discord = user_data['discord']

                f_shop = process_shop_data(shop)

                details_message = f"UUID: {uuid}\nIGN: {ign}\nDiscord: {discord}\nShop:\n{f_shop}"

                text_widget = scrolledtext.ScrolledText(frame, wrap='word', height=10, width=40, fg='white', bg='black', font={FONT})
                text_widget.insert(tk.END, details_message)
                text_widget.pack(padx=10, pady=10, expand=True, fill='both')
    else:
        popup_message = "Player not found: " + username
        messagebox.showinfo("Player Not Found", popup_message)

class App:
    def __init__(self, master):
        self.master = master
        master.title("Player Details + AltFinder")

        style = ttk.Style()

        master.configure(bg='black')

        style.configure("TFrame", background="black")
        style.configure("TLabel", foreground="white", background="black", font={FONT})
        style.configure("TNotebook", background="black", font={FONT})
        style.configure("TNotebook.Tab", background="black", foreground="black", borderwidth=0, font={FONT})
        style.map("TNotebook.Tab", background=[("selected", "black")])

        self.notebook = ttk.Notebook(master)
        self.notebook.pack(expand=True, fill='both')

        self.label = tk.Label(master, text="Enter the player name:", fg='white', bg='black', font={FONT})
        self.label.pack()

        self.entry = tk.Entry(master, bg='black', fg='white', font={FONT})
        self.entry.pack()

        self.button = tk.Button(master, text="Check Details", command=self.check_details, fg='white', bg='black', font={FONT})
        self.button.pack()

        self.entry['bg'] = 'black'
        self.button['bg'] = 'black'

        self.master.overrideredirect(False)
        self.master.geometry("1000x800")

    def check_details(self):
        username = self.entry.get()
        show_user_details(self.notebook, username)
        self.notebook.select(len(self.notebook.tabs()) - 1)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
