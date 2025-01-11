from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from db.db import Database
import os
import PyPDF2
from docx import Document

class DocumentMy:
    def __init__(self):
        self.documents = []
        self.paths = []

        self.directory_path = None
        self.file_list = []

        self.bd = Database()

    def read_docs(self, path):
        self.directory_path = path
        # self.title, self.type = os.path.splitext(os.path.basename(self.path))
        # print(self.directory_path)
        self._get_all_files()
        self._read_files()
        # print(self.documents)
        # print("paths, TF-IDF = ", self.paths)
        self.bd.add_documents_to_db(self.documents, self.paths)

    def _get_all_files(self):
        for root, _, files in os.walk(self.directory_path):
            for file in files:
                title, extension = os.path.splitext(file)
                self.file_list.append([root, title, extension])
                self.paths.append(root + '\\' + title + extension)
        return self.file_list

    def _read_files(self):
        for root, title, extension in self.file_list:
            path = os.path.join(root, f"{title}{extension}")
            self._read_data_from_file(path, extension)

    def _read_data_from_file(self, path, type):
        if type == ".txt":
            self._read_txt_file(path)
        if type == ".pdf":
            self._read_pdf_file(path)
        if type == ".docx":
            self._read_docx_file(path)

    def _read_pdf_file(self, path):
        with open(path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ''
            for page in reader.pages:
                text += page.extract_text() + ' '
        # print(text.lower())
        self.documents.append(text.lower())
        # self.text = text

    def _read_docx_file(self, path):
        doc = Document(path)
        text = ''
        for para in doc.paragraphs:
            text += para.text + ' '
        self.documents.append(text.lower())
        
    def _read_txt_file(self, path):
        with open(path) as f:
            text = f.read()
        self.documents.append(text.lower())

    def get_request(self, request):
        self.request = request

    def get_result(self):
        return self.bd.search_query_in_db(self.request)
