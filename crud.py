"""CRUD functions."""

from model import db, Cohort, Student, Lab, LabPair, connect_to_db
import requests
from random import randrange, choice
from pprint import pprint


##################################################################
# LAB FUNCTIONS #
##################################################################
def create_new_lab(title):
    return Lab(title=title)

def get_all_labs():
    return Lab.query.all()

def find_lab(lab_id):
    return Lab.query.filter_by(lab_id=lab_id).first()

##################################################################
# COHORT FUNCTIONS #
##################################################################
def format_cohort_id(cohort_id):
    c_id_list = []
    for char in cohort_id:
        if char.isalpha():
            char = char.lower()
        c_id_list.append(char)
    cohort_id = "".join(c_id_list)
    return cohort_id

def is_cohort_in_db(cohort_id):
    cohort = Cohort.query.filter_by(cohort_id=cohort_id).all()
    if cohort:
        return True
    return False   

def create_new_cohort_with_api(cohort_id):
    all_cohorts_url = 'https://fellowship.hackbrightacademy.com/api/cohorts/'
    payload = {'format': 'json'}
    res = requests.get(all_cohorts_url, params=payload)
    all_cohorts = res.json()    
    print('>>>>>>>>>>>>>>>>>>>>')
    print('got all cohorts json')
    
    cohort_dict = {}
    for cohort in all_cohorts:
        print(f"if {cohort['id']} == {cohort_id}")
        if cohort['id'] == cohort_id:
            cohort_dict = cohort
            print("cohort found!!!!")
            break
    
    if cohort_dict:
        print('accessing requested cohort')
        json_url = cohort['url']
        cohort_res = requests.get(json_url, params=payload)
        cohort_data = cohort_res.json()

        print('defining new cohort variables')
        title = cohort_data['title']
        cohort_number = cohort_data['cohort_number']
        description = cohort_data['description']
        nickname = cohort_data['nickname']
        start_date = cohort_data['start_date']
        end_date = cohort_data['end_date']

        new_cohort = Cohort(cohort_id=cohort_id, title=title, cohort_number=cohort_number,
                            description=description, nickname=nickname, start_date=start_date,
                            end_date=end_date, json_url=json_url
        )
        print('created new cohort object')
        db.session.add(new_cohort)
        print('added new cohort')
        db.session.commit()
        print('committed new cohort')
        print('>>>>>>>>>>>>>>>>>>>>')
        return(new_cohort)
    else:
        return None

def create_new_cohort_directly(cohort_id, title, cohort_number, description, nickname,
                               start_date, end_date, json_url):
    print('>>>>>>>>>>>>>>>>>>>>')    
    print('received new cohort variables')

    new_cohort = Cohort(cohort_id=cohort_id, title=title, cohort_number=cohort_number,
                        description=description, nickname=nickname, start_date=start_date,
                        end_date=end_date, json_url=json_url
    )
    print('created new cohort object')
    print(new_cohort)

    db.session.add(new_cohort)
    print('added new cohort')

    db.session.commit()
    print('committed new cohort')
    print('>>>>>>>>>>>>>>>>>>>>')

    return new_cohort

def get_all_cohorts():
    return Cohort.query.all()

def find_cohort(cohort_id):
    return Cohort.query.filter_by(cohort_id=cohort_id).first()

##################################################################
# STUDENT FUNCTIONS #
##################################################################
def create_new_student(fname, lname, cohort_id):
    student = Student(fname=fname, lname=lname, cohort_id=cohort_id)
    db.session.add(student)
    db.session.commit()
    return student

def create_new_student_all_fields(fname, lname, cohort_id, tech_level=None, discord_name=None):
    student = Student(fname=fname, lname=lname, tech_level=tech_level,
                   cohort_id=cohort_id, discord_name=discord_name)
    db.session.add(student)
    db.session.commit()
    return student

def find_student(student_id):
    student = Student.query.filter_by(student_id=student_id).first()
    return student

def update_student_tech_level(student_id, tech_level):
    student = Student.query.get(student_id)
    student.tech_level = tech_level
    db.session.commit()
    return student

def update_student_discord_name(student_id, discord_name):
    student = Student.query.get(student_id)
    student.discord_name = discord_name
    db.session.commit()
    return student

def find_all_students_in_cohort(cohort):
    return Student.query.filter_by(cohort=cohort).all()


##################################################################
# PAIR FUNCTIONS #
##################################################################

def make_pairs(cohort, pair_date, lab, process):
    lab_pairs = []

    # grab all students in the cohort, get list of ids.
    students = find_all_students_in_cohort(cohort)

    # dictionary to hold all students and their pair counts
    # student_id: {pair_id: pair_count, ...}
    pair_history = {}

    # loop through students and create dictionary of # times paired w/other students
    for student in students:
        pairs = LabPair.query.filter_by(user_id=student.student_id).all()
        pair_count_dict = {s.student_id:0 for s in students if s.student_id != student.student_id}
        
        # loop through pairs and +1 count
        for pair in pairs:
            if pair.bad_experience == True:
                pair_count_dict[pair.pair_id] += 99
            else:
                pair_count_dict[pair.pair_id] += 1
        
        # add this student & their pair count to the main pair_history dict
        pair_history[student.student_id] = pair_count_dict

    if process == "random":
        while len(pair_history) > 1:
            # grab random student_id from pair_history & delete
            student_id, student_pairs = choice(list(pair_history.items()))           
            del pair_history[student_id]

            # find student's lowest count pair & delete
            min_pair_id = choice(list(pair_history.keys()))
            min_pair_count = student_pairs[min_pair_id]
            for key, value in student_pairs.items():
                if key in pair_history: 
                    if value < min_pair_count:
                        min_pair_count = value
                        min_pair_id = key
            del pair_history[min_pair_id]

            # Add lab pair to lab pair list
            lab_pairs.append([find_student(student_id), find_student(min_pair_id)])

            # Commit to database
            create_labpairs(student_id, min_pair_id, pair_date, lab.lab_id)
        print(f"Even # lab pairs: {lab_pairs}")

        # if odd number, add last student onto a pair
        if pair_history:
            last_student = choice(list(pair_history.keys()))
            print(last_student)
            for i in range(len(lab_pairs)):
                student_1, student_2 = lab_pairs[i]
                print(student_1, student_2)
                if (LabPair.query.filter_by(user_id=last_student,
                                            pair_id=student_1.student_id,
                                            bad_experience=True).all() or 
                                            LabPair.query.filter_by(user_id=last_student,
                                            pair_id=student_2.student_id,
                                            bad_experience=True).all()):
                    continue
                else:
                    lab_pairs[i].append(find_student(last_student))
                    break
            create_labpairs(last_student, student_1.student_id, pair_date, lab.lab_id)
            create_labpairs(last_student, student_2.student_id, pair_date, lab.lab_id)

        print(f"Lab pairs: {lab_pairs}")

    # elif process == "tech_level":

    return lab_pairs

def create_labpairs(user_id, pair_id, pair_date, lab_id):
    user_pair = LabPair(user_id=user_id, pair_id=pair_id, pair_date=pair_date, lab_id=lab_id)
    other_pair = LabPair(user_id=pair_id, pair_id=user_id, pair_date=pair_date, lab_id=lab_id)
    db.session.add(user_pair)
    db.session.add(other_pair)
    db.session.commit()
    print(f"{user_pair} & {other_pair} committed to db!")

def pairs_by_date(cohort, pair_date):
    pair_list = []
    students = find_all_students_in_cohort(cohort)
    print(f"\nNumber of students in cohort: {len(students)}")

    for student in students:
        lab_pairs = LabPair.query.filter_by(user_id=student.student_id, pair_date=pair_date).all()
        for lab_pair in lab_pairs:
            student_pair = find_student(lab_pair.pair_id)
            is_added = False
            for pair in pair_list:
                if student in pair and student_pair in pair:
                    is_added = True
            if not is_added:
                pair_list.append([student, student_pair])
    print()
    pprint(pair_list)
    print()
    return pair_list


def update_pair_experience(student_id, pair_id):
    pass


if __name__ == "__main__":
    from server import app

    connect_to_db(app)
