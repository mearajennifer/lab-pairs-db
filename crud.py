"""CRUD functions."""

from model import db, Cohort, Student, Lab, LabPair, connect_to_db
import requests


def create_new_lab(title):
    return Lab(title=title)

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

def create_lab_pairs():
    pass

def update_pair_experience(student_id, pair_id):
    pass


if __name__ == "__main__":
    from server import app

    connect_to_db(app)
