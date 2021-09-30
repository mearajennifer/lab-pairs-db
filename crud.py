"""CRUD functions."""

from model import db, Cohort, Student, Lab, LabPair, connect_to_db
import requests
from random import randrange, choice
from pprint import pprint
from sqlalchemy import desc


##################################################################
# LAB FUNCTIONS #
##################################################################
def create_new_lab(title):
    """Creates a new lab object and adds to db."""

    lab = Lab(title=title)
    db.session.add(lab)
    db.session.commit()

    return lab

def get_all_labs():
    """Return all labs from the db.
    For example:
    >>> get_all_labs()
    [<Lab lab_id=1 title=Blockly>, <Lab lab_id=2 title=Guessing Game>, <Lab lab_id=3 title=Calculator 1>, <Lab lab_id=4 title=Calculator 2>, <Lab lab_id=5 title=List Slicing>, <Lab lab_id=6 title=Data Structures>, <Lab lab_id=7 title=Dictionaries: Word Count>, <Lab lab_id=8 title=Dictionaries: Restaurant>, <Lab lab_id=9 title=Markov Chains>, <Lab lab_id=10 title=Markov Chains: Discord>, <Lab lab_id=11 title=Object-Oriented Drawing (in Replit)>, <Lab lab_id=12 title=Practice with Object Oriented Melons>, <Lab lab_id=13 title=Object Oriented Melons>, <Lab lab_id=14 title=HTML: Forms>, <Lab lab_id=15 title=CSS: Trials>, <Lab lab_id=16 title=Flask: Intro>, <Lab lab_id=17 title=Madlibs>, <Lab lab_id=18 title=Shopping Site>, <Lab lab_id=19 title=APIs>, <Lab lab_id=20 title=Testing>, <Lab lab_id=21 title=JavaScript Trials: Part 1>, <Lab lab_id=22 title=JavaScript Trials: Part 2>, <Lab lab_id=23 title=JavaScript Sharkwords>, <Lab lab_id=24 title=JavaScript: Coffee Shop App>, <Lab lab_id=25 title=AJAX>, <Lab lab_id=26 title=React: Trading Cards>, <Lab lab_id=27 title=React: Trading Cards 2>, <Lab lab_id=28 title=Bootstrap>, <Lab lab_id=29 title=SQL Quiz>, <Lab lab_id=30 title=Project Tracker>, <Lab lab_id=31 title=Project Tracker Python>, <Lab lab_id=32 title=Movie Ratings App>, <Lab lab_id=33 title=Testing Flask>]
    """
    return Lab.query.all()

def find_lab(lab_id):
    return Lab.query.filter_by(lab_id=lab_id).first()

##################################################################
# COHORT FUNCTIONS #
##################################################################
def format_cohort_id(cohort_id):
    """Format's string to pass to API
    For example:
    >>> format_cohort_id('SERFT7')
    'serft7'
    """
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
        active = True

        new_cohort = Cohort(cohort_id=cohort_id, title=title, cohort_number=cohort_number,
                            description=description, nickname=nickname, start_date=start_date,
                            end_date=end_date, json_url=json_url, active=active
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

    new_cohort = Cohort(cohort_id=cohort_id, title=title, cohort_number=cohort_number,
                        description=description, nickname=nickname, start_date=start_date,
                        end_date=end_date, json_url=json_url, active=True
    )

    db.session.add(new_cohort)
    db.session.commit()

    return new_cohort

def get_all_cohorts():
    return Cohort.query.all()

def get_all_active_cohorts():
    return Cohort.query.filter_by(active=True).all()

def find_cohort(cohort_id):
    return Cohort.query.filter_by(cohort_id=cohort_id).first()

def update_cohort_status(cohort_id, active_status):
    cohort = find_cohort(cohort_id)
    cohort.active = active_status
    db.session.commit()
    return cohort


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

def update_student_name(student_id, fname, lname):
    student = Student.query.get(student_id)
    if fname:
        student.fname = fname
    if lname:
        student.lname = lname
    db.session.commit()
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

def update_student_active_status(student_id, active_status):
    student = Student.query.get(student_id)
    student.active = active_status
    db.session.commit()
    return student

def find_all_students_in_cohort(cohort):
    return Student.query.filter_by(cohort=cohort).all()

def find_all_active_students_in_cohort(cohort):
    return Student.query.filter_by(cohort=cohort, active=True).all()


##################################################################
# PAIR FUNCTIONS #
##################################################################

def make_pairs(cohort, pair_date, lab, process):
    lab_pairs = []

    # grab all students in the cohort, get list of ids.
    students = find_all_active_students_in_cohort(cohort)

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

        # if odd number, add last student onto a pair
        if pair_history:
            last_student = choice(list(pair_history.keys()))
            print(f'Last student is: {last_student}')
            for i in range(len(lab_pairs)):
                student_1, student_2 = lab_pairs[i]
                if (LabPair.query.filter_by(user_id=last_student,
                                            pair_id=student_1.student_id,
                                            bad_experience=True).all() or 
                                            LabPair.query.filter_by(user_id=last_student,
                                            pair_id=student_2.student_id,
                                            bad_experience=True).all()):
                    continue
                else:
                    lab_pairs[i].append(find_student(last_student))
                    print(f"Added remaining student to lab pair: {lab_pairs[i]}")
                    break
            create_labpairs(last_student, student_1.student_id, pair_date, lab.lab_id)
            create_labpairs(last_student, student_2.student_id, pair_date, lab.lab_id)

        print("New lab pairs created: ")
        pprint(lab_pairs)

    # elif process == "tech_level":

    return lab_pairs

def create_labpairs(user_id, pair_id, pair_date, lab_id):
    user_pair = LabPair(user_id=user_id, pair_id=pair_id, pair_date=pair_date, lab_id=lab_id)
    other_pair = LabPair(user_id=pair_id, pair_id=user_id, pair_date=pair_date, lab_id=lab_id)
    db.session.add(user_pair)
    db.session.add(other_pair)
    db.session.commit()
    # print(f"{user_pair} & {other_pair} committed to db!")

def pairs_by_date(cohort, pair_date):
    students = find_all_students_in_cohort(cohort)
    print(f"\nNumber of students in cohort: {len(students)}")
    print(f"Pairing date: {pair_date}")

    pair_list = []
    for student in students:
        print(f"\nGetting pairs for {student}")
        lab_pairs = LabPair.query.filter_by(user_id=student.student_id, pair_date=pair_date).all()
        print(f"\tLab pairs list: {lab_pairs}")
        for lab_pair in lab_pairs:
            student_pair = find_student(lab_pair.pair_id)
            is_added = False
            for pair in pair_list:
                if student in pair and student_pair in pair:
                    is_added = True
                elif student in pair:
                    pair.append(student_pair)
                    is_added = True
                elif student_pair in pair:
                    pair.append(student)
                    is_added = True
            if not is_added:
                pair_list.append([student, student_pair])
    pprint(pair_list)
    return pair_list

def pairs_without_date(cohort):
    students = find_all_students_in_cohort(cohort)
    print(f"\nNumber of students in cohort: {len(students)}")

    pairs_by_lab = {}
    for student in students:
        student_lab_pairs = LabPair.query.filter_by(user_id=student.student_id).all()
        for lab_pair in student_lab_pairs:
            # student = find_student(lab_pair.user_id)
            student_pair = find_student(lab_pair.pair_id)
            lab = find_lab(lab_pair.lab_id)
            date = lab_pair.pair_date
            if (date, lab) in pairs_by_lab:
                is_pair_added = False
                for pair_for_lab in pairs_by_lab[(date, lab)]:
                    if student in pair_for_lab and student_pair in pair_for_lab:
                        is_pair_added = True
                    elif student in pair_for_lab:
                        pair_for_lab.append(student_pair)
                        is_pair_added = True
                    elif student_pair in pair_for_lab:
                        pair_for_lab.append(student)
                        is_pair_added = True
                if not is_pair_added:
                    pairs_by_lab[(date, lab)].append([student, student_pair])
            else:
                pairs_by_lab[(date, lab)] = [[student, student_pair]]
    pprint(pairs_by_lab)
    return(pairs_by_lab)

def get_labs_and_pairs(student_id):
    labs_and_pairs = {}
    pairs = LabPair.query.filter_by(user_id=student_id).all()

    for pair in pairs:
        student_pair = Student.query.filter_by(student_id=pair.pair_id).first()
        lab = Lab.query.filter_by(lab_id=pair.lab_id).first()
        labs_and_pairs[pair] = [student_pair, lab]
    pprint(labs_and_pairs)
    return labs_and_pairs

def get_students_pair_count(student_id):
    lab_pairs = Student.query.filter_by(student_id=student_id).first().student_pairs
    pair_count = {}
    for pair in lab_pairs:
        if pair not in pair_count:
            pair_count[pair] = 1
        else:
            pair_count[pair] += 1
    pprint(pair_count)
    return pair_count

def update_pair_experience(student_id, pair_id):
    pass


if __name__ == "__main__":
    from server import app
    connect_to_db(app)
