file_name = "B:/Python projects/Python-Training/Files/l_22/quotes.txt"
class Quotes_Library:
    def __init__(self, file_name):
        self.file_name = file_name
        self.items = {}
        self.save_to_library()

    def authors_rating(self):
        slovarb = {}
        for id in self.return_ids():
            author_name = self.items[id]["author"]
            quote_len = len(self.items[id]["quote"])

            if author_name in slovarb:
                slovarb[author_name] = slovarb[author_name] + quote_len
            else:
                slovarb[author_name] = quote_len

        sorted_authors = []
        for author, weight in slovarb.items():
            sorted_authors.append((author, weight))

        n = len(sorted_authors)
        for i in range(n):
            for j in range(0, n - i - 1):
                if sorted_authors[j][1] < sorted_authors[j + 1][1]:
                    sorted_authors[j], sorted_authors[j + 1] = sorted_authors[j + 1], sorted_authors[j]

        print("Рейтинг авторов:")
        for author, weight in sorted_authors:
            print(f"{author}: {weight}")

        return sorted_authors

    def save_to_file(self):
        file = open(self.file_name, 'w', encoding="utf8")
        for id in self.items:
            author = self.items[id]["author"]
            theme = self.items[id]["theme"]
            quote = self.items[id]["quote"]
            line = author + ";" + theme + ";" + quote + "\n"
            file.write(line)
        file.close()

    def add_quote(self, author, theme, quote):
        if self.items:
            max_id = max(self.items.keys())
            new_id = max_id + 1
        else:
            new_id = 0

        self.items[new_id] = {"author": author, "theme": theme, "quote": quote}
        return new_id

    def delete_quote(self, quote_id):
        if quote_id in self.items:
            del self.items[quote_id]
            return True
        else:
            return False

    def save_to_library(self):
        id = 0
        with open(file_name, 'r', encoding="utf8") as file:Новый текстовый документ.py
            for line in file:
                a = line[:-1].split(";")
                self.items[id] = {"author": a[0], "theme": a[1], "quote": a[2]}
                id += 1

    def return_ids(self):
        return list(self.items.keys())

    def get_longest_quote(self):
        max_length = 0
        max_len_quote = -1
        idss = self.return_ids()
        for id in idss:
            if len(self.items[id]["quote"]) > max_length:
                max_length = len(self.items[id]["quote"])
                max_len_quote = self.items[id]["quote"]
        return max_len_quote

    def get_shortest_quote(self):
        min_length = 10000000
        min_len_quote = -1
        idss = self.return_ids()
        for id in idss:
            if len(self.items[id]["quote"]) < min_length:
                min_length = len(self.items[id]["quote"])
                min_len_quote = self.items[id]["quote"]
        return min_len_quote


a = Quotes_Library(file_name)
for id in a.items:
    print(id, a.items[id])
print(a.get_longest_quote())
print(a.get_shortest_quote())