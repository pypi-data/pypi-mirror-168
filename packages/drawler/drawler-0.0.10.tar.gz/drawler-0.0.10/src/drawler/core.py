"""core"""

from importlib import resources
from os.path import join
with resources.path('jar','KotlinInside-1.10.2-all.jar') as f:
    path_jar = join(*f.parts)

from jnius_config import set_classpath
set_classpath(path_jar)

from jnius import autoclass
from requests import Session

#def add_one(number):
#    return number + 1


class Drawler(object):
    
    def __init__(self, gall):
        """
        # Arguments
        gall: string
            The id of the gallery to be crawled on.
        jar_dir: string
            The path of the directory where the KotlinInside jar is located.
        """
        
        self.gall = gall

        user = autoclass("be.zvz.kotlininside.session.user.Anonymous")
        inside = autoclass("be.zvz.kotlininside.KotlinInside")
        http = autoclass("be.zvz.kotlininside.http.DefaultHttpClient")
        marker = autoclass("kotlin.jvm.internal.DefaultConstructorMarker")
        
        print("[ LOG ] Creating an instance ... ", end='')
        passwd = "gggigkeaagjid"
        inside.createInstance(user("ㅇㅇ",passwd), http(True,True))
        _i = inside(user("ㅇㅇ",passwd), http(True,True), marker)
        print("done")
        
        print("[ LOG ] Generating a client token ... ", end='')
        _i.generateClientToken()
        print("done")
        self._i = _i
        
        print("[ LOG ] Generating an App ID ... ", end='')
        self._app_id = _i.generateAppId()
        print("done")
        
        self._s = Session()


    def renew_app_id(self):
        self._app_id = self._i.generateAppId()

