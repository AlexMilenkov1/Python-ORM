import os
import django
from datetime import date

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Student


def add_students():
    Student.objects.create(
        student_id='FC5204',
        first_name='John',
        last_name='Doe',
        birth_date='1995-05-15',
        email='john.doe@university.com',
    )

    student = Student(
        student_id='FE0054',
        first_name='Jane',
        last_name='Smith',
        email='jane.smith@university.com',
    )

    student.save()

    Student.objects.create(
        student_id='FH2014',
        first_name='Alice',
        last_name='Johnson',
        birth_date='1998-02-10',
        email='alice.johnson@university.com',
    )

    Student.objects.create(
        student_id='FH2015',
        first_name='Bob',
        last_name='Wilson',
        birth_date='1996-11-25',
        email='bob.wilson@university.com',
    )


def get_students_info():
    result = []

    all_students = Student.objects.all()

    for student in all_students:
        result.append(f"Student №{student.student_id}: {student.first_name} {student.last_name}; Email: {student.email}")

    return '\n'.join(result)


def update_students_emails():
    all_students = Student.objects.all()

    current_domain = Student.objects.first().email.split('@')[1]
    new_domain = 'uni-students.com'

    for student in all_students:
        student.email = student.email.replace(current_domain, new_domain)

    Student.objects.bulk_update(all_students, ['email'])


def truncate_students():
    Student.objects.all().delete()


