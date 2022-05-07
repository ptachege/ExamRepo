from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    university = models.CharField(max_length=100)
    campus = models.CharField(max_length=100)
    current_year = models.CharField(max_length=100)
    course_taking = models.CharField(max_length=200)
    avatar = models.ImageField(null=True, blank=True)
    visitorcount = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class Exams(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    university = models.CharField(max_length=100)
    course_name = models.CharField(max_length=100)
    unit_name = models.CharField(max_length=100)
    unit_year = models.CharField(max_length=100)
    unit_code = models.CharField(max_length=100)
    unit_file = models.FileField()
    exam_year = models.CharField(blank=True, null=True, max_length=100)
    is_validate = models.BooleanField(default=False)

    def __str__(self):
        return self.unit_name + ' - ' + self.exam_year

    class Meta:
        verbose_name = 'Exam'
        verbose_name_plural = 'Exams'


class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=1000)
    time_send = models.DateTimeField(auto_now_add=True)
