# 📝 Python To-Do App

A lightweight To-Do application in Python that stores tasks in a JSON file.

---

## 📂 Project Structure
- **Task**: Represents a single to-do item (`id`, `title`, `description`, `completionStatus`).
- **TaskManager**: Handles CRUD operations and persistence.
  - Add, list, update, complete, delete tasks
  - Save/load tasks from `todos.json`
- **todos.json**: JSON file for persistent storage.

---

## ⚙️ Features
- Create, read, update, delete tasks
- Mark tasks complete/incomplete
- Interactive menu for easy management
- JSON-based storage for persistence

---

## 🚀 Getting Started
### Prerequisites
- Python 3.x

### Installation
```bash
git clone https://github.com/bekam-bit/Django-gdg-project.git
cd Django-gdg-project
```
### Run
```bash
python Task.py
```
### 📖 Usage
When you run the app, you’ll see a simple menu:</br>
``` bash
==== To-Do Menu ====
1. Add Task
2. List Tasks
3. Update Task
4. Mark Task Complete/Incomplete
5. Delete Task
6. Exit
====================
```
✅ Add Task → Enter a title and description, ID is assigned automatically.

✅ List Tasks → Shows all tasks with status (✅ Completed / ⏳ Pending).

✅ Update Task → Edit title or description.

✅ Mark Task → Toggle completion status.

✅ Delete Task → Remove a task permanently.

✅ Exit → Saves changes to todos.json and closes the program.

All changes are stored in todos.json, so tasks persist between runs.

### 🛠️ Future Work
CLI enhancements (subcommands, filters)

Task editing/deletion improvements

Due dates & priorities

Simple GUI

### 📜 License
This project is licensed under the MIT License – feel free to use and modify it.


