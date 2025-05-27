def load_students(filename):
    students = {}
    try:
        with open(filename, 'r') as file:
            for line in file:
                studentId, lastName, firstName, major, gpa = line.strip().split(',')
                students[studentId] = [lastName, firstName, major, gpa]
    except FileNotFoundError:
        print("File not found.")
    return students

def search_by_last_name(students, last_name):
    found = False
    for studentId, info in students.items():
        if info[0].lower() == last_name.lower():
            print(f"{studentId},{info[0]},{info[1]},{info[2]},{info[3]}")
            found = True
    if not found:
        print("No students found with that last name.")

def search_by_major(students, major):
    found = False
    for studentId, info in students.items():
        if info[2].lower() == major.lower():
            print(f"{studentId},{info[0]},{info[1]},{info[2]},{info[3]}")
            found = True
    if not found:
        print("No students found with that major.")

def main():
    filename = "students.txt"
    students = load_students(filename)

    while True:
        print("\nChoose an option:")
        print("1) Search by Last Name")
        print("2) Search by Major")
        print("3) Quit")
        choice = input("Enter your choice: ")

        if choice == '1':
            last_name = input("Enter last name to search for: ")
            search_by_last_name(students, last_name)
        elif choice == '2':
            major = input("Enter major to search for: ")
            search_by_major(students, major)
        elif choice == '3':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()