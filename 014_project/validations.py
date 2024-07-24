from django.core.exceptions import ValidationError


def contain_only_letters_and_spaces(value):
    for char in value:
        if not char.isalpha() and not char.isspace():
            raise ValidationError('Name can only contain letters and spaces')


def age_validation(value):
    if value < 18:
        raise ValidationError('Age must be greater than or equal to 18')

