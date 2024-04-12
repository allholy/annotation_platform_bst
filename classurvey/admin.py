from django.contrib import admin

from . import models


class SoundAnswerAdmin(admin.ModelAdmin):
    list_display = ('user_id','chosen_class','confidence','comment','date_created')
    list_filter = ['date_created']

class UserDetailsAdmin(admin.ModelAdmin):
    list_display = ('user_name','user_id','ip_address','date_created')
    search_fields = ['answer']

class TestSoundAdmin(admin.ModelAdmin):
    list_display = ('sound_id','sound_class','sound_group')

class ClassChoiceAdmin(admin.ModelAdmin):
    list_display = ('class_key','class_name','top_level','description','examples')


# given data
admin.site.register(models.ClassChoice, ClassChoiceAdmin)
admin.site.register(models.TestSound, TestSoundAdmin)

# user data
admin.site.register(models.SoundAnswer, SoundAnswerAdmin)
admin.site.register(models.UserDetailsModel, UserDetailsAdmin)