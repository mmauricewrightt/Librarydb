from faker import Faker
import random

fake = Faker()

def generate_book_title():
    templates = [
        "The {adj} {noun}",
        "{name}'s Secret",
        "Tales of the {adj} {place}",
        "Escape from {place}",
        "Chronicles of the {adj} {noun}",
        "Whispers in the {place}",
        "The Curse of the {adj} {noun}"
    ]

    title = random.choice(templates).format(
        adj=fake.word(ext_word_list=['dark', 'forgotten', 'ancient', 'lonely', 'golden', 'silent']),
        noun=fake.word(ext_word_list=['forest', 'mirror', 'empire', 'spell', 'river', 'mask']),
        place=fake.city(),
        name=fake.first_name()
    )

    return title

num_books = 100

books = []
for _ in range(100):
    bookName = generate_book_title()
    author_fname = fake.first_name()
    author_lname = fake.last_name()
    books.append(f'INSERT INTO Book(bookName, bookAuthor) VALUES("{bookName}", "{author_fname} {author_lname}");')

with open("C:/Users/mauri/Documents/Librarydb/data/seed_book_inserts.sql", "w") as file:
    file.write("\n".join(books))

# for _ in books:
#     print(_)


