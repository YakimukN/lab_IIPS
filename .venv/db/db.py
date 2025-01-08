import sqlite3

class Database():
    def __init__(self):
        self.con = sqlite3.connect("IIPS_TDFIDF_test.db")
        self.cursor = self.con.cursor()

        # self.cursor.execute("""CREATE TABLE docs_tfidf
        #         (title TEXT PRIMARY KEY,
        #         type TEXT,
        #         path TEXT,
        #         tokens TEXT,
        #         lemms TEXT,
        #         stemms TEXT,
        #         lemms_contecst TEXT)
        #     """)




        # data = [("first_title.txt", "2745 3765 23456 3457", ".txt", "D/folser/text.txt", "shgfs fdhgsk sfh sdfh gdfh gdfh dsfj"), ("second_title.txt", "asfsd, dfd, fdsf, dfas", ".txt", "D/folser/text.txt", "shgfs fdhgsk sfh sdfh gdfh gdfh dsfj")]
        # self.cursor.executemany("INSERT INTO docs_tfidf (title, tf_idf, type, path, tokens) VALUES (?, ?, ?, ?, ?)", data)
        # self.con.commit()

        # self.cursor.execute("SELECT * FROM docs_tfidf")
        # print(self.cursor.fetchall())

    @staticmethod
    def add_doc(path, title, type, text):
        print("path = ", path)
        print("type = ", type)
        print("title = ", title)
        print("text = ", text)
        print("method from db run")
        


# db = Database()












# import sqlite3;
#
# con = sqlite3.connect("IIPS.db")
# cursor = con.cursor()
#
# # данные для добавления
# # people = [("Sam", 28), ("Alice", 33), ("Kate", 25)]
# # cursor.executemany("INSERT INTO people (name, age) VALUES (?, ?)", people)
# # выполняем транзакцию
# # con.commit()


# cursor.execute("""CREATE TABLE docs
#                 (docName TEXT PRIMARY KEY,
#                 type TEXT,
#                 title TEXT,
#                 path TEXT)
#             """)
