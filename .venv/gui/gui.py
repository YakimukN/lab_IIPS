import os
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog as fd

from document.doc import DocumentMy


class GUI(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        self.title("Информационно-поисковая система")
        self.geometry("800+450")

        self._create_tabs()
        self._fill_tab_main()
        self._fill_tab_settings()
        self._fill_tab_help()
        
    def _create_tabs(self):
        self.tabview = ctk.CTkTabview(master=self, width=700, height=600)
        self.tabview.pack()

        self.tab_name_main = "Главная"
        self.tab_name_settings = "Настройки"
        self.tab_name_help = "Помощь"

        self.tabview.add(self.tab_name_main)
        self.tabview.add(self.tab_name_settings)
        self.tabview.add(self.tab_name_help)

        self.tabview.set(self.tab_name_main)
    
    def _fill_tab_main(self):
        master = self.tabview.tab(self.tab_name_main)
        self.input_req = ctk.CTkEntry(master=master, placeholder_text="Request...", width=510)
        self.input_req.place(y=20, x=10)

        self.btn_search = ctk.CTkButton(master=master, text="Search", width=140) # command
        self.btn_search.place(y=20, x=540)

        self.docs_label = ctk.CTkLabel(master=master, text="Documents:")
        self.docs_label.place(y=70, x=10)

        self.result_docs_textbox = ctk.CTkTextbox(master=master, width=670, height=440)
        self.result_docs_textbox.place(y=100, x=10)
        # self.result_docs_textbox.insert("0.0", text=text)
        
    def _fill_tab_settings(self):
        master = self.tabview.tab(self.tab_name_settings)

        self._rb_normalization(master)
        self._rb_search_in(master)
        self._checkbox_choice_type(master)

        self.btn_add_file = ctk.CTkButton(master=master, text="Add file", command=self.upload_file)
        self.btn_add_file.place(y=480, x=10)

        # def switch_event():
        #     print("switch toggled, current value:", switch_var.get())
        #
        # switch_var = ctk.StringVar(value="on")
        # switch = ctk.CTkSwitch(master=master, text="CTkSwitch", command=switch_event,
        #                                  variable=switch_var, onvalue="on", offvalue="off")
        # switch.place(y=440, x=10)

        # добавить кнопку про сублинейное масштабирование

        # добавить удалять ли стоп-слова

    def _rb_normalization(self, master):
        self.label = ctk.CTkLabel(master=master, text="Normalization")
        self.label.place(y=0, x=10)

        text_normalization_no = "No"
        text_normalization_stemm = "Stemming"
        text_normalization_lemm = "Lemmatization"
        text_normalization_lemm_context = "Lemmatization (context)"

        self.var_rb_normalization = tk.StringVar(value=text_normalization_no)

        self.rb_normalization_no = ctk.CTkRadioButton(master=master, text=text_normalization_no, variable=self.var_rb_normalization, value=text_normalization_no)
        self.rb_normalization_no.place(y=30, x=10)

        self.rb_normalization_no = ctk.CTkRadioButton(master=master, text=text_normalization_stemm, variable=self.var_rb_normalization, value=text_normalization_stemm)
        self.rb_normalization_no.place(y=60, x=10)

        self.rb_normalization_no = ctk.CTkRadioButton(master=master, text=text_normalization_lemm, variable=self.var_rb_normalization, value=text_normalization_lemm)
        self.rb_normalization_no.place(y=90, x=10)

        self.rb_normalization_no = ctk.CTkRadioButton(master=master, text=text_normalization_lemm_context, variable=self.var_rb_normalization, value=text_normalization_lemm_context)
        self.rb_normalization_no.place(y=120, x=10)

    def _rb_search_in(self, master):
        self.label = ctk.CTkLabel(master=master, text="Search in")
        self.label.place(y=160, x=10)

        text_search_in_title = "Title"
        text_search_in_context = "All text"

        self.var_rb_search_in = tk.StringVar(value=text_search_in_context)

        self.rb_search_in_title = ctk.CTkRadioButton(master=master, text=text_search_in_title, variable=self.var_rb_search_in, value=text_search_in_title)
        self.rb_search_in_title.place(y=190, x=10)

        self.rb_search_in_context = ctk.CTkRadioButton(master=master, text=text_search_in_context, variable=self.var_rb_search_in, value=text_search_in_context)
        self.rb_search_in_context.place(y=220, x=10)

    def _checkbox_choice_type(self, master):
        self.label = ctk.CTkLabel(master=master, text="Type of files")
        self.label.place(y=260, x=10)

        text_checkbox_all_types = "All types"
        text_checkbox_txt = ".txt"
        text_checkbox_pdf = ".pdf"
        text_checkbox_docx = ".docx"

        self.var_checkbox = tk.StringVar(value=text_checkbox_all_types)

        self.choice_all_types = ctk.CTkCheckBox(master=master, text=text_checkbox_all_types, variable=self.var_checkbox, onvalue=text_checkbox_all_types)
        self.choice_all_types.place(y=290, x=10)

        self.choice_txt = ctk.CTkCheckBox(master=master, text=text_checkbox_txt, variable=self.var_checkbox, onvalue=text_checkbox_txt)
        self.choice_txt.place(y=320, x=10)

        self.choice_pdf = ctk.CTkCheckBox(master=master, text=text_checkbox_pdf, variable=self.var_checkbox, onvalue=text_checkbox_pdf)
        self.choice_pdf.place(y=350, x=10)

        self.choice_docx = ctk.CTkCheckBox(master=master, text=text_checkbox_docx, variable=self.var_checkbox, onvalue=text_checkbox_docx)
        self.choice_docx.place(y=380, x=10)

    def _fill_tab_help(self):
        master = self.tabview.tab(self.tab_name_help)
        self.label = ctk.CTkLabel(master=master, text="This text in help")
        self.label.place(y=20, x=20)

    def upload_file(self):

        file_types_mapping = {
            'Text Files': ('*.txt', self.choice_txt._check_state),
            'PDF Files': ('*.pdf', self.choice_pdf._check_state),
            'Word Files': ('*.docx', self.choice_docx._check_state),
        }

        if self.choice_all_types._check_state:
            filetypes = [(name, pattern) for name, pattern in file_types_mapping.items()]
        else:
            filetypes = [(name, pattern) for name, (pattern, is_checked) in file_types_mapping.items() if is_checked]

        if not filetypes:
            self.show_info_window("Need to choose a file type")
            print("Need to choose a file type")
            return

        path = fd.askopenfilename(title='Open a file', initialdir='/', filetypes=filetypes)
        if path:
            doc = DocumentMy()
            doc.add_new_doc(path)

        # Выводим состояние нормализации
        print(self.var_rb_normalization.get())

        # if self.choice_all_types._check_state:
        #     filetypes = (('Text Files', '*.txt'), ('PDF Files', '*.pdf'), ('Word Files', '*.docx'))
        # else:
        #     if self.choice_txt._check_state:
        #         filetypes += (('Text Files', '*.txt'), )
        #     if self.choice_pdf._check_state:
        #         filetypes += (('PDF Files', '*.pdf'), )
        #     if self.choice_docx._check_state:
        #         filetypes += (('Word Files', '*.docx'), )
        # if len(filetypes) == 0:
        #     self.show_info_window("Need choose type")
        #     print("need choose type file")
        # else:
        #     path = fd.askopenfilename(title='Open a file', initialdir='/', filetypes=filetypes)
        #     if path:
        #         doc = DocumentMy()
        #         doc.add_new_doc(path)

        # print(self.var_rb_normalization.get())

    def btn_search(self):
        print()

    # функция для поиска в которую передавать параметры стемминг, лемматизация и так далее

    @staticmethod
    def show_info_window(text):
        message = ctk.CTkToplevel()
        message.title("Warning")
        message.geometry("400x200+800+450")
        message.grab_set()
        label = ctk.CTkLabel(master=message, text=text)
        label.place(x=40, y=40)
