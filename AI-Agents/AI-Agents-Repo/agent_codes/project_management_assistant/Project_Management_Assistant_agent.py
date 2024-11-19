
class Project:
    def __init__(self, name, deadline, status):
        self.name = name
        self.deadline = deadline
        self.status = status

class ProjectManagementAssistant:
    def __init__(self):
        self.projects = []

    def add_project(self, name, deadline, status):
        new_project = Project(name, deadline, status)
        self.projects.append(new_project)
        print(f"Project {name} added successfully.")

    def view_projects(self):
        for project in self.projects:
            print(f"Name: {project.name}, Deadline: {project.deadline}, Status: {project.status}")

    def delete_project(self, name):
        for project in self.projects:
            if project.name == name:
                self.projects.remove(project)
                print(f"Project {name} removed successfully.")
                return
        print(f"No project found with the name {name}")

def main():
    assistant = ProjectManagementAssistant()

    while True:
        print("\n1. Add Project")
        print("2. View Projects")
        print("3. Delete Project")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter project name: ")
            deadline = input("Enter project deadline: ")
            status = input("Enter project status: ")
            assistant.add_project(name, deadline, status)

        elif choice == '2':
            assistant.view_projects()

        elif choice == '3':
            name = input("Enter project name: ")
            assistant.delete_project(name)

        elif choice == '4':
            break

        else:
            print("Invalid choice. Please choose a valid option.")

if __name__ == "__main__":
    main()
