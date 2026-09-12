class Student:
    def __init__(self, name, age, student_id):
        self.name = name
        self.age = age
        self.student_id = student_id

    def __str__(self):
        return f"Student Name: {self.name}, Age: {self.age}, ID: {self.student_id}"

s1 = Student("Alice", 20, "S12345")
s2 = Student("Bob", 22, "S67890")

print(s1)
print(s2)

print(type(s1))
print(isinstance(s1, Student))
print(type(s1).__name__)