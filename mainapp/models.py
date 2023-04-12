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
    phone_number1 = models.CharField(max_length=20, null=True, blank=True)
    phone_number2 = models.CharField(max_length=20, null=True, blank=True)
    image = models.ImageField(
        upload_to=f'users/profile_image', null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    rating = models.DecimalField(
        max_digits=2, decimal_places=0, null=True, blank=True)
    about = models.TextField(null=True, blank=True)

    # ? Freelancer fields
    experience = models.IntegerField(null=True, blank=True)
    skills = models.ManyToManyField(
        Skills, verbose_name=("skills"), blank=True, null=True)
    specialization = models.CharField(("specialization"), max_length=100)
    minimal_price = models.DecimalField(
        max_digits=10, decimal_places=0, null=True, blank=True)
    service_image1 = models.ImageField(
        verbose_name='service_image1', upload_to=f'users/service_images', null=True, blank=True)
    service_image2 = models.ImageField(
        verbose_name='service_image1', upload_to=f'users/service_images', null=True, blank=True)
    service_image3 = models.ImageField(
        verbose_name='service_image1', upload_to=f'users/service_images', null=True, blank=True)
    service_image4 = models.ImageField(
        verbose_name='service_image1', upload_to=f'users/service_images', null=True, blank=True)
    service_image5 = models.ImageField(
        verbose_name='service_image1', upload_to=f'users/service_images', null=True, blank=True)

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class ServiceType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Service(models.Model):
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    minimal_price = models.DecimalField(max_digits=10, decimal_places=0)
    image1 = models.ImageField(
        'Image 1', upload_to=f'users/service_images', null=True, blank=True)
    image2 = models.ImageField(
        'Image 2', upload_to=f'users/service_images', null=True, blank=True)
    image3 = models.ImageField(
        'Image 3', upload_to=f'users/service_images', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)


class Order(models.Model):
    choices = (
        ('pending', 'Ожидание исполнения'),
        ('in_progress', 'В процессе'),
        ('completed', 'Завершено')
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    budget = models.DecimalField(max_digits=10, decimal_places=0)
    views = models.IntegerField(default=0)
    deadline = models.DateField()
    status = models.CharField(
        max_length=255, choices=choices, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ActiveOrder(models.Model):
    choices = (
        ('in_progress', 'В процессе'),
        ('completed', 'Завершено')
    )
    order = models.ForeignKey(Order, verbose_name=("order"),
                              on_delete=models.CASCADE)
    freelancer = models.ForeignKey(CustomUser, verbose_name=(
        'freelancer'), on_delete=models.CASCADE)

    def __str__(self):
        return self.order.title
