import mysql.connector
import customtkinter
import bcrypt
from PIL import Image

# Connect to MySQL database
mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="pass_manage"
)

# Default theme settings
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

# Initialize root window
root = customtkinter.CTk()

# Function to switch between frames
def show_frame(frame, title, size):
    root.title(title)
    root.geometry(size)
    frame.tkraise()


# function to handle account creation, does 2 things; insert account info into database, send user back to login page
def create_account():
    #get user and pass
    username = new_user_entry.get()
    password = new_pass_entry.get()

    # encrypt password using bcrypt
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash_pass = bcrypt.hashpw(bytes, salt)

    # Check for duplicate username in the database
    mycursor = mydb.cursor()
    mycursor.execute("SELECT COUNT(*) FROM users WHERE username = %s", (username,))
    result = mycursor.fetchone()

    # If username exists, show error message
    if result[0] > 0:
        # You can display an error message to the user using a label or pop-up
        account_error_label.configure(text="Username already exists. Try another one.", text_color="red")
        return


    #insert user and new hashed pass using bcrypt into database
    mycursor = mydb.cursor()
    sql = "INSERT INTO users (username, masterpass) VALUES (%s, %s)"
    val = (username, hash_pass)
    mycursor.execute(sql, val)

    mydb.commit()

    show_frame(login_frame, "Login", '300x400')


def login_account():
    # Get entered username and password
    username = user_entry.get()
    password = pass_entry.get()

    # Retrieve the hashed password for the entered username
    mycursor = mydb.cursor()
    sql = "SELECT masterpass FROM users WHERE username = %s"
    mycursor.execute(sql, (username,))
    result = mycursor.fetchone()
    
    # Check if username exists in the database
    if result:
        stored_hashed_password = result[0]

        # Compare the entered password with the hashed password in the database
        if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
            login_error_label.configure(text="Login Succesful", text_color="green")
            show_frame(home_frame, "Password Manager", '1280x720')
        else:
            login_error_label.configure(text="Incorrect password", text_color="red")
    else:
        login_error_label.configure(text="Username not found", text_color="red")

def toggle_pass(entry_widget, image_label):
    current_show = entry_widget.cget("show")
    if current_show == "*":
        entry_widget.configure(show="")
        image_label.configure(image=eye_open_image)
    else:
        entry_widget.configure(show="*")
        image_label.configure(image=eye_closed_image)

# === Login Page Frame ===
login_frame = customtkinter.CTkFrame(root)
login_frame.place(relwidth=1, relheight=1)

# Username label and entry
user_frame = customtkinter.CTkFrame(login_frame)
user_frame.pack(pady=(50, 10), padx=(0, 28))

user_label = customtkinter.CTkLabel(user_frame, text="Username:")
user_label.pack(side="left", padx=5)

user_entry = customtkinter.CTkEntry(user_frame)
user_entry.pack(side="right", padx=5)

# Password label and entry
pass_frame = customtkinter.CTkFrame(login_frame)
pass_frame.pack(pady=10)

pass_label = customtkinter.CTkLabel(pass_frame, text="Password:")
pass_label.pack(side="left", padx=5)

#preload images
eye_open_image = customtkinter.CTkImage(dark_image=Image.open("eye_open.png",), size=(20, 20))
eye_closed_image = customtkinter.CTkImage(dark_image=Image.open("eye_closed.png"), size=(20, 20))

pass_entry = customtkinter.CTkEntry(pass_frame, show="*")
pass_entry.pack(side="left", padx=5)

#orignally eye closed
image_label = customtkinter.CTkLabel(pass_frame, image=eye_closed_image, text="")
image_label.pack(side="right", padx=5)

# Bind the label click event to toggle password visibility
image_label.bind("<Button-1>", lambda e: toggle_pass(pass_entry, image_label))

# Error label for login
login_error_label = customtkinter.CTkLabel(login_frame, text="", font=("Arial", 12))
login_error_label.pack(pady=(10, 20))

# Login button
login_button = customtkinter.CTkButton(login_frame, text="Login", command=login_account)
login_button.pack()

# bind enter key so user doesnt have to hit the login button everytime
user_entry.bind('<Return>', lambda event: login_account())
pass_entry.bind('<Return>', lambda event: login_account())

# Button to navigate to the Create Account page
create_button = customtkinter.CTkButton(
    login_frame, text="Create Account", fg_color="red", hover_color="indian red",
    command=lambda: show_frame(create_account_frame, "Account Creation", '300x400')
)
create_button.pack(pady=(10, 0))

# === Create Account Page Frame ===
create_account_frame = customtkinter.CTkFrame(root)
create_account_frame.place(relwidth=1, relheight=1)

# Labels and entries for creating a new account
new_user_label = customtkinter.CTkLabel(create_account_frame, text="New Username:")
new_user_label.pack(pady=(50, 0))

new_user_entry = customtkinter.CTkEntry(create_account_frame)
new_user_entry.pack()

new_pass_label = customtkinter.CTkLabel(create_account_frame, text="New Password:")
new_pass_label.pack(pady=(10, 0))

new_pass_entry = customtkinter.CTkEntry(create_account_frame, show="*")
new_pass_entry.pack()

# Error label for account creation
account_error_label = customtkinter.CTkLabel(create_account_frame, text="", font=("Arial", 12))
account_error_label.pack(pady=(10, 20))

# Button to go back to the login page
back_button = customtkinter.CTkButton(
    create_account_frame, text="Back to Login",
    command=lambda: show_frame(login_frame, "Login", '300x400')
)
back_button.pack(pady=(20, 0))

# Button to submit new account details
submit_button = customtkinter.CTkButton(create_account_frame, text="Create Account", fg_color="red", hover_color="indian red", command=create_account)
submit_button.pack(pady=10)


# =====main home frame ==============

# === Create Account Page Frame ===
home_frame = customtkinter.CTkFrame(root)
home_frame.place(relwidth=1, relheight=1)

home_label = customtkinter.CTkLabel(home_frame, text="Hello World!")
home_label.pack()


# Start by showing the login frame
show_frame(login_frame, "Login", '300x400')

# Start main loop
root.mainloop()