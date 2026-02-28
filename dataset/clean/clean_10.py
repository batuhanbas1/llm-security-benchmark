def validate_age(age):
    if not isinstance(age, int) or age < 0 or age > 120:
        raise ValueError("Invalid age")
    return True