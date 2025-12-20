import json
import os

fileName="todos.json"

class Task:
    def __init__(self,id,title,description,completionStatus):
        self.id=id
        self.title=title
        self.description=description
        self.completionStatus=completionStatus
    
    def to_dict(self):
        return {
            "id":self.id,
            "title":self.title,
            "description": self.description,
            "completionStatus":self.completionStatus
        }

    @classmethod
    def from_dict(cls,data):
        return cls(data["id"],data["title"],data["description"],data.get("completionStatus",False))

class TaskManager:
    def __init__(self):
        self.tasks=[]
    def loadTasks(self):
        if os.path.exists(fileName):
            with open(fileName,"r") as file:
                data=json.load(file)
                self.tasks=[Task.from_dict(d) for d in data]
    def saveTasks(self):
        with open(fileName,"w") as file:
            json.dump([task.to_dict() for task in self.tasks],file,indent=4)
    
    def addTask(self,title,description):
        self.loadTasks()
        task_id=len(self.tasks)+1
        new_task=Task(task_id,title,description,completionStatus=False)
        self.tasks.append(new_task)
        self.saveTasks()
        print(f"Task '{title}' added succesfully")
    
    def viewTasks(self):
        self.loadTasks()
        if not self.tasks:
            print("No tasks found")
            return
        for task in self.tasks:
            status="Done" if task.completionStatus else "Pending"
            print(f"Id: {task.id} Title: {task.title} Status: {status} Description: {task.description}")
            
    
    def mark_complete(self, task):
        task.completionStatus = True
        self.saveTasks()
        print(f"Task '{task.title}' marked as Done!")

    def mark_pending(self, task):
        task.completionStatus = False
        self.saveTasks()
        print(f"Task '{task.title}' marked as Pending!")

    # Helper to find task by ID
    def get_task_by_id(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def updateTasks(self, task_id):
        task = self.get_task_by_id(task_id)
        if not task:
            print(f"Task {task_id} not found")
            return

        # Update title
        new_title = input(f"Enter new title (leave blank to keep '{task.title}'): ")
        if new_title.strip():
            task.title = new_title

        # Update description
        new_description = input(f"Enter new description (leave blank to keep '{task.description}'): ")
        if new_description.strip():
            task.description = new_description

        # Update completion using professional methods
        status_input = input(f"Mark task as complete? (yes/no, current: {'Done' if task.completionStatus else 'Pending'}): ").lower()
        if status_input in ["yes", "y"]:
            self.mark_complete(task)
        elif status_input in ["no", "n"]:
            self.mark_pending(task)
        else:
            # Save any other changes if completion status unchanged
            self.saveTasks()
            print(f"Task {task_id} updated (completion unchanged)")

        print(f"Task {task_id} updated successfully!")

    
    def deleteTask(self,task_id):
        if not self.tasks:
            print("No tasks found")
            return
        for i, task in enumerate(self.tasks):
            if task_id == task.id:
                removed=self.tasks.pop(i)
                self.saveTasks()
                print(f"Task '{removed.title}' removed!")
                return
        print("task not found")

def main():
    manager = TaskManager()

    while True:
        print("\n===== TODO App Menu =====")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Mark Task as Complete")
        print("6. Mark Task as Pending")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            title = input("Enter task title: ")
            description = input("Enter task description: ")
            manager.addTask(title, description)

        elif choice == "2":
            manager.viewTasks()

        elif choice == "3":
            manager.viewTasks()
            try:
                task_id = int(input("Enter task ID to update: "))
                manager.updateTasks(task_id)
            except ValueError:
                print("Please enter a valid number.")

        elif choice == "4":
            manager.viewTasks()
            try:
                task_id = int(input("Enter task ID to delete: "))
                manager.deleteTask(task_id)
            except ValueError:
                print("Please enter a valid number.")

        elif choice == "5":
            manager.viewTasks()
            try:
                task_id = int(input("Enter task ID to mark as complete: "))
                task = manager.get_task_by_id(task_id)
                if task:
                    manager.mark_complete(task)
                else:
                    print("Task not found")
            except ValueError:
                print("Please enter a valid number.")

        elif choice == "6":
            manager.viewTasks()
            try:
                task_id = int(input("Enter task ID to mark as pending: "))
                task = manager.get_task_by_id(task_id)
                if task:
                    manager.mark_pending(task)
                else:
                    print("Task not found")
            except ValueError:
                print("Please enter a valid number.")

        elif choice == "7":
            print("Thank you for using the TODO app!")
            break

        else:
            print("Invalid choice! Please enter a number between 1 and 7.")

if __name__ == "__main__":
    main()
