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

insertBLOB(r"C:\Users\Mutiara\Downloads\RPL\Hardees_Site_705x742_BEC_Biscuit.jpg", "Bacon, Egg & Cheese Biscuit", 20000, "The McDonald's Bacon, Egg & Cheese Biscuit breakfast sandwich features a warm, buttermilk biscuit brushed with real butter, thick cut Applewood smoked bacon, a fluffy folded egg, and a slice of melty American cheese.")