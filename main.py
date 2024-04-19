import mysql.connector
from customtkinter import CTkLabel
from tabulate import *
import tkinter
import customtkinter




# System settings
customtkinter.set_appearance_mode("System")
#customtkinter.set_default_color_theme("red")

# app frame
app = customtkinter.CTk()
app.geometry("720x480")
app.title("Netflix DB")

# Adding elements

# Title
welcome_text = "Welcome to the Netflix Database"
welcome_label = CTkLabel(master=app, text=welcome_text, font=("Arial", 28), text_color='red')
welcome_label.pack(padx=10, pady=10)

#Run App
app.mainloop()













NetflixDB = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Thomas2003!',
    database='Netflix_DB'
)
if (NetflixDB):
    print('connected')

controller = NetflixDB.cursor(prepared=True)


# Not needed
list_of_Tables = []
controller.execute('SHOW TABLES')
for i, x in enumerate(controller):
    if i < 14:
        list_of_Tables.append(x)


def print_tables():
    SQLCommand = """
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'Netflix_DB' 
    AND table_type = 'BASE TABLE' 
    AND table_name NOT LIKE '%\_view%'
    AND table_name NOT LIKE '%\_pivot%'
    """
    controller.execute(SQLCommand)
    tables = controller.fetchall()

    formatted_tables = [list(table) for table in tables]

    tables_str = tabulate(formatted_tables, headers=["Table Names"], tablefmt="plain")
    print(tables_str)
    print('--------')


def choose(c1, c2):
    flag = True
    while (flag):
        try:
            choice = int(input('What would you like to do? (enter a number)'))
            if c1 <= choice <= c2:
                flag = False
                print("You selected:", choice)
                print('================')
                break
            else:
                print("Invalid number. Please enter a number between " + str(c1) + " and " + str(c2) + ".")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    return choice


def create_table(tableName, attributeANDValues):
    columns = []
    for attr, dataType in attributeANDValues.items():
        columns.append(f"{attr} {dataType}")

    columnList = ", ".join(columns)

    sql = f"""CREATE TABLE {tableName} ({columnList})"""
    controller.execute(sql)
    NetflixDB.commit()
    controller.execute(f"SELECT * FROM {tableName}")
    print('done')



def insert_row(tableName, attributeList, attributeValues):
    values = attributeValues.split(',')
    placeholders = ','.join(['%s'] * len(values))
    sql = f"INSERT INTO {tableName} ({','.join(attributeList)}) VALUES ({placeholders})"
    controller.execute(sql, values)
    NetflixDB.commit()
    return print("check")

def show_table(tableName):
    sql = f"SELECT * FROM {tableName}"
    controller.execute(sql)

    column_names = [col[0] for col in controller.description]
    max_col_width = 20
    print("  ".join([name.ljust(max_col_width) for name in column_names]))
    print("-" * (len(column_names) * (max_col_width + 2) - 1))


    for row in controller:
        formatted_row = [str(val).ljust(max_col_width)[:max_col_width] for val in row]
        print("  ".join(formatted_row))

def update_row(tableName, updateData, whereClause):
    setClause = ", ".join([f"{key} = %s" for key in updateData.keys()])
    sql = f"UPDATE {tableName} SET {setClause} WHERE {whereClause}"

    values = list(updateData.values())

    controller.execute(sql, values)
    NetflixDB.commit()

def delete_row(tableName, whereClause):
    sql = f"DELETE FROM {tableName} WHERE {whereClause}"

    controller.execute(sql)
    NetflixDB.commit()













print('Welcome to the Netflix Database!' + '\n----------------------------------------------')

while True:
    print('\nOPTIONS:\n1)Create \n2)Read \n3)Update \n4)Delete \n5)Quit\n')
    action = choose(1, 5)
    if action == 5:
        print('Exiting Netflix Database')
        break

    if action == 1:
        print('\nYou chose to create!')
        print('1)Create new table\n2)Create new entry in existing table')
        create_action = choose(1, 2)

        if create_action == 1:
            print('\nTo create a new table, answer the following...')
            tableName = input("What will be your new tables name:")

            attributes = input("What would you like your attributes to be?(comma seperated)")
            attributes = attributes.split(",")
            attributes = [item.strip() for item in attributes]
            attributes = set(attributes)
            types = []
            for element in attributes:
                newIn = input(f"What data type should {element} be:")
                types.append(newIn)

            attributes_types = dict(zip(attributes, types))

            create_table(tableName, attributes_types)

        elif create_action == 2:
            print('\nWhich table would you like to add too?')
            print_tables()
            choice = input("type the table name(exactly):")

            match choice:
                case "movie":
                    attributes = ['MID', 'MName', 'MReleaseDate', 'MRuntime']
                    userInput = input(
                        "Enter your movie's MID, MName, MReleaseDate, and MRuntime in a comma seperated list: ")
                    insert_row('movie', attributes, userInput)
                case "people":
                    attributes = ['people', 'PID', 'PName', 'DOB', 'IsActor', 'IsDirector', 'IsWriter']
                    userInput = input(
                        "Enter your person's PID, PName, DOB, IsActor, IsDirector, and IsWriter in a comma seperated list: ")
                    insert_row('people', attributes, userInput)
                case "characters":
                    attributes = ['CID', 'CName']
                    userInput = input("Enter your character's CID and CName in a comma seperated list: ")
                    insert_row('characters', attributes, userInput)
                case "genre":
                    attributes = ['GID', 'GName']
                    userInput = input("Enter your genre's GID and GName in a comma seperated list: ")
                    insert_row('genre', attributes, userInput)
                case "rating":
                    attributes = ['RID', 'Rating', 'Votes']
                    userInput = input("Enter you rating's RID, Rating, and Votes in a comma seperated list: ")
                    insert_row('rating', attributes, userInput)
                case "series":
                    attributes = ['SID', 'SName', 'SReleaseDate', 'SEnd']
                    userInput = input(
                        "Enter your series' SID, Sname, SReleaseYear, and SEndYear in a comma seperated list")
                    insert_row('series', attributes, userInput)

    elif action == 2:
        print('\nYou chose Read.')
        print_tables()
        choice = input("Which Table Would you like to see?(type the exact name)")
        show_table(choice)

    elif action == 3:
        print('\nYou chose to Update.')
        print_tables()
        choice = input('Which table would you like to Update?(type the exact name)')
        show_table(choice)
        row = input('Which row would you like to update?(select the ID)')
        match choice:
            case "movie":
                where = "MID = " + row
            case "people":
                where = "PID = " + row
            case "characters":
                where = "CID = " + row
            case "genre":
                where = "GID = " + row
            case "rating":
                where = "RID = " + row
            case "series":
                where = "SID = " + row
        update = input("What would you like to update?(type the exact attribute(s), comma seperated)")
        update = update.split(",")
        update = [item.strip() for item in update]
        update = set(update)
        userIn = []
        for element in update:
            newIn = input(f"What would you like the new {element} to be:")
            userIn.append(newIn)

        newInput = dict(zip(update, userIn))

        update_row(choice, newInput, where)

    elif action == 4:
        print('\nYou chose to Delete')
        print('1)Delete a table\n2)Delete an entry in a table')
        create_action = choose(1, 2)

        if create_action == 1:
            print_tables()
            table = input('Which table would you like to delete: (type exact name)')
            sql = f"DROP TABLE {table}"
            controller.execute(sql)
            NetflixDB.commit()
            print('Deleted Successfully!')

        elif create_action == 2:
            print_tables()
            choice = input('Which table would you like to delete from?(type the exact name)')
            show_table(choice)
            row = input('Which row would you like to delete?(select the ID)')
            match choice:
                case "movie":
                    where = "MID = " + row
                case "people":
                    where = "PID = " + row
                case "characters":
                    where = "CID = " + row
                case "genre":
                    where = "GID = " + row
                case "rating":
                    where = "RID = " + row
                case "series":
                    where = "SID = " + row
            delete_row(choice, where)











controller.close()
NetflixDB.close()
print('Thanks for using, your session has now ended!')


















