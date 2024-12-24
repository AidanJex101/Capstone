import sqlite3
import datetime
import csv
import bcrypt


date = datetime.date.today().strftime("%Y-%m-%d")
connection = sqlite3.connect("CompetencyTracker.db")
cursor = connection.cursor()

with open("create_tables.txt", "r") as readfile:
  cursor.executescript(readfile.read())

def search_a_user():
  user_input = input("Please enter a first or last name of the user you wish to search for:\n<>")
  user_tuple = (f"%{user_input}%", f"%{user_input}%")
  query = "SELECT * FROM Users WHERE first_name LIKE ? or last_name LIKE ?"
  lines = cursor.execute(query, user_tuple).fetchall()
  for line in lines:
    print(line)
    print(f"\nUser ID: {line[0]}\nFirst name: {line[1]}\nLast name: {line[2]}\nPhone:{line[3]}\nEmail:{line[4]}\nActive Status: {line[5]}\nUser Type: {line[6]}\nHire Date: {line[7]}\n")

def add_user():
  try:
    user_first = input("Enter a first name: ")
    user_last = input("Enter a last name: ")
    user_phone = input("Enter a phone number: ")
    user_email = input("Enter a email: ")
    user_password = input("Enter a password: ")
    salt = bcrypt.gensalt()
    bytes = user_password.encode("utf-8")
    hashed_password = bcrypt.hashpw(bytes, salt)

    hire_date = date
    user_tuple = (user_first, user_last, user_phone, user_email, hashed_password, hire_date)
    query = "INSERT INTO Users (first_name, last_name, phone, email, password, hire_date) VALUES (?, ?, ?, ?, ?, ?)"
    cursor.execute(query, user_tuple)
    connection.commit()
    print("User " + user_first + " was added to the Users table")
  except:
    print("User could not be added to the database, please try entering valid values for the form!")

def add_competency():
  try:
    user_name = input("Enter Competency Name: ")
    user_tuple = (user_name, date)
    query = "INSERT INTO Competencies (name, date_created) Values (?, ?)"
    cursor.execute(query, user_tuple)
    connection.commit()
    print("Competency " + user_name + " Created")
  except:
    print("Competency could not be added, please try again!")

def add_assessment():
  lines = cursor.execute("SELECT * FROM competencies").fetchall()
  for line in lines:
    print(f"Competency ID: {line[0]} Competency Name: {line[1]} Date Created: {line[2]}\n")
  try:
    user_competency_id = input("Enter a competency ID to add the assessment to: ")
    user_name = input("Enter assessment name: ")
    user_tuple = (user_competency_id, user_name, date)
    query = "INSERT INTO Assessments (competency_id, name, date_created) Values (?, ?, ?)"
    cursor.execute(query, user_tuple)
    connection.commit()
    print("Assessment Added")
  except:
    print("Assessment could not be added, please try a different competency id!")

def add_assessment_result():
  try:
    user_assessment = input("Enter an assessment ID: ")
    user_user_id = input("Enter User ID: ")
    manager_id = 0
    user_score = input("Enter a score for user: (1-4) ")
    user_tuple = (user_user_id, user_assessment, manager_id, user_score, date)
    query = "INSERT INTO AssessmentResults (user_id, assessment_id, manager_id, score, date_taken) VALUES (?, ?, ?, ?, ?)"
    cursor.execute(query, user_tuple)
    connection.commit()
    print("Result Added\n")
  except:
    print("Result could not be added, please try again later!")

def import_assessment_results_csv(user_id, assessment_id, score, date_taken):
    manager_id = 0
    user_tuple = (user_id, assessment_id, manager_id, score, date_taken)
    query = "INSERT INTO AssessmentResults (user_id, assessment_id, manager_id, score, date_taken) VALUES (?, ?, ?, ?, ?)"
    cursor.execute(query, user_tuple)
    connection.commit()

def edit_user():
  try:
    user_user_id = input("Enter user ID you wish to edit: ")
    user_first = input("Enter new first name: ")
    user_last = input("Enter new last name: ")
    user_phone = input("Enter new phone number: ")
    user_email = input("Enter new email: ")
    user_password = input("Enter new password: ")
    salt = bcrypt.gensalt()
    bytes = user_password.encode("utf-8")
    hashed_password = bcrypt.hashpw(bytes, salt)
    user_active = input("Enter new active status: ")
    user_type = input("Enter new user type: ")
    hire_date = input("Enter new hire date: ")
    user_tuple = (user_first, user_last, user_phone, user_email, hashed_password, user_active, user_type, hire_date, user_user_id)
    query = "UPDATE Users SET first_name = ?, last_name = ?, phone = ?, email = ?, password = ?, active = ?, user_type = ?, hire_date = ?) WHERE user_id = ?"
    cursor.execute(query, user_tuple)
    connection.commit()
    print("User " + user_first + " was edited in the Users table")
  except:
    print("User could not be edited, please try again!")

def edit_competency():
  try:
    user_competency = input("Enter a competency ID: ")
    user_name = input("Enter new competency name: ")
    user_date = input("Enter new creation date: ")
    user_tuple = (user_name, user_date, user_competency)
    query = "UPDATE Competencies SET name = ?, date_created = ? WHERE competency_id = ?"
    cursor.execute(query, user_tuple)
    connection.commit()
    print("Competency has been edited")
  except:
    print("Competency could not edited, please try again!")

def edit_assessment():
  try:
    user_assessment = input("Enter assessment ID: ")
    user_name = input("Enter new assessment name: ")
    user_date = input("Enter new assessment creation date: ")
    user_tuple = (user_name, user_date, user_assessment)
    query = "UPDATE Assessments SET name = ?, date_created = ? WHERE assessment_id = ?"
    cursor.execute(query, user_tuple)
    connection.commit()
    print("Assessment has been edited")
  except:
    print("Assessment could not be edited, please try again")

def edit_assessment_result():
  try:
    user_user_id = input("Enter user ID: ")
    user_assessment = input("Enter assessment ID: ")
    user_manager = input("Enter new manager ID: ")
    user_score = input("Enter new score: ")
    user_date = input("Enter new date taken: ")
    user_tuple = (user_manager, user_score, user_date, user_user_id, user_assessment)
    query = "UPDATE AssessmentResults SET manager_id = ?, score = ?, date_taken = ? WHERE user_id = ? and assessment_id = ?"
    cursor.execute(query, user_tuple)
    connection.commit()
    print("Assessment Result has been edited")
  except:
    print("Assessment result could not be edited, please try again!")

def delete_assessment_result():
  try:
    user_user_id = input("Enter user ID: ")
    user_assessment = input("Enter assessment ID: ")
    user_tuple = (user_user_id, user_assessment)
    query = "DELETE FROM AssessmentResults WHERE user_id = ? and assessment_id = ?"
    cursor.execute(query, user_tuple)
    connection.commit()
    print("Assessment Result has been deleted")
  except:
    print("Assessment result could not be deleted, please try again!")

def view_all_assessment_data():
  user_assessment = input("Enter Assessment ID: ")
  query = "SELECT user_id, score FROM AssessmentResults WHERE competency_id = ? ORDER BY user_id"
  lines = cursor.execute(query, user_assessment).fetchall()
  print("Results for Assessment " + user_assessment)
  for line in lines:
    print(f"User ID: {line[0]} Score: {line[1]}")

def view_all_users():
  query = "SELECT * FROM Users"
  lines = cursor.execute(query).fetchall()
  for line in lines:
    print(line)
    print(f"\nUser ID: {line[0]}\nFirst name: {line[1]}\nLast name:{line[2]}\nPhone:{line[3]}\nEmail:{line[4]}\nActive: {line[5]}\nUser Type: {line[6]}\nHire Date: {line[7]}\n")

def view_specific_assessment_data():
  user_user_id = input("Enter the user ID you would like to view: ")
  query = "SELECT AssessmentResults.user_id, AssessmentResults.assessment_id, Assessments.competency_id, AssessmentResults.score FROM AssessmentResults FULL OUTER JOIN Assessments ON AssessmentResults.assessment_id = Assessments.assessment_id WHERE user_id = ? ORDER BY Assessments.competency_id"
  lines = cursor.execute(query, user_user_id).fetchall()
  for line in lines:
    print(f"User ID: {line[0]} Competency ID: {line[2]}, Assessment ID: {line[1]} Score: {line[3]}")

def view_specific_assessments_taken():
  user_user_id = input("Enter the user ID you would like to view: ")
  query = "SELECT AssessmentResults.assessment_id, Assessments.competency_id, Assessments.name FROM AssessmentResults FULL OUTER JOIN ON AssessmentResults.assessment_id = Assessments.assessment_id WHERE user_id = ? ORDER BY Assessments.competency_id"
  lines = cursor.execute(query, user_user_id).fetchall()
  for line in lines:
    print(f"Competency ID: {line[1]} Assessment ID: {line[0]} Name: {line[2]}")


def import_assessment_results():
  user_file = input("Enter CSV File name to import (include the extension): ")
  with open(user_file, 'r') as csvfile:
    csv_dict_reader = csv.DictReader(csvfile)
    for row in csv_dict_reader:
      import_assessment_results_csv(row["user_id"], row["assessment_id"], row["score"], row["date_taken"])
  print("Import Complete")


def export_assessment_results():
  try:
    user_competency = input("Enter Competency ID: ")
    user_file_name = input("Enter name for file (do not include file extension): ")
    query = "SELECT ar.user_id, c.name, a.competency_id, ar.score, MAX(ar.date_taken) FROM Users u LEFT JOIN AssessmentResults ar on u.user_id = ar.user_id LEFT JOIN Assessments a on ar.assessment_id = a.assessment_id LEFT JOIN Competencies c on a.competency_id = c.competency_id  WHERE c.competency_id = ? GROUP BY u.user_id, u.first_name, u.last_name, c.name"
    new_rows = [["user_id", "competency_name", "competency_id", "score", "date_taken"]]
    lines = cursor.execute(query, user_competency).fetchall()
    
    rows = []
    for line in lines:
      rows.append(line)

    query = "SELECT user_id FROM Users"
    lines = cursor.execute(query).fetchall()
    user_ids = []
    for line in lines:
      user_ids.append(line[0])
    
    for row in rows:
      if row[0] in user_ids:
        user_ids.pop(user_ids.index(row[0]))
    
    query = "SELECT name FROM Competencies WHERE competency_id = ?"
    competency_name_tuple = cursor.execute(query, user_competency).fetchone()
    competency_name = competency_name_tuple[0]


    for id in user_ids:
      score = 0
      date_taken = "Not taken"
      null_row = (id, competency_name, user_competency, score, date_taken)
      rows.append(null_row)

    total = 0
    part = 0
    for row in rows:
      total += 1
      part += row[3]
      new_rows.append(row)
    average = part / total
    new_rows.append(("Competency Average:", average))

    with open((user_file_name + ".csv"), "w") as output_file:
      write = csv.writer(output_file)
      write.writerows(new_rows)
  except:
    print("Competency results not found, please try again!")


def export_user_competency():
  try:
    user_id = input("Enter User ID: ")
    user_file_name = input("Enter name for file (do not include file extension): ")
    query = "SELECT ar.user_id, u.email, c.name, c.competency_id, ar.score, ar.date_taken FROM Competencies c LEFT JOIN Assessments a on  c.competency_id = a.competency_id LEFT JOIN AssessmentResults ar on a.assessment_id = ar.assessment_id AND ar.user_id = ? LEFT JOIN Users u on ar.user_id = u.user_id ORDER BY a.competency_id"
    lines = cursor.execute(query, user_id).fetchall()
    
    rows = []
    for line in lines:
      rows.append(line)

    query = "SELECT competency_id FROM Competencies"
    lines = cursor.execute(query).fetchall()
    compentency_ids = []
    for line in lines:
      compentency_ids.append(line[0])

    new_rows = [["user_id", "email", "competency_name", "competency_id", "score", "date_taken"]]

    for id in compentency_ids:
      staged_row = []
      for row in rows:
        row = list(row)
        if not row[5]:
          row[5] = "1000-01-01"
        print(type(row[5]))
        if row[3] == id and not staged_row:
            staged_row = row 
        if row[3] == id and staged_row != row: 
          print(staged_row[5])
          date1 = datetime.datetime.strptime(staged_row[5], "%Y-%m-%d")
          date2 = datetime.datetime.strptime(row[5], "%Y-%m-%d")
          if date2 > date1:
            staged_row = row
      new_rows.append(staged_row)
    
    user_email = ""
    query = "SELECT email FROM Users WHERE user_id = ?"
    email_tuple = cursor.execute(query, user_id).fetchone()
    user_email = email_tuple[0]

    part = 0
    total = 0
    for row in new_rows:
      if row[4] != "score":
        if row[5] == "1000-01-01":
          row[5] = "Not Taken"
          row[0] = user_id
          row[4] = 0
          row[1] = user_email
        total += 1
        part += row[4]
    average = part / total
    new_rows.append(["User average:", average])


    with open((user_file_name + ".csv"), "w") as output_file:
      write = csv.writer(output_file)
      write.writerows(new_rows)
  except:
    print("Competency data could not be found, please try again!")

def add_menu():
  print("ADD MENU")
  print("(0) Add a user")
  print("(1) Add a Compentency") 
  print("(2) Add an assessment to a Competency")
  print("(3) Add an assessment result for a user")
  print("(Q) Quit")
  user_menu_choice = input("<> ")
  match user_menu_choice:
    case "0":
      add_user()
    case "1":
      add_competency()
    case "2":
      add_assessment()
    case "3":
      add_assessment_result()
    case "Q":
      print("You have exited the add menu")
    case _:
      print("Thats not a valid option")
  
def edit_menu():
  print("EDIT MENU")
  print("(0) Edit a user")
  print("(1) Edit a Compentency")
  print("(2) Edit a assessment")
  print("(3) Edit an assessment result for a user")
  user_menu_choice = input("<> ")
  match user_menu_choice:
    case "0":
      add_user()
    case "1":
      add_competency()
    case "2":
      add_assessment()
    case "3":
      add_assessment_result()
    case "Q":
      print("You have exited the add menu")
    case _:
      print("Thats not a valid option")

def manager_menu():
  while True:
    print("\n********** Manager Menu **********\n")
    print("(0)  View all users")
    print("(1)  Search a User")
    print("(2)  View Assessment Data for all users")
    print("(3)  View Compentency Report")
    print("(4)  View Assessment Data for a specific User")
    print("(5)  Add Menu")
    print("(6)  Edit Menu")
    print("(7)  Delete Assessment Result")
    print("(8)  Export to CSV")
    print("(9)  Import from CSV")
    print("(Q)  Quit\n")

    user_menu_choice = input("{ ")

    match user_menu_choice:
      case "0":
        view_all_users()
      case "1":
        search_a_user()
      case "2":
        view_all_assessment_data()
      case "3":
        view_specific_assessment_data()
      case "4":
        view_specific_assessments_taken()
      case "5":
        add_menu()
      case "6":
        edit_menu()
      case "7":
        delete_assessment_result()
      case "8":
        export_menu()
      case "9":
        import_assessment_results()
      case "Q":
        break
      case _:
        print("Thats not a valid option")

def user_menu():
  return

def login_menu():
  while True:
    logged_in = False
    

    query = "SELECT email, password, user_type, user_id FROM Users"
    lines = cursor.execute(query).fetchall()
    
    
    print("\n***Log In Menu***\n")
    username = input("Enter your User ID: ")
    password = input("Enter your Password: ")
    user_bytes = password.encode("utf-8")
    for line in lines:
      if bcrypt.checkpw(user_bytes, line[1]) and username == line[0]:
        logged_in_id = line[3] 
        if line[2] == "manager":
          manager_menu()
        else:
          user_menu()
        logged_in = True
        break
    if not logged_in:
      print("Incorrect username or password, please try again!")

def export_menu():
    print("Export Menu")
    print("(1) Export User Competency Summary")
    print("(2) Export Competency Results Summary")

    user_input = input(">>> ")

    match user_input:
      case "1":
        export_user_competency()
      case "2":
        export_assessment_results()
      case __:
        print("That is not a valid entry, please try again!")
    

manager_menu()