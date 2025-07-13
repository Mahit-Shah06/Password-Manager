import tkinter as kt
from tkinter import ttk
import config

class GUI:
    def __init__(self):
        self.window = kt.Tk()
        self.window.title("Password Manager")
        screen_height = self.window.winfo_screenheight()
        screen_width = self.window.winfo_screenwidth()
        self.width = min(config.width, screen_width - 100)
        self.height = min(config.height, screen_height - 100)
        self.window.geometry(f"{self.width}x{self.height}")

        self.entry_boxes = {}
        self.top_frame, self.left_frame, self.right_frame = self.create_frames()

        self.left_grid()
        self.right_grid()

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

        grid_container = kt.Frame(self.left_frame, bg=config.bgcolor)
        grid_container.place(relx = 0.5, rely = 0.4, anchor = "center")

        for index, field_text in enumerate(fields):
            
            label = kt.Label(grid_container, text = field_text, bg = config.bgcolor, font = config.text_font, fg = config.font_color)
            label.grid(row = index, column = 0, sticky = "ne", padx = (10, 5), pady = 5)

            if field_text == "Website : ":
                entry = ttk.Combobox(grid_container, textvariable = "website_var", values = "website_list", width = 37)
            elif field_text == "Notes : ":
                entry = kt.Text(grid_container, height = 5, width = 30)
            else:
                entry = kt.Entry(grid_container, width = 40)
            
            entry.grid(row = index, column = 1, sticky = "w", padx = (5, 10), pady = 5)
            entry_boxes[field_text] = entry

        buttons_dict = {
            "Add Password" : [self.add_password, 31, "w"],
            "Import" : [self.import_file, 15, "e"],
            "Export" : [self.export_file, 15, "e"]
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
    
    def right_grid(self):
        grid_container = kt.Frame(self.right_frame, bg=config.bgcolor)
        grid_container.place(relx = 0.5, rely = 0.4, anchor = "center")

        search_label = kt.Label(grid_container, text = "Search : ", bg = config.bgcolor, font = config.text_font, fg = config.font_color)
        search_label.grid(row = 0, column = 0, sticky = "ne", padx = (10, 5), pady = 5)

        search_box = kt.Text(grid_container, height = 1, width = 40)
        search_box.grid(row = 0, column = 2, sticky = "w", padx = (5, 10), pady = 5 )

        columns = ["Website", "Email", "Password", "Notes"]

        password_table = ttk.Treeview(
            grid_container,
            columns = columns,
            show = "headings",
            height = 15
        )

        for i in columns:
            password_table.heading(i, text = i)
            password_table.column(i, width = 182)

        password_table.grid(row=1, column=0, columnspan=3, padx=10, pady=(10, 0))

        return search_box

    def add_password(self):
        pass

    def import_file(self):
        pass

    def export_file(self):
        pass

    def run(self):
        self.window.mainloop()