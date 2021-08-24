"""CRUD functions."""

from model import db, Cohort, Student, Lab, LabPair, connect_to_db
import requests


def create_new_lab(title):
    return Lab(title=title)

def create_new_cohort(cohort_id):
    all_cohorts_url = 'https://fellowship.hackbrightacademy.com/api/cohorts/'
    payload = {'format': 'json'}
    res = requests.get(all_cohorts_url, params=payload)
    all_cohorts = res.json()    
    print('>>>>>>>>>>>>>>>>>>>>')
    print('got all cohorts json')
    
    for cohort in all_cohorts:
        if cohort['id'] == cohort_id:
            cohort_dict = cohort
            break
    
    print('accessing requested cohort')
    json_url = cohort['url']
    cohort_res = requests.get(json_url, params=payload)
    cohort_data = cohort_res.json()

    cohort_id = cohort_data['id']
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

    db.session.add(new_cohort)
    print('added new cohort')
    db.session.commit()
    print('committed new cohort')
    print('>>>>>>>>>>>>>>>>>>>>')
    return(new_cohort)

def create_new_student(fname, lname, cohort_id):
    student = Student(fname=fname, lname=lname, cohort_id=cohort_id)
    db.session.add(student)
    db.session.commit()
    return student

def create_new_student_all_fields(fname, lname, tech_level, cohort_id, discord_name):
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
