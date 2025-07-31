from faker import Faker
import random

fake = Faker()

emails = ['gmail', 'yahoo', 'hotmail']

num_members = 20
num_libs = 10
num_admins = 2


admin = ["INSERT INTO Account(firstName, lastName, email, accountType) VALUES('Maurice', 'Wright', 'mmauricewrightt@gmail.com', 'admin');"]

librarians = []
for _ in range(10):
    fname = fake.first_name()
    lname = fake.last_name()
    email = f'{fname}.{lname}@{random.choice(emails)}.com'
    account = 'librarian'
    librarians.append(f"INSERT INTO Account(firstName, lastName, email, accountType) VALUES('{fname}', '{lname}', '{email}', '{account}');")

visitors = []
for _ in range(20):
    fname = fake.first_name()
    lname = fake.last_name()
    email = f'{fname}.{lname}@{random.choice(emails)}.com'
    account = 'visitor'
    visitors.append(f"INSERT INTO Account(firstName, lastName, email, accountType) VALUES('{fname}', '{lname}', '{email}', '{account}');")



inserts = admin + librarians + visitors


with open("C:/Users/mauri/Documents/librarydb/data/seed_account_inserts.sql", "w") as file:
    file.write("\n".join(inserts))

# for _ in inserts:
#     print(_)
