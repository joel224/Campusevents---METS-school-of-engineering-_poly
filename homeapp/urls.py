from django.urls import path
from . import views

urlpatterns = [

    path('',views.index, name='home'),
    path('logout/',views.logout,name='logout'),
    

    #admin
    path('event-success/', views.event_success, name='event_success'),
    path('adminindex/',views.adminindex, name='adminindex'),
    path('adminlogin/',views.adminlogin, name='adminlogin'),
    path('adminfeedbackview/',views.adminfeedbackview, name='adminfeedbackview'),
    path('adminstafflist/',views.adminstafflist, name='adminstafflist'),
    #student view for admin
    path('admintudentlist/',views.admintudentlist, name='admintudentlist'),
    #To view upcoming Events for Admin
    path('admineventview/',views.admineventview, name='admineventview'),
    #to view judge for Admin
    path('adminjudgeview/', views.adminjudgeview, name='adminjudgeview'),
    #To view completed events for admin
    path('adminevent_completed_view/', views.adminevent_completed_view,name='adminevent_completed_view'),
    path('eventsdelete/<int:id>/',views.eventsdelete, name='eventsdelete'),
    #Edit Events for upcoming events
    path('editevents/<int:event_id>/', views.editevents, name='editevents'),
    #Allocate Staff
    path('adminstaffallocate/', views.adminstaffallocate, name='adminstaffallocate'),
    #view assigned staff
    path('adminassignedstaff/',views.adminassignedstaff, name='adminassignedstaff'),
    path('adminvieweventplayer/', views.adminvieweventplayer, name='adminvieweventplayer'),

    #allocate Judge to events
    path('adminjudgeallocate/',views.adminjudgeallocate, name='adminjudgeallocate'),
    #to fetch the details of judge in assigning judge
    path('get_judge_details/', views.get_judge_details, name='get_judge_details'),

    #To view payment history of students by admin
    path('paymenthistoryadmin/',views.paymenthistoryadmin, name='paymenthistoryadmin'),
    
   



    #staff
    path('staffregister/',views.staff_register, name='staffregister' ),
    path('stafflogin/',views.staff_login, name='stafflogin'),
    path('staffprofile/', views.staff_profile, name='staffprofile'),
    path('staffprofileupdate/',views.staffprofile_update, name='staffprofileupdate'),
    path('delete_staff/',views.delete_staff, name='delete_staff'),
    path('staffconfirmdelete/<int:id>/',views.staffconfirmdelete,name='staffconfirmdelete'),
    path('staffindex/',views.staffindex, name='staffindex'),
    #path('staff_organizerlist/',views.staff_organizerlist,name='staff_organizerlist'),
    path('staffstudentlist/',views.staffstudentlist, name='staffstudentlist'),
    # Work assigned by admin to staff
    path('staffworkedassigned/',views.staffworkedassigned, name='staffworkedassigned'),
    #Upcoming events for staff
    path('staffeventview/', views.staffeventview, name='staffeventview'),
   
    path('assign_event_student/', views.admin_event_allocation, name='assign_event_to_student'),
    #To view judge for staff:
    path('staffjudgeview/', views.staffjudgeview, name='staffjudgeview'),
    # to view payment history for the staff
    path('paymenthistorystaff/', views.paymenthistorystaff, name='paymenthistorystaff'),
    path('staffresultview/', views.staffresultview, name='staffresultview'),
    #staff can view feedback of student
    path('staffstudentfeedback/', views.staffstudentfeedback, name='staffstudentfeedback'),

    

    #student
    path('studentindex/',views.studentindex, name='studentindex'),
    path('studentregister/',views.student_register,name='student_register'),
    path('ai/', views.ai, name='create_event'),
    path('check_date_conflict/', views.check_date_conflict, name='check_date_conflict'),
    path('create-event/',views.ai,name='create_event'),
    path('studentlogin/',views.student_login,name='studentlogin'),
    path('studentprofile/',views.student_profile, name='studentprofile'),
    path('studentprofile-update/',views.studentprofile_update, name='studentprofile-update'),
    path('studentdelete/', views.delete_student, name='studentdelete'),
    path('studentconfirmdelete/<int:id>/', views.studentconfirmdelete, name='studentconfirmdelete'),
    path('student_feedbacksubmit/',views.student_feedbacksubmit,name='student_feedbacksubmit'),
    path('feedbacksuccess/',views.feedbacksuccess,name='feedbacksuccess'),
    path('studentstafflist/',views.studentstafflist,name='studentstafflist'),
    #path('studentorganizerlist/',views.studentorganizerlist, name='studentorganizerlist'),
    path('studentviewevent/',views.studentshowevents,name='studentviewevent'),
    path('student_bookings/',views.student_bookings,name='student_bookings'),

    path('student_event_assignments/', views.student_event_assignments, name='student_event_assignments'),
    #Add Events
    path('addevents/',views.addevents, name='addevents'),
    #to Book the event for student
    path('book_event/<int:event_id>/', views.book_event, name='book_event'),
    #total view of events:
    path('studenteventviewstotal/', views.studenteventviewstotal, name='studenteventviewstotal'),
    #total view of judge for students:
    path('studentsjudgeview/', views.studentsjudgeview, name='studentsjudgeview'),
    # to show the winner for students
    path('event_winners_view/', views.event_winners_view, name='event_winners_view'),
    #student payment history
    path('student_payment_history/',views.student_payment_history, name='student_payment_history'),
    



    #judgement
    path('judgeindex/',views.judgeindex, name='judgeindex'),
    path('judgeregisteration/',views.judgeregisteration,name='judgeregisteration'),
    path('judgelogin/',views.judgelogin, name='judgelogin'),
    path('judgeprofile/',views.judgeprofile, name='judgeprofile'),
    path('judgeupdate/',views.judgeprofile_update, name='judgeprofile_update'),
    path('delete_judge/', views.delete_judge, name='delete_judge'),
    path('judgeconfirmdelete/<int:id>/',views.judgeconfirmdelete, name='judgeconfirmdelete'),
    path('judgestaffview/',views.judgestaffview, name='judgestaffview'),
    path('judgestudentview/',views.judgestudentview, name='judgestudentview'),
    #view assigned events
    path('judge/assigned_events/', views.judge_assigned_events, name='judge_assigned_events'),
    path('judgeeventsviews/', views.judgeeventsviews, name='judgeeventsviews'),

     path('award_prizes/<int:event_id>/', views.award_prizes, name='award_prizes'),

     #Result page for Judge:
     path('resultforjudge/',views.resultforjudge,name='resultforjudge'),



    #payment
    
    path('initiate-payment/<int:cid>/', views.initiate_payment, name='initiate_payment'),
    path('confirm-payment/<int:cid>/<str:order_id>/<str:payment_id>/<str:signature>/', views.confirm_payment, name='confirm_payment'), 
]
