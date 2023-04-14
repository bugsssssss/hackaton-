from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User


class UserType(models.Model):
    user_type = models.CharField(max_length=100)

    def __str__(self):
        return self.user_type


class Skills(models.Model):
    skill = models.CharField(max_length=100)

    def __str__(self):
        return self.skill

    class Meta:
        verbose_name = 'Skill'
        verbose_name_plural = 'Skills'


class Chat(models.Model):
    sender = models.ForeignKey(
        'mainapp.CustomUser', on_delete=models.CASCADE, related_name='sender')
    send_to = models.ForeignKey('mainapp.CustomUser', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.sender} - {self.send_to}"


class Message(models.Model):
    statuses = (
        ('S', 'Sent'),
        ('R', 'Read'),
        ('D', 'Deleted'),
    )
    chat = models.ForeignKey('mainapp.Chat', on_delete=models.CASCADE)
    sender = models.ForeignKey(
        'mainapp.CustomUser', on_delete=models.CASCADE, related_name='message_sender')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=statuses, default='S')
    edited_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.sender.username} - {self.text}"


class Language(models.Model):
    language = models.CharField(max_length=100)

    def __str__(self):
        return self.language


class Experience(models.Model):
    owner = models.ForeignKey(
        'mainapp.CustomUser', on_delete=models.CASCADE, related_name='experience_owner')
    experience = models.CharField(max_length=100)
    from_year = models.IntegerField()
    to_year = models.IntegerField()

    def __str__(self):
        return self.experience


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
        upload_to=f'users/profile_image', null=True, blank=True, default='')
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    rating = models.DecimalField(
        max_digits=2, decimal_places=0, null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    personal_info = models.TextField(null=True, blank=True)
    # ? Freelancer fields
    experience = models.ManyToManyField(Experience, blank=True, null=True)
    experience_years = models.IntegerField(null=True, blank=True)
    skills = models.ManyToManyField(
        Skills, verbose_name=("skills"), blank=True, null=True)
    specialization = models.CharField(
        ("specialization"), max_length=100, null=True, blank=True)
    minimal_price = models.DecimalField(
        max_digits=10, decimal_places=0, null=True, blank=True)
    languages = models.TextField(("languages"), blank=True, null=True)
    education = models.TextField(("education"), blank=True, null=True)
    awards = models.TextField(("awards"), blank=True, null=True)
    service_info = models.TextField(("service_info"), blank=True, null=True)
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


class Wallet(models.Model):
    owner = models.ForeignKey("mainapp.CustomUser", verbose_name=(
        "owner"), on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    last_transaction = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.owner.username


class Category(models.Model):
    name = models.CharField(max_length=255)
    subtitle = models.CharField(("subtitle"), max_length=255)
    picture = models.ImageField(
        'picture', upload_to=f'users/service_images', null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class ServiceType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Service(models.Model):
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ForeignKey("mainapp.Category", verbose_name=(
        "category"), on_delete=models.CASCADE)
    minimal_price = models.DecimalField(max_digits=10, decimal_places=0)
    image1 = models.ImageField(
        'Image 1', upload_to=f'users/service_images', null=True, blank=True)
    image2 = models.ImageField(
        'Image 2', upload_to=f'users/service_images', null=True, blank=True)
    image3 = models.ImageField(
        'Image 3', upload_to=f'users/service_images', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)


class Payment(models.Model):
    payment_choices = (
        ('fixed', 'Фиксированная'),
        ('hourly', 'Почасовая'),
    )
    payment_status = {
        ('pending', 'Ожидание'),
        ('completed', 'Успешно'),
        ('canceled', 'Отменено'),
    }
    payment_currency = (
        ('usd', 'USD'),
        ('eur', 'EUR'),
        ('rub', 'RUB'),
        ('uzs', 'UZS')
    )
    order = models.ForeignKey(
        'mainapp.Order', on_delete=models.CASCADE, blank=True, null=True)
    owner = models.ForeignKey('mainapp.CustomUser', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=0)
    currency = models.CharField(
        max_length=3, choices=payment_currency, default='uzs')
    status = models.CharField(
        max_length=10, choices=payment_status, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.order} - {self.amount} {self.currency}"


class Order(models.Model):
    choices = (
        ('pending', 'Ожидание исполнения'),
        ('in_progress', 'В процессе'),
        ('completed', 'Завершено'),
        ('canceled', 'Отменено'),
    )
    budget_types = (
        ('fixed', 'Фиксированная'),
        ('hourly', 'Почасовая'),
    )
    budget_currency = (
        ('usd', 'USD'),
        ('eur', 'EUR'),
        ('rub', 'RUB'),
        ('uzs', 'UZS')
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    freelancer = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='freelancer', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    budget = models.DecimalField(max_digits=10, decimal_places=0)
    budget_currency = models.CharField(
        'currency', max_length=3, choices=budget_currency)
    budget_type = models.CharField(
        'budget_type', max_length=10, choices=budget_types)
    views = models.IntegerField(default=0)
    deadline = models.DateField()
    required_skills = models.CharField(("required skills"), max_length=255)
    country = models.CharField(
        'country', max_length=100, null=True, blank=True)
    city = models.CharField('city', max_length=100, null=True, blank=True)
    status = models.CharField(
        max_length=255, choices=choices, default='pending')
    is_published = models.BooleanField(("published"), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class OrderFeedback(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    feedback = models.CharField('feedback', max_length=255)
    is_published = models.BooleanField(("published"), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.feedback


class ActiveOrder(models.Model):
    order = models.ForeignKey(Order, verbose_name=("order"),
                              on_delete=models.CASCADE)
    freelancer = models.ForeignKey(CustomUser, verbose_name=(
        'freelancer'), on_delete=models.CASCADE)

    def __str__(self):
        return self.order.title
