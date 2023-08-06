"""Crawler for posts"""

from base64 import b64encode

from .core import Drawler
from ._const import _HEADERS_APP

class PostDrawler(Drawler):
    """Crawler for retreiving a post"""

    def get_post(self, no):
        url = (
            "http://m.dcinside.com/api/gall_view_new.php?"
            "id={:s}&no={:d}&app_id={:s}"
        ).format(self.gall, no, self._app_id)
        url_hash = b64encode(url.encode('utf-8')).decode('utf-8')
        a = self._s.get(
            'http://m.dcinside.com/api/redirect.php?hash={:s}'.format(url_hash),
            headers=_HEADERS_APP, 
            timeout=5
        )
        if r'\uae00\uc5c6\uc74c' in a.text: return
        info, = a.json(strict=False)
        return info
    
