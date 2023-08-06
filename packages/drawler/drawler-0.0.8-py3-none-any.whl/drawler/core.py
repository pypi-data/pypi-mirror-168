"""core"""

from importlib import resources
from os.path import join
with resources.path('jar','KotlinInside-1.10.2-all.jar') as f:
    path_jar = join(*f.parts)

from jnius_config import set_classpath
set_classpath(path_jar)

def add_one(number):
    return number + 1


