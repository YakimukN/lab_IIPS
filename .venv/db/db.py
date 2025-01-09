import sqlite3
import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import wordnet
from nltk import download

class Database():
    def __init__(self):
        self.conn = sqlite3.connect("tfidf_documents.db")
        self.cursor = self.conn.cursor()
        self.vectorizer = TfidfVectorizer()
        self.create_tables()


    def create_tables(self):
        self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS documents (
                    id INTEGER PRIMARY KEY,
                    path TEXT,
                    tfidf_vector BLOB
                )
                """)
        self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS vectorizer (
                    id INTEGER PRIMARY KEY,
                    vectorizer BLOB
                )
                """)
        self.conn.commit()

    def save_vectorizer_to_db(self):
        serialized_vectorizer = pickle.dumps(self.vectorizer)
        self.cursor.execute("INSERT OR REPLACE INTO vectorizer (id, vectorizer) VALUES (1, ?)", (serialized_vectorizer,))
        self.conn.commit()

    def load_vectorizer_from_db(self):
        self.cursor.execute("SELECT vectorizer FROM vectorizer WHERE id = 1")
        row = self.cursor.fetchone()
        if row:
            return pickle.loads(row[0])
        else:
            print("Database is empty")
            # raise ValueError("Vectorizer not found in database")

    def add_documents_to_db(self, documents, paths):
        self.paths = paths
        print(self.paths)
        tfidf_matrix = self.vectorizer.fit_transform(documents)

        self.save_vectorizer_to_db()

        for i, (doc, path) in enumerate(zip(documents, self.paths)):
            tfidf_vector = pickle.dumps(tfidf_matrix[i].toarray())
            self.cursor.execute("INSERT INTO documents (path, tfidf_vector) VALUES (?, ?)",
                           (path, tfidf_vector))
        self.conn.commit()

    def search_query_in_db(self, request):
        # Загружаем обученный векторизатор из базы данных
        self.vectorizer = self.load_vectorizer_from_db()
        expanded_query = self.expand_query_with_synonyms(request)  # Расширяем запрос синонимами
        results = []
        # Преобразуем запрос в TF-IDF вектор
        if self.vectorizer:
            query_vector = self.vectorizer.transform([expanded_query])

            self.cursor.execute("SELECT id, path, tfidf_vector FROM documents")
            for doc_id, path, tfidf_blob in self.cursor.fetchall():
                tfidf_vector = pickle.loads(tfidf_blob)
                # Вычисляем косинусное сходство
                similarity = cosine_similarity(query_vector, np.array(tfidf_vector)).flatten()[0]
                results.append((path, similarity))

            results = sorted((x for x in results if x[1] > 0), key=lambda x: x[1], reverse=True)
            print(results)
        return results

    def expand_query_with_synonyms(self, request):
        words = request.split()
        expanded_words = set(words)  # Начинаем с оригинальных слов
        for word in words:
            expanded_words.update(self.get_synonyms(word))
        return ' '.join(expanded_words)

    def get_synonyms(self, word):
        synonyms = set()
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                synonyms.add(lemma.name().replace('_', ' '))
        print(list(synonyms))
        return list(synonyms)