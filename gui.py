import tkinter as kt
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import config
from db import DataBase
from seed_core import SeedHandler
from crypto_core import Encrypter
import json

class GUI:
    def __init__(self):
        self.window = kt.Tk()
        self.window.title("Password Manager")
        screen_height = self.window.winfo_screenheight()
        screen_width = self.window.winfo_screenwidth()
        self.width = min(config.width, screen_width - 100)
        self.height = min(config.height, screen_height - 100)
        self.window.geometry(f"{self.width}x{self.height}")
        self.window.resizable(False, False)

        self.top_frame, self.left_frame, self.right_frame = self.create_frames()

        self.public_key_text = kt.StringVar(value="Public Key: Not Connected")
        self.seed_phrase_text = kt.StringVar(value="Seed Phrase: Not Connected")
        self.seed_phrase_hidden = True

        self.entry_boxes = self.left_grid()
        self.right_grid()

        self.db = DataBase()
        self.encrypter = None
        self.seed_phrase = None
        self.public_key = None
        self.seed_handler = SeedHandler()
        self.decrypted_password_list = []

    def create_frames(self):
        frames = {}

        outer_frame = kt.Frame(self.window, bg = config.bdcolor, padx = 5, pady = 5, height = 60)
        outer_frame.pack(side = "top", fill = "x")
        outer_frame.pack_propagate(False)

        inside_frame = kt.Frame(outer_frame, bg = config.bgcolor, height = 60)
        inside_frame.pack(side = "top", fill = "x")

        inside_label = kt.Label(inside_frame, text = "Password Manager", bg = config.bgcolor, fg = config.title_color, font=("Segoe UI", 22, "bold"))
        inside_label.pack(fill = "both")

        frames["top_outer"] = outer_frame 
        frames["top_frame"] = inside_frame 

        sides = {"left" : self.width*0.35, "right" : self.width*0.65}

        for side in sides:

            outer_frame = kt.Frame(self.window, bg = config.bdcolor, padx = 5, pady = 5, width = sides[side])
            outer_frame.pack(side = side, fill = "both", expand = True)
            outer_frame.pack_propagate(False)

            inside_frame = kt.Frame(outer_frame, bg = config.bgcolor, width = sides[side])
            inside_frame.pack(side = side, fill = "both", expand = True)
            inside_frame.pack_propagate(False)

            frames[f"{side}_outer"] = outer_frame
            frames[f"{side}_frame"] = inside_frame
        
        return frames["top_frame"], frames["left_frame"], frames["right_frame"]

    def left_grid(self):
        fields = [
            "Website : ",
            "Email : ",
            "Password : ",
            "Notes : "
        ]
        entry_boxes = {}

        index = 1

        grid_container = kt.Frame(self.left_frame, bg = config.bgcolor)
        grid_container.place(relx = 0.5, rely = 0.45, anchor = "center")

        theme_label = kt.Label(grid_container, text = "Theme : ", bg = config.bgcolor, font = config.text_font, fg = config.font_color)
        theme_label.grid(row = 0, column = 0, sticky = "ne", padx = (10, 5), pady = 5)

        with open("themes.json", "r") as f:
            theme_names = list(json.load(f).keys())

        selected_theme = kt.StringVar(value=config.selected_theme)
        
        theme_menu = kt.OptionMenu(grid_container, selected_theme, *theme_names, command = self.change_theme)
        theme_menu.config(bg=config.button_bg, fg=config.button_fg, activebackground=config.hover_bg, font=config.button_font, borderwidth=0, highlightthickness=0, width = 30)

        theme_menu["menu"].config(bg=config.button_bg, fg=config.button_fg)
        theme_menu.grid(row = 0, column = 1, sticky = "n")

        for field_text in fields:
            
            label = kt.Label(grid_container, text = field_text, bg = config.bgcolor, font = config.text_font, fg = config.font_color)
            label.grid(row = index, column = 0, sticky = "ne", padx = (10, 5), pady = 5)

            if field_text == "Notes : ":
                entry = kt.Text(grid_container, height = 5, width = 30)
            else:
                entry = kt.Entry(grid_container, width = 40)

            entry.grid(row = index, column = 1, sticky = "w", padx = (5, 10), pady = 5)
            entry_boxes[field_text] = entry
            index+=1

        buttons_dict = {
            "Add Password" : [self.add_password, 31, "w"],
            "Import" : [self.import_file, 31, "n"],
            "Export" : [self.export_file, 31, "n"],
            "Connect" :  [self.connect, 31, "w"]
        }

        for i in buttons_dict:
            button = kt.Button(
            grid_container,
            text = i,
            command = buttons_dict[i][0],
            bg = config.button_bg,
            fg = config.button_fg,
            font = config.button_font,
            activebackground = config.hover_bg,
            width = buttons_dict[i][1]
            )
            button.grid(row = index + 1, column = 1, pady=(10, 5), sticky = buttons_dict[i][2])
            index+=1

        return entry_boxes

    def change_theme(self, theme_name):
        """Updates the settings file with the new theme and asks for a restart."""
        try:
            with open("settings.json", "w") as f:
                json.dump({"selected_theme": theme_name}, f)
            
            messagebox.showinfo("Theme Changed", f"Theme set to '{theme_name}'.\nPlease restart the application for changes to take full effect.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save theme settings: {e}")

    def connect(self):
        self.popup = kt.Toplevel(self.window)
        self.popup.title("Connect Wallet")

        new_button = kt.Button(self.popup, text="Create New Wallet", command=self.create_wallet)
        import_button = kt.Button(self.popup, text="Import Wallet", command=self.import_wallet)

        new_button.pack(pady = 10)
        import_button.pack(pady = 10)

    def create_wallet(self):
        self.popup.destroy()
        while True:
            seed_phrase = self.seed_handler.generate_seed_phrase()
            private_key = self.seed_handler.seed_to_key(seed_phrase)
            public_key_candidate = self.seed_handler.get_public_key(private_key)

            if not self.db.check_if_public_key_exists(public_key_candidate):
                break

        seed_dialog = kt.Toplevel(self.window)
        seed_dialog.title("Your New Unique Seed Phrase")
        
        # Make the dialog modal
        seed_dialog.transient(self.window)
        seed_dialog.grab_set()
        
        instruction_label = kt.Label(seed_dialog, text="Please save this seed phrase in a secure place. You will need it to log in.")
        instruction_label.pack(pady=10, padx=10)

        # Use a read-only Entry widget to display the seed phrase, making it selectable
        seed_entry = kt.Entry(seed_dialog, width=60)
        seed_entry.insert(0, seed_phrase)
        seed_entry.config(state="readonly")
        seed_entry.pack(pady=5, padx=10)

        # --- Function to copy the seed phrase to the clipboard ---
        def copy_seed():
            self.window.clipboard_clear()
            self.window.clipboard_append(seed_phrase)
            # Optional: Give user feedback
            copy_button.config(text="Copied!")

        # --- Add Buttons ---
        button_frame = kt.Frame(seed_dialog)
        button_frame.pack(pady=10)

        copy_button = kt.Button(button_frame, text="Copy to Clipboard", command=copy_seed)
        copy_button.pack(side="left", padx=5)

        ok_button = kt.Button(button_frame, text="OK", command=seed_dialog.destroy)
        ok_button.pack(side="left", padx=5)
        
        # Wait for the user to close the dialog before proceeding
        self.window.wait_window(seed_dialog)

        messagebox.showinfo(
            "Info",
            "Please now log in using the 'Import Wallet' option."
        )

        for item in self.password_table.get_children():
            self.password_table.delete(item)

    def import_wallet(self):
        self.popup.destroy()
        import_window = kt.Toplevel(self.window)
        import_window.title("Import Wallet")
        
        label = kt.Label(import_window, text="Enter your seed phrase:")
        label.pack(pady=5)
        
        seed_entry = kt.Entry(import_window, width=50)
        seed_entry.pack(pady=5)
        
        def on_submit():
            seed_phrase = seed_entry.get()
            if not seed_phrase:
                messagebox.showerror("Error", "Seed phrase cannot be empty.")
                return

            try:
                self.seed_phrase = seed_phrase
                private_key = self.seed_handler.seed_to_key(seed_phrase)
                self.public_key = self.seed_handler.get_public_key(private_key)
                self.encrypter = Encrypter(private_key)
                self.public_key_text.set(f"Public Key: {self.public_key}")
                self.seed_phrase_text.set(f"Seed Phrase: {self.seed_phrase}")
                import_window.destroy()
                self.show_passwords()

                messagebox.showinfo("Success", "Wallet successfully imported and logged in")

            except Exception as e:
                messagebox.showerror(
                    "Import Failed", 
                    "The seed phrase you entered is invalid. Please check it and try again.",
                    parent=import_window
                )

        submit_button = kt.Button(import_window, text="Submit", command=on_submit)
        submit_button.pack(pady=10)

    def add_password(self):
        website = self.entry_boxes["Website : "].get()
        email = self.entry_boxes["Email : "].get()
        password = self.entry_boxes["Password : "].get()
        notes = self.entry_boxes["Notes : "].get("1.0", "end-1c")

        if not self.encrypter or not self.db:
            messagebox.showerror("Error", "Please connect a wallet first.")
            return

        else:
            if not website or not email or not password:
                messagebox.showerror(title = "Error", message = "Please fill in all the required fields.")
                return

            is_duplicate = False
            
            for entry in self.data:
                for list_pass in self.decrypted_password_list:
                    if entry["website"] == website and entry["email"] == email and list_pass == password:
                        is_duplicate = True 
                        messagebox.showerror(title = "Error", message=f"This email and password already exists for {website}.")
                        break
                if is_duplicate:
                    break

            if not is_duplicate:
                Encrypted_password = self.encrypter.encryption(password)
                data = [website, email, Encrypted_password, notes]
                self.db.add_data(data, self.public_key)

                self.entry_boxes["Website : "].delete(0, "end")
                self.entry_boxes["Email : "].delete(0, "end")
                self.entry_boxes["Password : "].delete(0, "end")
                self.entry_boxes["Notes : "].delete("1.0", "end")

                messagebox.showinfo(title="Success", message="Data added successfully!")

                self.show_passwords()

    def import_file(self):
        pass

    def export_file(self):
        pass

    def right_grid(self):
        grid_container = kt.Frame(self.right_frame, bg=config.bgcolor)
        grid_container.place(relx = 0.5, rely = 0.4, anchor = "center")

        search_box = kt.Text(grid_container, height = 1, width = 40)
        search_box.grid(row = 0, column = 1, sticky = "w", padx = (5, 10), pady = 5 )

        search_label = kt.Label(grid_container, text = "Search : ", bg = config.bgcolor, font = config.text_font, fg = config.font_color)
        search_label.grid(row = 0, column = 0, sticky = "ne", padx = (10, 5), pady = 5)

        columns = ["Website", "Email", "Password", "Notes"]

        self.password_table = ttk.Treeview(
            grid_container,
            columns = columns,
            show = "headings",
            height = 15
        )

        for i in columns:
            self.password_table.heading(i, text = i)
            self.password_table.column(i, width = 182)

        self.password_table.grid(row=1, column=0, columnspan=3, padx=10, pady=(10, 0))

        info_frame = kt.Frame(grid_container, bg = config.bgcolor)
        info_frame.grid(row=3, column=0, columnspan=3)

        public_key_label = kt.Label(info_frame, textvariable = self.public_key_text, bg = config.bgcolor, font = ("Consolas", 11, "bold"), fg = config.title_color)
        public_key_label.pack()
        
        seed_phrase_label = kt.Label(info_frame, textvariable = self.seed_phrase_text, bg = config.bgcolor, font = ("Consolas", 11, "bold"), fg = config.title_color)
        seed_phrase_label.pack()

        button_frame = kt.Frame(grid_container, bg = config.bgcolor)
        button_frame.grid(row = 4, column = 0, columnspan = 3)

        copy_button = kt.Button(button_frame, text = "Copy Seed Phrase", bg = config.button_bg, font = config.button_font, fg = config.button_fg, command = self.copy_seed_phrase)
        copy_button.pack(side = "left", padx = 5)

        export_button = kt.Button(button_frame, text = "Export Seed Phrase", bg = config.button_bg, font = config.button_font, fg = config.button_fg, command = self.export_seed_phrase)
        export_button.pack(side = "left", padx = 5)

        return search_box
    
    def copy_seed_phrase(self):
        if not self.seed_phrase:
            messagebox.showerror("Error", "Please Connect your seed phrase first")
            return
        self.window.clipboard_append(self.seed_phrase)
        messagebox.showinfo("Success", "Seed Phrase copied to your clipboard")

    def export_seed_phrase(self):
        if not self.seed_phrase:
            messagebox.showerror("Error", "Please Connect your seed phrase first")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension = ".txt",
            filetypes = [("Text files", "*.txt"), ("All files", "*.*")],
            title="Save Seed Phrase As..."
        )

        if file_path:
            try:
                with open(file_path, "w") as f:
                    f.write("Your Seed phrase for Password Manager:\n\n")
                    f.write(self.seed_phrase)
                messagebox.showinfo("Success", f"Your seed phrase has been successfully save to {file_path}")
            except Exception as e:
                messagebox.showerror("Failed", f"Failed to save your seed phrase: {e}")

    def show_passwords(self):
        if not self.public_key:
            return
        
        self.data = self.db.fetch_data(self.public_key)
        decrypted_passwords = []

        for item in self.password_table.get_children():
            self.password_table.delete(item)
        
        for entry in self.data:
            encrypted_password = entry["password"]
            decrypted_password = self.encrypter.decryption(encrypted_password)
            self.password_table.insert("", "end", values=(entry["website"], entry["email"], decrypted_password, entry["notes"]))
            decrypted_passwords.append(decrypted_password)


    def run(self):
        self.window.mainloop()