# Your final assignment is about creating a register / login functionality to your app.
# You need to also associate each todo item created in the database with the corresponding logged-in user.
# For storing and retrieving the users you ARE REQUIRED TO USE SQLAlchemy. if not using SQLAlchemy, then the whole assignment will give you a direct fail (0 points).

# What you need to do:
# First, create table for holding users. Class model should be called 'User' and name of the table should be 'users'.
#   The users table should have at least the fields userId, username and password.
#   Make sure that you also have foreign key relationship between the items and users tables and relationship created from both tables into each another.
# Before your main application launches, it should ask the user if they want to REGISTER or LOGIN
#   If user wants to REGISTER, the application should then ask the user for the username and password combination
#      If user with this username already exists in the table users, app should notify about that and not create the new user
#      If this username did not exist, create account for the user in the table users
#   If user wants to LOGIN, then you need to ask user the username and password
#      If the given username and password combination does not exist in the table users, then inform user about this and do not allow user into the system
#      If this username and password combination exists in the table users, then allow the user in the system and store the user that logged in
# Finally, you will also need to associate each item created with the logged-in user. This way each logged-in user will have their own todo items.

import sys
from database import User,Item,UserItem,session

#user register
def askUser():
  while True:
      print("\nREGISTER or LOGIN")
      print("1: REGISTER")
      print("2: LOGIN")
      print("3: Exit\n")
      selection = input()
      if (selection == "1"): register()
      elif (selection == "2"): login()
      elif (selection == "3"): sys.exit("Goodbye!")

#register
def register():
  print("Please input username and password!")
  userName = input()
  password = input()
  newUser = User(username = userName,password = password)
  exists = session.query(User).filter(User.username == userName).first()
  if exists is not None:
    print("Username already exists!") 
  else: 
    session.add(newUser)
    session.commit()
  
#login
def login():
  print("Please input username and password!")
  userName = input()
  password = input()
  username_exists = session.query(User).filter(User.username == userName, User.password == password).first()
  print(username_exists)
#check name exists
  if username_exists:
    print("Login Succeed!")
    main(userName)
     
  else:
    print("Username or Password Error!")

  

# Main app function
def main(userName):
  while True:
      print("\nWhat do you want to do today?")
      print("1: View todo items")
      print("2: Create new todo item")
      print("3: Remove item")
      print("4: Exit\n")
      selection = input()
      if (selection == "1"): showItems(userName)
      elif (selection == "2"): createItem(userName)
      elif (selection == "3"): removeItem(userName)
      elif (selection == "4"): sys.exit("Goodbye!")

# Lists all todo items
def showItems(userName):
  print("\nYour todo lists:")
  print("---")
  user = session.query(User).filter( User.username == userName ).first()
  for item in user.items:
    print(item.itemId, ": " + item.name)
  print("---\n")
  

# Creates new todo item
def createItem(userName):
  global items
  print("Name for the item:")
  itemName = input()
  users = session.query(User).filter(User.username == userName, ).first()
  users.items.append(Item( name = itemName ))
  session.commit()

# Removes todo item with ID
def removeItem(userName):
  itemAmount = session.query(Item).count()

  if (itemAmount < 1):
    print("You should add some items first.")
    return
  
  print("Give ID:")
  itemId = int(input())
  removableItem = session.query(Item).filter(Item.name == itemId).first()
  users = session.query(User).filter( User.username == userName ).first()
                
 

  if (removableItem.count() > 0):
    users.items.remove(removableItem)
    session.commit()
  else:
    print("Invalid ID!")


    

# Start the app
print("Welcome to TOD-O LIST O-MAKER Version 5123.524")
askUser()

