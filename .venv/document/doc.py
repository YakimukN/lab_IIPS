from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from db.db import Database
import os
import PyPDF2
from docx import Document

class DocumentMy:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.documents = []
        self.tfidf_matrix = None

    def add_new_doc(self, path):
        self.path = path
        self.title, self.type = os.path.splitext(os.path.basename(self.path))
        self._read_data_from_file()

        # Database.add_doc(path=self.path, title=self.title, type=self.type, text=self.text)

    def _read_data_from_file(self):
        if self.type == ".txt":
            self._read_txt_file()
        elif self.type == ".pdf":
            self._read_pdf_file()
        elif self.type == ".docx":
            self._read_docx_file()

    def _read_pdf_file(self):
        with open(self.path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ''
            for page in reader.pages:
                text += page.extract_text() + '\n'
        print(text)
        self.text = text

    def _read_docx_file(self):
        doc = Document(self.path)
        text = ''
        for para in doc.paragraphs:
            text += para.text + '\n'
        # return text
        print(text)
        self.text = text
        
    def _read_txt_file(self):
        with open(self.path) as f:
            text = f.read()
        print(text)
        self.text = text

    def get_lemmas(self):
        lemmatizer = WordNetLemmatizer()
        lemmatized_words = [lemmatizer.lemmatize(word) for word in tokens]
        # print(lemmatized_words)
        return lemmatized_words
        print()

    def get_lemmas_in_context(self):
        print()

    def get_tokens(self):
        tokens = word_tokenize(text)
        # print(tokens)
        return tokens
        print()

    def get_stemms(self, tokens):
        stemmer = PorterStemmer()
        stemmed_words = [stemmer.stem(word) for word in tokens]
        print(stemmed_words)
        print()

    def delete_stopwords(tokens):
        filtered_tokens = [word for word in tokens if not word in stopwords.words('english')]
        # print(filtered_tokens)
        return filtered_tokens

    def all_to_lower_case(tokens):
        return [word.lower() for word in tokens]
        # print(result)

        



    def add_documents(self, documents):
        self.documents = documents
        self.tfidf_matrix = self.vectorizer.fit_transform(documents)
        print(self.tfidf_matrix.toarray()[2])
        # print(self.vectorizer.get_feature_names_out())

    def search(self, query):
        # Преобразуем запрос в вектор TF-IDF
        self.query_vector = self.vectorizer.transform([query])
        # print("dgsffdg ========= ", query_vector)
        # Вычисляем косинусное сходство
        similarities = np.dot(self.tfidf_matrix, self.query_vector.T).toarray().flatten()
        # print(query_vector)
        # print(query_vector.T)

        # Получаем индексы документов, отсортированные по релевантности
        sorted_indexes = np.argsort(similarities)[::-1]
        # print(sorted_indexes)
        return [(self.documents[i], similarities[i]) for i in sorted_indexes]











# # Пример использования
# documents = [
#     "Python is a programming language",
#     "Java is also a programming language",
#     "Machine learning is interesting",
#     "Python is used in machine learning",
#     "in this year i am was fun"
# ]
# 
# search_engine = DocumentMy()
# search_engine.add_documents(documents)
# 
# query = "Python is fun programming"
# results = search_engine.search(query)
# 
# # print(search_engine.arr_to_str())
# 
# # search_engine.fun_test()
# 
# 
# for doc, score in results:
#     print(f"Score: {score:.4f} - Document: {doc}")