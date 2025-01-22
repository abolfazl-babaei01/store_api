from django.core.validators import RegexValidator


phone_regex = RegexValidator(
    regex=r'^09\d{9}$',
    message="Mobile Number Must Be Like: 09123456789"
)
