
import sqlite3

db = sqlite3.connect(
    "/home/pat/projects/patrick-williams/development/docker/shared_directory/spellingBeeDB.sqlite",
    detect_types=sqlite3.PARSE_DECLTYPES
)
letters = "maelopy"

stuff =db.execute(
    "SELECT letters, accepted, pangrams, rejected FROM bees WHERE letters = ?",
    (letters,)
).fetchone()

print("letters: ",stuff[0]," accepted: ",stuff[1]," pangrams: ", stuff[2]," rejected: ",stuff[3])

db.close()
