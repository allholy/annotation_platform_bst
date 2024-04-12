from django.db import models


# sounds for testing
class TestSound(models.Model):
    sound_id = models.CharField(max_length=50)
    sound_class = models.CharField(max_length=50)
    sound_group = models.IntegerField()
    
    def __str__(self):
        return f"<TestSound {self.sound_id}>"

class ClassChoice(models.Model):
    class_key = models.CharField(max_length=10)
    class_name = models.CharField(max_length=50)
    top_level = models.CharField(max_length=20)
    description = models.CharField(max_length=255, null=True)
    examples = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"<ClassChoice {self.class_name}>"

class TopLevel(models.Model):
    top_level_name = models.CharField(max_length=10)
    top_level_description = models.CharField(max_length=255)

    def __str__(self):
        return f"<TopLevel {self.class_name}>"
    
class SoundAnswer(models.Model):
    user_id = models.CharField(max_length=50)  # random generate
    test_sound = models.ForeignKey(TestSound, on_delete=models.CASCADE)
    date_created = models.DateTimeField('Creation date', auto_now_add=True) #timezone aware

    # NOTE: If you change the keys, you have to be careful
    # to change them manually in annotate_sound.html file.

    # Import choices and put them in a tuple.
    chosen_class = models.CharField(max_length=15, default="")
    likert_choices = ((1, 'Very Unconfident'), (2, 'Unconfident'), (3, 'Neutral'), (4, 'Confident'), (5, 'Very Confident'))
    confidence = models.IntegerField(choices=likert_choices,default="")
    comment = models.CharField(max_length=100, null=True, blank=True, default="")

class UserDetailsModel(models.Model):
    user_id = models.CharField(max_length=50) #, unique=True
    ip_address = models.GenericIPAddressField(null=True)
    user_name = models.CharField(max_length=50, null=True, default="")
    date_created = models.DateTimeField('Creation date', auto_now_add=True)
