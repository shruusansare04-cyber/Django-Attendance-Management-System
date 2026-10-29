
from django.urls import path
from . import views


urlpatterns = [

    # =========================
    # Home
    # =========================

    path(
        "",
        views.home,
        name="home"
    ),


    # =========================
    # Login / Logout
    # =========================

    path(
        "login/",
        views.login_view,
        name="login"
    ),

    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),


    # =========================
    # Dashboards
    # =========================

    path(
        "dashboard/",
        views.dashboard,
        name="dashboard"
    ),

    path(
        "student-dashboard/",
        views.student_dashboard,
        name="student_dashboard"
    ),

    path(
        "teacher-dashboard/",
        views.teacher_dashboard,
        name="teacher_dashboard"
    ),

    path(
        "admin-dashboard/",
        views.admin_dashboard,
        name="admin_dashboard"
    ),


    # =========================
    # Student
    # =========================

    path(
        "add-student/",
        views.add_student,
        name="add_student"
    ),

    path(
        "students/",
        views.student_list,
        name="student_list"
    ),


    # =========================
    # Teacher
    # =========================

    path(
        "add-teacher/",
        views.add_teacher,
        name="add_teacher"
    ),

    path(
        "teachers/",
        views.teacher_list,
        name="teacher_list"
    ),

    path(
        "teacher/<int:teacher_id>/",
        views.teacher_detail,
        name="teacher_detail"
    ),

    path(
        "teacher/<int:teacher_id>/edit/",
        views.edit_teacher,
        name="edit_teacher"
    ),

    path(
        "teacher/<int:teacher_id>/delete/",
        views.delete_teacher,
        name="delete_teacher"
    ),


    # =========================
    # Subject
    # =========================

    path(
        "add-subject/",
        views.add_subject,
        name="add_subject"
    ),

    path(
        "subjects/",
        views.subject_list,
        name="subject_list"
    ),

    path(
        "subject/<int:subject_id>/",
        views.subject_detail,
        name="subject_detail"
    ),

    path(
        "subject/<int:subject_id>/edit/",
        views.edit_subject,
        name="edit_subject"
    ),

    path(
        "subject/<int:subject_id>/delete/",
        views.delete_subject,
        name="delete_subject"
    ),


    # =========================
    # Attendance
    # =========================

    path(
        "attendance/",
        views.mark_attendance,
        name="mark_attendance"
    ),

    path(
        "attendance-list/",
        views.attendance_list,
        name="attendance_list"
    ),

    path(
        "attendance/<int:attendance_id>/edit/",
        views.edit_attendance,
        name="edit_attendance"
    ),

    path(
        "attendance/<int:attendance_id>/delete/",
        views.delete_attendance,
        name="delete_attendance"
    ),

    path(
        "attendance-percentage/",
        views.attendance_percentage,
        name="attendance_percentage"
    ),

    path(
        "subject-wise-attendance/",
        views.subject_wise_attendance,
        name="subject_wise_attendance"
    ),
]

