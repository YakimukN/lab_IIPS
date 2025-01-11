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

        ctk.set_appearance_mode("dark")
        # ctk.set_default_color_theme("green")
        self.title("Search system")
        self.geometry("700x400+500+400")

        self.doc = DocumentMy()
        self._create_tabs()
        self._fill_tab_main()
        self._fill_tab_help()
        self.label_links = []
        self.result = []

    def _create_tabs(self):
        self.tabview = ctk.CTkTabview(master=self, width=700, height=400)
        self.tabview.pack()

        self.tab_name_main = "Main"
        self.tab_name_help = "Help"

        self.tabview.add(self.tab_name_main)
        self.tabview.add(self.tab_name_help)

        self.tabview.set(self.tab_name_main)

    def _fill_tab_main(self):
        master = self.tabview.tab(self.tab_name_main)
        self.input_req = ctk.CTkEntry(master=master, placeholder_text="Request...", width=510)
        self.input_req.place(y=20, x=10)

        self.btn_search = ctk.CTkButton(master=master, text="Search", width=140, command=self.btn_search)
        self.btn_search.place(y=20, x=540)

        self.docs_label = ctk.CTkLabel(master=master, text="Documents:")
        self.docs_label.place(y=70, x=10)

        self.btn_add_file = ctk.CTkButton(master=master, text="Add documents to BD", command=self.add_docs, width=660)
        self.btn_add_file.place(y=310, x=10)

    def _fill_tab_help(self):
        master = self.tabview.tab(self.tab_name_help)
        self.label = ctk.CTkLabel(master=master, justify="left", text="""
        Help for users
        """)
        self.label.place(y=0, x=0)

        self.label_add = ctk.CTkLabel(master=master, justify="left", text="""
        Add Files To Database
        To add files to the database you should click on the “add file” button and in the window that appears select the 
        folder from which you want to upload documents.
        """)
        self.label_add.place(y=60, x=0)

        self.label_add = ctk.CTkLabel(master=master, justify="left", text="""
        Search In This system
        to search you should enter a query in the text field on the page “main” and the result of the query will be displayed 
        at the bottom in the form of a list of relevant files.
        """)
        self.label_add.place(y=140, x=0)

        self.label_add = ctk.CTkLabel(master=master, justify="left", text="""
        This system supports three types of files: .txt, .pdf, .docx
        """)
        self.label_add.place(y=220, x=0)

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
            for label in self.label_links:
                label.destroy()
            self.label_links.clear()
            y = 100
            for file in self.result:
                self.create_link(master=self.tabview.tab(self.tab_name_main), filepath=file[0], y=y)
                y += 30

    def open_document(self, filepath):
        if os.path.exists(filepath):
            webbrowser.open(filepath)
        else:
            print(f"Файл {filepath} не найден.")

    def create_link(self, master, filepath, y):
        link = ctk.CTkLabel(master=master, text=filepath)
        link.place(x=20, y=y)
        link.bind("<Button-1>", lambda e: self.open_document(filepath))
        self.label_links.append(link)
