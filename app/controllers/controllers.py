from app.services.student import *
from app.services.admin import *
from app.services.advisor import *
from app.services.subject import *
from app.services.assessment import *
from app.services.grade import *
from app.services.program import *
from app.services.evaluation import *


def fetch_students_main(**kwargs):
    return fetch_students(**kwargs)

def add_advisee_bulk_main(**kwargs):
    return add_advisee_bulk(**kwargs)

def add_advisee_main(**kwargs):
    return add_advisee(**kwargs)

def register_advisor_in_bulk_main(**kwargs):
    return register_advisor_in_bulk(**kwargs)


def register_student_in_bulk_main(**kwargs):
    return register_student_in_bulk(**kwargs)

def drop_advisors_main(**kwargs):
    return drop_advisors(**kwargs)


def drop_students_main(**kwargs):
    return drop_students(**kwargs)

def get_all_programs_main(**kwargs):
    return get_all_programs(**kwargs)


def get_all_subjects_main(**kwargs):
    return get_all_subjects(**kwargs)


def get_all_advisors_main(**kwargs):
    return get_all_advisors(**kwargs)


def login_admin_main(**kwargs):
    return login_admin(**kwargs)


def register_admin_main(**kwargs):
    return register_admin(**kwargs)

def get_advisor_student_semester_class_main(**kwargs):
    return get_advisor_student_semester_class(**kwargs)

def get_advisor_student_semester_main(**kwargs):
    return get_advisor_student_semester(**kwargs)

def get_advisor_students_main(**kwargs):
    return get_advisor_students(**kwargs)

def course_outline_manual_main(**kwargs):
    return course_outline_manual(**kwargs)

def course_outline_main(**kwargs):
    return course_outline(**kwargs)

def get_subject_assessments_main(**kwargs):
    return get_subject_assessments(**kwargs)

def get_student_assessment_grades_main(**kwargs):
    return get_student_assessment_grades(**kwargs)

def student_class_code_main(**kwargs):
    return student_class_code(**kwargs)

def register_student_main(**kwargs):
    return register_student(**kwargs)

def login_student_main(**kwargs):
    return login_student(**kwargs)

def register_advisor_main(**kwargs):
    return register_advisor(**kwargs)

def login_advisor_main(**kwargs):
    return login_advisor(**kwargs)

def get_admin_main(**kwargs):
    return get_admin(**kwargs)

def get_students_main(**kwargs):
    return get_students(**kwargs)

def get_student_main(**kwargs):
    return get_student(**kwargs)

def add_admin_main(**kwargs):
    return add_admin(**kwargs)

def update_admin_main(**kwargs):
    return update_admin(**kwargs)

def delete_admin_main(**kwargs):
    return delete_admin(**kwargs)

def save_grades_main(**kwargs):
    return save_grades(**kwargs)

def add_new_assessment_main(**kwargs):
    return add_new_assessment(**kwargs)


def get_student_evaluation(**kwargs):
    return evaluate_student(**kwargs)