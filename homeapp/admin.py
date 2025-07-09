from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(staff_Registration),
admin.site.register(student_Registration),
admin.site.register(createevents),
admin.site.register(Feedback),
admin.site.register(staffallocate),
admin.site.register(events_participants),
admin.site.register(Payment)

admin.site.register(judgeregister)