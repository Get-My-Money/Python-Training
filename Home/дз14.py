file_name = "B:/Python projects/Python-Training/Files/l_22/quotes.txt"

class Quotes_Library:
    def __init__(self, file_name):
        self.file_name = file_name
        self.items = {}
        self.save_to_library()
    
    def topic_popularity(self):
        slovarb = {}
        for id in self.return_ids():
            theme = self.items[id]["theme"]
            theme_quote = len(self.items[id]["quote"])
            if theme in list(slovarb):
                slovarb[theme] += theme_quote
            else:
                slovarb[theme] = theme_quote
        
        slovarb_lst = list(slovarb.items())
        for j in range(len(slovarb_lst)):
            for i in range(len(slovarb_lst) - 1):
                if slovarb_lst[i][1] > slovarb_lst[i+1][1]:
                   slovarb_lst[i], slovarb_lst[i+1] = slovarb_lst[i+1], slovarb_lst[i]
        slovarb_lst.reverse()
        print(slovarb_lst)
    
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

    def save_to_library(self):
        id = 0
        with open(file_name, 'r', encoding="utf8") as file:
            for line in file:
                a = line[:-1].split(";")
                self.items[id] = {"author": a[0], "theme" : a[1], "quote" : a[2]}
                id += 1
                
    def return_ids(self):
        return list(self.items.keys())

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
    
    def count_words(self):
        all_words = []
        total_symbols = 0
        
        for id in self.return_ids():
            quote = self.items[id]["quote"]
            words = quote.split()
            all_words.extend(words)
            total_symbols += len(quote)
        
        total_words = len(all_words)
        avg_words = total_words / len(self.items) if self.items else 0
        
        word_counts = {}
        for word in all_words:
            clean_word = word.strip('.,!?;:"()').lower()
            if clean_word:
                if clean_word in word_counts:
                    word_counts[clean_word] += 1
                else:
                    word_counts[clean_word] = 1
        
        top_words = list(word_counts.items())
        n = len(top_words)
        for i in range(n):
            for j in range(0, n - i - 1):
                if top_words[j][1] < top_words[j + 1][1]:
                    top_words[j], top_words[j + 1] = top_words[j + 1], top_words[j]
        
        print(f"Общее колличество слов: {total_words}")
        print(f"Средняя дленна цитаты в словах: {avg_words:.2f}")
        print("Топ-5 самых частых слов:")
        for i, (word, count) in enumerate(top_words[:5], 1):
            print(f"{i}. '{word}' - {count} раз")
        
        return {
            'total_words': total_words,
            'avg_words': avg_words,
            'top_words': top_words[:5]
        }

    def estimate_mood(self, tupes, object):
        negative_words = ["проблема", "страх", "ошибка"]
        positive_words = ["жизнь", "любовь", "мечта"]
        
        negative_emotional = 0
        positive_emotional = 0
        
        if tupes == "Author":
            for id in self.return_ids():
                if self.items[id]['author'] == object:
                    quote = self.items[id]["quote"].lower()
                    for word in positive_words:
                        if word in quote:
                            positive_emotional += 1
                    for word in negative_words:
                        if word in quote:
                            negative_emotional += 1
                            
        elif tupes == "Theme":
            for id in self.return_ids():
                if self.items[id]['theme'] == object:
                    quote = self.items[id]["quote"].lower()
                    for word in positive_words:
                        if word in quote:
                            positive_emotional += 1
                    for word in negative_words:
                        if word in quote:
                            negative_emotional += 1
        else:
            return "Ошибка"
        
        total = positive_emotional + negative_emotional
        if total == 0:
            return "Нет данных для оценки настроения"
        
        if positive_emotional > negative_emotional:
            mood = "Позитивное"
        elif negative_emotional > positive_emotional:
            mood = "Негативное"
        else:
            mood = "Нейтральное"
        
        print(f"Настроение ({tupes}: {object}): {mood}")
        print(f"Позитивных слов: {positive_emotional}")
        print(f"Негативных слов: {negative_emotional}")
        print(f"Баланс: {positive_emotional - negative_emotional}")
        
        return {
            'mood': mood,
            'positive': positive_emotional,
            'negative': negative_emotional,
            'balance': positive_emotional - negative_emotional
        }

    def search_by_pattern(self, pattern):
        found_quotes = []
        for id in self.return_ids():
            if pattern.lower() in self.items[id]["quote"].lower():
                found_quotes.append({
                    'id': id,
                    'author': self.items[id]["author"],
                    'theme': self.items[id]["theme"],
                    'quote': self.items[id]["quote"]
                })
        
        print(f"Найдено цитат с паттерном '{pattern}': {len(found_quotes)}")
        for quote in found_quotes:
            print(f"ID: {quote['id']}, Автор: {quote['author']}, Тема: {quote['theme']}")
            print(f"Цитата: {quote['quote']}")
            print("-" * 50)
        
        return found_quotes

    def get_author_stats(self, author_name):
        quotes_count = 0
        total_length = 0
        themes = set()
        
        for id in self.return_ids():
            if self.items[id]["author"] == author_name:
                quotes_count += 1
                total_length += len(self.items[id]["quote"])
                themes.add(self.items[id]["theme"])
        
        if quotes_count == 0:
            print(f"Автор '{author_name}' не найден")
            return None
        
        avg_length = total_length / quotes_count
        print(f"Статистика для автора: {author_name}")
        print(f"Количство цитат: {quotes_count}")
        print(f"Общая длинна цитат: {total_length} символов")
        print(f"Средняя длина цитаты: {avg_length:.2f} символов")
        print(f"Темы: {', '.join(themes)}")
        
        return {
            'quotes_count': quotes_count,
            'total_length': total_length,
            'avg_length': avg_length,
            'themes': list(themes)
        }

    def get_theme_stats(self, theme_name):
        quotes_count = 0
        authors = set()
        total_length = 0
        
        for id in self.return_ids():
            if self.items[id]["theme"] == theme_name:
                quotes_count += 1
                authors.add(self.items[id]["author"])
                total_length += len(self.items[id]["quote"])
        
        if quotes_count == 0:
            print(f"Тема '{theme_name}' не найдена")
            return None
        
        avg_length = total_length / quotes_count
        print(f"Статистика для темы: {theme_name}")
        print(f"Колличество цитат: {quotes_count}")
        print(f"Авторы: {', '.join(authors)}")
        print(f"Общая длинна цитат: {total_length} символов")
        print(f"Средняя длина цитаты: {avg_length:.2f} символов")
        
        return {
            'quotes_count': quotes_count,
            'authors': list(authors),
            'total_length': total_length,
            'avg_length': avg_length
        }

    def show_all_quotes(self):
        print(f"Всего цитат в библиотеке: {len(self.items)}")
        print("=" * 60)
        for id in self.return_ids():
            print(f"ID: {id}")
            print(f"Автор: {self.items[id]['author']}")
            print(f"Тема: {self.items[id]['theme']}")
            print(f"Цитата: {self.items[id]['quote']}")
            print("-" * 60)
    
    def get_total_stats(self):
        total_quotes = len(self.items)
        total_authors = len(set(self.items[id]["author"] for id in self.return_ids()))
        total_themes = len(set(self.items[id]["theme"] for id in self.return_ids()))
        total_length = sum(len(self.items[id]["quote"]) for id in self.return_ids())
        
        print("Общая статистика библиотеки:")
        print(f"Всего цитат: {total_quotes}")
        print(f"Всего авторов: {total_authors}")
        print(f"Всего тем: {total_themes}")
        print(f"Общий обьем текста: {total_length} символов")
        
        return {
            'total_quotes': total_quotes,
            'total_authors': total_authors,
            'total_themes': total_themes,
            'total_length': total_length
        }

a = Quotes_Library(file_name)