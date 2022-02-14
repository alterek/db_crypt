import sqlite3


path = 'C:/sqlite/cards.db'
con = sqlite3.connect(path)
cur = con.cursor()
ins = []
name = ["Иванов", "Смирнов", "Кузнецов", "Попов", "Васильев"]
cards = [1100, 2200, 3300, 4400, 5500]
for i in range(5):
    image = open('D:/' + str(i+1) + '.BMP', 'rb')
    image_read = image.read()
    row = [i+1, name[i], cards[i], image_read]
    ins.append(row)

cur.executemany("INSERT INTO CARDS (CARD_ID, CLI_NAME, CARD_NO, FINGERPRINT) VALUES (?, ?, ?, ?)", tuple(ins))
con.commit()
