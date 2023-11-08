from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
settings.configure()
print(check_password('123',make_password('pbkdf2_sha256$600000$cVK47wvFlEfhUTf249JA0m$JCia/3HyIg5WOV36Un2EAF1tT8PiA96I9C7wH1vKOVw=')))
