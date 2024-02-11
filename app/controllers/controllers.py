from app.services.student import *
from app.services.admin import *

def get_admin_main(**kwargs):
    return get_admin(**kwargs)

def get_students_main(**kwargs):
    return get_students(**kwargs)


def add_admin_main(**kwargs):
    return add_admin(**kwargs)


def update_admin_main(**kwargs):
    return update_admin(**kwargs)

def delete_admin_main(**kwargs):
    return delete_admin(**kwargs)