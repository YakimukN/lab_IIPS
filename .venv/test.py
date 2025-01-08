# from sklearn.feature_extraction.text import TfidfVectorizer
# import numpy as np
#
#
# class SearchEngine:
#     def __init__(self):
#         self.vectorizer = TfidfVectorizer()
#         self.documents = []
#         self.tfidf_matrix = None
#
#     def add_documents(self, documents):
#         self.documents = documents
#         self.tfidf_matrix = self.vectorizer.fit_transform(documents)
#         print(self.tfidf_matrix.toarray()[2])
#         # print(self.vectorizer.get_feature_names_out())
#
#     def search(self, query):
#         # Преобразуем запрос в вектор TF-IDF
#         self.query_vector = self.vectorizer.transform([query])
#         # print("dgsffdg ========= ", query_vector)
#         # Вычисляем косинусное сходство
#         similarities = np.dot(self.tfidf_matrix, self.query_vector.T).toarray().flatten()
#         # print(query_vector)
#         # print(query_vector.T)
#
#         # Получаем индексы документов, отсортированные по релевантности
#         sorted_indexes = np.argsort(similarities)[::-1]
#         # print(sorted_indexes)
#         return [(self.documents[i], similarities[i]) for i in sorted_indexes]
#
#
# # Пример использования
# documents = [
#     "Python is a programming language",
#     "Java is also a programming language",
#     "Machine learning is interesting",
#     # "Python is used in machine learning",
#     # "in this year i am was fun"
# ]
#
# search_engine = SearchEngine()
# search_engine.add_documents(documents)
#
# # query = "Python programming"
# query = "Python is fun programming"
# results = search_engine.search(query)
#
#
#
# for doc, score in results:
#     print(f"Score: {score:.4f} - Document: {doc}")
#
#
#
#
#
#
#
#
# import nltk
# from nltk.stem import WordNetLemmatizer
# from nltk.corpus import wordnet as wn
#
# # nltk.download('averaged_perceptron_tagger_eng')
#
# def get_wordnet_pos(treebank_tag):
#     if treebank_tag.startswith('J'):
#         return wn.ADJ
#     elif treebank_tag.startswith('V'):
#         return wn.VERB
#     elif treebank_tag.startswith('N'):
#         return wn.NOUN
#     elif treebank_tag.startswith('R'):
#         return wn.ADV
#     else:
#         return None
#
# def lemmatize_with_pos(words):
#     lemmatizer = WordNetLemmatizer()
#     lemmatized_words = []
#
#     for word, pos in words:
#         wordnet_pos = get_wordnet_pos(pos) or wn.NOUN  # По умолчанию выбираем NOUN
#         lemmatized_word = lemmatizer.lemmatize(word, pos=wordnet_pos)
#         lemmatized_words.append(lemmatized_word)
#
#     return lemmatized_words
#
# import string
# from nltk import pos_tag, word_tokenize
#
# text = "The boys are playing with their toys. I ran. I was reading."
#
# exclude = set(string.punctuation)
# result = ''.join(ch for ch in text if ch not in exclude)
# tokens = word_tokenize(result)
# tagged_words = pos_tag(tokens)
#
# # Лемматизация с учетом части речи
# lemmatized = lemmatize_with_pos(tagged_words)
#
# print(f'Original: {tokens}')
# print(f'Lemmatized: {lemmatized}')


# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
#
# # Шаг 1. Собираем коллекцию документов
# documents = [
#     "Поисковая система использует tf-idf для оценки релевантности.",
#     "TF-IDF означает Term Frequency-Inverse Document Frequency.",
#     "Эта модель широко применяется в задачах информационного поиска.",
#     "Система поиска сравнивает запросы пользователей с текстом документов.",
# ]
#
# # Шаг 2. Создаем TF-IDF индекс
# vectorizer = TfidfVectorizer()
# tfidf_matrix = vectorizer.fit_transform(documents)
#
# # Выводим векторное представление документов (опционально)
# print("Фичи TF-IDF:", vectorizer.get_feature_names_out())
# print("TF-IDF матрица:\n", tfidf_matrix.toarray())
#
#
# # Шаг 3. Выполняем поиск
# def search(query, top_n=3):
#     query_vector = vectorizer.transform([query])  # Преобразуем запрос в TF-IDF вектор
#     similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()  # Вычисляем косинусное сходство
#
#     # Сортируем документы по убыванию релевантности
#     ranked_indices = similarities.argsort()[::-1][:top_n]
#     return [(documents[i], similarities[i]) for i in ranked_indices if similarities[i] > 0]
#
#
# # Пример пользовательского запроса
# query = "поиск tf-idf"
# results = search(query)
#
# # Шаг 4. Выводим результаты
# print("\nРезультаты поиска:")
# for doc, score in results:
#     print(f"Релевантность: {score:.4f} | Документ: {doc}")
#



#
#
#
#
#
#
#
# import sqlite3
# import pickle
# import numpy as np
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
#
# # Создаём базу данных SQLite
# conn = sqlite3.connect("tfidf_documents4.db")
# cursor = conn.cursor()
#
# # # # Создание таблицы
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
#
#
#
# vectorizer = TfidfVectorizer()
# # Путь для сохранения векторизатора
# vectorizer_path = "tfidf_vectorizer.pkl"
#
#
#
#
#
#
#
# # Шаг 1: Добавление документов в базу данных
# def add_documents_to_db(documents, paths):
#     global vectorizer  # Указываем, что модифицируем глобальный объект
#     tfidf_matrix = vectorizer.fit_transform(documents)
#
#     # Сохраняем обученный векторизатор
#     with open(vectorizer_path, "wb") as f:
#         pickle.dump(vectorizer, f)
#
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
#     # Загружаем обученный векторизатор
#     with open(vectorizer_path, "rb") as f:
#         vectorizer = pickle.load(f)
#
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
# query = "this"
# results = search_query_in_db(query)
#
# # Вывод результатов
# for title, path, score in results:
#     print(f"Релевантность: {score:.4f}, Название: {title}, Путь: {path}")
#
































import sqlite3
import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import wordnet
from nltk import download

# download('wordnet')  # Убедитесь, что WordNet загружен

def get_synonyms(word):
    """
    Получает список синонимов для заданного слова из WordNet.
    """
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name().replace('_', ' '))
    print(list(synonyms))
    return list(synonyms)

def expand_query_with_synonyms(query):
    """
    Расширяет запрос, добавляя синонимы для каждого слова из запроса.
    """
    words = query.split()
    expanded_words = set(words)  # Начинаем с оригинальных слов
    for word in words:
        expanded_words.update(get_synonyms(word))
    return ' '.join(expanded_words)

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

def save_vectorizer_to_db(vectorizer):
    serialized_vectorizer = pickle.dumps(vectorizer)
    print(serialized_vectorizer)
    cursor.execute("INSERT OR REPLACE INTO vectorizer (id, vectorizer) VALUES (1, ?)", (serialized_vectorizer,))
    conn.commit()

def load_vectorizer_from_db():
    cursor.execute("SELECT vectorizer FROM vectorizer WHERE id = 1")
    row = cursor.fetchone()
    if row:
        return pickle.loads(row[0])
    else:
        raise ValueError("Vectorizer not found in database")

def add_documents_to_db(documents, paths):
    global vectorizer
    tfidf_matrix = vectorizer.fit_transform(documents)
    save_vectorizer_to_db(vectorizer)
    for i, (doc, path) in enumerate(zip(documents, paths)):
        tfidf_vector = pickle.dumps(tfidf_matrix[i].toarray())
        cursor.execute("INSERT INTO documents (title, path, tfidf_vector) VALUES (?, ?, ?)",
                       (f"Document {i + 1}", path, tfidf_vector))
    conn.commit()

def search_query_in_db(query, top_n=23):
    vectorizer = load_vectorizer_from_db()
    expanded_query = expand_query_with_synonyms(query)  # Расширяем запрос синонимами
    query_vector = vectorizer.transform([expanded_query])

    results = []
    cursor.execute("SELECT id, title, path, tfidf_vector FROM documents")
    for doc_id, title, path, tfidf_blob in cursor.fetchall():
        tfidf_vector = pickle.loads(tfidf_blob)
        similarity = cosine_similarity(query_vector, np.array(tfidf_vector)).flatten()[0]
        results.append((title, path, similarity))

    results = sorted(results, key=lambda x: x[2], reverse=True)[:top_n]
    return results

# Пример использования
documents = [
    "This is a test document about machine learning.",
    "TF-IDF is a method for text vectorization.",
    "This document discusses search engines and information retrieval.",
    "Artificial intelligence is a branch of computer science that focuses on creating intelligent machines.",
    "Machine learning is a subset of AI that involves teaching computers to learn from data.",
    "Neural networks are used in deep learning, which is a method in artificial intelligence."
]

paths = ["D:/Texts/text1.txt", "D:/Texts/text2.txt", "D:/Texts/text3.txt", "D:/Texts/text4.txt", "D:/Texts/text5.txt", "D:/Texts/text6.txt"]

# add_documents_to_db(documents, paths)

query = "pet"
results = search_query_in_db(query)

for title, path, score in results:
    print(f"Релевантность: {score:.4f}, Название: {title}, Путь: {path}")
