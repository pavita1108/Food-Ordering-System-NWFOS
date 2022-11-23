import sqlite3

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

def insertBLOB(photo, name, harga, deskripsi):
    try:
        sqliteConnection = sqlite3.connect('data.sqlite')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        sqlite_insert_blob_query = """ INSERT INTO menu
                                  (Gambar, Nama, Harga, Deskripsi) VALUES (?, ?, ?, ?)"""

        empPhoto = convertToBinaryData(photo)
        # Convert data into tuple format
        data_tuple = (empPhoto, name, harga, deskripsi)
        cursor.execute(sqlite_insert_blob_query, data_tuple)
        sqliteConnection.commit()
        print("Image and file inserted successfully as a BLOB into a table")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed")

insertBLOB(r"C:\Users\Mutiara\Downloads\RPL\almond croissant.JPG", "Almond Croissant ", 18000, "Rich, almond flan enveloped in a croissant, then topped with sliced almonds. It's the perfect combination of sweet and savory.")
insertBLOB(r"C:\Users\Mutiara\Downloads\RPL\cheese bagels.JPG", "Cheese Bagels", 12000, "A New York style bagel topped with Asiago cheese, poppy and sesame seeds, onion and garlic.")
insertBLOB(r"C:\Users\Mutiara\Downloads\RPL\tuna puff.JPG", "Tuna Puff", 26000, "Buttery flaky savory tuna puff pastry")
insertBLOB(r"C:\Users\Mutiara\Downloads\RPL\redvelvet.JPG", "Scarlet Velvet Cake", 35000, "This Red Velvet cake frosted with Classci cream Cheese")
insertBLOB(r"C:\Users\Mutiara\Downloads\RPL\ciskek.jpg", "New York Cheesecake", 35000, "A staple at its best Cheesecake, New York style")
insertBLOB(r"C:\Users\Mutiara\Downloads\RPL\mocha.jpg", "Mocha Frappuccino", 43000, "Mocha sauce, Frappuccino® roast coffee, milk and ice all come together for a mocha flavor that'll leave you wanting more.")
insertBLOB(r"C:\Users\Mutiara\Downloads\RPL\caramel.jpg", "Caramel Frappuccino", 50000, "Buttery caramel syrup meets coffee, milk and ice for a rendezvous in the blender. Then whipped cream and caramel sauce layer the love on top.")
insertBLOB(r"C:\Users\Mutiara\Downloads\RPL\greentea.jpg", "Green Tea Cream Frappuccino", 53000, "We blend sweetened premium matcha green tea, milk and ice and top it with sweetened whipped cream to give you a delicious boost of energy.")
insertBLOB(r"C:\Users\Mutiara\Downloads\RPL\tivana.jpg", "TEAVANA Mint Blend Hot Tea", 18000, "A bracing blend of mint with a pinch of tarragon. Light, sweet flavours of spearmint and the bold,cooling taste of peppermint and gentle, warming tarragon. Delicately balanced in colour, crisp in flavour and refreshingly delicious.")
insertBLOB(r"C:\Users\Mutiara\Downloads\RPL\americano.jpg", "Caffè Americano", 10000, "HOT: Rich, full-bodied espresso with hot water.")