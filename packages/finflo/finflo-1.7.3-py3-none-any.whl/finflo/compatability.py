import django
from .exception import VersionError 



# checks django bers



if django.VERSION >= (3, 0):
    pass
else:
    raise VersionError
