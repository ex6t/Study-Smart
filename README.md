# Study-Smart

## Overview

**Study Smart** is a desktop study application built with **Python**, **PyQt6**, and **SQLite**. The goal of the project is to give students one place to organize their study materials instead of constantly switching between different apps.

The application allows users to create an account, log in securely, manage notes, create flashcards, take quizzes, and view their study progress through an easy-to-use interface. Since this project was completed during a short summer semester, we focused on building a clean, functional application with a solid foundation that can easily be expanded in the future.

---

## Features

- User registration and login
- Secure account authentication using SQLite
- Dashboard with quick navigation
- Create, edit, view, and delete notes
- Import notes from text files
- Flashcard management
- Quiz management
- Built in pomodoro timer
- Study checklist
- Modern desktop interface built with PyQt6

---

## Technologies Used

- Python 3
- PyQt6
- SQLite3
- Git & GitHub
- Trello (for ticketing)
- Agile SCRUM

---

## Team Workflow

Our team followed an Agile Scrum workflow throughout the project.

At the beginning of each sprint, we met to decide which features needed to be completed and created Trello cards for each task. Each team member worked on their own feature branch so multiple features could be developed at the same time without interfering with each other's work.

Once a feature was finished, it was pushed to GitHub and reviewed before being merged into the main branch. Throughout development we regularly tested the application together to make sure new features worked correctly with the existing code.

---

## Project Structure
```bash
Study-Smart/
|
|- main.py
|
|-- tests/
|
|-- app/
|   |-- database/
|   |-- screens/
|   |-- widgets/
```
---

## Running the Project

### 1. Clone the repository

```bash
git clone https://github.com/ex6t/Study-Smart.git
```

### 2. Open the project folder

```bash
cd Study-Smart
```

### 3. Install the required libraries

```bash
pip install PyQt6
```

### 4. Run the application

```bash
python3 main.py
```

On Windows you may need to use:

```bash
python main.py
```

### 5. (Optional) Install PyInstaller
```bash
pip install -U pyinstaller
```

### 6. Build a standalone executable
```bash
python -m PyInstaller --windowed --name "Study Smart" main.py
```

The built executable will be in the 'dist/' folder.

---

## Git Workflow

```bash
git pull origin main
git switch -c username/feature-name

# Make your changes

git add .
git commit -m "Describe your changes"
git push -u origin username/feature-name
```

After testing, a Pull Request was created and merged into the main branch.

---

## Future Improvements

- AI-generated study recommendations
- PDF note importing
- Study timers
- Quiz Performance and Study Metrics
- Cloud synchronization
- Password recovery / security
- Dark mode

---

## Developers

- Joshua Padilla
- Kevin Davis
- Keith Palmer
- Devin Cullen
