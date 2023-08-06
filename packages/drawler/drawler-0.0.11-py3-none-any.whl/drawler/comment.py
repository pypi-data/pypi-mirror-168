"""Crawler for retrieving comments"""

from base64 import b64encode

from .core import Drawler
from ._const import _HEADERS_APP


class Comment(Drawler):
    """Crawler for retrieving comments"""

    def get(self, no, page=1, newest=True):
        reply_page = page

        sort_str = "csort=new&" if newest else ""
        
        url_cmt = (
            "http://m.dcinside.com/api/comment_new.php?"
            "{:s}id={:s}&no={:d}&re_page={:d}&app_id={:s}="
        ).format(sort_str, self.gall, no, reply_page, self._app_id).encode('utf-8')

        mobileurl = (
            "http://m.dcinside.com/api/redirect.php?"
            "hash={:s}%3D%3D"
        ).format(b64encode(url_cmt).decode('utf-8'))

        a = self._s.get(mobileurl, headers=_HEADERS_APP, timeout=self._TIMEOUT)
        res = a.json(strict=False)
        out = None
        if type(res) is dict: out = res
        elif type(res) is list and len(res) == 1: out, = res
        else:
            print(res)
            raise ValueError("Unexpected response")
        return out

