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

    cohorts = crud.get_all_active_cohorts()

    if not cohorts:
        flash("There are no cohorts in the database.")
        return redirect("/add-cohort")
    
    return render_template("view-cohorts.html", cohorts=cohorts)

@app.route("/update-cohort", methods=["GET", "POST"])
def update_cohort():
    """Displays form or updates a cohort status"""

    if request.method == "GET":
        cohorts = crud.get_all_cohorts()
        return render_template("update-cohort.html", cohorts=cohorts)

    elif request.method == "POST":
        cohort_id = request.form.get("cohort_id")
        active_status = request.form.get("active_status", None)
        
        if active_status:
            if active_status == "active":
                cohort = crud.update_cohort_status(cohort_id, active_status=True)
            elif active_status == "inactive":
                cohort = crud.update_cohort_status(cohort_id, active_status=False)
            print(f"Cohort active status updated to {active_status}!")

        return redirect("/view-cohorts")

    return redirect("/")


##################################################################
# STUDENT ROUTES #
##################################################################

@app.route("/add-students", methods=["GET", "POST"])
def add_students_form():
    """Display form to add students or process form with student data & add to db."""

    if request.method == "GET":
        cohorts = crud.get_all_active_cohorts()
        return render_template("add-students.html", cohorts=cohorts)

    elif request.method == "POST":
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        tech_level = request.form.get("tech_level", None)
        cohort_id = request.form.get("cohort_id")
        discord_name = request.form.get("discord_name", None)

        student = crud.create_new_student_all_fields(fname, lname, cohort_id, tech_level, discord_name)
        flash(f"Student {student.fname} {student.lname} added!")
        return redirect("/add-students")

@app.route("/update-students", methods=["GET", "POST"])
def update_students_form():
    """Display form to update students or process updates to student data & add to db."""

    if request.method == "GET":
        cohorts = crud.get_all_active_cohorts()
        return render_template("update-students.html", cohorts=cohorts)
    
    elif request.method == "POST":
        student_id = request.form.get("student_id")
        fname = request.form.get("fname", None)
        lname = request.form.get("lname", None)
        tech_level = request.form.get("tech_level", None)
        discord_name = request.form.get("discord_name", None)
        active_status = request.form.get("active_status", None)
        print(">>>>>>>>>>>>")
        print(f"Student ID: {student_id}")

        student = crud.find_student(student_id)
        print(student)
        if tech_level: 
            student = crud.update_student_tech_level(student.student_id, tech_level)
            print("Tech level updated!")

        if fname or lname:
            student = crud.update_student_name(student.student_id, fname, lname)
            print("Student name updated!")
        
        if discord_name:
            student = crud.update_student_discord_name(student.student_id, discord_name)
            print("Discord name updated!")

        if active_status:
            if active_status == "active":
                student = crud.update_student_active_status(student.student_id, active_status=True)
            elif active_status == "inactive":
                student = crud.update_student_active_status(student.student_id, active_status=False)
            print(f"Student active status updated to {active_status}!")
        
        print(">>>>>>>>>>>>")
        flash(f"The changes you requested for {student.fname} {student.lname} were completed!")
        return redirect("/update-students")

##################################################################
# LAB PAIR ROUTES #
##################################################################

@app.route("/create-pairs", methods=["GET", "POST"])
def create_pairs():
    """Display form to create lab pairs or process and display lab pairs."""
    
    cohorts = crud.get_all_active_cohorts()
    labs = crud.get_all_labs()
    pairs = []
    
    if request.method == "GET":
        # display form
        return render_template("form-create-pairs.html", cohorts=cohorts, labs=labs, pairs=pairs)
    
    elif request.method == "POST":
        # receive form data & create pairs
        cohort_id = request.form.get("cohort_id")
        pair_date = request.form.get("pair_date")
        lab_id = request.form.get("lab_id")
        print(f"Lab id is {lab_id}")
        process = request.form.get("process")

        cohort = crud.find_cohort(cohort_id)
        lab = crud.find_lab(lab_id)

        pairs = crud.make_pairs(cohort, pair_date, lab, process)

        return render_template("view-pairs.html", lab=lab, pairs=pairs, pair_date=pair_date)

@app.route("/update-pair-experience", methods=["GET", "POST"])
def update_pair_experience():
    """Display pair experience update form OR process form."""
    cohorts = crud.get_all_active_cohorts()
    
    if request.method == "GET":
        # display form
        return render_template("form-pair-experience.html", cohorts=cohorts)
    
    elif request.method == "POST":
        # get form data, query/update db, redirect
        user_id = request.form.get("user_id")
        pair_id = request.form.get("pair_id")
        pair_date = request.form.get("pair_date")
        experience = request.form.get("experience")

        lab_pairs = crud.find_lab_pair(user_id, pair_id, pair_date)

        if lab_pairs:
            if experience == "negative":
                bad_experience = True
            elif experience == "positive":
                bad_experience =  False
            lab_pairs = crud.update_pair_experience(lab_pairs, bad_experience)
            flash("Pair experience updated!")
        else:
            flash("No pair found to update!")
        return redirect("/update-pair-experience")

    return redirect("/")

@app.route("/view-cohort-pairs", methods=["GET", "POST"])
def view_cohort_pairs():
    """Display cohort pairs form or process & display cohort pairs"""
    cohorts = crud.get_all_active_cohorts()
    
    if request.method == "GET":
        #display form
        return render_template("form-cohort-pairs.html", cohorts=cohorts)
    
    elif request.method == "POST":
        # get form data, query db, display pairs
        cohort_id = request.form.get("cohort_id")
        pair_date = request.form.get("pair_date")

        cohort = crud.find_cohort(cohort_id)

        if pair_date:
            # find all pairs on that date and return list
            pairs = crud.pairs_by_date(cohort, pair_date)
        else:
            # find all pairs on all dates and return dict
            # {(date, lab): [[student, pair], ...] ...}
            pairs = crud.pairs_without_date(cohort)

        ##### maybe need a LabDate table to easily grab lab info? #####
        return render_template("view-cohort-pairs.html", pairs=pairs, pair_date=pair_date, cohort=cohort)
    return redirect("/")

@app.route("/view-student-pairs", methods=["GET", "POST"])
def view_student_pairs():
    """Display student pairs form or process & display student pairs"""
    cohorts = crud.get_all_active_cohorts()

    if request.method == "GET":
        return render_template("form-student-pairs.html", cohorts=cohorts)
    elif request.method == "POST":
        student_id = request.form.get("student_id")
        student = crud.find_student(student_id)

        labs_and_pairs = crud.get_labs_and_pairs(student_id)
        pairs_count = crud.get_students_pair_count(student_id)

        return render_template("view-student-pairs.html", student=student, labs_and_pairs=labs_and_pairs, pairs_count=pairs_count)
    return redirect("/")

if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
