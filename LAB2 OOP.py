import json
import os
import datetime

class Student:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __str__(self):
        return f"Name: {self.name}, Email: {self.email}"

class Faculty:
    def __init__(self, name, field):
        self.name = name
        self.field = field
        self.students = []

    def add_student(self, student):
        self.students.append(student)

    def graduate_student(self, student_email):
        for student in self.students:
            if student.email == student_email:
                self.students.remove(student)
                return True
        return False

    def get_enrolled_students(self):
        return [str(student) for student in self.students]

    def get_graduates(self):
        return []

    def has_student(self, student_email):
        for student in self.students:
            if student.email == student_email:
                return True
        return False

    def __str__(self):
        return f"Faculty: {self.name}, Field: {self.field}"

class University:
    def __init__(self):
        self.faculties = []
        self.students = []
        self.load_state()

    def create_faculty(self, name, field):
        faculty = Faculty(name, field)
        self.faculties.append(faculty)
        self.log_operation("Faculty creation", f"Name: {name}, Field: {field}")

    def assign_student_to_faculty(self, student_email, faculty_name):
        student = self.find_student(student_email)
        faculty = self.find_faculty(faculty_name)

        if student and faculty:
            if not faculty.has_student(student_email):
                faculty.add_student(student)
                self.log_operation("Assign student to faculty", f"Student: {student.name}, Faculty: {faculty_name}")
            else:
                print(f"Error: Student {student_email} is already assigned to Faculty {faculty_name}.")
        else:
            print("Error: Invalid student or faculty.")

    def graduate_student_from_faculty(self, student_email, faculty_name):
        faculty = self.find_faculty(faculty_name)

        if faculty:
            if faculty.graduate_student(student_email):
                self.log_operation("Graduate student from faculty", f"Student: {student_email}, Faculty: {faculty_name}")
            else:
                print(f"Error: Student {student_email} not found in Faculty {faculty_name}.")
        else:
            print("Error: Invalid faculty.")

    def display_enrolled_students(self, faculty_name):
        faculty = self.find_faculty(faculty_name)

        if faculty:
            print(f"Enrolled Students in {faculty_name}:\n")
            for student in faculty.get_enrolled_students():
                print(student)
        else:
            print("Error: Invalid faculty.")

    def display_graduates(self, faculty_name):
        faculty = self.find_faculty(faculty_name)

        if faculty:
            print(f"Graduates from {faculty_name}:\n")
            for graduate in faculty.get_graduates():
                print(graduate)
        else:
            print("Error: Invalid faculty.")

    def tell_if_student_belongs_to_faculty(self, student_email, faculty_name):
        faculty = self.find_faculty(faculty_name)

        if faculty:
            if faculty.has_student(student_email):
                print(f"Yes, student {student_email} belongs to Faculty {faculty_name}.")
            else:
                print(f"No, student {student_email} does not belong to Faculty {faculty_name}.")
        else:
            print("Error: Invalid faculty.")

    def create_student(self, name, email):
        student = Student(name, email)
        self.students.append(student)
        self.log_operation("Student creation", f"Name: {name}, Email: {email}")

    def find_student(self, student_email):
        for student in self.students:
            if student.email == student_email:
                return student
        return None

    def find_faculty(self, faculty_name):
        for faculty in self.faculties:
            if faculty.name == faculty_name:
                return faculty
        return None

    def display_university_faculties(self):
        print("University Faculties:\n")
        for faculty in self.faculties:
            print(faculty)

    def display_faculties_in_field(self, field):
        print(f"Faculties in {field}:\n")
        for faculty in self.faculties:
            if faculty.field == field:
                print(faculty)

    def save_state(self):
        data = {
            "faculties": [(faculty.name, faculty.field, [student.email for student in faculty.students]) for faculty in self.faculties],
            "students": [(student.name, student.email) for student in self.students]
        }

        with open('state.json', 'w') as file:
            json.dump(data, file)

    def load_state(self):
        if os.path.exists('state.json'):
            with open('state.json', 'r') as file:
                data = json.load(file)

            for faculty_data in data["faculties"]:
                faculty = Faculty(faculty_data[0], faculty_data[1])
                self.faculties.append(faculty)

                for student_email in faculty_data[2]:
                    student = self.find_student(student_email)
                    if student:
                        faculty.add_student(student)

            for student_data in data["students"]:
                student = Student(student_data[0], student_data[1])
                self.students.append(student)

    def log_operation(self, operation, details):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open('operation_log.txt', 'a') as file:
            file.write(f"[{timestamp}] Operation: {operation}, Details: {details}\n")

def batch_enrollment(system, file_name):
    try:
        with open(file_name, 'r') as file:
            lines = file.readlines()
            for line in lines:
                name, email = line.strip().split(',')
                system.create_student(name, email)
    except FileNotFoundError:
        print(f"Error: File {file_name} not found.")

def batch_graduation(system, file_name):
    try:
        with open(file_name, 'r') as file:
            emails = file.readlines()
            for email in emails:
                system.graduate_student_from_faculty(email.strip(), "Unknown")  # Assume faculty name is not available in the file
    except FileNotFoundError:
        print(f"Error: File {file_name} not found.")

# Example usage
if __name__ == "__main__":
    university_system = University()

    while True:
        print("\n1. Create a new faculty.")
        print("2. Assign a student to a faculty.")
        print("3. Graduate a student from a faculty.")
        print("4. Display current enrolled students in a faculty.")
        print("5. Display graduates from a faculty.")
        print("6. Check if a student belongs to a faculty.")
        print("7. Create a new student.")
        print("8. Search what faculty a student belongs to by email.")
        print("9. Display University faculties.")
        print("10. Display all faculties belonging to a field.")
        print("11. Batch enrollment operation for students via a text file.")
        print("12. Batch graduation operation for students via text file.")
        print("13. Save current state.")
        print("0. Exit.")

        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter faculty name: ")
            field = input("Enter faculty field: ")
            university_system.create_faculty(name, field)

        elif choice == "2":
            student_email = input("Enter student email: ")
            faculty_name = input("Enter faculty name: ")
            student = university_system.find_student(student_email)
            faculty = university_system.find_faculty(faculty_name)

        elif choice == "3":
            student_email = input("Enter student email: ")
            faculty_name = input("Enter faculty name: ")
            university_system.graduate_student_from_faculty(student_email, faculty_name)

        elif choice == "4":
            faculty_name = input("Enter faculty name: ")
            university_system.display_enrolled_students(faculty_name)

        elif choice == "5":
            faculty_name = input("Enter faculty name: ")
            university_system.display_graduates(faculty_name)

        elif choice == "6":
            student_email = input("Enter student email: ")
            faculty_name = input("Enter faculty name: ")
            university_system.tell_if_student_belongs_to_faculty(student_email, faculty_name)

        elif choice == "7":
            name = input("Enter student name: ")
            email = input("Enter student email: ")
            university_system.create_student(name, email)

        elif choice == "8":
            student_email = input("Enter student email: ")
            student = university_system.find_student(student_email)
            if student:
                faculty_name = "Unknown"
                print(f"Student {student_email} belongs to: {faculty.name}")
            else:
                print(f"Student {student_email} not found.")

        elif choice == "9":
            university_system.display_university_faculties()

        elif choice == "10":
            field = input("Enter field: ")
            university_system.display_faculties_in_field(field)

        elif choice == "11":
            file_name = input("Enter file name for batch enrollment: ")
            batch_enrollment(university_system, file_name)

        elif choice == "12":
            file_name = input("Enter file name for batch graduation: ")
            batch_graduation(university_system, file_name)

        elif choice == "13":
            university_system.save_state()
            print("Current state saved successfully.")

        elif choice == "0":
            break

        else:
            print("Invalid choice. Please try again.")
