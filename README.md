# AIBE Coffee List App

Welcome to the AIBE Coffee List App! This app allows you to manage your coffee list, track consumption and debt, and make payments seamlessly. Built with Kivy for a touch-friendly interface.

## Getting Started

1. Make sure you have Python 3.9+ installed on your machine.
2. Clone this repository to your local machine.
3. Navigate to the project directory.
4. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

5. Initialize the database:

    ```bash
    cd tools
    python init_database.py
    ```

6. Run the app:

    ```bash
    python main.py
    ```

## Features

- **User management**: Create new users with first name, last name, and lab affiliation. Existing users with incomplete profiles are prompted to complete them.
- **Coffee tracking**: Select from available coffee products, track consumption over a two-week rolling window, and view a ranked leaderboard.
- **Debt tracking**: Per-user debt accumulates with purchases and is displayed on the main screen. Users with high debt receive payment reminders.
- **Cleaning credits**: Users earn score credits for cleaning tasks, which factor into leaderboard ranking.
- **Contributions**: Record contributions via QR code payment flow.
- **Screensaver & black screen**: Auto-activates after periods of inactivity.

## Project Structure

- `backend/` — Data manager for SQLite database operations (users, consumption, cleaning, debt).
- `database/` — SQLite database file.
- `frontend/` — Kivy screens:
  - `main_screen.py` — User leaderboard with alphabet filter, ranked user buttons, and navigation.
  - `new_user_screen.py` — New user creation form with on-screen keyboard and lab selection.
  - `user_profile_screen.py` — Profile completion form for existing users missing first/last name or lab.
  - `select_coffee_screen.py` — Coffee product selection.
  - `payment_screen.py` — Payment and debt management.
  - `cleaning_screen.py` — Cleaning task logging.
  - `contribute_screen.py` — Contribution flow.
  - `screensaver_screen.py` — Screensaver on inactivity.
  - `black_screen.py` — Black screen after extended inactivity.
- `widgets/` — Reusable UI components (e.g. goose overlay).
- `assets/` — Images and static assets.
- `tools/` — Database initialization and utility scripts.
- `products.json` — Coffee product definitions.
- `cleaning.json` — Cleaning task definitions.

## Contributing

We welcome contributions to the AIBE Coffee List App! If you have any ideas, bug reports, or feature requests, please feel free to open an issue or submit a pull request.
