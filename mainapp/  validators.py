from django.core.exceptions import ValidationError


def CustomPasswordValidator(password):
    if len(password) < 8:
        raise ValidationError(
            'Пароль должен быть не менее 8 символов',
            code='password_too_short',
        )
    if not any(char.isdigit()for char in password):
        raise ValidationError(
            'Пароль должен содержать хотя бы одну цифру',
            code='password_no_digit',
        )
