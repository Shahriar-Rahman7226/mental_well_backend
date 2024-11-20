from django.contrib import admin
from apps.user_profile.models import *

# Register your models here.
admin.site.register(SpecializationModel)
admin.site.register(CounselorProfileModel)
admin.site.register(ClientProfileModel)
admin.site.register(CounselorAchievements)
admin.site.register(FounderProfileModel)