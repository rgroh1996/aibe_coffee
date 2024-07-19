# AIBE Coffee List App

Welcome to the AIBE Coffee List App! This app allows you to manage your coffee list and make payments seamlessly.

## Getting Started

To start the app, follow these steps:

1. Make sure you have Python 3.9 installed on your machine.
2. Clone this repository to your local machine.
3. Navigate to the project directory.
4. Install the required dependencies by running the following command:

    ```bash
    pip install -r requirements.txt
    ```

5. Initialized the database

    ```bash
    cd tools 
    python init_database.py
    ```

6. Run the following command to start the app without logging voltage (-- to seperate kivy args):

    ```bash
    python main.py -- --noshelly
    ```

## Project Structure

The project is organized into the following folders:

- `backend`: Contains the data manager module responsible for managing coffee data.
- `database`: Contains the SQLite database used to store coffee information.
- `tools`: Contains scripts and notebooks for database initialization and inspection.
- `frontend`: Contains the different screens of the app, including the main screen, new user screen, select coffee screen, and payment screen.

## Contributing

We welcome contributions to the AIBE Coffee List App! If you have any ideas, bug reports, or feature requests, please feel free to open an issue or submit a pull request. We appreciate your help!
