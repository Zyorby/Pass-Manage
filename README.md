# Password Manager App

A simple yet secure password manager built with Python and **CustomTkinter** for the UI. This application allows users to store their account names and passwords in a local MySQL database with bcrypt and AES encryption for added security.

## Features

- **Account Management**: Add, view, and manage accounts and their passwords.
- **Secure Storage**: Passwords are securely encrypted using bcrypt and AES before being stored in the database.
- **Dynamic UI**: The accounts and passwords are displayed in a dynamic, table-like format using CustomTkinter.
- **Database Integration**: MySQL database is used to store account information and passwords securely.
- **Lockout Mechanism**: The application has an integrated lockout mechanism to prevent unauthorized access.

## Technologies Used

- **Python**: The programming language used to build the application.
- **CustomTkinter**: For creating modern and customizable GUI elements.
- **MySQL**: For securely storing user data.
- **bcrypt**: For securely hashing and encrypting passwords.

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/password-manager.git
    ```

2. **Navigate into the project directory**:
    ```bash
    cd password-manager
    ```

3. **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

   Ensure you have **MySQL** installed and running. You will need to set up your MySQL database with the necessary tables. A basic setup might look like:

   ```sql
   -- Users table
    CREATE TABLE users (
        username VARCHAR(255) PRIMARY KEY,
        masterpass VARCHAR(60)
    );
    
    -- Passwords table
    CREATE TABLE passwords (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255),
        account_name VARCHAR(255),
        password_hash VARCHAR(60),
        FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE
    );
