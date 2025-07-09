from django.db import models




# Create your models here.

#staff Registration Model
class staff_Registration(models.Model):
    username=models.CharField(max_length=35, null=True, blank=True)
    password=models.CharField(max_length=35, null=True, blank=True)
    gender_choice=(('Male','male'),
        ('Female','female'),
        ('Prefer Not to Say','prefer not to say'),
    )
    gender=models.CharField(max_length=20, choices=gender_choice, null=True, blank=True)
    dob=models.DateField(null=True,blank=True)
    email=models.EmailField(unique=True, null=True, blank=True)
    department_choice =(
         ('Information_Technology', 'INFORMATION_TECHNOLOGY'),
    ('Computer_Science', 'COMPUTER_SCIENCE'),
    ('Computer_Technology', 'COMPUTER_TECHNOLOGY'),
    ('Biotechnology', 'BIOTECHNOLOGY'),
    ('Physics', 'PHYSICS'),
    ('Chemistry', 'CHEMISTRY'),
    ('Mathematics', 'MATHEMATICS'),
    ('Environmental_Science', 'ENVIRONMENTAL_SCIENCE'),
    ('Astronomy', 'ASTRONOMY'),
    ('Microbiology', 'MICROBIOLOGY'),
    ('Genetics', 'GENETICS'),
    ('Biochemistry', 'BIOCHEMISTRY'),
    ('Geology', 'GEOLOGY'),
    ('Botany', 'BOTANY'),
    ('Zoology', 'ZOOLOGY'),
    ('Psychology', 'PSYCHOLOGY'),
    ('Neuroscience', 'NEUROSCIENCE'),
    ('Applied_Physics', 'APPLIED_PHYSICS'),
    ('Astronomical_Sciences', 'ASTRONOMICAL_SCIENCES'),
    ('Marine_Biology', 'MARINE_BIOLOGY'),
    ('Forensic_Science', 'FORENSIC_SCIENCE'),
    ('Business_Administration', 'BUSINESS_ADMINISTRATION'),
    ('Commerce', 'COMMERCE'),
    ('Economics', 'ECONOMICS'),
    ('Accountancy', 'ACCOUNTANCY'),
    ('Finance', 'FINANCE'),
    ('Marketing', 'MARKETING'),
    ('Business_Law', 'BUSINESS_LAW'),
    ('International_Business', 'INTERNATIONAL_BUSINESS'),
    ('Taxation', 'TAXATION'),
    ('Entrepreneurship', 'ENTREPRENEURSHIP')
    )
    department=models.CharField(max_length=25,choices=department_choice ,null=True, blank=True)
    designation_choice =(
        ('HOD','HOD'),
        ('Assistant_Professor','ASSISTANT PROFESSOR'),
        ('Professor','PROFESSOR'),
    )
    designation=models.CharField(max_length=25,choices=designation_choice, null=True, blank=True)
    pic=models.ImageField(upload_to="staffpic/")
    mobile_no=models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.username

# Student Registration Model:
class student_Registration(models.Model):
    username=models.CharField(max_length=35, null=True, blank=True)
    department_choice =(
        ('Information_Technology', 'INFORMATION_TECHNOLOGY'),
    ('Computer_Science', 'COMPUTER_SCIENCE'),
    ('Computer_Technology', 'COMPUTER_TECHNOLOGY'),
    ('Biotechnology', 'BIOTECHNOLOGY'),
    ('Physics', 'PHYSICS'),
    ('Chemistry', 'CHEMISTRY'),
    ('Mathematics', 'MATHEMATICS'),
    ('Environmental_Science', 'ENVIRONMENTAL_SCIENCE'),
    ('Astronomy', 'ASTRONOMY'),
    ('Microbiology', 'MICROBIOLOGY'),
    ('Genetics', 'GENETICS'),
    ('Biochemistry', 'BIOCHEMISTRY'),
    ('Geology', 'GEOLOGY'),
    ('Botany', 'BOTANY'),
    ('Zoology', 'ZOOLOGY'),
    ('Psychology', 'PSYCHOLOGY'),
    ('Neuroscience', 'NEUROSCIENCE'),
    ('Applied_Physics', 'APPLIED_PHYSICS'),
    ('Astronomical_Sciences', 'ASTRONOMICAL_SCIENCES'),
    ('Marine_Biology', 'MARINE_BIOLOGY'),
    ('Forensic_Science', 'FORENSIC_SCIENCE'),
    ('Business_Administration', 'BUSINESS_ADMINISTRATION'),
    ('Commerce', 'COMMERCE'),
    ('Economics', 'ECONOMICS'),
    ('Accountancy', 'ACCOUNTANCY'),
    ('Finance', 'FINANCE'),
    ('Marketing', 'MARKETING'),
    ('Business_Law', 'BUSINESS_LAW'),
    ('International_Business', 'INTERNATIONAL_BUSINESS'),
    ('Taxation', 'TAXATION'),
    ('Entrepreneurship', 'ENTREPRENEURSHIP')
    )
    department=models.CharField(max_length=35,choices=department_choice ,null=True, blank=True)
    semester=models.CharField(max_length=15,null=True,blank=True)
    rollno=models.CharField(max_length=15, null=True, blank=True)
    gender_choice=(('Male','Male'),
        ('Female','Female'),
        ('Prefer Not to Say','Prefer not to say'),
    )
    gender=models.CharField(max_length=20, choices=gender_choice, null=True, blank=True)
    dob=models.DateField(null=True,blank=True)
    email=models.EmailField(unique=True, null=True, blank=True)
    password=models.CharField(max_length=35, null=True, blank=True)
    pic=models.ImageField(upload_to="studentpic/")
    mobile_no=models.IntegerField(null=True, blank=True)
    def __str__(self):
        return self.username
    



    
class Feedback(models.Model):
    RATING_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]
    Student_Name = models.ForeignKey(student_Registration, on_delete=models.CASCADE, null=True, blank=True)
    feedback_text = models.TextField()
    rating = models.IntegerField(choices=RATING_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.Student_Name:
            return f"{self.Student_Name.username} Rating: {self.rating}, Feedback: {self.feedback_text[:50]}..."
        else:
            return f"Anonymous Rating: {self.rating}, Feedback: {self.feedback_text[:50]}..."
#Events 



# Admin events create page 

class createevents(models.Model):
    cat_choices=(
        ('games','Games'),
        ('entertainment','Entertainment'),
        ('seminar','Seminar'),
        ('workshops','Workshops')
    )
    event_category=models.CharField(max_length=28, choices=cat_choices)
    version_choices=(
        ('Paid','PAID'),
        ('Free','FREE')
    )
    version=models.CharField(max_length=10, choices=version_choices)
    event_name=models.CharField(max_length=50)
    events_description=models.TextField()
    amount=models.IntegerField( null=True, blank=True)
    image=models.ImageField(upload_to='events/')
    doe=models.DateField(unique=True)
    rend=models.DateField()
    resultdate=models.DateField()
    event_created = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.event_name
     

# Staff Allocate:
class staffallocate(models.Model):
    staffname=models.ForeignKey(staff_Registration, on_delete=models.CASCADE)
    event_details=models.ForeignKey(createevents, on_delete=models.CASCADE)
    msg=models.TextField()

    def __str__(self):
        return f"{self.staffname.username}"
    
#Judge Registration Form:
class judgeregister(models.Model):
    jname=models.CharField(max_length=35)
    gender_choice=(
        ('Male','MALE'),
        ('Female','FEMALE'),
        ('Prefer Not to Say','Prefer not to say'),

    )
    gender=models.CharField(max_length=17, choices=gender_choice)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=30)
    dob=models.DateField()
    qualification=models.TextField()
    experience=models.IntegerField()
    profilepic=models.ImageField(upload_to="judgeprofile/")
    def __str__(self):
        return self.jname
    

#events_participants 

import random
import string

class events_participants(models.Model):
    student = models.ForeignKey('student_Registration', on_delete=models.CASCADE)
    events = models.ForeignKey('createevents', on_delete=models.CASCADE)
    bookstatus = models.CharField(max_length=21, choices=(('booked', 'Booked'), ('unplan', 'Unplan')))
    booking_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    payment_id = models.CharField(max_length=255, null=True, blank=True)  # To store Razorpay payment ID
    payment_status_choices = (
        ('pending', 'Pending'),
        ('successful', 'Successful'),
        ('failed', 'Failed')
    )
    PAYMENT_STATUS_CHOICES = [
        ('paid', 'PAID'),
        ('not paid', 'Not Paid'),
        ('failed', 'Failed'),
    ]
    payment_status = models.CharField(max_length=20, choices=payment_status_choices, default='not paid')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Generate unique booking number if not set
        if not self.booking_number:
            self.booking_number = self.generate_booking_number()
        super(events_participants, self).save(*args, **kwargs)

    def generate_booking_number(self):
        """Generate a unique booking number based on the event and student."""
        # You can customize the format as needed, e.g., Event ID + Student ID + Random Suffix
        event_id = str(self.events.id)
        student_id = str(self.student.id)
        random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        
        # Example: Booking number format = "EVENTID-STUDENTID-RANDOM_SUFFIX"
        return f"{event_id}{student_id}{random_suffix}"
    
    def __str__(self):
        return f"Booking Number: {self.booking_number} - {self.student} for {self.events}"


class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('successful', 'Successful'),
        ('failed', 'Failed'),
    ]
    
    razorpay_payment_id = models.CharField(max_length=255)
    razorpay_order_id = models.CharField(max_length=255)
    razorpay_signature = models.CharField(max_length=255)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=50, choices=PAYMENT_STATUS_CHOICES, default='pending')
    event = models.ForeignKey(createevents, on_delete=models.CASCADE)
    student = models.ForeignKey(student_Registration, on_delete=models.CASCADE)  # Assuming you use Django's User model for students
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.razorpay_payment_id} for Event {self.event.event_name}"
    
    

    
class Prize(models.Model):
    event = models.ForeignKey(createevents, on_delete=models.CASCADE)
    
    participant1 = models.ForeignKey('events_participants', on_delete=models.CASCADE, related_name='prize_participant1')
    participant2 = models.ForeignKey('events_participants', on_delete=models.CASCADE, related_name='prize_participant2')
    participant3 = models.ForeignKey('events_participants', on_delete=models.CASCADE, related_name='prize_participant3')
    
    judge = models.ForeignKey(judgeregister, on_delete=models.CASCADE)
    
    awarded_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.participant1.student.username} - {self.event.event_name} '

# Judge Allocate:
class judgeallocate(models.Model):
    judgename=models.ForeignKey(judgeregister, on_delete=models.CASCADE)
    event_details=models.ForeignKey(createevents, on_delete=models.CASCADE)
    msg=models.TextField()

    def __str__(self):
        return f"{self.judgename.jname}"
    

# Students assigned by staff:

class studentallocation(models.Model):
    student=models.ForeignKey(student_Registration, on_delete=models.CASCADE)
    staff=models.ForeignKey(staff_Registration, on_delete=models.CASCADE)
    event=models.ForeignKey(createevents, on_delete=models.CASCADE)
    msg=models.TextField()

    def __str__(self):
        return f"{self.student.username}"