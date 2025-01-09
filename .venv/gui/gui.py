import os
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog as fd
import webbrowser

import document.doc
from document.doc import DocumentMy


class GUI(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.doc = DocumentMy()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        self.title("Информационно-поисковая система")
        self.geometry("800+450")

        self._create_tabs()
        self._fill_tab_main()
        self._fill_tab_settings()
        self._fill_tab_help()
        self.result = []
        
    def _create_tabs(self):
        self.tabview = ctk.CTkTabview(master=self, width=700, height=600)
        self.tabview.pack()

        self.tab_name_main = "Main"
        self.tab_name_settings = "Settings"
        self.tab_name_help = "Help"

        self.tabview.add(self.tab_name_main)
        self.tabview.add(self.tab_name_settings)
        self.tabview.add(self.tab_name_help)

        self.tabview.set(self.tab_name_main)
    
    def _fill_tab_main(self):
        master = self.tabview.tab(self.tab_name_main)
        self.input_req = ctk.CTkEntry(master=master, placeholder_text="Request...", width=510)
        self.input_req.place(y=20, x=10)

        self.btn_search = ctk.CTkButton(master=master, text="Search", width=140, command=self.btn_search) # command
        self.btn_search.place(y=20, x=540)

        self.docs_label = ctk.CTkLabel(master=master, text="Documents:")
        self.docs_label.place(y=70, x=10)

        self.result_docs_textbox = ctk.CTkTextbox(master=master, width=670, height=440)
        self.result_docs_textbox.place(y=100, x=10)
        # self.result_docs_textbox.insert("0.0", text=text)

    def _fill_tab_settings(self):
        master = self.tabview.tab(self.tab_name_settings)

        self._rb_search_in(master)
        self._checkbox_choice_type(master)

        self.btn_add_file = ctk.CTkButton(master=master, text="Add documents to BD", command=self.add_docs, width=300)
        self.btn_add_file.place(y=480, x=10)

    def _rb_search_in(self, master):
        self.label = ctk.CTkLabel(master=master, text="Search in")
        self.label.place(y=0, x=10)

        text_search_in_title = "Title"
        text_search_in_context = "All text"

        self.var_rb_search_in = tk.StringVar(value=text_search_in_context)

        self.rb_search_in_title = ctk.CTkRadioButton(master=master, text=text_search_in_title, variable=self.var_rb_search_in, value=text_search_in_title)
        self.rb_search_in_title.place(y=30, x=10)

        self.rb_search_in_context = ctk.CTkRadioButton(master=master, text=text_search_in_context, variable=self.var_rb_search_in, value=text_search_in_context)
        self.rb_search_in_context.place(y=60, x=10)

    def _checkbox_choice_type(self, master):
        self.label = ctk.CTkLabel(master=master, text="Type of files")
        self.label.place(y=100, x=10)

        text_checkbox_all_types = "All types"
        text_checkbox_txt = ".txt"
        text_checkbox_pdf = ".pdf"
        text_checkbox_docx = ".docx"

        self.var_checkbox = tk.StringVar(value=text_checkbox_all_types)

        self.choice_all_types = ctk.CTkCheckBox(master=master, text=text_checkbox_all_types, variable=self.var_checkbox, onvalue=text_checkbox_all_types)
        self.choice_all_types.place(y=130, x=10)

        self.choice_txt = ctk.CTkCheckBox(master=master, text=text_checkbox_txt, variable=self.var_checkbox, onvalue=text_checkbox_txt)
        self.choice_txt.place(y=160, x=10)

        self.choice_pdf = ctk.CTkCheckBox(master=master, text=text_checkbox_pdf, variable=self.var_checkbox, onvalue=text_checkbox_pdf)
        self.choice_pdf.place(y=190, x=10)

        self.choice_docx = ctk.CTkCheckBox(master=master, text=text_checkbox_docx, variable=self.var_checkbox, onvalue=text_checkbox_docx)
        self.choice_docx.place(y=220, x=10)

    def _fill_tab_help(self):
        master = self.tabview.tab(self.tab_name_help)
        self.label = ctk.CTkLabel(master=master, text="This text in help")
        self.label.place(y=20, x=20)

    def add_docs(self):
        directory_path = fd.askdirectory(title="Choose folder")
        if directory_path:
            self.doc.read_docs(directory_path)

    def btn_search(self):
        self.doc.get_request(self.input_req.get())
        self.result = self.doc.get_result()
        if not self.result:
            print("fault")
        else:
            y = 100
            for file in self.result:
                self.create_link(master=self.tabview.tab(self.tab_name_main), filepath=file[0], y=y)
                y+=30

    def open_document(self, filepath):
        if os.path.exists(filepath):
            webbrowser.open(filepath)
        else:
            print(f"Файл {filepath} не найден.")

    def create_link(self, master, filepath, y):
        link = ctk.CTkLabel(master=master, text=filepath)
        link.place(x=20, y=y)
        link.bind("<Button-1>", lambda e: self.open_document(filepath))
