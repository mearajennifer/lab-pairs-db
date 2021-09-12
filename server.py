"""Server for student lab pairs."""

from flask import Flask, render_template, redirect, request, flash, session
from model import connect_to_db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = 'SECRETSECRETSECRET'
app.jinja_env.undefined = StrictUndefined


##################################################################
# GENERAL ROUTES #
##################################################################

@app.route("/")
def show_homepage():
    return render_template("index.html")

##################################################################
# COHORT ROUTES #
##################################################################

@app.route("/add-cohort", methods=["GET", "POST"])
def add_cohort_form():
    """Display form to add cohort or process form with cohort id & grab data from API."""

    if request.method == "GET":
        return render_template("add-cohort.html")
    
    elif request.method == "POST":
        cohort_id = request.form.get("cohort_id")
        cohort_id = crud.format_cohort_id(cohort_id)

        does_exist = crud.is_cohort_in_db(cohort_id)
        if does_exist:
            flash("Cohort is already in your database!")
            return redirect("/")

        cohort = crud.create_new_cohort_with_api(cohort_id)
        if not cohort:
            flash("Cohort not found! Please try again.")
            return redirect("/")
        
        flash(f"Cohort {cohort.title} added!")
        return redirect("/")

@app.route("/manually-add-cohort", methods=["POST"])
def manually_add_cohort_form():
    """Process form with cohort data and add to db."""

    cohort_id = request.form.get("cohort_id")
    title = request.form.get("title", None)
    cohort_number = request.form.get("cohort_number", None)
    description = request.form.get("description", None)
    nickname = request.form.get("nickname", None)
    start_date = request.form.get("start_date", None)
    end_date = request.form.get("end_date", None)
    json_url = request.form.get("json_url", None)

    cohort_id = crud.format_cohort_id(cohort_id)

    does_exist = crud.is_cohort_in_db(cohort_id)
    if does_exist:
        flash("Cohort is already in your database!")
        return redirect("/")
    
    cohort = crud.create_new_cohort_directly(
        cohort_id,
        title,
        cohort_number,
        description,
        nickname,
        start_date,
        end_date,
        json_url
        )
    flash(f"Cohort {cohort.cohort_id} added!")
    return redirect("/")

@app.route("/view-cohorts", methods=["GET"])
def show_all_cohorts():
    """Display all cohorts in db."""

    cohorts = crud.get_all_cohorts()

    if not cohorts:
        flash("There are no cohorts in the database.")
        return redirect("/add-cohort")
    
    return render_template("view-cohorts.html", cohorts=cohorts)


##################################################################
# STUDENT ROUTES #
##################################################################

@app.route("/add-students", methods=["GET", "POST"])
def add_students_form():
    """Display form to add students or process form with student data & add to db."""

    if request.method == "GET":
        cohorts = crud.get_all_cohorts()
        return render_template("add-students.html", cohorts=cohorts)

    elif request.method == "POST":
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        tech_level = request.form.get("tech_level", None)
        cohort_id = request.form.get("cohort_id")
        discord_name = request.form.get("discord_name", None)

        student = crud.create_new_student_all_fields(fname, lname, cohort_id, tech_level, discord_name)
        flash(f"Student {student.fname} {student.lname} added!")
        return redirect("/")

@app.route("/update-students", methods=["GET", "POST"])
def update_students_form():
    """Display form to update students or process updates to student data & add to db."""

    if request.method == "GET":
        cohorts = crud.get_all_cohorts()
        return render_template("update-students.html", cohorts=cohorts)
    
    elif request.method == "POST":
        student_id = request.form.get("student_id")
        tech_level = request.form.get("tech_level", None)
        discord_name = request.form.get("discord_name", None)
        print(">>>>>>>>>>>>")
        print(f"Student ID: {student_id}")

        student = crud.find_student(student_id)
        print(student)
        if tech_level: 
            student = crud.update_student_tech_level(student.student_id, tech_level)
            print("Tech level updated!")
        
        if discord_name:
            student = crud.update_student_discord_name(student.student_id, discord_name)
            print("Discord name updated!")
        
        print(">>>>>>>>>>>>")
        flash(f"The changes you requested for {student.fname} {student.lname} were completed!")
        return redirect("/update-students")

##################################################################
# LAB PAIR ROUTES #
##################################################################

@app.route("/create-pairs", methods=["GET", "POST"])
def create_pairs():
    """Display form to create lab pairs or process and display cohort pairs."""
    
    cohorts = crud.get_all_cohorts()
    labs = crud.get_all_labs()
    pairs = []
    
    if request.method == "GET":    
        return render_template("create-pairs-form.html", cohorts=cohorts, labs=labs, pairs=pairs)
    # template: select cohort, select date, select process (random, tech level, and eventually, create your own pairs)
    
    if request.method == "POST":
        cohort_id = request.form.get("cohort_id")
        pair_date = request.form.get("pair_date")
        lab_id = request.form.get("lab_id")
        process = request.form.get("process")

        cohort = crud.find_cohort(cohort_id)
        lab = crud.find_lab(lab_id)

        pairs = crud.make_pairs(cohort, pair_date, lab, process)

        return render_template("display-pairs.html", lab=lab, pairs=pairs, pair_date=pair_date)

@app.route("/view-cohort-pairs", methods=["GET", "POST"])
def view_cohort_pairs():
    """   """
    # template: drop down menu with cohorts, if pairs data is passed then show it
    return redirect("/")

if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
