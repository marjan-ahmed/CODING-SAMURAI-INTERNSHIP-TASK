# import sqlite3 as sq

# con = sq.connect("first_db.db")
# cur = con.cursor()
# res = cur.execute(
#     """
#     CREATE TABLE movie(
#         id INTEGER PRIMARY KEY,
#         name TEXT NOT NULL,
#         time TEXT NOT NULL
#         )
#     """
# )

# def main():
#     while True:
#         print('\n Youtube Manager App')
#         print('\n 1. List Vids')
#         print('\n 2. Add Vids')
#         print('\n 3. Update Lists')
#         print('\n 4. Del Vids')
#         print('\n 5. Exit')
        
#         choice = input("Enter your choice: ")
        
#         def list_vids():
#             pass
        
#         def add_vids(name, time):
#             pass
        
#         match choice:
#             case 1:
#                 list_vids()
#             case 2:
#                 name = input("Enter the video name: ")
#                 time = int(input("Enter a time: "))
#                 add_vids(name, time)
#             case 3:
#                 update_vids()
#         conn.

# if __name__ == '__main__':
#     main()