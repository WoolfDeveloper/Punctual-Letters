from punctualizer import PunctualLetterController
from msg_repository import MessageRepository
import tkinter
from tkinter import filedialog
import tkinter.messagebox
import customtkinter
import os 

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("green")

class ScreenController(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        self.message_repo = MessageRepository()

        self.title("Punctual Letters Epub Converter")

        icon = tkinter.PhotoImage(file="assets/icon.png")
        self.iconphoto(True, icon)

        self.geometry(f"{900}x{400}")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.title_label = customtkinter.CTkLabel(self, text="Punctual Letters!", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.title_label.grid(row=0, column=0, pady=(10, 10), sticky="nsew")

        self.input_frame = customtkinter.CTkFrame(self)
        self.input_frame.grid(row=1, column=0, pady=(0, 5))

        self.input_label_1 = customtkinter.CTkLabel(self.input_frame, text="Select an .epub file:", anchor="w")
        self.input_label_1.grid(row=0, column=0, padx=(20, 10), pady=(10, 0), sticky="nw")

        self.input_path_from = tkinter.StringVar()
        self.input_entry_path_from = customtkinter.CTkEntry(self.input_frame, textvariable=self.input_path_from, width=600, placeholder_text="Press Browse button to select an .epub file.")
        self.input_entry_path_from.grid(row=1, column=0, padx=(20, 10))

        self.input_button_1 = customtkinter.CTkButton(self.input_frame, text="Browse", command=self.browse_path_1)
        self.input_button_1.grid(row=1, column=1, padx=(10, 20))

        self.input_label_2 = customtkinter.CTkLabel(self.input_frame, text="Select the route in which the Punctualized epubs are saved:", anchor="w")
        self.input_label_2.grid(row=2, column=0, padx=(20, 10), pady=(10, 0), sticky="nw")

        self.input_path_to = tkinter.StringVar()
        self.input_entry_path_to = customtkinter.CTkEntry(self.input_frame, textvariable=self.input_path_to, width=600)
        self.input_entry_path_to.grid(row=3, column=0, padx=(20, 10), pady=(0, 20))

        self.input_button_2 = customtkinter.CTkButton(self.input_frame, text="Browse", command=self.browse_path_2)
        self.input_button_2.grid(row=3, column=1, padx=(10, 20), pady=(0, 20))

        self.process_frame = customtkinter.CTkFrame(self, bg_color='transparent')
        self.process_frame.grid(row=2, column=0, pady=(5, 20))

        self.progressbar_1 = customtkinter.CTkProgressBar(self.process_frame, width=600, height=10, determinate_speed=1)
        self.progressbar_1.set(0)
        self.progressbar_1.grid(row=0, column=0, padx=(20, 10), pady=(10, 10), sticky="w")

        self.process_button = customtkinter.CTkButton(self.process_frame, text="Punctualize!", command=self.puntualize)
        self.process_button.grid(row=0, column=1, padx=(10, 20), pady=20, sticky="e")

    def browse_path_1(self):
        path = filedialog.askopenfilename()
        if path:
            self.input_path_from.set(path)

    def browse_path_2(self):
        path = filedialog.askdirectory()
        if path:
            self.input_path_to.set(path)

    def process_inputs(self):
        input_1_value = self.input_path_from.get()
        input_2_value = self.input_entry_path_to.get()
        tkinter.messagebox.showinfo("Inputs", f"Input 1: {input_1_value}\nInput 2: {input_2_value}")

    def puntualize(self):
        self.progressbar_1.set(0)
        from_path_value = self.input_entry_path_from.get()
        file = self.validate_epubs(from_path_value)
        if not file:
            return
        self.progressbar_1.start()
        to_path_value = self.input_path_to.get()
        puntual_letter = PunctualLetterController(to_path_value)
        puntual_letter.setNewEpubPath(file)
        processed = puntual_letter.processfile()
        if not processed:
            self.reset_progress_bar()
            tkinter.messagebox.showerror("Error", self.message_repo.get_error("err.not_processed"))
        else: 
            self.put_full_progress_bar()
            tkinter.messagebox.showinfo("Success", self.message_repo.get_success("succ.epub_processed"))

    def validate_epubs(self, path):
        if os.path.isfile(path) and path.endswith('.epub'):
            return path
        else:
            tkinter.messagebox.showerror("Error", self.message_repo.get_error("err.file_null"))
            return None

    def put_full_progress_bar(self):
        self.progressbar_1.stop()
        self.progressbar_1.set(100)

    def reset_progress_bar(self):
        self.progressbar_1.stop()
        self.progressbar_1.set(0)

    def process_from_path(path):
        if os.path.isfile(path):
            return os.path.dirname(path)
        elif os.path.isdir(path):
            return path
        else:
            return None

if __name__ == "__main__":
    app = ScreenController()
    app.mainloop()