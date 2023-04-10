from django.db import models
from django.contrib.auth.models import User, AbstractUser, Group, Permission


class UserType(models.Model):
    user_type = models.CharField(max_length=100)

    def __str__(self):
        return self.user_type


class Skills(models.Model):
    skill = models.CharField(max_length=100)

    def __str__(self):
        return self.skill


class CustomUser(AbstractUser):
    # ? variant 1 with choices
    # USER_TYPE_CHOICES = [
    #     ('F', 'Freelancer'),
    #     ('C', 'Client'),
    # ]
    # user_type = models.CharField(
    #     max_length=1, choices=USER_TYPE_CHOICES, default='C')

    # ? variant 2 with ForeignKey (Group)
    # user_type = models.ForeignKey(
    #     Group, verbose_name=("Group"), on_delete=models.CASCADE, blank=True, null=True)

    # ? variant 3 with ForeignKey (UserType)
    user_type_id = models.ForeignKey(UserType, verbose_name=(
        "user_type"), on_delete=models.CASCADE, blank=True, null=True)

    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    image = models.ImageField(
        upload_to=f'users/', null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    experience = models.IntegerField(null=True, blank=True)
    skills = models.ManyToManyField(
        Skills, verbose_name=("skills"), blank=True, null=True)

    def __str__(self):
        return self.username
