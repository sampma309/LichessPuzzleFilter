import helpers
from sqlite3 import Error
import csv


def main():
    
    # Create connection to puzzles.db
    db = helpers.create_connection('puzzles.db')

    # Create table 'puzzles' in puzzles.db
    create_table(db)

    # Read data from puzzles.csv and import to puzzles.db
    import_data('puzzles.csv', db)

    db.commit()
    db.close()


def create_table(db):
    
    try:
        db.execute('CREATE TABLE puzzles("PuzzleId" TEXT, "FEN" TEXT, "Moves" TEXT, "Rating" INTEGER, "Pieces" TEXT);')
        print("Table 'puzzles' created successfully")
    except Error as e:
        print(f"The error '{e}' has occurred. Terminating program.")


def import_data(file, db):


    cur = db.cursor()

    # Open file
    try:
        with open(file, newline='') as csvfile:
            reader = csv.reader(csvfile)
            counter = 0
            for row in reader:
                cur.execute("INSERT INTO puzzles (PuzzleId, FEN, Moves, Rating) VALUES (?, ?, ?, ?);",
                           (row[0], row[1], row[2], int(row[3])))
                counter += 1
                if counter % 10000 == 0:
                    print(f"{counter} puzzles imported")
    except IOError:
        print(f"Unable to open file '{file}'. Terminating program.")
    finally:
        csvfile.close()
    
    db.commit()
        
if __name__ == '__main__':
    main()
