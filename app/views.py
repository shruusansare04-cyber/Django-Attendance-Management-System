from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Student, Teacher, Subject, Attendance, UserProfile


# ==================== HOME ====================

def home(request):
    return render(request, "home.html")


# ==================== LOGIN ====================

def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("dashboard")

        messages.error(request, "Invalid username or password.")

    return render(request, "login.html")


# ==================== LOGOUT ====================

@login_required
def logout_view(request):
    logout(request)
    return redirect("login")


# ==================== MAIN DASHBOARD ====================

@login_required
def dashboard(request):
    try:
        profile = UserProfile.objects.get(user=request.user)

        if profile.role == "student":
            return redirect("student_dashboard")

        if profile.role == "teacher":
            return redirect("teacher_dashboard")

        if profile.role == "admin":
            return redirect("admin_dashboard")

    except UserProfile.DoesNotExist:
        if request.user.is_superuser:
            return redirect("admin_dashboard")

    return redirect("home")


# ==================== STUDENT MANAGEMENT ====================

@login_required
def add_student(request):
    if request.method == "POST":
        name = request.POST.get("name")
        roll_no = request.POST.get("roll_no")
        email = request.POST.get("email")
        course = request.POST.get("course")

        Student.objects.create(
            name=name,
            roll_no=roll_no,
            email=email,
            course=course
        )

        messages.success(request, "Student added successfully.")
        return redirect("student_list")

    return render(request, "student.html")


@login_required
def student_list(request):
    students = Student.objects.all().order_by("roll_no")

    return render(
        request,
        "student_list.html",
        {"students": students}
    )


# ==================== STUDENT DASHBOARD ====================

@login_required
def student_dashboard(request):
    student = Student.objects.filter(user=request.user).first()

    total = 0
    present = 0
    percentage = 0

    if student:
        records = Attendance.objects.filter(student=student)
        total = records.count()
        present = records.filter(status=True).count()

        if total > 0:
            percentage = round((present / total) * 100, 2)

    return render(
        request,
        "student_dashboard.html",
        {
            "student": student,
            "total": total,
            "present": present,
            "percentage": percentage
        }
    )


# ==================== TEACHER MANAGEMENT ====================

@login_required
def add_teacher(request):
    subjects = Subject.objects.all()

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject_id = request.POST.get("subject")

        teacher = Teacher.objects.create(
            name=name,
            email=email
        )

        if subject_id:
            subject = get_object_or_404(Subject, id=subject_id)
            teacher.subjects.add(subject)

        messages.success(request, "Teacher added successfully.")
        return redirect("teacher_list")

    return render(
        request,
        "teacher.html",
        {"subjects": subjects}
    )


@login_required
def teacher_list(request):
    teachers = Teacher.objects.all()

    return render(
        request,
        "teachers.html",
        {"teachers": teachers}
    )


@login_required
def teacher_detail(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)

    return render(
        request,
        "teacher_detail.html",
        {"teacher": teacher}
    )


@login_required
def edit_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    subjects = Subject.objects.all()

    if request.method == "POST":
        teacher.name = request.POST.get("name")
        teacher.email = request.POST.get("email")
        teacher.save()

        subject_id = request.POST.get("subject")
        teacher.subjects.clear()

        if subject_id:
            subject = get_object_or_404(Subject, id=subject_id)
            teacher.subjects.add(subject)

        messages.success(request, "Teacher updated successfully.")
        return redirect("teacher_detail", teacher_id=teacher.id)

    return render(
        request,
        "edit_teacher.html",
        {
            "teacher": teacher,
            "subjects": subjects
        }
    )


@login_required
def delete_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)

    if request.method == "POST":
        teacher.delete()
        messages.success(request, "Teacher deleted successfully.")
        return redirect("teacher_list")

    return render(
        request,
        "delete_teacher.html",
        {"teacher": teacher}
    )


# ==================== TEACHER DASHBOARD ====================

@login_required
def teacher_dashboard(request):
    teacher = Teacher.objects.filter(
        email=request.user.email
    ).first()

    student_count = Student.objects.count()
    subject_count = teacher.subjects.count() if teacher else 0
    attendance_count = Attendance.objects.count()

    return render(
        request,
        "teacher_dashboard.html",
        {
            "teacher": teacher,
            "student_count": student_count,
            "subject_count": subject_count,
            "attendance_count": attendance_count
        }
    )


# ==================== SUBJECT MANAGEMENT ====================

@login_required
def add_subject(request):
    if request.method == "POST":
        name = request.POST.get("name")
        code = request.POST.get("code")

        Subject.objects.create(
            name=name,
            code=code
        )

        messages.success(request, "Subject added successfully.")
        return redirect("subject_list")

    return render(request, "add_subject.html")


@login_required
def subject_list(request):
    subjects = Subject.objects.all()

    return render(
        request,
        "subjects.html",
        {"subjects": subjects}
    )


@login_required
def subject_detail(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)

    return render(
        request,
        "subject_detail.html",
        {"subject": subject}
    )


@login_required
def edit_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)

    if request.method == "POST":
        subject.name = request.POST.get("name")
        subject.code = request.POST.get("code")
        subject.save()

        messages.success(request, "Subject updated successfully.")
        return redirect("subject_detail", subject_id=subject.id)

    return render(
        request,
        "edit_subject.html",
        {"subject": subject}
    )


@login_required
def delete_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)

    if request.method == "POST":
        subject.delete()
        messages.success(request, "Subject deleted successfully.")
        return redirect("subject_list")

    return render(
        request,
        "delete_subject.html",
        {"subject": subject}
    )


# ==================== MARK ATTENDANCE ====================

@login_required
def mark_attendance(request):
    students = Student.objects.all()
    subjects = Subject.objects.all()

    if request.method == "POST":
        student_id = request.POST.get("student")
        subject_id = request.POST.get("subject")
        date = request.POST.get("date")
        status = request.POST.get("status")

        student = get_object_or_404(Student, id=student_id)
        subject = get_object_or_404(Subject, id=subject_id)

        Attendance.objects.create(
            student=student,
            subject=subject,
            date=date,
            status=(status == "present")
        )

        messages.success(request, "Attendance saved successfully.")
        return redirect("attendance_list")

    return render(
        request,
        "mark_attendance.html",
        {
            "students": students,
            "subjects": subjects
        }
    )


# ==================== ATTENDANCE LIST ====================

@login_required
def attendance_list(request):
    attendance_records = Attendance.objects.select_related(
        "student",
        "subject"
    ).order_by("-date")

    return render(
        request,
        "attendance_list.html",
        {"attendance_records": attendance_records}
    )


# ==================== EDIT ATTENDANCE ====================

@login_required
def edit_attendance(request, attendance_id):
    attendance = get_object_or_404(Attendance, id=attendance_id)
    students = Student.objects.all()
    subjects = Subject.objects.all()

    if request.method == "POST":
        student_id = request.POST.get("student")
        subject_id = request.POST.get("subject")
        date = request.POST.get("date")
        status = request.POST.get("status")

        attendance.student = get_object_or_404(
            Student,
            id=student_id
        )

        attendance.subject = get_object_or_404(
            Subject,
            id=subject_id
        )

        attendance.date = date
        attendance.status = (status == "present")
        attendance.save()

        messages.success(request, "Attendance updated successfully.")
        return redirect("attendance_list")

    return render(
        request,
        "edit_attendance.html",
        {
            "attendance": attendance,
            "students": students,
            "subjects": subjects
        }
    )


# ==================== DELETE ATTENDANCE ====================

@login_required
def delete_attendance(request, attendance_id):
    attendance = get_object_or_404(Attendance, id=attendance_id)

    if request.method == "POST":
        attendance.delete()
        messages.success(request, "Attendance deleted successfully.")
        return redirect("attendance_list")

    return render(
        request,
        "delete_attendance.html",
        {"attendance": attendance}
    )


# ==================== ATTENDANCE PERCENTAGE ====================

@login_required
def attendance_percentage(request):
    students = Student.objects.all()
    attendance_data = []

    for student in students:
        records = Attendance.objects.filter(student=student)
        total = records.count()
        present = records.filter(status=True).count()

        percentage = round((present / total) * 100, 2) if total else 0

        attendance_data.append({
            "student": student,
            "total": total,
            "present": present,
            "percentage": percentage
        })

    return render(
        request,
        "attendance_percentage.html",
        {"attendance_data": attendance_data}
    )


# ==================== SUBJECT-WISE ATTENDANCE ====================

@login_required
def subject_wise_attendance(request):
    students = Student.objects.all()
    subjects = Subject.objects.all()
    data = []

    for student in students:
        for subject in subjects:
            records = Attendance.objects.filter(
                student=student,
                subject=subject
            )

            total = records.count()
            present = records.filter(status=True).count()

            percentage = round((present / total) * 100, 2) if total else 0

            data.append({
                "student": student,
                "subject": subject,
                "total": total,
                "present": present,
                "percentage": percentage
            })

    return render(
        request,
        "subject_wise_attendance.html",
        {"data": data}
    )


# ==================== ADMIN DASHBOARD ====================

@login_required
def admin_dashboard(request):
    student_count = Student.objects.count()
    teacher_count = Teacher.objects.count()
    subject_count = Subject.objects.count()
    attendance_count = Attendance.objects.count()

    return render(
        request,
        "admin_dashboard.html",
        {
            "student_count": student_count,
            "teacher_count": teacher_count,
            "subject_count": subject_count,
            "attendance_count": attendance_count
        }
    )
