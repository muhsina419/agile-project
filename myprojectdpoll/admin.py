from django.contrib import admin
from .models import Voter
from .models import Profile
from .models import UserProfile
from .models import Candidate
# Register your models here.


admin.site.register(Voter)
admin.site.register(Profile)
admin.site.register(UserProfile)
admin.site.register(Candidate)



