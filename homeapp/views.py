from django.shortcuts import render,redirect,HttpResponse, get_object_or_404
from .models import staff_Registration, student_Registration,Feedback, createevents,staffallocate,events_participants,Payment,Prize,judgeallocate,studentallocation
from django.contrib import messages
import razorpay
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

#logout 
def logout(request):
    request.session.flush()
    return redirect('/')


#Admin----------------------------------------------------------------------------------------------------------------------------

# admin index
def adminindex(request):
    current_date = timezone.now().date()
    staff_count = staff_Registration.objects.count()
    student_count=student_Registration.objects.count()
    events = createevents.objects.filter( rend__gte=current_date).count()
    judge=judgeregister.objects.count()
    context={
        'staff_count':staff_count,
        'student_count':student_count,
        'events':events,
        'judge':judge
    }
    return render(request,'adminindex.html',context)

def adminjudgeview(request):
    judge=judgeregister.objects.all()
    return render(request,'adminjudgeview.html',{'judge':judge})

#admin login
def adminlogin(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user='admin'
        userpass='kgadmin321'
        if username== user and password==userpass:
            return redirect('adminindex')
        else:
            alert="<script>alert('Email or password is Incorrect');window.location.href='/adminlogin/';</script>"
            return HttpResponse(alert)
    return render(request,'adminlogin.html')

def adminfeedbackview(request):
    user=Feedback.objects.all()
    return render(request,'adminfeedbackview.html',{'user':user})


#create events
# Admin Events Creation Page:
from datetime import datetime

def addevents(request):
    if request.method =='POST':
        event_category= request.POST.get('event_category')
        version=request.POST.get('version')
        event_name=request.POST.get('event_name')
        events_description=request.POST.get('events_description')
        amount=request.POST.get('amount')
        image=request.FILES.get('image')
        doe=request.POST.get('doe')
        rend=request.POST.get('rend')
        resultdate=request.POST.get('resultdate')
        try:
            doe = datetime.strptime(doe, '%Y-%m-%d').date()  # Make sure the date format matches your input
            rend = datetime.strptime(rend, '%Y-%m-%d').date()
            resultdate = datetime.strptime(resultdate, '%Y-%m-%d').date()
        except ValueError:
            # Return an error if date conversion fails (handle invalid date format)
            alert="<script>alert('Invalid date format. Please use YYYY-MM-DD.');window.location.href='/addevents/';</script>"
            return HttpResponse(alert)

        # Check if the doe (date of event) is unique
        if createevents.objects.filter(doe=doe).exists():
            # If the date already exists, return an error message
            alert="<script>alert('An event already exists on this date.');window.location.href='/addevents/';</script>"
            return HttpResponse(alert)

        user=createevents(event_category=event_category,version=version,event_name=event_name,events_description=events_description,
                          amount=amount,image=image,doe=doe,rend=rend,resultdate=resultdate)
        user.save()
        return render(request,'Eventaddedsuccess.html')
    return render(request,'admincreateevent.html')

# to view the upcoming events
def admineventview(request):
    current_date = timezone.now().date()
    events = createevents.objects.filter( rend__gte=current_date)
    return render(request,'adminviewevent.html', {'events': events})

# to view the completed events
def adminevent_completed_view(request):
    current_date = timezone.now().date()
    events = createevents.objects.filter( doe__lt=current_date)
    return render(request,'admineventscompleted.html', {'events': events})

#delete events
def eventsdelete(request, id):
    events=createevents.objects.get(id=id)
    events.delete()
    alert="<script>alert('Events Deleted Successfully');window.location.href='/adminevent_completed_view/';</script>"
    return HttpResponse(alert)

#payment History for Admin:
def paymenthistoryadmin(request):
    # Get the payment_id from the GET request (search term)
    payment_id = request.GET.get('payment_id', '')  # Default to an empty string if no ID is provided
    
    # If a payment_id is provided, filter payments by that ID
    if payment_id:
        data = Payment.objects.filter(razorpay_payment_id__icontains=payment_id).order_by('-created_at')
    else:
        # Get all payments and order by created_at descending to show latest first
        data = Payment.objects.all().order_by('-created_at')

    return render(request, 'paymenthistoryadmin.html', {'data': data})


#Edit Events
def editevents(request,event_id):
    # Fetch all available event categories
    event_categories = get_object_or_404(createevents, id=event_id)

    if request.method == 'POST':

        # Retrieve form data
        event_category = request.POST.get('event_category')
        version = request.POST.get('version')
        event_name = request.POST.get('event_name')
        events_description = request.POST.get('events_description')
        amount = request.POST.get('amount')
        image = request.FILES.get('image')
        doe = request.POST.get('doe')
        rend = request.POST.get('rend')
        resultdate = request.POST.get('resultdate')

        event_categories.event_category=event_category
        event_categories.version=version
        event_categories.event_name=event_name
        event_categories.events_description=events_description
        if amount:
            event_categories.amount=amount
        if image:
            event_categories.image=image
        event_categories.doe=doe
        event_categories.rend=rend
        event_categories.resultdate=resultdate
        

        # Convert 'amount' to an integer (or float depending on your field definition)
        amount = int(amount) if amount else None
        try:
            doe = datetime.strptime(doe, '%Y-%m-%d').date()  # Make sure the date format matches your input
            rend = datetime.strptime(rend, '%Y-%m-%d').date()
            resultdate = datetime.strptime(resultdate, '%Y-%m-%d').date()
        except ValueError:
            # Return an error if date conversion fails (handle invalid date format)
            alert="<script>alert('Invalid date format. Please use YYYY-MM-DD.');window.location.href='/addevents/';</script>"
            return HttpResponse(alert)

        # Check if the doe (date of event) is unique
        if createevents.objects.filter(doe=doe).exists():
            # If the date already exists, return an error message
            alert="<script>alert('An event already exists on this date.');window.location.href='/addevents/';</script>"
            return HttpResponse(alert)        

        # Save the event to the database
        event_categories.save()

        # Show success message and redirect
        messages.success(request, "Event Updated successfully!")
        return redirect('admineventview')  # Redirect to event list or event success page

    return render(request, 'editevents.html',{'event_categories': event_categories})

# Allocate staff:
def adminstaffallocate(request):
    if request.method == 'POST':
        staff_id = request.POST.get('staffname')
        event_id = request.POST.get('event_details')
        msg = request.POST.get('msg')

        # Fetch the selected staff and event objects using their IDs
        staff = staff_Registration.objects.get(id=staff_id)
        event = createevents.objects.get(id=event_id)

        # Create a new staff allocation
        allocation = staffallocate(
            staffname=staff,
            event_details=event,
            msg=msg
        )
        allocation.save()
        alert="<script>alert('Staff assign to event successfully!');window.location.href='/adminindex/'</script>"
        return HttpResponse(alert)

    # Get the list of staff members and events to populate the dropdowns
    staff_list = staff_Registration.objects.all()
    event_list = createevents.objects.all()

    # Pass the staff and event lists to the template
    return render(request, 'adminstaffallocate.html', {
        'staff_list': staff_list,
        'event_list': event_list
    })


#view assigned staff for admin:
def adminassignedstaff(request):
    
    current_date = timezone.now().date()
    user=staffallocate.objects.filter(event_details__rend__gte=current_date)
    return render(request,'assignedviewstaff.html',{'user':user})

#Full Staff Details for admin View Only:
def adminstafflist(request):
    user=staff_Registration.objects.all()
    return render(request,'adminstafflist.html',{'user':user})


#Allocate Judge for the events:

def adminjudgeallocate(request):
    if request.method == 'POST':
        judge_id = request.POST.get('jname')
        event_id = request.POST.get('event_details')
        msg = request.POST.get('msg')

        # Fetch the selected judge and event objects using their IDs
        try:
            judge = judgeregister.objects.get(id=judge_id)
            event = createevents.objects.get(id=event_id)
        except judgeregister.DoesNotExist:
            return HttpResponse("<script>alert('Judge not found!');window.location.href='/adminindex/'</script>")
        except createevents.DoesNotExist:
            return HttpResponse("<script>alert('Event not found!');window.location.href='/adminindex/'</script>")

        # Create a new staff allocation
        allocation = judgeallocate(
            judgename=judge,
            event_details=event,
            msg=msg
        )
        allocation.save()
        alert = "<script>alert('Judge assigned to event successfully!');window.location.href='/adminindex/'</script>"
        return HttpResponse(alert)

    # Get the list of judges and events to populate the dropdowns
    judge_list = judgeregister.objects.all()
    event_list = createevents.objects.all()

    # Pass the judge and event lists to the template
    return render(request, 'adminsjudgeallocate.html', {
        'judge_list': judge_list,
        'event_list': event_list
    })

#to fetch the details of judge
def get_judge_details(request):
    judge_id = request.GET.get('judge_id')  # Fetch the judge_id from the query string
    
    try:
        # Fetch the judge from the database
        judge = judgeregister.objects.get(id=judge_id)
        
        # Create a dictionary with the judge details
        judge_details = {
            'qualification': judge.qualification,
            'experience': judge.experience,
            'dob': judge.dob,
            'gender': judge.gender,
            'email': judge.email,
            'profilepic': judge.profilepic.url if judge.profilepic else '',
        }

        # Return the judge details as a JSON response
        return JsonResponse({'status': 'success', 'judge_details': judge_details})

    except judgeregister.DoesNotExist:
        # Handle case where the judge is not found
        return JsonResponse({'status': 'error', 'message': 'Judge not found'})

#Full Student Details for admin view only:
def admintudentlist(request):
    user=student_Registration.objects.all()
    return render(request,'adminstudentlist.html',{'user':user})



# View students participated:

from datetime import timedelta


from django.shortcuts import render
from .models import createevents, events_participants
from django.utils import timezone

def adminvieweventplayer(request):
    # Fetch search query parameters
    search_booking_number = request.GET.get('booking_number', '')
    
    # Fetch all participants, if no search term is provided
    participants = events_participants.objects.all()
    
    # If search term for booking_number is provided, filter by it
    if search_booking_number:
        participants = participants.filter(booking_number__icontains=search_booking_number)
    
    
    # Create a dictionary of events with their participants
    event_participants = {}
    for participant in participants:
        event = participant.events
        if event not in event_participants:
            event_participants[event] = []
        event_participants[event].append(participant)
    
    # Fetch all events (for rendering event names and categories)
    events = createevents.objects.all()

    return render(request, 'admin-events-booked-view.html', {
        'event_participants': event_participants,
        'events': events,
        'search_booking_number': search_booking_number
    })

#Booking Details view for students
def student_bookings(request):
    # Fetch the logged-in student's email from session
    student_email = request.session.get('email')
    if not student_email:
        messages.error(request, "You must be logged in to view your bookings.")
        return redirect('studentlogin')

    try:
        # Retrieve the student using the email from session
        student = student_Registration.objects.get(email=student_email)
    except student_Registration.DoesNotExist:
        messages.error(request, "Student registration not found.")
        return redirect('studentlogin')

    # Fetch the bookings and payment records for the student
    bookings = events_participants.objects.filter(student=student)
    payments = Payment.objects.filter(student=student)
    now = timezone.now()    

    # Check if there are any bookings or payments
    if not bookings.exists():
        messages.info(request, "You have no event bookings.")
    
    if not payments.exists():
        messages.info(request, "You have no payment records.")

    # Render the template to display the student's bookings and payments
    return render(request, 'student_bookings.html', {
        'student': student,
        'bookings': bookings,
        'payments': payments,
        'now': now
    })



#Home page --------------------------------------------------------------------------------------------------------------------
def index(request):
    return render(request, 'index.html')


#------------------------------------------------------------------------------------------------------------------------------
#Staff Register Page
def staff_register(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        gender=request.POST.get('gender')
        dob=request.POST.get('dob')
        email=request.POST.get('email')
        department=request.POST.get('department')
        designation=request.POST.get('designation')
        mobile_no=request.POST.get('mobile_no')
        pic=request.FILES.get('pic')

        data=staff_Registration(username=username,password=password,gender=gender,dob=dob,email=email,department=department,designation=designation,mobile_no=mobile_no,pic=pic)
        data.save()
        messages.success(request, "Staff-Registered Successfully")
        return redirect('stafflogin')

    return render(request,'staff-Registration.html')

# staff Login 

def staff_login(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')

        try:
            user=staff_Registration.objects.get(email=email,password=password)
            email=user.email
            request.session['email']=email
            return redirect('/staffindex/')
        except:
             msg="invalid email or password"
             return render(request,'stafflogin.html',{"msg":msg})
    return render(request,'stafflogin.html')

#staff Profile
def staff_profile(request):
    email=request.session.get('email')
    if not email:
        alert_message="<script>alert('email doesnot exists ');window.location.href='/stafflogin/';</script>"
        return HttpResponse(alert_message)
        
    user=get_object_or_404(staff_Registration, email=email)
    user_info={
        'username':user.username,
        'password':user.password,
        'gender':user.gender,
        'dob':user.dob,
        'email':user.email,
        'department':user.department,
        'designation':user.designation,
        'mobile_no':user.mobile_no,
        'pic':user.pic
    }
    return render(request,'staffprofile.html',user_info)


#staff profile update
def staffprofile_update(request):
    email=request.session.get('email')
    if not email:
        return redirect('stafflogin')
    
    if request.method=='POST':
        user=staff_Registration.objects.get(email=email)
        username=request.POST.get('username')
        password=request.POST.get('password')
        gender=request.POST.get('gender')
        dob=request.POST.get('dob')
        email=request.POST.get('email')
        department=request.POST.get('department')
        designation=request.POST.get('designation')
        mobile_no=request.POST.get('mobile_no')
        pic=request.FILES.get('pic')

        user.username=username
        user.password=password
        if gender:
            user.gender=gender
        if dob:
            user.dob=dob
        user.email=email
        user.department=department
        user.designation=designation
        user.mobile_no=mobile_no
        if pic:
            user.pic=pic


        user.save()

        user_info={
        'username':user.username,
        'password':user.password,
        'gender':user.gender,
        'dob':user.dob,
        'email':user.email,
        'department':user.department,
        'designation':user.designation,
        'mobile_no':user.mobile_no,
        'pic':user.pic
        }
        messages.success(request, "Profile Updated Successfully")
        return render(request,'staffprofile.html', user_info)
    else:
        user=staff_Registration.objects.get(email=email)
        user_info={
        'username':user.username,
        'password':user.password,
        'gender':user.gender,
        'dob':user.dob,
        'email':user.email,
        'department':user.department,
        'designation':user.designation,
        'mobile_no':user.mobile_no,
        'pic':user.pic
        }
    return render(request,'staffupdate.html', user_info)


#staff profile delete
def delete_staff(request):  
    email=request.session.get('email')
    user=get_object_or_404(staff_Registration, email=email)
    staff={
        'id': user.id,
        'username':user.username,
        'password':user.password,
        'gender':user.gender,
        'dob':user.dob,
        'email':user.email,
        'department':user.department,
        'designation':user.designation,
        'mobile_no':user.mobile_no
    }
    context = {'staff': staff, 'user': user}
   
    return render(request,'staffdelete.html', context)

# confirm staff delete:
def staffconfirmdelete(request, id):
    staffdata=staff_Registration.objects.get(id=id)
    staffdata.delete()
    messages.success(request, "Profile Deleted Successfully")
    return redirect('/')

#staff page:
def staffindex(request):
    current_date = timezone.now().date()
    staff_count = staff_Registration.objects.count()
    student_count=student_Registration.objects.count()
    events = createevents.objects.filter( rend__gte=current_date).count()
    judge=judgeregister.objects.count()
    context={
        'staff_count':staff_count,
        'student_count':student_count,
        'events':events,
        'judge':judge
        
    }
    return render(request, 'staffindex.html',context)


#Full Student Details for Staff view only:
def staffstudentlist(request):
    user=student_Registration.objects.all()
    return render(request,'staffstudentlist.html',{'user':user})

# full judge view for staff
def staffjudgeview(request):
    judge=judgeregister.objects.all()
    return render(request,'staffjudgeview.html',{'judge':judge})



#Work assigned by admin for events to staff:
def staffworkedassigned(request):
    current_date = timezone.now().date()  # Get the current date
    user_email = request.session.get('email')  # Get the user's email from the session
    
    if user_email:  # Check if email exists in the session
        # Filter staff allocations based on the user's email and event date (rend >= today)
        staff = staffallocate.objects.filter(
            staffname__email=user_email, 
            event_details__rend__gte=current_date
        )
        print(f"Found {staff.count()} staff assignments.")
        return render(request, 'staffworkassigned.html', {'staff': staff})
    else:
        # Handle case where email is not in the session
        alert="<script>alert('Please Login-In');window.location.href='/stafflogin/';</script>"
        return HttpResponse(alert)
    

#Event Views for Staff:
def staffeventview(request):
    current_date = timezone.now().date()
    events = createevents.objects.filter( rend__gte=current_date)
    return render(request,'staffviewevents.html', {'events': events})


# staff can assign students for the particular events
def admin_event_allocation(request):
    # Fetch the logged-in staff from the session
    staff_email = request.session.get('email')  # Fetch the staff's email from the session
    if staff_email:
        try:
            # Fetch the staff member by email
            staff_data = staff_Registration.objects.get(email=staff_email)
        except staff_Registration.DoesNotExist:
            return HttpResponse("<script>alert('You are not authorized to assign events!');window.location.href='/login/'</script>")

        # Fetch the events allocated to this staff member from the staffallocate model
        staff_allocated_events = staffallocate.objects.filter(staffname=staff_data)

        # If there are no events allocated to the staff member, set a flag
        if not staff_allocated_events:
            no_events_assigned = True
            event_list = []  # No events to display
        else:
            no_events_assigned = False
            event_list = [event.event_details for event in staff_allocated_events]

        if request.method == 'POST':
            student_id = request.POST.get('student')
            event_id = request.POST.get('event')
            msg = request.POST.get('msg')

            # Fetch the selected student and event
            try:
                student = student_Registration.objects.get(id=student_id)
                event = createevents.objects.get(id=event_id)
            except student_Registration.DoesNotExist:
                return HttpResponse("<script>alert('Student not found!');window.location.href='/adminindex/'</script>")
            except createevents.DoesNotExist:
                return HttpResponse("<script>alert('Event not found!');window.location.href='/adminindex/'</script>")

            # Create a new allocation for the student and event with the message
            allocation = studentallocation(
                student=student,
                staff=staff_data,  # Use the current logged-in staff
                event=event,
                msg=msg
            )
            allocation.save()

            # Notify the staff of the success and redirect
            alert = "<script>alert('Event assigned to student successfully!');window.location.href='/adminindex/'</script>"
            return HttpResponse(alert)

        # If the request method is GET, load the form with available students and events
        student_list = student_Registration.objects.all()  # Fetch all students

        return render(request, 'assign_event_to_student.html', {
            'student_list': student_list,
            'event_list': event_list,
            'staff_data': staff_data,
            'no_events_assigned': no_events_assigned  # Pass the flag to the template
        })
    else:
        # If no session email found, redirect to login
        return HttpResponse("<script>alert('Unauthorized access!');window.location.href='/login/'</script>")
    




#payment History for staff:
def paymenthistorystaff(request):
    # Get the payment_id from the GET request (search term)
    payment_id = request.GET.get('payment_id', '')  # Default to an empty string if no ID is provided
    
    # If a payment_id is provided, filter payments by that ID
    if payment_id:
        data = Payment.objects.filter(razorpay_payment_id__icontains=payment_id).order_by('-created_at')
    else:
        # Get all payments and order by created_at descending to show latest first
        data = Payment.objects.all().order_by('-created_at')

    return render(request, 'paymenthistorystaff.html', {'data': data})


#------------------------------------------------------------------------------------------------------
#students

#student index page:
def studentindex(request):
    current_date = timezone.now().date()
    staff_count = staff_Registration.objects.count()
    student_count=student_Registration.objects.count()
    events = createevents.objects.filter( rend__gte=current_date).count()
    judge=judgeregister.objects.count()
    context={
        'staff_count':staff_count,
        'student_count':student_count,
        'events':events,
        'judge':judge
        
    }

    return render(request, 'studentindex.html',context)

#Student Register Page
def student_register(request):
    if request.method=="POST":
        username=request.POST.get('username')
        department=request.POST.get('department')
        semester=request.POST.get('semester')
        rollno=request.POST.get('rollno')
        gender=request.POST.get('gender')
        dob=request.POST.get('dob')
        email=request.POST.get('email')
        password=request.POST.get('password')
        mobile_no=request.POST.get('mobile_no')
        pic=request.FILES.get('pic')

        if student_Registration.objects.filter(rollno=rollno).exists():
            return HttpResponse("<script> alert('The roll number is already registered. Please choose Your Roll Number.');  window.location.href = '/studentregister';    </script> "  ) # Adjust this to the correct URL for the registration page

        # Check if email already exists in the database
        if student_Registration.objects.filter(email=email).exists():
           
            return HttpResponse("<script> alert('The roll number is already registered. Please choose Your Roll Number.');  window.location.href = '/studentregister';    </script> "  ) # Adjust this to the correct URL for the registration page

        data=student_Registration(username=username,department=department,semester=semester,rollno=rollno,gender=gender,dob=dob,email=email,password=password,mobile_no=mobile_no,pic=pic)
        data.save()
        messages.success(request, "Student profile Created Successfully")
        return redirect('/')

    return render(request,'student-Registration.html')


import json
import os
import calendar
from datetime import datetime, date
from django.http import JsonResponse
from django.db import connection
from dateutil.relativedelta import relativedelta
import requests
from django.conf import settings

# Predefined month lengths
import json
import os
import calendar
from datetime import datetime, date, timedelta # Import timedelta for date ranges
from django.http import JsonResponse
from django.db import connection
from dateutil.relativedelta import relativedelta
import requests
from django.conf import settings

# Predefined month lengths (used if total_month_days is not calculated based on date)
MONTH_DAYS = {
    1: 31, # January
    2: 28, # February (leap year handled in code)
    3: 31, # March
    4: 30, # April
    5: 31, # May
    6: 30, # June
    7: 31, # July
    8: 31, # August
    9: 30, # September
    10: 31, # October
    11: 30, # November
    12: 31 # December
}

# Helper function to find the commencement date (looking for the word "commencement")
def find_commencement_date(month_data):
    """
    Finds the commencement date from the month's calendar data events.
    Looks for events with "commencement" (case-insensitive) in the description.
    Returns the start date (date or date_range.start) as a date object or None if not found.
    """
    if not month_data or 'events' not in month_data:
        return None

    for event in month_data.get("events", []):
        description = event.get("description", "").lower()
        # Look for the word "commencement" in the description
        if "commencement" in description:
            # Get the date - assume single date first, then range start
            if 'date' in event and event['date']: # Check if 'date' exists and is not empty
                try:
                    return datetime.strptime(event["date"], "%Y-%m-%d").date()
                except (ValueError, TypeError):
                    print(f"Warning: Could not parse date '{event.get('date')}' for commencement event: {event.get('description', 'N/A')}")
                    continue # Skip this event, try others
            elif 'date_range' in event and event['date_range'].get('start'): # Check if date_range and start exist and start is not empty
                 try:
                    return datetime.strptime(event["date_range"]["start"], "%Y-%m-%d").date()
                 except (ValueError, TypeError):
                    print(f"Warning: Could not parse start date range '{event['date_range'].get('start')}' for commencement event: {event.get('description', 'N/A')}")
                    continue # Skip this event, try others

    return None # Commencement event not found


# Helper function to get all busy dates in a month from JSON events
def get_json_busy_dates_in_month(month_data, month_start_date):
    """
    Collects all busy dates from JSON events within the given month.
    Returns a set of date objects.
    """
    busy_dates = set()
    if not month_data or 'events' not in month_data:
        return busy_dates

    month_end_date = month_start_date + relativedelta(months=1) - timedelta(days=1)

    for event in month_data.get("events", []):
        if event.get('status') == 'busy':
            try:
                if 'date' in event and event['date']:
                    event_date = datetime.strptime(event["date"], "%Y-%m-%d").date()
                    # Check if the event date is within the current month
                    if event_date.year == month_start_date.year and event_date.month == month_start_date.month:
                         busy_dates.add(event_date)

                elif 'date_range' in event and event['date_range'].get('start') and event['date_range'].get('end'):
                    start_date = datetime.strptime(event["date_range"]["start"], "%Y-%m-%d").date()
                    end_date = datetime.strptime(event["date_range"]["end"], "%Y-%m-%d").date()

                    # Limit the range to the current month
                    range_start = max(start_date, month_start_date)
                    range_end = min(end_date, month_end_date)

                    # Add all dates within the (potentially limited) busy range
                    for single_date in (range_start + timedelta(n) for n in range((range_end - range_start).days + 1)):
                         busy_dates.add(single_date)

            except (ValueError, KeyError):
                 print(f"Warning: Could not parse date or date range for busy event: {event.get('description', 'N/A')}")
                 continue # Skip invalid event

    return busy_dates


# Helper function to get all busy dates in a month from Database events
def get_db_busy_dates_in_month(month_start_date):
    """
    Collects all busy dates from database events within the given month.
    Returns a set of date objects.
    """
    busy_dates = set()
    month_end_date = month_start_date + relativedelta(months=1) - timedelta(days=1)

    try:
        with connection.cursor() as cursor:
            # Query database for events within the selected month range
            cursor.execute("""
                SELECT doe FROM homeapp_createevents
                WHERE doe BETWEEN %s AND %s
            """, [month_start_date, month_end_date])

            db_busy_events = cursor.fetchall()
            for event_date_tuple in db_busy_events:
                 if event_date_tuple and len(event_date_tuple) > 0:
                    # Assuming 'doe' is stored as a date or datetime and fetchall returns tuples
                    event_date = event_date_tuple[0] # Get the date object from the tuple
                    # Ensure it's a date object
                    if isinstance(event_date, datetime):
                         event_date = event_date.date()
                    if isinstance(event_date, date):
                         busy_dates.add(event_date)
                    else:
                         print(f"Warning: Unexpected data type for database event date: {type(event_date)}")

    except Exception as e:
        print(f"Error retrieving busy dates from database: {e}")
        # Decide how to handle database errors in the count - for now, just print warning.

    return busy_dates


import json
import os
import calendar
from datetime import datetime, date, timedelta
from django.http import JsonResponse
from django.db import connection
from dateutil.relativedelta import relativedelta
import requests
from django.conf import settings

# Predefined month lengths (used if total_month_days is not calculated based on date)
MONTH_DAYS = {
    1: 31, # January
    2: 28, # February (leap year handled in code)
    3: 31, # March
    4: 30, # April
    5: 31, # May
    6: 30, # June
    7: 31, # July
    8: 31, # August
    9: 30, # September
    10: 31, # October
    11: 31, # November
    12: 31 # December
}

# Helper function to find the commencement date (looking for the word "commencement")
def find_commencement_date(month_data):
    """
    Finds the commencement date from the month's calendar data events.
    Looks for events with "commencement" (case-insensitive) in the description.
    Returns the start date (date or date_range.start) as a date object or None if not found.
    """
    if not month_data or 'events' not in month_data:
        return None

    for event in month_data.get("events", []):
        description = event.get("description", "").lower()
        # Look for the word "commencement" in the description
        if "commencement" in description:
            # Get the date - assume single date first, then range start
            if 'date' in event and event['date']: # Check if 'date' exists and is not empty
                try:
                    return datetime.strptime(event["date"], "%Y-%m-%d").date()
                except (ValueError, TypeError):
                    print(f"Warning: Could not parse date '{event.get('date')}' for commencement event: {event.get('description', 'N/A')}")
                    continue # Skip this event, try others
            elif 'date_range' in event and event['date_range'].get('start'): # Check if date_range and start exist and start is not empty
                 try:
                    return datetime.strptime(event["date_range"]["start"], "%Y-%m-%d").date()
                 except (ValueError, TypeError):
                    print(f"Warning: Could not parse start date range '{event['date_range'].get('start')}' for commencement event: {event.get('description', 'N/A')}")
                    continue # Skip this event, try others

    return None # Commencement event not found


def check_date_conflict(request):
    if request.method == 'POST':
        selected_date_str = request.POST.get('doe')
        if selected_date_str:
            try:
                selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
                current_month_key = selected_date.strftime("%B_%Y").lower()

                print(f"--- Date Conflict Check Started ---")
                print(f"Selected Date String: {selected_date_str}")
                print(f"Selected Date Object: {selected_date}")
                print(f"Calculated Month Key: {current_month_key}")

                calendar_path = os.path.join(settings.BASE_DIR, 'CALENDAR.json')
                print(f"Constructed Calendar Path: {calendar_path}")

                date_conflict = False
                conflict_messages = []
                calendar_analysis = {
                    'current_month_data': None,
                    'instructional_days': None
                }
                ai_date_suggestions = ""
                calendar_data_full = None
                month_data = None
                total_month_days = 0 # Initialize total_month_days here

                # --- Load Calendar Data ---
                if os.path.exists(calendar_path):
                    print(f"Calendar file found at: {calendar_path}")
                    try:
                        with open(calendar_path, 'r', encoding='utf-8') as f:
                            calendar_data_full = json.load(f)
                        print(f"Calendar JSON loaded successfully.\n\n")
                    except json.JSONDecodeError:
                        print(f"Error: Could not decode JSON from {calendar_path}")
                        conflict_messages.append(f"Error: Could not decode JSON from {calendar_path}")
                    except Exception as e:
                        print(f"Error: Could not read calendar file {calendar_path}: {e}")
                        conflict_messages.append(f"Error: Could not read calendar file {calendar_path}: {e}")
                else:
                    print(f"Warning: Calendar file not found at {calendar_path}")
                    conflict_messages.append(f"Warning: Calendar file not found at {calendar_path}")

                # --- 1. CALENDAR DATE ANALYSIS (Load Month Data) ---
                if calendar_data_full and 'calendar_data' in calendar_data_full:
                    print(f"Attempting to get month data for key: {current_month_key}")
                    month_data = calendar_data_full['calendar_data'].get(current_month_key)
                    if month_data:
                        print(f"Month data found for {current_month_key}.")
                        calendar_analysis['current_month_data'] = month_data
                    else:
                         print(f"Month data NOT found for {current_month_key} in calendar_data.")
                         conflict_messages.append(f"Warning: No calendar data found for {selected_date.strftime('%B %Y')}.")

                # --- Calculate Total Days in Month (Needed for several checks) ---
                try:
                    if selected_date.month == 2:
                        is_leap = calendar.isleap(selected_date.year)
                        total_month_days = 29 if is_leap else 28
                    else:
                        total_month_days = MONTH_DAYS.get(selected_date.month, 30)
                    print(f"Total days in month ({selected_date.strftime('%B %Y')}): {total_month_days}")

                except KeyError:
                    print(f"Error: Invalid month number {selected_date.month}")
                    conflict_messages.append(f"Warning: Could not determine days in month {selected_date.month}.")
                except Exception as e:
                    print(f"Error calculating total days: {e}")
                    conflict_messages.append(f"Warning: Error calculating total days.")


                # --- Instructional Days Extraction (Needed for complex calculation) ---
                instructional_days = None
                if month_data and 'month_info' in month_data:
                    print(f"'month_info' found in month data.")
                    instructional_days_str = month_data['month_info'].get('instructional_days')
                    print(f"Retrieved instructional_days_str: {instructional_days_str}")
                    if instructional_days_str is not None:
                        try:
                            instructional_days = int(instructional_days_str)
                            calendar_analysis['instructional_days'] = instructional_days
                            print(f"Successfully parsed instructional_days: {instructional_days}")
                        except (ValueError, TypeError):
                            print(f"Warning: Invalid format for instructional_days in {current_month_key}: {instructional_days_str}")
                            conflict_messages.append(f"Warning: Instructional days data for {selected_date.strftime('%B %Y')} is invalid.")
                    else:
                         print(f"instructional_days_str is None.")
                else:
                     print(f"'month_info' not available in month data for {selected_date.strftime('%B %Y')}. Instructional days will be treated as None.")


                # --- Commencement Day Logic (Integrated and Updated) ---
                commencement_date = None
                if month_data: # Proceed with commencement logic only if month data is loaded
                    commencement_date = find_commencement_date(month_data)

                    if commencement_date:
                        print(f"Commencement date found: {commencement_date}")

                        # Check 1: Selected date is before commencement
                        if selected_date < commencement_date:
                            date_conflict = True
                            conflict_messages.append(
                                f"Conflict: Selected date ({selected_date_str}) is before the Commencement Day ({commencement_date.strftime('%Y-%m-%d')})."
                            )
                            print("Commencement day conflict detected (before commencement).")

                        # Check 2: Commencement is on the last day of the month (using calculated total_month_days)
                        # This check makes sense only if total_month_days was successfully calculated
                        if total_month_days > 0 and commencement_date.day == total_month_days:
                             conflict_messages.append("Conflict: Commencement is on the last day of the month. No days available after it for allotment based on this rule.")
                             date_conflict = True # This is a conflict based on the rule
                             print("Commencement on last day conflict detected.")


                        # Check 3: The specific complex subtraction rule as clarified
                        # Applies only if we have a valid commencement date, total days, instructional days, and selected date day
                        if total_month_days > 0 and instructional_days is not None:
                             print(f"Performing complex Commencement calculation based on formula: tdm - cd - doe - inst")
                             print(f"Calculation: {total_month_days} (tdm) - {commencement_date.day} (cd) - {selected_date.day} (doe) - {instructional_days} (inst)")

                             # Calculate the value based on the exact formula provided
                             calculated_value = total_month_days - commencement_date.day - selected_date.day - instructional_days

                             print(f"Complex calculation result: {calculated_value}")

                             # Check the threshold: if result is LESS THAN or EQUAL TO 2, then conflict
                             if calculated_value <= 2:
                                 date_conflict = True # Mark as conflict
                                 conflict_messages.append(
                                     f"Conflict: Based on complex rule (tdm - cd - doe - inst <= 2), no days are available for allotment. Result: {calculated_value}"
                                 )
                                 print("Complex Commencement calculation conflict detected.")
                             else:
                                 print("Complex Commencement calculation passed (result > 2).")
                        else:
                             print("Skipping complex Commencement calculation (missing total days or instructional days).")


                # --- Strict Instructional Days Constraint Check (Removed as requested) ---
                # The previous check "if instructional_days > total_month_days - 1:" is removed as requested.
                # print("Skipping strict instructional days constraint check as it was removed.")


                # --- Existing JSON Event Check (Check if the *selected date itself* is busy in JSON) ---
                # This checks if the *specific selected date* is busy in JSON, regardless of other rules.
                if month_data: # Only check JSON events if month_data was successfully loaded
                    print(f"Checking if selected date {selected_date_str} is busy in JSON events...")
                    for event in month_data.get("events", []):
                        # Check single date events
                        if 'date' in event and event["date"] == selected_date_str:
                             print(f"Single date match found for selected date.")
                             if event.get("status") == "busy":
                                 print(f"Event on selected date is busy: {event.get('description', 'N/A')}")
                                 date_conflict = True
                                 conflict_messages.append(f"Conflict: Selected date is a busy date in JSON - {event.get('description', 'No description')}")
                             # No need to check date ranges if a single date match was found

                         # Check date range events if no single date match found for selected date
                        elif 'date_range' in event:
                             try:
                                 start = datetime.strptime(event["date_range"]["start"], "%Y-%m-%d").date()
                                 end = datetime.strptime(event["date_range"]["end"], "%Y-%m-%d").date()
                                 # Check if selected date falls within a busy range
                                 if event.get('status') == 'busy' and start <= selected_date <= end:
                                     print(f"Selected date falls within busy range: {start} to {end}")
                                     date_conflict = True
                                     conflict_messages.append(f"Conflict: Selected date falls within busy period in JSON - {event.get('description', 'No description')}")
                             except (ValueError, KeyError) as e:
                                 print(f"Error parsing date range for event {event.get('description', 'N/A')}: {e}")
                                 # Warning already added during collection of busy dates, maybe add a specific one here if needed
                                 # conflict_messages.append(f"Warning: Could not parse date range for event '{event.get('description', 'N/A')}'.")
                else:
                     print("Skipping JSON event specific date check because month data is not available.")


                # --- 2. DATABASE CONFLICT CHECK (Check if the *selected date itself* is busy in DB) ---
                # This checks if the *specific selected date* is busy in the database, regardless of other rules.
                print(f"Checking if selected date {selected_date_str} is busy in the database...")
                try:
                    with connection.cursor() as cursor:
                        # Check only the selected date
                        cursor.execute("""
                            SELECT event_name FROM homeapp_createevents
                            WHERE doe = %s
                        """, [selected_date_str])

                        db_conflicts_specific_date = cursor.fetchone() # Use fetchone as we only expect one row or none
                        if db_conflicts_specific_date:
                            print(f"Database conflict found for selected date: {db_conflicts_specific_date[0]}")
                            date_conflict = True
                            conflict_messages.append(f"Conflict: Selected date is an existing database event - {db_conflicts_specific_date[0]}")
                        else:
                            print("No database conflict found for selected date.")
                except Exception as e:
                    print(f"Error checking database for selected date conflict: {e}")
                    # Warning already added during collection of busy dates, maybe add a specific one here if needed
                    # conflict_messages.append(f"Warning: Error checking database for conflicts.")


                # --- 3. AI DATE SUGGESTIONS (Existing Logic) ---
                print(f"Checking if AI suggestions are needed (date_conflict={date_conflict}, warnings={any('Warning:' in msg for msg in conflict_messages)})...")
                if (date_conflict or any("Warning:" in msg for msg in conflict_messages)) and calendar_data_full:
                    if month_data: # Require at least current month data for meaningful context
                         print("Sufficient calendar data for AI suggestions.")
                         try:
                             base_date = selected_date if isinstance(selected_date, date) else date.today()

                             prev_month_date = base_date - relativedelta(months=1)
                             next_month_date = base_date + relativedelta(months=1)
                             next_next_month_date = base_date + relativedelta(months=2)

                             next_month_key = next_month_date.strftime("%B_%Y").lower()
                             next_next_month_key = next_next_month_date.strftime("%B_%Y").lower()

                             next_month_data = calendar_data_full.get('calendar_data', {}).get(next_month_key)
                             next_next_month_data = calendar_data_full.get('calendar_data', {}).get(next_next_month_key)

                             current_month_events = month_data.get('events', []) if month_data else []
                             current_month_notes = month_data.get('month_info', {}).get('notes', '') if month_data else ''
                             next_month_events = next_month_data.get('events', []) if next_month_data else []
                             next_next_month_events = next_next_month_data.get('events', []) if next_next_month_data else []

                             calendar_context = {
                                 'selected_date': selected_date_str,
                                 'current_month': {
                                     'name': selected_date.strftime("%B %Y"),
                                     'instructional_days': calendar_analysis.get('instructional_days', 'N/A'),
                                     'notes': current_month_notes,
                                     'events': current_month_events
                                 },
                                 'next_month': {
                                     'name': next_month_date.strftime("%B %Y"),
                                     'events': next_month_events
                                 },
                                 'next_next_month': {
                                     'name': next_next_month_date.strftime("%B %Y"),
                                     'events': next_next_month_events
                                 }
                             }

                             conflict_reasons_str = '\n'.join(conflict_messages)

                             prompt = f"""Analyze these calendar details for a college principal trying to schedule an event:

Requested Date: {calendar_context['selected_date']} ({calendar_context['current_month']['name']})
Instructional Days Required this Month: {calendar_context['current_month']['instructional_days']}
Relevant Notes for Current Month: {calendar_context['current_month']['notes'] or 'None'}

Issues Detected with Requested Date:
{conflict_reasons_str}

Calendar Data:
Current Month ({calendar_context['current_month']['name']}):
{json.dumps(calendar_context['current_month']['events'], indent=2)}

Next Month ({calendar_context['next_month']['name']}):
{json.dumps(calendar_context['next_month']['events'], indent=2)}

Month After Next ({calendar_context['next_next_month']['name']}):
{json.dumps(calendar_context['next_next_month']['events'], indent=2)}

 Please suggest:
               1. alternative dates in the current month (if available)         
                2. tell me abt dates in the next month
                        3. Options in month after next
                        

                        Consider instructional days,exam warning and existing events while planing the alternative day
                        Format your response with clear&very short. without a paragraph .dont include bulletpoints
                        example:
                        When the document says "No. of Instructional days: 5" for November 2024, it means that there are only 5 days in that month when classes or instruction are scheduled to take place.
                        This likely indicates that there are no chance for holidays, breaks, or other non-instructional days that reduce the number of working days dedicated to teaching and learning in November 2024.
                        please note Holidays affect instructional         days,plan wisely like a principal of collage
"""
                             # print(f"AI Prompt:\n{prompt}") # Uncomment to see the full prompt

                             api_key = "6f0081b18ca64ba28a7ed491f3536b95"  # Your actual API key

                             if api_key == 'YOUR_FALLBACK_API_KEY':
                                 print("Warning: AIMLAPI key not found in settings.")
                                 ai_date_suggestions = "AI Suggestion Error: API key not configured."
                             else:
                                 print("Calling AI API...")
                                 try:
                                     response = requests.post(
                                         "https://api.aimlapi.com/v1/chat/completions",
                                         headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
                                         json={"model": "gpt-4o-mini", "messages": [{"role": "user", "content": prompt}]},
                                         timeout=30
                                     )
                                     response.raise_for_status()

                                     data = response.json()
                                     # print(f"AI API Response Data: {data}") # Uncomment to see raw AI response
                                     ai_date_suggestions = data.get('choices', [{}])[0].get('message', {}).get('content', "AI Error: No suggestions available in response.")
                                     print(f"AI Suggestions: {ai_date_suggestions}")

                                 except requests.exceptions.RequestException as api_err:
                                     print(f"API Request Error: {api_err}")
                                     ai_date_suggestions = f"AI Suggestion Error: Could not connect to API ({api_err})."
                                 except Exception as api_e:
                                     print(f"API Processing Error: {api_e}")
                                     ai_date_suggestions = f"AI Suggestion Error: {api_e}."
                         except Exception as e:
                             print(f"Error preparing data or calling AI for date suggestions: {str(e)}")
                             ai_date_suggestions = f"Could not generate date suggestions due to an internal error: {str(e)}"
                    else:
                        print("Insufficient calendar data for AI suggestions (month data missing).")
                        ai_date_suggestions = "Could not generate suggestions: Insufficient calendar data available."
                else:
                    print("No conflicts or warnings detected, skipping AI suggestions.")
                    ai_date_suggestions = "No conflicts detected for this date."


                # --- Final Conflict Determination and Response ---
                print(f"Date Conflict Status: {date_conflict}")
                print(f"Conflict Messages: {conflict_messages}")
                print(f"Calendar Analysis (Instructional Days): {calendar_analysis.get('instructional_days', 'N/A')}")
                print(f"AI Suggestions Output: {ai_date_suggestions}")
                print(f"--- Date Conflict Check Finished ---")

                return JsonResponse({
                    'date_conflict': date_conflict,
                    'conflict_messages': list(set(conflict_messages)), # Use set to remove duplicates
                    'calendar_analysis': {
                        'selected_date': selected_date_str,
                        'instructional_days_in_month': calendar_analysis.get('instructional_days', 'N/A')
                    },
                    'ai_date_suggestions': ai_date_suggestions,
                    'commencement_date': commencement_date.strftime('%Y-%m-%d') if commencement_date else None,
                    'total_month_days': total_month_days if total_month_days > 0 else 'N/A'
                })

            except ValueError:
                print(f"ValueError: Invalid date format received: {selected_date_str}")
                return JsonResponse({'error': 'Invalid date format. Use%Y-%m-%d.'}, status=400) # Corrected format in message
            except Exception as e:
                import traceback
                print(f"Fatal error processing date check for {selected_date_str}: {e}")
                traceback.print_exc()
                return JsonResponse({'error': f'An internal server error occurred. Please contact support.'}, status=500)
        else:
            print("Error: No date provided in the request.")
            return JsonResponse({'error': 'No date provided in the request.'}, status=400)
    else:
        print("Error: Invalid request method (not POST).")
        return JsonResponse({'error': 'Invalid request method. Use POST.'}, status=405)

# Please install OpenAI SDK first: `pip3 install openai`
import requests
from django.shortcuts import render
from django.contrib import messages
import json
import os
from django.db import connection
from datetime import datetime
from dateutil.relativedelta import relativedelta

def ai(request):
    filepath = r"data.json"
    calendar_path = r"CALENDAR.json"

    if request.method == 'POST':
        # Get all form data (preserved exactly as in original)
        form_data = {
            'event_category': request.POST.get('event_category'),
            'version': request.POST.get('version'),
            'event_name': request.POST.get('event_name'),
            'events_description': request.POST.get('events_description'),
            'amount': request.POST.get('amount'),
            'doe': request.POST.get('doe'),
            'rend': request.POST.get('rend'),
            'resultdate': request.POST.get('resultdate'),
            'eventName': request.POST.get('eventName'),
            'category': request.POST.get('category'),
            'type': request.POST.get('type'),
            'participants': request.POST.get('participants'),
            'duration': request.POST.get('duration'),
            'budget': request.POST.get('budget'),
            'promotion': request.POST.get('promotion'),
            'time': request.POST.get('time'),
            'options': request.POST.getlist('options'),
        }

        # Initialize variables
        date_conflict = False
        conflict_messages = []
        calendar_analysis = {
            'current_month': None,
            'prev_month': None,
            'next_month': None,
            'instructional_days': None
        }
        ai_date_suggestions = ""

        # 1. CALENDAR DATE ANALYSIS
        if form_data['doe']:
            try:
                # Parse dates and get surrounding months
                selected_date = datetime.strptime(form_data['doe'], '%Y-%m-%d').date()
                prev_month = selected_date - relativedelta(months=1)
                next_month = selected_date + relativedelta(months=1)
                next_next_month = selected_date + relativedelta(months=2)
                
                # Generate the format keys for each month (like "november_2024")
                current_month_key = selected_date.strftime("%B_%Y").lower()
                prev_month_key = prev_month.strftime("%B_%Y").lower()
                next_month_key = next_month.strftime("%B_%Y").lower()
                next_next_month_key = next_next_month.strftime("%B_%Y").lower()
                
                if os.path.exists(calendar_path):
                    with open(calendar_path, 'r', encoding='utf-8') as f:
                        calendar_data = json.load(f)
                    
                    # Get data for each month using the generated keys
                    calendar_analysis = {
                        'current_month': calendar_data['calendar_data'].get(current_month_key),
                        'prev_month': calendar_data['calendar_data'].get(prev_month_key),
                        'next_month': calendar_data['calendar_data'].get(next_month_key),
                        'next_next_month': calendar_data['calendar_data'].get(next_next_month_key),
                        'instructional_days': None
                    }
                    
                    # Check for instructional days in current month
                    if calendar_analysis['current_month'] and 'month_info' in calendar_analysis['current_month']:
                        calendar_analysis['instructional_days'] = calendar_analysis['current_month']['month_info'].get('instructional_days')
                    
                    # Check for date conflicts in current month
                    if calendar_analysis['current_month']:
                        for event in calendar_analysis['current_month'].get('events', []):
                            if 'date' in event and event['date'] == form_data['doe']:
                                if event.get('status') == 'busy':
                                    date_conflict = True
                                    conflict_messages.append(f"Busy date: {event['description']}")
                            elif 'date_range' in event:
                                if event['date_range']['start'] <= form_data['doe'] <= event['date_range']['end']:
                                    date_conflict = True
                                    conflict_messages.append(f"Event period: {event['description']}")
            
            except Exception as e:
                print(f"Error processing calendar data: {e}")

        # 2. DATABASE CONFLICT CHECK
        if form_data['doe']:
            try:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        SELECT event_name FROM homeapp_createevents 
                        WHERE doe = %s
                    """, [form_data['doe']])
                    
                    db_conflicts = cursor.fetchall()
                    if db_conflicts:
                        date_conflict = True
                        for event in db_conflicts:
                            conflict_messages.append(f"Existing event: {event[0]}")
            except Exception as e:
                print(f"Error checking database: {e}")

        # 3. AI FUNCTIONALITY
        api_key = '6f0081b18ca64ba28a7ed491f3536b95'
        ai_response = ""
        
        # Generate AI date suggestions if there are conflicts
        if date_conflict and calendar_analysis['current_month']:
            try:
                # Prepare calendar context for AI
                calendar_context = {
                    'selected_date': form_data['doe'],
                    'current_month': {
                        'name': selected_date.strftime("%B %Y"),
                        'instructional_days': calendar_analysis['instructional_days'],
                        'notes': calendar_analysis['current_month'].get('month_info', {}).get('notes', '') if calendar_analysis['current_month'] else '',
                        'events': calendar_analysis['current_month'].get('events', []) if calendar_analysis['current_month'] else []
                    },
                    'next_month': {
                        'name': next_month.strftime("%B %Y"),
                        'events': calendar_analysis['next_month'].get('events', []) if calendar_analysis['next_month'] else []
                    },
                    'next_next_month': {
                        'name': next_next_month.strftime("%B %Y"),
                        'events': calendar_analysis['next_next_month'].get('events', []) if calendar_analysis['next_next_month'] else []
                    }
                }

                prompt = f"""Analyze these calendar details and suggest better dates for an event:
                
                Current date selection:
                - Selected Date: {calendar_context['selected_date']}
                - Current Month: {calendar_context['current_month']['name']}
                - Instructional Days: {calendar_context['current_month']['instructional_days']}

                Conflicts Detected:
                {'\n'.join(conflict_messages)}

                Calendar Events:
                Current Month ({calendar_context['current_month']['name']}):
                {json.dumps(calendar_context['current_month']['events'], indent=2)}

                Next Month ({calendar_context['next_month']['name']}):
                {json.dumps(calendar_context['next_month']['events'], indent=2)}

                Month After Next ({calendar_context['next_next_month']['name']}):
                {json.dumps(calendar_context['next_next_month']['events'], indent=2)}
                
                Please suggest:
                1. alternative dates in the current month (if available)
                2. tell me abt dates in the next month
                3. Options in month after next
                4. Explain why each suggestion might work better
                
                Consider instructional days,exam warning and existing events while planing the alternative day
                Format your response with clear&very short. without a paragraph .
                example:
                When the document says "No. of Instructional days: 5" for November 2024, it means that there are only 5 days in that month when classes or instruction are scheduled to take place.    
This likely indicates that there are chance for holidays, breaks, or other non-instructional days that reduce the number of working days dedicated to teaching and learning in November 2024.
please note Holidays affect instructional days,plan wise & plese dont add non acsi charaters like *# etc ,make it short&simple                
                """
                
                response = requests.post(
                    "https://api.aimlapi.com/v1/chat/completions",
                    headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
                    json={"model": "gpt-4o-mini", "messages": [{"role": "user", "content": prompt}]}
                )
                
                if response.ok:
                    data = response.json()
                    ai_date_suggestions = data['choices'][0]['message']['content'] if 'choices' in data else ""
                else:
                    ai_date_suggestions = f"API Error: {response.status_code} - {response.text}"

            except Exception as e:
                print(f"Error generating date suggestions: {str(e)}")
                ai_date_suggestions = f"Could not generate date suggestions: {str(e)}"

        # 3. ORIGINAL AI FUNCTIONALITY (preserved exactly)
        api_key = '6f0081b18ca64ba28a7ed491f3536b95'
        ai_response = ""
        
        if form_data['options']:
            if 'night' in form_data['options'] or 'day' in form_data['options']:
                # Time-based event suggestion
                selected_time = "night" if 'night' in form_data['options'] else "day"
                try:
                    if os.path.exists(filepath):
                        with open(filepath, 'r', encoding='utf-8') as f:
                            event_data = json.load(f)
                        event_names = [event.get('eventName') for event in event_data if isinstance(event, dict) and 'eventName' in event]
                        if event_names:
                            prompt = f"Out of the following events: {', '.join(event_names)}, suggest one event that is most appropriate for the {selected_time}."
                            response = requests.post(
                                "https://api.aimlapi.com/v1/chat/completions",
                                headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
                                json={"model": "gpt-4o-mini", "messages": [{"role": "user", "content": prompt}]}
                            )
                            if response.ok:
                                data = response.json()
                                ai_response = data['choices'][0]['message']['content'] if 'choices' in data else "No suggestions available"
                except Exception as e:
                    ai_response = f"Error: {str(e)}"
            else:
                # General AI suggestion
                prompt = f"Create an event with these details:\nName: {form_data['eventName']}\nCategory: {form_data['category']}\nType: {form_data['type']}\nParticipants: {form_data['participants']}\nDuration: {form_data['duration']}\nBudget: {form_data['budget']}\nPromotion: {form_data['promotion']}\nTime: {form_data['time']}\nPlease suggest event ideas and improvements."
                response = requests.post(
                    "https://api.aimlapi.com/v1/chat/completions",
                    headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
                    json={"model": "o1", "messages": [{"role": "user", "content": prompt}]}
                )
                if response.ok:
                    data = response.json()
                    ai_response = data['choices'][0]['message']['content'] if 'choices' in data else "No suggestions available"
        else:
            # Simple compliment
            prompt = f"Nice event: {form_data['event_name']} (Category: {form_data['event_category']}). Give a 10-word compliment."
            response = requests.post(
                "https://api.aimlapi.com/v1/chat/completions",
                headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
                json={"model": "o1", "messages": [{"role": "user", "content": prompt}]}
            )
            if response.ok:
                data = response.json()
                ai_response = data['choices'][0]['message']['content'] if 'choices' in data else "Nice event planning!"

        # Prepare context
        # In your view function, modify the context preparation:
        context = {
            **form_data,
            'ai_response': ai_response,
            'ai_date_suggestions': ai_date_suggestions if date_conflict else "",
            'date_conflict': date_conflict,
            'conflict_messages': conflict_messages,
            'calendar_analysis': calendar_analysis,
            'message': "Your event has been successfully submitted!"
        }

        messages.success(request, context['message'])
        return render(request, 'admincreateevent.html', context)
    print("date_conflict:", date_conflict)
    print("conflict_messages:", conflict_messages)
    print("calendar_analysis:", calendar_analysis)
    return render(request, 'admincreateevent.html')

def event_success(request):
    # Retrieve data from session
    ai_response = request.session.get('ai_response', '')
    form_data = request.session.get('form_data', {})

    # Clear the session data
    if 'ai_response' in request.session:
        del request.session['ai_response']
    if 'form_data' in request.session:
        del request.session['form_data']

    context = {
        'ai_response': ai_response,
        **form_data  # Include all preserved form data
    }
    return render(request, 'event_success.html', context)

def student_login(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')

        try:
            user=student_Registration.objects.get(email=email,password=password)
            email=user.email
            request.session['email']=email
            return redirect('/studentindex/')
        except:
             msg="invalid email or password"
             return render(request,'studentlogin.html',{"msg":msg})
    return render(request,'studentlogin.html')

#student Profile
def student_profile(request):
    email=request.session.get('email')
    if not email:
        alert_message="<script>alert('email doesnot exists ');window.location.href='/studentlogin/';</script>"
        return HttpResponse(alert_message)
        
    user=get_object_or_404(student_Registration, email=email)
    user_info={
        'username':user.username,
        'department':user.department,
        'semester':user.semester,
        'rollno':user.rollno,
        'gender':user.gender,
        'dob':user.dob,
        'email':user.email,
        'password':user.password,
        'mobile_no':user.mobile_no,
        'pic':user.pic,
        
    }
    return render(request,'studentsprofile.html',user_info)


#student profile update
def studentprofile_update(request):
    email=request.session.get('email')
    if not email:
        return redirect('studentlogin')
    
    if request.method=='POST':
        user=student_Registration.objects.get(email=email)
        username=request.POST.get('username')
        department=request.POST.get('department')
        semester=request.POST.get('semester')
        rollno=request.POST.get('rollno')
        gender=request.POST.get('gender')
        dob=request.POST.get('dob')
        email=request.POST.get('email')
        password=request.POST.get('password')
        mobile_no=request.POST.get('mobile_no')
        pic=request.FILES.get('pic')

        user.username=username
        user.department=department
        user.semester=semester
        user.rollno=rollno
        if gender:
            user.gender=gender
        if dob:
            user.dob=dob
        user.email=email
        user.password=password
        user.mobile_no=mobile_no
        if pic:
            user.pic=pic

        user.save()

        user_info={
        'username':user.username,
        'department':user.department,
        'semester':user.semester,
        'rollno':user.rollno,
        'gender':user.gender,
        'dob':user.dob,
        'email':user.email,
        'password':user.password,
        'mobile_no':user.mobile_no,
        'pic':user.pic
        }
        return render(request,'studentsprofile.html', user_info)
    else:
        user=student_Registration.objects.get(email=email)
        user_info={
        'username':user.username,
        'department':user.department,
        'semester':user.semester,
        'rollno':user.rollno,
        'gender':user.gender,
        'dob':user.dob,
        'email':user.email,
        'password':user.password,
        'mobile_no':user.mobile_no,
        'pic':user.pic
        }
    return render(request,'studentsupdate.html', user_info)

#student profile delete
def delete_student(request):  
    email=request.session.get('email')
    user=get_object_or_404(student_Registration, email=email)
    student={
        'id': user.id,
        'username':user.username,
        'department':user.department,
        'semester':user.semester,
        'rollno':user.rollno,
        'gender':user.gender,
        'dob':user.dob,
        'email':user.email,
        'password':user.password,
        'mobile_no':user.mobile_no
    }
    context = {'student': student, 'user': user}
   
    return render(request,'studentdelete.html', context)

# confirm student profile delete:
def studentconfirmdelete(request, id):
    studentdata=student_Registration.objects.get(id=id)
    studentdata.delete()
    return redirect('/')

def student_feedbacksubmit(request):
    
    if request.method == "POST":
        
        feedback_text = request.POST.get('feedback_text')
        rating = request.POST.get('rating')
        
        
        
        if not feedback_text or not rating:
            # Handle missing fields
            alert_message = "<script>alert('Please fill in all required fields.'); window.location.href='/driver_feedbackrate';</script>"
            return HttpResponse(alert_message)
        
        try:
            rating = int(rating)
            if rating not in [1, 2, 3, 4, 5]:
                raise ValueError("Invalid rating value")
        except (ValueError, TypeError):
            # Handle invalid rating
            alert_message = "<script>alert('Invalid rating value. Please select a valid rating.'); window.location.href='/student_feedbacksubmit/';</script>"
            return HttpResponse(alert_message)
         
        # Create and save the Feedback instance
        user=request.session.get('email')
        us=student_Registration.objects.get(email=user)
       
        feedback = Feedback (
            Student_Name=us,
            feedback_text=feedback_text,
            rating=rating
        )
        feedback.save()

        # Redirect to a success page
        return redirect('feedbacksuccess')
    else:
        # Render the feedback form
        return render(request, 'student_feedback.html')
    

def feedbacksuccess(request):
    return render(request,'feedbacksuccess.html')


#Full Staff Details for Student View Only:
def studentstafflist(request):
    user=staff_Registration.objects.all()
    return render(request,'studentstafflist.html',{'user':user})



# Show Events to students:
from django.utils import timezone

def studentshowevents(request):
    # Get student's email from session
    student_email = request.session.get('email')
    print(student_email) 
    
    if not student_email:
        # If there's no email in the session, redirect to login page or show an error message
        messages.error(request, "You must be logged in to view events.")
        return redirect('studentlogin')  # You can change this to the appropriate login URL
    
    try:
        # Retrieve the student object from the database using the email
        student = student_Registration.objects.get(email=student_email)
    except student_Registration.DoesNotExist:
        # If student does not exist, handle the error (you can redirect or show an error message)
        messages.error(request, "Student registration not found.")
        return redirect('studentlogin')  # Or handle as needed
    
    # Get today's date
    current_date = timezone.now().date()

    # Get all upcoming events
    events = createevents.objects.filter(rend__gte=current_date)

    # Filter by search (event name)
    search_query = request.GET.get('search', '')
    if search_query:
        events = events.filter(event_name__icontains=search_query)

    # Filter by category
    category_filter = request.GET.get('category', '')
    if category_filter:
        events = events.filter(event_category=category_filter)

    # Filter by Free/Paid
    price_filter = request.GET.get('price', '')
    if price_filter:
        if price_filter == 'Free':
            events = events.filter(version='Free')
        elif price_filter == 'Paid':
            events = events.exclude(version='Free')

    # Get all unique categories for the category filter
    categories = createevents.objects.values_list('event_category', flat=True).distinct()

    # Exclude events that the student has already booked
    booked_event_ids = events_participants.objects.filter(student=student, bookstatus='booked').values_list('events', flat=True)
    events = events.exclude(id__in=booked_event_ids)  # Exclude booked events

    return render(request, 'studentviewevent.html', {
        'events': events,
        'categories': categories,
        'search': search_query,
        'category': category_filter,
        'price': price_filter
    })

from django.db import IntegrityError

# Book Events for free
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import createevents, events_participants, student_Registration
from django.db import IntegrityError

def book_event(request, event_id):
    # Fetch the event by its ID
    try:
        event = createevents.objects.get(id=event_id)
    except createevents.DoesNotExist:
        messages.error(request, "Event not found!")
        return redirect('events_list')
    
    # Fetch the logged-in student's email from session
    student_email = request.session.get('email')  # Retrieve email from session
    if not student_email:
        messages.error(request, "You must be logged in to book an event.")
        return redirect('studentlogin')  # Redirect to login page

    # Retrieve the student from the database using the email from session
    try:
        student = student_Registration.objects.get(email=student_email)
    except student_Registration.DoesNotExist:
        messages.error(request, "Student registration not found.")
        return redirect('studentlogin')  # Handle as needed

    # Check if the student has already booked this event
    existing_booking = events_participants.objects.filter(student=student, events=event)
    if existing_booking.exists():
        messages.error(request, "You have already booked this event!")
        return redirect('studentindex')

    # Create a new booking
    try:
        # Automatically assign a booking number
        booking = events_participants.objects.create(
            student=student,  # Use the student object here
            events=event,
            bookstatus='booked',
            
        )
        return render(request, 'bookedstatus.html', {
            'booking': booking,
            'event': event,
            'student': student
        })

        #messages.success(request, f"Successfully booked event '{event.event_name}'. Your booking number is {booking.booking_number}.")
    except IntegrityError:
        messages.error(request, "There was an error while processing your booking. Please try again.")
    
    return redirect('studentindex')  # Redirect back to events list page


# View to display the student's booked events with their booking number


#This code is to view all events for the students
def studenteventviewstotal(request):
    current_date = timezone.now().date()
    events = createevents.objects.filter(rend__gte=current_date).order_by('-doe')
    return render(request,'studenteventsviewtotal.html', {'events': events})


 #This code is to view the judge for students
def studentsjudgeview(request):
    judge= judgeregister.objects.all()
    return render(request,'studentsjudgeview.html',{'judge':judge})


# to View the winners in events for students
def event_winners_view(request):
    today = date.today()

    # Get all events and their respective prizes
    prizes = Prize.objects.filter(event__resultdate__lte=today).order_by('-event__doe')
    events = createevents.objects.filter()  # Optionally filter or add additional filtering here if needed
    return render(request, 'student_event_winners.html', {'prizes': prizes, 'events': events})


#to view payment of each student if they paid
def student_payment_history(request):
    # Retrieve the email from the session
    student_email = request.session.get('email')
    
    if student_email:
        # Fetch the student using the email
        try:
            student = student_Registration.objects.get(email=student_email)
        except student_Registration.DoesNotExist:
            # Handle case where the student does not exist
            return redirect('/studentlogin/')  # Or show an error message

        # Get all the payments made by the student
        payments = Payment.objects.filter(student=student).order_by('-created_at')

        # Pass the student and payments to the template
        context = {
            'student': student,
            'payments': payments
        }
        
        return render(request, 'studentpayment_history.html', context)
    else:
        # If email is not found in session, redirect to login
        return redirect('/studentlogin/')



#Judge--------------------------------------------------------------------------------------------------------------

from .models import judgeregister

def judgeindex(request):
    current_date = timezone.now().date()
    staff_count = staff_Registration.objects.count()
    student_count=student_Registration.objects.count()
    events = createevents.objects.filter( rend__gte=current_date).count()
    
    context={
        'staff_count':staff_count,
        'student_count':student_count,
        'events':events
    }
    return render(request,'judgeindex.html',context)

def judgeregisteration(request):
    if request.method == 'POST':
        jname = request.POST.get('jname')
        gender = request.POST.get('gender')
        email = request.POST.get('email')
        password = request.POST.get('password')
        dob = request.POST.get('dob')
        experience = request.POST.get('experience')
        qualifications = request.POST.get('qualification')
        profilepic = request.FILES.get('profilepic')

        # Check if the email already exists in the database
        if judgeregister.objects.filter(email=email).exists():
            alert="<script>alert('This Email already Registered');window.location.href='/judgeregisteration/';</script>"
            return HttpResponse(alert)
        
        # If the email does not exist, save the judge registration data
        judgeregister.objects.create(
            jname=jname,
            gender=gender,
            email=email,
            password=password,
            dob=dob,
            qualification=qualifications,
            experience=experience,
            profilepic=profilepic,
        )
        messages.success(request, "Judge-Registered Successfully")
        return redirect('judgelogin')
        

    return render(request, 'judgeregister.html')


def judgelogin(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')

        try:
            user=judgeregister.objects.get(email=email,password=password)
            email=user.email
            request.session['email']=email
            return redirect('/judgeindex/')
        except:
             msg="invalid email or password"
             return render(request,'judgelogin.html',{"msg":msg})
    
    return render(request,'judgelogin.html')

# staff view for Judge:
def judgestaffview(request):
    user=staff_Registration.objects.all()
    return render(request,'judgestafflist.html',{'user':user})

# student view for judge
def judgestudentview(request):
    user=student_Registration.objects.all()
    return render(request,'judgestudentlist.html',{'user':user})

#events view for the judge:
def judgeeventsviews(request):
    current_date = timezone.now()
    data=createevents.objects.filter(rend__gte=current_date)
    return render(request,'judgeeventsview.html',{'data':data})


#Judge Profile
def judgeprofile(request):
    email=request.session.get('email')
    if not email:
        alert_message="<script>alert('email doesnot exists ');window.location.href='/judgelogin/';</script>"
        return HttpResponse(alert_message)
        
    user=get_object_or_404(judgeregister, email=email)
    user_info={
        'username':user.jname,
        'password':user.password,
        'gender':user.gender,
        'dob':user.dob,
        'email':user.email,
        'qualification':user.qualification,
        'experience':user.experience,
        'pic':user.profilepic
    }
    return render(request,'judgeprofile.html',user_info)


#Judge profile update
def judgeprofile_update(request):
    email=request.session.get('email')
    if not email:
        return redirect('judgelogin')
    
    if request.method=='POST':
        user=judgeregister.objects.get(email=email)
        jname=request.POST.get('jname')
        gender=request.POST.get('gender')
        email=request.POST.get('email')
        password=request.POST.get('password')
        dob=request.POST.get('dob')
        qualification=request.POST.get('qualification')
        experience=request.POST.get('experience')
        profilepic=request.FILES.get('profilepic')
        user.jname=jname
        user.password=password
        if gender:
            user.gender=gender
        if dob:
            user.dob=dob
        user.email=email
        user.qualification=qualification
        user.experience=experience
        if profilepic:
            user.profilepic=profilepic


        user.save()

        user_info={
        'username':user.jname,
        'password':user.password,
        'gender':user.gender,
        'dob':user.dob,
        'email':user.email,
        'qualification':user.qualification,
        'experience':user.experience,
        'pic':user.profilepic
        }
        messages.success(request, "Profile Updated Successfully")
        return render(request,'judgeprofile.html', user_info)
    else:
        user=judgeregister.objects.get(email=email)
        user_info={
        'username':user.jname,
        'password':user.password,
        'gender':user.gender,
        'dob':user.dob,
        'email':user.email,
        'qualification':user.qualification,
        'experience':user.experience,
        'pic':user.profilepic
        }
    return render(request,'judgeupdate.html', user_info)


#Judge profile delete
def delete_judge(request):  
    email=request.session.get('email')
    user=get_object_or_404(judgeregister, email=email)
    judge={
        'id': user.id,
        'username':user.jname,
        'password':user.password,
        'gender':user.gender,
        'dob':user.dob,
        'email':user.email,
        'qualification':user.qualification,
        'experience':user.experience,
    }
    context = {'staff': judge, 'user': user}
   
    return render(request,'judgedelete.html', context)

# confirm Judge delete:
def judgeconfirmdelete(request, id):
    staffdata=judgeregister.objects.get(id=id)
    staffdata.delete()
    messages.success(request, "JudgeProfile Deleted Successfully")
    return redirect('/')






#Assigned events by admin for judge
def judge_assigned_events(request):
    judge_email = request.session.get('email')  # Get the judge's email from the session
    j = judgeregister.objects.get(email=judge_email)  # Get the judge from the database
    
    # Fetch all events assigned to the judge
    assigned_events = judgeallocate.objects.filter(judgename=j)

    # Add participants directly to the event objects
    for allocation in assigned_events:
        event = allocation.event_details
        participants = events_participants.objects.filter(events=event)  # Fetch participants for each event
        event.participants = participants  # Attach participants to event

    # Debug: Print to check if participants are attached
    for allocation in assigned_events:
        print(f"Event: {allocation.event_details.event_name}, Participants: {allocation.event_details.participants}")

    return render(request, 'judge_assigned_events.html', {
        'assigned_events': assigned_events,  # Pass events with participants
    })

def award_prizes(request, event_id):
    # Get the event object
    event = createevents.objects.get(id=event_id)
    
    # Check if prizes have already been awarded for this event
    existing_prize = Prize.objects.filter(event=event).first()  # Fetch the first prize if already awarded

    # Pass the flag to the template if prizes have been awarded
    prize_awarded = existing_prize is not None

    # If there is already a prize awarded, show the prize and prevent reassignment
    if prize_awarded:
        alert = "<script>alert('Prizes have already been awarded for this event.');window.location.href='/judge/assigned_events/';</script>"
        return HttpResponse(alert)

    # Get all participants who are 'booked' for the event
    participants = events_participants.objects.filter(events=event, bookstatus='booked')
    
    # Ensure there are at least 3 participants for the event
    if participants.count() < 3:
        return render(request, 'error_page.html', {'message': 'At least 3 students must be booked for the event to award prizes.'})

    # If the form is submitted, create the prizes
    if request.method == 'POST':
        jud = request.session['email']
        judge = judgeregister.objects.get(email=jud)
        
        # Get the selected participants from the form
        first_place_id = request.POST.get('first_place')
        second_place_id = request.POST.get('second_place')
        third_place_id = request.POST.get('third_place')
        
        # Get the participants based on the IDs
        first_place = events_participants.objects.get(id=first_place_id)
        second_place = events_participants.objects.get(id=second_place_id)
        third_place = events_participants.objects.get(id=third_place_id)
        
        # Ensure that all participants are distinct for the 3 prizes
        if first_place == second_place or first_place == third_place or second_place == third_place:
            alert = "<script>alert('A participant cannot be awarded more than one prize in the same event.');window.location.href='/judge/assigned_events/';</script>"
            return HttpResponse(alert)

        # Assign the prizes
        Prize.objects.create(
            event=event,
            participant1=first_place,
            participant2=second_place,
            participant3=third_place,
            judge=judge
        )
        alert = "<script>alert('Prize Set Correctly, Thank you');window.location.href='/judgeindex/';</script>"
        return HttpResponse(alert)
    
    # Pass the participants to the template
    return render(request, 'judgeeventresult.html', {'event': event, 'participants': participants,'prize_awarded': prize_awarded})

from itertools import groupby
from operator import itemgetter
from datetime import date
def resultforjudge(request):
    today = date.today()

    # Filter Prizes where the associated event's resultdate is on or after today
    prizes = Prize.objects.filter(event__resultdate__lte=today).order_by('-awarded_on')  # Order by awarded_on descending
    
    # Return the prizes to the template
    return render(request, 'judgeresultpage.html', {'prizes': prizes})



#payment System ----------------------------------------------------------------------------------------------------
# views.py
import json
import razorpay
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


#Payment code need to be corrected 

def initiate_payment(request, cid):
    if not request.session.get('email'):
        return JsonResponse({'status': 'failure', 'error': 'Not logged in'}, status=401)

    try:
        events = createevents.objects.get(id=cid)
        amount = int(events.amount* 100)

        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        payment_order = client.order.create({
            'amount': amount,
            'currency': 'INR',
            'payment_capture': '1'
        })

        user = student_Registration.objects.get(email=request.session['email'])
        response_data = {
            'status': 'success',
            'order_id': payment_order['id'],
            'amount': amount,
            'buyer': {
                'name': user.username,
                'email': user.email,
                'phone': str(user.mobile_no),
                'event_id': events.id
            }
        }
        return JsonResponse(response_data)

    except events.DoesNotExist:
        return JsonResponse({'status': 'failure', 'error': 'Invalid Event'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'failure', 'error': str(e)}, status=500)
from django.db import transaction
@csrf_exempt
@transaction.atomic
def confirm_payment(request, cid, order_id, payment_id, signature):
    try:
        # Initialize Razorpay client
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        
        # Fetch and validate the payment
        payment = client.payment.fetch(payment_id)
        print(f"Payment details: {payment}")  # Debug log
        
        # Verify payment signature
        params_dict = {
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }
        
        try:
            client.utility.verify_payment_signature(params_dict)
        except Exception as e:
            print(f"Signature verification failed: {str(e)}")  # Debug log
            return JsonResponse({
                'status': 'failure',
                'error': 'Payment verification failed'
            }, status=400)
        
        if payment['status'] != 'captured':
            return JsonResponse({
                'status': 'failure',
                'error': 'Payment not captured'
            }, status=400)
            
        # Get the necessary objects
        try:
            event = get_object_or_404(createevents, id=cid)
            user = get_object_or_404(student_Registration, email=request.session.get('email'))
            
            # Create payment record
            payment_obj = Payment.objects.create(
                student=user,
                event=event,
                razorpay_order_id=order_id,
                razorpay_payment_id=payment_id,
                razorpay_signature=signature,
                payment_status='successful',
                amount_paid=event.amount
            )
            
            # Create participant record
            participant = events_participants.objects.create(
                student=user,
                events=event,
                bookstatus="booked",
                payment_id=payment_id,
                payment_status="paid"
            )
            
            # If everything succeeded, render success page
            return render(request, 'pay_success.html', {
               'event': event,
                'booking_number': participant.booking_number,
                'amount': event.amount,
                'Payment': payment_obj,  # Passing the Payment object
                'student': user,         # Passing the student object
                'payment_date': payment_obj.created_at,
                        })
                        
        except Exception as e:
            print(f"Database operation failed: {str(e)}")  # Debug log
            return JsonResponse({
                'status': 'failure',
                'error': 'Failed to record payment'
            }, status=500)
            
    except Exception as e:
        print(f"Payment confirmation failed: {str(e)}")  # Debug log
        return JsonResponse({
            'status': 'failure',
            'error': str(e)
        }, status=500)
    

#student assigned by staff view:
def student_event_assignments(request):
    if request.session.get('email'):  # Check if the student is logged in
        student_email = request.session['email']
        
        try:
            student_data = student_Registration.objects.get(email=student_email)  # Get student data
        except student_Registration.DoesNotExist:
            return HttpResponse("<script>alert('Student not found!');window.location.href='/login/'</script>")

        # Fetch the allocations for the logged-in student and order by event doe (latest first)
        allocations = studentallocation.objects.filter(student=student_data).order_by('-event__doe')

        # Get today's date to compare with event date
        today = date.today()

        return render(request, 'studentassignedbystaff.html', {
            'allocations': allocations,
            'today': today
        })
    
    else:
        return HttpResponse("<script>alert('Please login first!');window.location.href='/login/'</script>")



# result for staff view
def staffresultview(request):
       # Get today's date
    today = date.today()
    
    # Filter events with resultdate greater than or equal to today's date, sorted by resultdate (latest first)
    events_after_today = createevents.objects.filter(resultdate__lte=today).order_by('-resultdate')
    
    # Fetch prizes related to the filtered events, ordered by event's resultdate descending
    result = Prize.objects.filter(event__in=events_after_today).order_by('-event__resultdate')
    return render(request,'staffresultview.html',{'result':result})


#staff view of student feedback:
def staffstudentfeedback(request):
    # Order feedbacks by the 'created_at' field in descending order
    data = Feedback.objects.all().order_by('-created_at')

    # Add the filled_stars and empty_stars lists to each feedback
    for feedback in data:
        feedback.filled_stars = range(feedback.rating)  # A list for filled stars
        feedback.empty_stars = range(feedback.rating, 5)  # A list for empty stars

    return render(request, 'staffstudentfeedback.html', {'data': data})