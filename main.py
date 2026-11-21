import tkinter as tk
from tkinter import messagebox
import json
import os
import webbrowser


# =========================================================
# FILES
# =========================================================

DATA_FILE = "students.json"
APPLICATION_FILE = "applications.json"
COMPANY_FILE = "company.json"


# =========================================================
# COLORS
# =========================================================

BG_COLOR = "#EAF4FF"

GREEN = "#10B981"
BLUE = "#2563EB"
PURPLE = "#7C3AED"
ORANGE = "#F59E0B"
TEAL = "#0D9488"
RED = "#EF4444"
INDIGO = "#4F46E5"
AMBER = "#D97706"
DARK_GREY = "#374151"

WHITE = "#FFFFFF"
TEXT_COLOR = "#1F2937"


# =========================================================
# LOAD STUDENTS
# =========================================================

def load_students():

    if os.path.exists(DATA_FILE):

        try:
            with open(DATA_FILE, "r") as file:
                return json.load(file)

        except:
            return []

    return []


students = load_students()


# =========================================================
# SAVE STUDENTS
# =========================================================

def save_data():

    with open(DATA_FILE, "w") as file:
        json.dump(students, file, indent=4)


# =========================================================
# ADD STUDENT
# =========================================================

def add_student():

    window = tk.Toplevel(root)
    window.title("Add Student")
    window.geometry("550x600")
    window.configure(bg=BG_COLOR)
    window.resizable(False, False)

    tk.Label(
        window,
        text="➕ Add Student",
        font=("Arial", 22, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(pady=25)

    tk.Label(
        window,
        text="Student Name",
        bg=BG_COLOR
    ).pack()

    name_entry = tk.Entry(window, width=40, font=("Arial", 12))
    name_entry.pack(pady=6)

    tk.Label(
        window,
        text="Roll Number",
        bg=BG_COLOR
    ).pack()

    roll_entry = tk.Entry(window, width=40, font=("Arial", 12))
    roll_entry.pack(pady=6)

    tk.Label(
        window,
        text="Department",
        bg=BG_COLOR
    ).pack()

    department_entry = tk.Entry(window, width=40, font=("Arial", 12))
    department_entry.pack(pady=6)

    tk.Label(
        window,
        text="CGPA",
        bg=BG_COLOR
    ).pack()

    cgpa_entry = tk.Entry(window, width=40, font=("Arial", 12))
    cgpa_entry.pack(pady=6)

    tk.Label(
        window,
        text="Skills",
        bg=BG_COLOR
    ).pack()

    skills_entry = tk.Entry(window, width=40, font=("Arial", 12))
    skills_entry.pack(pady=6)


    def save_student():

        name = name_entry.get().strip()
        roll = roll_entry.get().strip()
        department = department_entry.get().strip()
        cgpa = cgpa_entry.get().strip()
        skills = skills_entry.get().strip()

        if not name or not roll or not department or not cgpa or not skills:

            messagebox.showwarning(
                "Warning",
                "Please fill all fields."
            )

            return

        try:

            cgpa_value = float(cgpa)

            if cgpa_value < 0 or cgpa_value > 10:

                messagebox.showwarning(
                    "Invalid CGPA",
                    "CGPA 0 se 10 ke beech honi chahiye."
                )

                return

        except ValueError:

            messagebox.showwarning(
                "Invalid CGPA",
                "CGPA me number enter karein."
            )

            return


        for student in students:

            if student["roll"] == roll:

                messagebox.showwarning(
                    "Duplicate",
                    "Ye Roll Number already registered hai."
                )

                return


        student = {

            "name": name,
            "roll": roll,
            "department": department,
            "cgpa": cgpa_value,
            "skills": skills,
            "placement_status": "Not Placed"

        }

        students.append(student)

        save_data()

        messagebox.showinfo(
            "Success",
            "Student successfully added!"
        )

        window.destroy()


    tk.Button(
        window,
        text="Save Student",
        width=22,
        height=2,
        font=("Arial", 12, "bold"),
        bg=GREEN,
        fg=WHITE,
        command=save_student
    ).pack(pady=25)


# =========================================================
# VIEW STUDENTS
# =========================================================

def view_students():

    window = tk.Toplevel(root)
    window.title("View Students")
    window.geometry("950x550")
    window.configure(bg=BG_COLOR)

    tk.Label(
        window,
        text="👨‍🎓 All Students",
        font=("Arial", 22, "bold"),
        bg=BG_COLOR
    ).pack(pady=20)

    if not students:

        tk.Label(
            window,
            text="No students found.",
            font=("Arial", 14),
            bg=BG_COLOR
        ).pack(pady=30)

        return


    table = tk.Frame(window, bg=BG_COLOR)
    table.pack()


    headers = [
        "Name",
        "Roll No.",
        "Department",
        "CGPA",
        "Skills",
        "Status"
    ]


    for column, header in enumerate(headers):

        tk.Label(
            table,
            text=header,
            font=("Arial", 11, "bold"),
            borderwidth=1,
            relief="solid",
            width=15,
            bg=BLUE,
            fg=WHITE
        ).grid(row=0, column=column)


    for row, student in enumerate(students, start=1):

        values = [

            student["name"],
            student["roll"],
            student["department"],
            student["cgpa"],
            student["skills"],
            student["placement_status"]

        ]


        for column, value in enumerate(values):

            tk.Label(
                table,
                text=value,
                borderwidth=1,
                relief="solid",
                width=15,
                bg=WHITE
            ).grid(row=row, column=column)


# =========================================================
# SEARCH STUDENT
# =========================================================

def search_student():

    window = tk.Toplevel(root)
    window.title("Search Student")
    window.geometry("650x500")
    window.configure(bg=BG_COLOR)

    tk.Label(
        window,
        text="🔍 Search Student",
        font=("Arial", 22, "bold"),
        bg=BG_COLOR
    ).pack(pady=25)

    tk.Label(
        window,
        text="Enter Roll Number",
        font=("Arial", 12),
        bg=BG_COLOR
    ).pack()

    roll_entry = tk.Entry(
        window,
        width=35,
        font=("Arial", 12)
    )

    roll_entry.pack(pady=10)


    result_label = tk.Label(
        window,
        text="",
        font=("Arial", 12),
        justify="left",
        bg=BG_COLOR
    )

    result_label.pack(pady=20)


    def search():

        roll = roll_entry.get().strip()

        if roll == "":

            messagebox.showwarning(
                "Warning",
                "Please enter Roll Number."
            )

            return


        for student in students:

            if student["roll"] == roll:

                result = (

                    "Name: " + student["name"] + "\n"
                    "Roll Number: " + student["roll"] + "\n"
                    "Department: " + student["department"] + "\n"
                    "CGPA: " + str(student["cgpa"]) + "\n"
                    "Skills: " + student["skills"] + "\n"
                    "Placement Status: " +
                    student["placement_status"]

                )

                result_label.config(text=result)

                return


        result_label.config(
            text="Student not found."
        )


    tk.Button(
        window,
        text="Search",
        width=20,
        height=2,
        font=("Arial", 12, "bold"),
        bg=PURPLE,
        fg=WHITE,
        command=search
    ).pack(pady=10)


# =========================================================
# COMPANY / JOB DETAILS
# =========================================================

def company_details():

    window = tk.Toplevel(root)
    window.title("Company & Job Details")
    window.geometry("700x750")
    window.configure(bg=BG_COLOR)
    window.resizable(False, False)


    tk.Label(
        window,
        text="🏢 Company & Job Details",
        font=("Arial", 22, "bold"),
        bg=BG_COLOR
    ).pack(pady=20)


    # Company Name

    tk.Label(
        window,
        text="Company Name",
        bg=BG_COLOR
    ).pack()

    company_entry = tk.Entry(
        window,
        width=45,
        font=("Arial", 12)
    )

    company_entry.pack(pady=5)


    # Job Role

    tk.Label(
        window,
        text="Job Role",
        bg=BG_COLOR
    ).pack()

    role_entry = tk.Entry(
        window,
        width=45,
        font=("Arial", 12)
    )

    role_entry.pack(pady=5)


    # Eligible Roll Numbers

    tk.Label(
        window,
        text="Eligible Roll Numbers",
        bg=BG_COLOR
    ).pack()

    roll_entry = tk.Entry(
        window,
        width=45,
        font=("Arial", 12)
    )

    roll_entry.pack(pady=5)


    # Required Skills

    tk.Label(
        window,
        text="Required Skills",
        bg=BG_COLOR
    ).pack()

    skills_entry = tk.Entry(
        window,
        width=45,
        font=("Arial", 12)
    )

    skills_entry.pack(pady=5)


    # Minimum CGPA

    tk.Label(
        window,
        text="Minimum CGPA",
        bg=BG_COLOR
    ).pack()

    cgpa_entry = tk.Entry(
        window,
        width=45,
        font=("Arial", 12)
    )

    cgpa_entry.pack(pady=5)


    # Job Type

    tk.Label(
        window,
        text="Job Type",
        bg=BG_COLOR
    ).pack()

    job_type = tk.StringVar(value="Full Time")

    tk.OptionMenu(
        window,
        job_type,
        "Full Time",
        "Part Time"
    ).pack(pady=5)


    # Work Mode

    tk.Label(
        window,
        text="Work Mode",
        bg=BG_COLOR
    ).pack()

    work_mode = tk.StringVar(value="On-site")

    tk.OptionMenu(
        window,
        work_mode,
        "On-site",
        "Remote",
        "Hybrid"
    ).pack(pady=5)


    # Working Time

    tk.Label(
        window,
        text="Working Time",
        bg=BG_COLOR
    ).pack()

    time_entry = tk.Entry(
        window,
        width=45,
        font=("Arial", 12)
    )

    time_entry.pack(pady=5)


    # Job Description

    tk.Label(
        window,
        text="Job Description",
        bg=BG_COLOR
    ).pack()

    description_entry = tk.Entry(
        window,
        width=45,
        font=("Arial", 12)
    )

    description_entry.pack(pady=5)


    # Apply Link

    tk.Label(
        window,
        text="Apply Link",
        bg=BG_COLOR
    ).pack()

    apply_entry = tk.Entry(
        window,
        width=45,
        font=("Arial", 12)
    )

    apply_entry.pack(pady=5)


    def save_company():

        company = company_entry.get().strip()
        role = role_entry.get().strip()
        eligible_rolls = roll_entry.get().strip()
        skills = skills_entry.get().strip()
        minimum_cgpa = cgpa_entry.get().strip()
        working_time = time_entry.get().strip()
        description = description_entry.get().strip()
        apply_link = apply_entry.get().strip()


        if (
            company == ""
            or role == ""
            or skills == ""
            or minimum_cgpa == ""
            or working_time == ""
        ):

            messagebox.showwarning(
                "Warning",
                "Please fill the required fields."
            )

            return


        try:

            minimum_cgpa = float(minimum_cgpa)

            if minimum_cgpa < 0 or minimum_cgpa > 10:

                messagebox.showwarning(
                    "Invalid CGPA",
                    "CGPA 0 se 10 ke beech honi chahiye."
                )

                return

        except ValueError:

            messagebox.showwarning(
                "Invalid CGPA",
                "Minimum CGPA me number enter karein."
            )

            return


        job = {

            "company": company,
            "job_role": role,
            "eligible_rolls": eligible_rolls,
            "skills": skills,
            "minimum_cgpa": minimum_cgpa,
            "job_type": job_type.get(),
            "work_mode": work_mode.get(),
            "working_time": working_time,
            "description": description,
            "apply_link": apply_link

        }


        jobs = []


        if os.path.exists(COMPANY_FILE):

            try:

                with open(COMPANY_FILE, "r") as file:
                    old_data = json.load(file)

                if isinstance(old_data, list):
                    jobs = old_data

                elif isinstance(old_data, dict):
                    jobs = [old_data]

            except:
                jobs = []


        jobs.append(job)


        with open(COMPANY_FILE, "w") as file:

            json.dump(
                jobs,
                file,
                indent=4
            )


        messagebox.showinfo(
            "Success",
            "Company and job details saved successfully!"
        )

        window.destroy()


    tk.Button(
        window,
        text="Save Company / Job",
        width=25,
        height=2,
        font=("Arial", 12, "bold"),
        bg=ORANGE,
        fg=WHITE,
        command=save_company
    ).pack(pady=15)


# =========================================================
# CHECK ELIGIBILITY
# =========================================================

def check_eligibility():

    window = tk.Toplevel(root)
    window.title("Check Eligibility")
    window.geometry("600x450")
    window.configure(bg=BG_COLOR)


    tk.Label(
        window,
        text="✅ Check Student Eligibility",
        font=("Arial", 22, "bold"),
        bg=BG_COLOR
    ).pack(pady=25)


    tk.Label(
        window,
        text="Enter Roll Number",
        font=("Arial", 12),
        bg=BG_COLOR
    ).pack()


    roll_entry = tk.Entry(
        window,
        width=35,
        font=("Arial", 12)
    )

    roll_entry.pack(pady=10)


    result_label = tk.Label(
        window,
        text="",
        font=("Arial", 14, "bold"),
        bg=BG_COLOR
    )

    result_label.pack(pady=25)


    def check():

        roll = roll_entry.get().strip()

        for student in students:

            if student["roll"] == roll:

                if float(student["cgpa"]) >= 6.0:

                    result_label.config(
                        text=(
                            "Name: " + student["name"] +
                            "\nCGPA: " + str(student["cgpa"]) +
                            "\n\nSTATUS: ELIGIBLE"
                        ),
                        fg=TEAL
                    )

                else:

                    result_label.config(
                        text=(
                            "Name: " + student["name"] +
                            "\nCGPA: " + str(student["cgpa"]) +
                            "\n\nSTATUS: NOT ELIGIBLE"
                        ),
                        fg=RED
                    )

                return


        result_label.config(
            text="Student not found.",
            fg=RED
        )


    tk.Button(
        window,
        text="Check Eligibility",
        width=20,
        height=2,
        font=("Arial", 12, "bold"),
        bg=TEAL,
        fg=WHITE,
        command=check
    ).pack(pady=10)

# =========================================================
# PROFESSIONAL PLACEMENT STATUS
# =========================================================

def placement_status():

    window = tk.Toplevel(root)
    window.title("Placement Status")
    window.geometry("700x650")
    window.configure(bg=BG_COLOR)
    window.resizable(False, False)

    tk.Label(
        window,
        text="📋 Placement Status",
        font=("Arial", 24, "bold"),
        bg=BG_COLOR,
        fg=TEXT_COLOR
    ).pack(pady=20)

    tk.Label(
        window,
        text="Enter Student Roll Number",
        font=("Arial", 12, "bold"),
        bg=BG_COLOR
    ).pack()

    roll_entry = tk.Entry(
        window,
        width=35,
        font=("Arial", 12)
    )
    roll_entry.pack(pady=8)

    tk.Label(
        window,
        text="Company Name",
        font=("Arial", 11, "bold"),
        bg=BG_COLOR
    ).pack()

    company_entry = tk.Entry(
        window,
        width=40,
        font=("Arial", 12)
    )
    company_entry.pack(pady=5)

    tk.Label(
        window,
        text="Job Role",
        font=("Arial", 11, "bold"),
        bg=BG_COLOR
    ).pack()

    role_entry = tk.Entry(
        window,
        width=40,
        font=("Arial", 12)
    )
    role_entry.pack(pady=5)

    tk.Label(
        window,
        text="Package / Salary",
        font=("Arial", 11, "bold"),
        bg=BG_COLOR
    ).pack()

    package_entry = tk.Entry(
        window,
        width=40,
        font=("Arial", 12)
    )
    package_entry.pack(pady=5)

    tk.Label(
        window,
        text="Application Status",
        font=("Arial", 11, "bold"),
        bg=BG_COLOR
    ).pack(pady=(8, 2))

    status_var = tk.StringVar(
        value="Applied"
    )

    status_menu = tk.OptionMenu(
        window,
        status_var,
        "Applied",
        "Shortlisted",
        "Selected",
        "Rejected"
    )

    status_menu.config(
        width=20,
        font=("Arial", 11)
    )

    status_menu.pack(pady=5)

    tk.Label(
        window,
        text="Joining Date",
        font=("Arial", 11, "bold"),
        bg=BG_COLOR
    ).pack(pady=(8, 2))

    joining_entry = tk.Entry(
        window,
        width=40,
        font=("Arial", 12)
    )
    joining_entry.pack(pady=5)

    result_label = tk.Label(
        window,
        text="",
        font=("Arial", 12),
        justify="left",
        bg=BG_COLOR
    )
    result_label.pack(pady=10)


    def update_placement():

        roll = roll_entry.get().strip()
        company = company_entry.get().strip()
        role = role_entry.get().strip()
        package = package_entry.get().strip()
        status = status_var.get()
        joining_date = joining_entry.get().strip()

        if roll == "":

            messagebox.showwarning(
                "Warning",
                "Please enter Roll Number."
            )

            return

        for student in students:

            if student["roll"] == roll:

                student["placement_status"] = status
                student["company"] = company
                student["job_role"] = role
                student["package"] = package
                student["joining_date"] = joining_date

                save_data()

                result_label.config(
                    text=(
                        "Student: " + student["name"] +
                        "\nRoll Number: " + roll +
                        "\nCompany: " + company +
                        "\nJob Role: " + role +
                        "\nPackage: " + package +
                        "\nApplication Status: " + status +
                        "\nJoining Date: " + joining_date
                    ),
                    fg=TEAL
                )

                messagebox.showinfo(
                    "Success",
                    "Placement information updated successfully!"
                )

                return

        messagebox.showwarning(
            "Not Found",
            "Student Roll Number not found."
        )


    tk.Button(
        window,
        text="💾 Update Placement",
        width=25,
        height=2,
        font=("Arial", 12, "bold"),
        bg=RED,
        fg=WHITE,
        command=update_placement
    ).pack(pady=10)



# =========================================================
# SEARCH JOBS
# =========================================================

def search_jobs():

    window = tk.Toplevel(root)
    window.title("Search Jobs")
    window.geometry("850x650")
    window.configure(bg=BG_COLOR)


    tk.Label(
        window,
        text="🔎 Search Jobs",
        font=("Arial", 24, "bold"),
        bg=BG_COLOR
    ).pack(pady=20)


    tk.Label(
        window,
        text="Search by Job Role or Skill",
        font=("Arial", 12, "bold"),
        bg=BG_COLOR
    ).pack()


    search_entry = tk.Entry(
        window,
        width=45,
        font=("Arial", 12)
    )

    search_entry.pack(pady=10)


    results_frame = tk.Frame(
        window,
        bg=BG_COLOR
    )

    results_frame.pack(
        fill="both",
        expand=True,
        padx=25,
        pady=15
    )


    def search():

        search_text = search_entry.get().strip().lower()

        for widget in results_frame.winfo_children():
            widget.destroy()


        if search_text == "":

            messagebox.showwarning(
                "Warning",
                "Please enter a job role or skill."
            )

            return


        if not os.path.exists(COMPANY_FILE):

            tk.Label(
                results_frame,
                text="No jobs available.",
                font=("Arial", 14, "bold"),
                bg=BG_COLOR
            ).pack(pady=30)

            return


        try:

            with open(COMPANY_FILE, "r") as file:
                jobs = json.load(file)

        except:

            jobs = []


        if isinstance(jobs, dict):
            jobs = [jobs]


        found = False


        for job in jobs:

            company = job.get("company", "")
            role = job.get("job_role", "")
            skills = job.get("skills", "")

            searchable = (
                company + " " +
                role + " " +
                skills
            ).lower()


            if search_text in searchable:

                found = True


                card = tk.Frame(
                    results_frame,
                    bg=WHITE,
                    bd=2,
                    relief="solid"
                )

                card.pack(
                    fill="x",
                    pady=8
                )


                tk.Label(
                    card,
                    text=company,
                    font=("Arial", 17, "bold"),
                    bg=WHITE
                ).pack(pady=(10, 2))


                tk.Label(
                    card,
                    text=role,
                    font=("Arial", 13, "bold"),
                    bg=WHITE
                ).pack()


                tk.Label(
                    card,
                    text="Skills: " + skills,
                    bg=WHITE
                ).pack(pady=3)


                tk.Label(
                    card,
                    text=(
                        "Type: " +
                        job.get("job_type", "") +
                        "   |   Mode: " +
                        job.get("work_mode", "")
                    ),
                    bg=WHITE
                ).pack()


                tk.Button(
                    card,
                    text="View Details / Apply",
                    bg=INDIGO,
                    fg=WHITE,
                    font=("Arial", 11, "bold"),
                    command=lambda j=job: show_job_details(j)
                ).pack(pady=10)


        if not found:

            tk.Label(
                results_frame,
                text="No matching jobs found.",
                font=("Arial", 14, "bold"),
                bg=BG_COLOR
            ).pack(pady=30)


    tk.Button(
        window,
        text="🔍 Search",
        width=20,
        height=2,
        font=("Arial", 12, "bold"),
        bg=INDIGO,
        fg=WHITE,
        command=search
    ).pack(pady=10)


# =========================================================
# JOB DETAILS + APPLY
# =========================================================

def show_job_details(job):

    window = tk.Toplevel(root)
    window.title("Job Details")
    window.geometry("650x650")
    window.configure(bg=BG_COLOR)


    tk.Label(
        window,
        text=job.get("company", ""),
        font=("Arial", 24, "bold"),
        bg=BG_COLOR
    ).pack(pady=20)


    details = (

        "Job Role: " + job.get("job_role", "") +
        "\n\nRequired Skills: " + job.get("skills", "") +
        "\n\nMinimum CGPA: " +
        str(job.get("minimum_cgpa", "")) +
        "\n\nJob Type: " +
        job.get("job_type", "") +
        "\n\nWork Mode: " +
        job.get("work_mode", "") +
        "\n\nWorking Time: " +
        job.get("working_time", "") +
        "\n\nDescription: " +
        job.get("description", "")

    )


    tk.Label(
        window,
        text=details,
        font=("Arial", 12),
        bg=BG_COLOR,
        justify="left",
        wraplength=550
    ).pack(pady=15)


    tk.Label(
        window,
        text="Enter Roll Number to Apply",
        font=("Arial", 12, "bold"),
        bg=BG_COLOR
    ).pack(pady=10)


    roll_entry = tk.Entry(
        window,
        width=35,
        font=("Arial", 12)
    )

    roll_entry.pack(pady=5)


    def apply_job():

        roll = roll_entry.get().strip()


        if roll == "":

            messagebox.showwarning(
                "Warning",
                "Please enter Roll Number."
            )

            return


        student_found = False


        for student in students:

            if student["roll"] == roll:

                student_found = True

                student_cgpa = float(student["cgpa"])

                required_cgpa = float(
                    job.get("minimum_cgpa", 0)
                )


                if student_cgpa < required_cgpa:

                    messagebox.showwarning(
                        "Not Eligible",
                        "Student CGPA is below the required CGPA."
                    )

                    return


                required_rolls = job.get(
                    "eligible_rolls",
                    ""
                ).strip()


                if required_rolls != "":

                    allowed_rolls = [
                        x.strip()
                        for x in required_rolls.split(",")
                    ]

                    if roll not in allowed_rolls:

                        messagebox.showwarning(
                            "Not Eligible",
                            "This Roll Number is not eligible for this job."
                        )

                        return


                applications = []


                if os.path.exists(APPLICATION_FILE):

                    try:

                        with open(
                            APPLICATION_FILE,
                            "r"
                        ) as file:

                            applications = json.load(file)

                    except:

                        applications = []


                application = {

                    "roll": roll,
                    "student_name": student["name"],
                    "company": job.get("company", ""),
                    "job_role": job.get("job_role", ""),
                    "status": "Applied"

                }


                applications.append(application)


                with open(
                    APPLICATION_FILE,
                    "w"
                ) as file:

                    json.dump(
                        applications,
                        file,
                        indent=4
                    )


                messagebox.showinfo(
                    "Application Submitted",
                    "Application successfully submitted!"
                )


                if job.get("apply_link", "").strip() != "":

                    try:
                        webbrowser.open(
                            job.get("apply_link")
                        )
                    except:
                        pass


                window.destroy()

                return


        if not student_found:

            messagebox.showwarning(
                "Not Found",
                "Student Roll Number not found."
            )


    tk.Button(
        window,
        text="📝 Apply Now",
        width=22,
        height=2,
        font=("Arial", 12, "bold"),
        bg=GREEN,
        fg=WHITE,
        command=apply_job
    ).pack(pady=20)


# =========================================================
# MY APPLICATIONS
# =========================================================

def my_applications():

    window = tk.Toplevel(root)
    window.title("My Applications")
    window.geometry("800x550")
    window.configure(bg=BG_COLOR)


    tk.Label(
        window,
        text="📝 My Applications",
        font=("Arial", 24, "bold"),
        bg=BG_COLOR
    ).pack(pady=25)


    tk.Label(
        window,
        text="Enter Student Roll Number",
        font=("Arial", 12, "bold"),
        bg=BG_COLOR
    ).pack()


    roll_entry = tk.Entry(
        window,
        width=35,
        font=("Arial", 12)
    )

    roll_entry.pack(pady=10)


    results_frame = tk.Frame(
        window,
        bg=BG_COLOR
    )

    results_frame.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=20
    )


    def show_applications():

        roll = roll_entry.get().strip()


        for widget in results_frame.winfo_children():
            widget.destroy()


        if roll == "":

            messagebox.showwarning(
                "Warning",
                "Please enter Roll Number."
            )

            return


        if not os.path.exists(APPLICATION_FILE):

            tk.Label(
                results_frame,
                text="No applications found.",
                font=("Arial", 14, "bold"),
                bg=BG_COLOR
            ).pack(pady=30)

            return


        try:

            with open(
                APPLICATION_FILE,
                "r"
            ) as file:

                applications = json.load(file)

        except:

            applications = []


        found = False


        for application in applications:

            if application.get("roll") == roll:

                found = True


                card = tk.Frame(
                    results_frame,
                    bg=WHITE,
                    bd=2,
                    relief="solid"
                )

                card.pack(
                    fill="x",
                    pady=8
                )


                tk.Label(
                    card,
                    text=application.get("company", ""),
                    font=("Arial", 16, "bold"),
                    bg=WHITE
                ).pack(pady=(10, 3))


                tk.Label(
                    card,
                    text=application.get("job_role", ""),
                    font=("Arial", 13, "bold"),
                    bg=WHITE
                ).pack()


                tk.Label(
                    card,
                    text="Status: " +
                    application.get("status", "Applied"),
                    font=("Arial", 11, "bold"),
                    bg=WHITE
                ).pack(pady=(5, 10))


        if not found:

            tk.Label(
                results_frame,
                text="No applications found for this Roll Number.",
                font=("Arial", 14, "bold"),
                bg=BG_COLOR
            ).pack(pady=30)


    tk.Button(
        window,
        text="View Applications",
        width=22,
        height=2,
        font=("Arial", 12, "bold"),
        bg=AMBER,
        fg=WHITE,
        command=show_applications
    ).pack(pady=15)

# =========================================================
# MODERN DASHBOARD
# =========================================================

root = tk.Tk()

root.title("Student Placement Management System")
root.geometry("1000x720")
root.resizable(False, False)
root.configure(bg=BG_COLOR)


# ---------- HEADER ----------

header = tk.Frame(
    root,
    bg=BG_COLOR
)
header.pack(fill="x", padx=35, pady=(25, 8))


# Logo

tk.Label(
    header,
    text="🎓",
    font=("Arial", 40),
    bg=BG_COLOR
).pack(side="left", padx=(0, 15))


# Title

title_box = tk.Frame(
    header,
    bg=BG_COLOR
)

title_box.pack(side="left")


tk.Label(
    title_box,
    text="Student Placement Management System",
    font=("Arial", 24, "bold"),
    bg=BG_COLOR,
    fg=TEXT_COLOR
).pack(anchor="w")


tk.Label(
    title_box,
    text="Build Your Future  |  Get Placed  |  Achieve Your Goals",
    font=("Arial", 11),
    bg=BG_COLOR,
    fg="#4169A1"
).pack(anchor="w", pady=(4, 0))


# ---------- WELCOME CARD ----------

welcome = tk.Frame(
    header,
    bg="#E5F0FF"
)

welcome.pack(
    side="right",
    ipadx=12,
    ipady=8
)


tk.Label(
    welcome,
    text="👤",
    font=("Arial", 25),
    bg="#E5F0FF"
).pack(side="left", padx=8)


welcome_text = tk.Frame(
    welcome,
    bg="#E5F0FF"
)

welcome_text.pack(side="left", padx=5)


tk.Label(
    welcome_text,
    text="Welcome",
    font=("Arial", 9),
    bg="#E5F0FF",
    fg="#4169A1"
).pack(anchor="w")


tk.Label(
    welcome_text,
    text="Sohil",
    font=("Arial", 15, "bold"),
    bg="#E5F0FF",
    fg=TEXT_COLOR
).pack(anchor="w")


tk.Label(
    welcome_text,
    text="BCA 2nd Year",
    font=("Arial", 9),
    bg="#E5F0FF",
    fg="#4169A1"
).pack(anchor="w")


# =========================================================
# DASHBOARD BUTTON AREA
# =========================================================

dashboard = tk.Frame(
    root,
    bg=BG_COLOR
)

dashboard.pack(
    padx=30,
    pady=10
)


# ---------- BUTTON CREATOR ----------

def dashboard_button(
    text,
    row,
    column,
    color,
    command
):

    button = tk.Button(
        dashboard,
        text=text,
        width=25,
        height=3,
        font=("Arial", 13, "bold"),
        bg=color,
        fg="white",
        activebackground=color,
        activeforeground="white",
        bd=0,
        relief="flat",
        cursor="hand2",
        command=command
    )

    button.grid(
        row=row,
        column=column,
        padx=9,
        pady=8
    )


# =========================================================
# MAIN OPTIONS
# =========================================================

dashboard_button(
    "➕  Add Student",
    0, 0,
    "#16A34A",
    add_student
)


dashboard_button(
    "👨‍🎓  View Students",
    0, 1,
    "#2563EB",
    view_students
)


dashboard_button(
    "🔍  Search Student",
    0, 2,
    "#7C3AED",
    search_student
)


dashboard_button(
    "🏢  Company Details",
    1, 0,
    "#EA580C",
    company_details
)


dashboard_button(
    "✅  Check Eligibility",
    1, 1,
    "#0D9488",
    check_eligibility
)


dashboard_button(
    "📋  Placement Status",
    1, 2,
    "#DC2626",
    placement_status
)


dashboard_button(
    "🔎  Search Jobs",
    2, 0,
    "#4F46E5",
    search_jobs
)


dashboard_button(
    "📝  My Applications",
    2, 1,
    "#D97706",
    my_applications
)


dashboard_button(
    "🚪  Exit",
    2, 2,
    "#374151",
    root.destroy
)


# =========================================================
# QUICK OVERVIEW
# =========================================================

overview = tk.Frame(
    root,
    bg=WHITE,
    bd=1,
    relief="solid"
)

overview.pack(
    fill="x",
    padx=40,
    pady=(8, 5)
)


tk.Label(
    overview,
    text="📊  Quick Overview",
    font=("Arial", 16, "bold"),
    bg=WHITE,
    fg=TEXT_COLOR
).pack(
    anchor="w",
    padx=20,
    pady=(10, 6)
)


stats = tk.Frame(
    overview,
    bg=WHITE
)

stats.pack(
    fill="x",
    padx=12,
    pady=(0, 12)
)


# ---------- STAT BOX ----------

def create_stat(
    parent,
    title,
    value,
    color
):

    box = tk.Frame(
        parent,
        bg="#F5F8FC",
        width=205,
        height=65
    )

    box.pack(
        side="left",
        padx=7
    )

    box.pack_propagate(False)


    tk.Label(
        box,
        text=title,
        font=("Arial", 9),
        bg="#F5F8FC",
        fg=color
    ).pack(
        anchor="w",
        padx=12,
        pady=(7, 0)
    )


    tk.Label(
        box,
        text=value,
        font=("Arial", 18, "bold"),
        bg="#F5F8FC",
        fg=TEXT_COLOR
    ).pack(
        anchor="w",
        padx=12
    )


# Total Students

create_stat(
    stats,
    "Total Students",
    str(len(students)),
    "#2563EB"
)


# Placed Students

placed_count = 0

for student in students:

    if student.get("placement_status") == "Placed":
        placed_count += 1


create_stat(
    stats,
    "Placed Students",
    str(placed_count),
    "#16A34A"
)


# Applications

try:

    with open(APPLICATION_FILE, "r") as file:
        applications = json.load(file)

    application_count = len(applications)

except:

    application_count = 0


create_stat(
    stats,
    "Applications",
    str(application_count),
    "#7C3AED"
)


# Companies

try:

    with open(COMPANY_FILE, "r") as file:
        companies = json.load(file)

    company_count = len(companies)

except:

    company_count = 0


create_stat(
    stats,
    "Companies",
    str(company_count),
    "#EA580C"
)


# =========================================================
# FOOTER
# =========================================================

tk.Label(
    root,
    text="© 2026 Student Placement Management System | Made with ❤️ for Better Careers",
    font=("Arial", 9),
    bg=BG_COLOR,
    fg="#5B7BB2"
).pack(pady=5)


# =========================================================
# START
# =========================================================

root.mainloop()


# Add Student

tk.Button(
    dashboard,
    text="➕ Add Student",
    width=25,
    height=2,
    font=("Arial", 12, "bold"),
    bg=GREEN,
    fg=WHITE,
    command=add_student
).grid(row=0, column=0, padx=20, pady=12)

d
# View Students

tk.Button(
    dashboard,
    text="👨‍🎓 View Students",
    width=25,
    height=2,
    font=("Arial", 12, "bold"),
    bg=BLUE,
    fg=WHITE,
    command=view_students
).grid(row=0, column=1, padx=20, pady=12)


# Search Student

tk.Button(
    dashboard,
    text="🔍 Search Student",
    width=25,
    height=2,
    font=("Arial", 12, "bold"),
    bg=PURPLE,
    fg=WHITE,
    command=search_student
).grid(row=1, column=0, padx=20, pady=12)


# Company Details

tk.Button(
    dashboard,
    text="🏢 Company Details",
    width=25,
    height=2,
    font=("Arial", 12, "bold"),
    bg=ORANGE,
    fg=WHITE,
    command=company_details
).grid(row=1, column=1, padx=20, pady=12)


# Check Eligibility

tk.Button(
    dashboard,
    text="✅ Check Eligibility",
    width=25,
    height=2,
    font=("Arial", 12, "bold"),
    bg=TEAL,
    fg=WHITE,
    command=check_eligibility
).grid(row=2, column=0, padx=20, pady=12)


# Placement Status

tk.Button(
    dashboard,
    text="📋 Placement Status",
    width=25,
    height=2,
    font=("Arial", 12, "bold"),
    bg=RED,
    fg=WHITE,
    command=placement_status
).grid(row=2, column=1, padx=20, pady=12)


# Search Jobs

tk.Button(
    dashboard,
    text="🔎 Search Jobs",
    width=25,
    height=2,
    font=("Arial", 12, "bold"),
    bg=INDIGO,
    fg=WHITE,
    command=search_jobs
).grid(row=3, column=0, padx=20, pady=12)


# My Applications

tk.Button(
    dashboard,
    text="📝 My Applications",
    width=25,
    height=2,
    font=("Arial", 12, "bold"),
    bg=AMBER,
    fg=WHITE,
    command=my_applications
).grid(row=3, column=1, padx=20, pady=12)


# Exit

tk.Button(
    root,
    text="🚪 Exit",
    width=20,
    height=2,
    font=("Arial", 12, "bold"),
    bg=DARK_GREY,
    fg=WHITE,
    command=root.destroy
).pack(pady=30)


# =========================================================
# START APPLICATION
# =========================================================

root.mainloop()
