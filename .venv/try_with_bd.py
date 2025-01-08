# import sqlite3
# import pickle
# import numpy as np
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
#
# # Создаём базу данных SQLite
# conn = sqlite3.connect("tfidf_documents3.db")
# cursor = conn.cursor()
#
# # # Создание таблицы
# # cursor.execute("""
# # CREATE TABLE IF NOT EXISTS documents (
# #     id INTEGER PRIMARY KEY,
# #     title TEXT,
# #     path TEXT,
# #     tfidf_vector BLOB
# # )
# # """)
# # conn.commit()
#
# # Инициализация TfidfVectorizer
# vectorizer = TfidfVectorizer()
#
#
# # Шаг 1: Добавление документов в базу данных
# def add_documents_to_db(documents, paths):
#     tfidf_matrix = vectorizer.fit_transform(documents)
#     for i, (doc, path) in enumerate(zip(documents, paths)):
#         # Сериализуем TF-IDF вектор
#         tfidf_vector = pickle.dumps(tfidf_matrix[i].toarray())
#         cursor.execute("INSERT INTO documents (title, path, tfidf_vector) VALUES (?, ?, ?)",
#                        (f"Document {i + 1}", path, tfidf_vector))
#     conn.commit()
#
#
# # Шаг 2: Выполнение поиска
# def search_query_in_db(query, top_n=3):
#     # Преобразуем запрос в TF-IDF вектор
#     query_vector = vectorizer.transform([query])
#
#     results = []
#     cursor.execute("SELECT id, title, path, tfidf_vector FROM documents")
#     for doc_id, title, path, tfidf_blob in cursor.fetchall():
#         # Десериализуем TF-IDF вектор
#         tfidf_vector = pickle.loads(tfidf_blob)
#         # Вычисляем косинусное сходство
#         similarity = cosine_similarity(query_vector, np.array(tfidf_vector)).flatten()[0]
#         results.append((title, path, similarity))
#
#     # Сортируем результаты по релевантности
#     results = sorted(results, key=lambda x: x[2], reverse=True)[:top_n]
#     return results
#
#
# # Пример использования
# documents = [
#     "This is a test document about machine learning.",
#     "TF-IDF is a method for text vectorization.",
#     "This document discusses search engines and information retrieval."
# ]
#
# # paths = ["path/to/doc1.txt", "path/to/doc2.txt", "path/to/doc3.txt"]
# paths = ["D:/Texts/text1.txt", "D:/Texts/text2.txt", "D:/Texts/text3.txt", "D:/Texts/text.txt"]
#
# # Добавляем документы в базу данных
# # add_documents_to_db(documents, paths)
#
# # Поиск по запросу
# query = "text vectorization"
# results = search_query_in_db(query)
#
# # Вывод результатов
# for title, path, score in results:
#     print(f"Релевантность: {score:.4f}, Название: {title}, Путь: {path}")


import sqlite3
import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Создаём базу данных SQLite
conn = sqlite3.connect("tfidf_documents.db")
cursor = conn.cursor()

# Создаём таблицы для документов и векторизатора
cursor.execute("""
CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY,
    title TEXT,
    path TEXT,
    tfidf_vector BLOB
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS vectorizer (
    id INTEGER PRIMARY KEY,
    vectorizer BLOB
)
""")
conn.commit()

# Инициализация TfidfVectorizer
vectorizer = TfidfVectorizer()


# Шаг 1: Сохранение векторизатора в базу данных
def save_vectorizer_to_db(vectorizer):
    serialized_vectorizer = pickle.dumps(vectorizer)
    cursor.execute("INSERT OR REPLACE INTO vectorizer (id, vectorizer) VALUES (1, ?)", (serialized_vectorizer,))
    conn.commit()


# Шаг 2: Загрузка векторизатора из базы данных
def load_vectorizer_from_db():
    cursor.execute("SELECT vectorizer FROM vectorizer WHERE id = 1")
    row = cursor.fetchone()
    if row:
        return pickle.loads(row[0])
    else:
        raise ValueError("Vectorizer not found in database")


# Шаг 3: Добавление документов в базу данных
def add_documents_to_db(documents, paths):
    global vectorizer  # Указываем, что модифицируем глобальный объект
    tfidf_matrix = vectorizer.fit_transform(documents)

    # Сохраняем векторизатор в базу данных
    save_vectorizer_to_db(vectorizer)

    for i, (doc, path) in enumerate(zip(documents, paths)):
        # Сериализуем TF-IDF вектор
        tfidf_vector = pickle.dumps(tfidf_matrix[i].toarray())
        cursor.execute("INSERT INTO documents (title, path, tfidf_vector) VALUES (?, ?, ?)",
                       (f"Document {i + 1}", path, tfidf_vector))
    conn.commit()


# Шаг 4: Выполнение поиска
def search_query_in_db(query, top_n=23):
    # Загружаем обученный векторизатор из базы данных
    vectorizer = load_vectorizer_from_db()

    # Преобразуем запрос в TF-IDF вектор
    query_vector = vectorizer.transform([query])

    results = []
    cursor.execute("SELECT id, title, path, tfidf_vector FROM documents")
    for doc_id, title, path, tfidf_blob in cursor.fetchall():
        # Десериализуем TF-IDF вектор
        tfidf_vector = pickle.loads(tfidf_blob)
        # Вычисляем косинусное сходство
        similarity = cosine_similarity(query_vector, np.array(tfidf_vector)).flatten()[0]
        results.append((title, path, similarity))

    # Сортируем результаты по релевантности
    results = sorted(results, key=lambda x: x[2], reverse=True)[:top_n]
    return results




import os
# получаем имена всех файлов в папке по указанному пути и во всех вложенных папках
def get_all_files(directory):
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list

# считываем все содержимое из всех файлов и вложенный папок заданной директории
def read_all_files(files):
    texts = []
    for file in files:
        with open(file) as f:
            # print(f.read())
            texts.append(f.read())
    return texts




# Пример использования
documents = []

directory_path = 'D:\\Texts'  # путь к директории
files = get_all_files(directory_path)
documents = read_all_files(files)

#     "This is a test document about machine learning.",
#     "TF-IDF is a method for text vectorization.",
#     "This document discusses search engines and information retrieval."
# ]

# paths = ["D:/Texts/text1.txt", "D:/Texts/text2.txt", "D:/Texts/text3.txt"]

# Добавляем документы в базу данных
# add_documents_to_db(documents, files)

# Поиск по запросу
query = "all"
results = search_query_in_db(query)

# Вывод результатов
for title, path, score in results:
    print(f"Релевантность: {score:.4f}, Название: {title}, Путь: {path}")
