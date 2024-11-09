class IOError(ValueError):
    pass


pattern_username: str = r'[A-z0-9]{2,32}'
pattern_phone: str = r'[0-9]{10}'
pattern_birthday: str = r'%d.%m.%Y'
pattern_email: str = (
    r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*"
    r"@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$"
)