"""Crawler for lists"""

from base64 import b64encode
from math import floor

from .core import Drawler
from ._const import _APP_API, _HEADERS_APP

_ARTICLE_LIST = _APP_API + "gall_list_new.php"
_ApiUrl_REDIRECT = _APP_API + "redirect.php"

class ListDrawler(Drawler):
    """Cralwer for retrieving a list"""
    
    def get_list(self, page, recomm=False):
        
        _page = int(page)
        assert (_page == page) and (1 <= _page)
        
        url = "{:s}?id={:s}&page={:d}&app_id={:s}".format(_ARTICLE_LIST, self.gall, _page, self._app_id)
        if recomm: url += "&recommend=1"
        url_redir = _ApiUrl_REDIRECT + "?hash=" + b64encode(url.encode('utf-8')).decode("utf-8")

        res = self._s.get(url_redir, headers=_HEADERS_APP, timeout=5)
        info, = res.json(strict=False)
        return info

    def get_most_recent_post_no(self, return_json=False):
        js = self.get_list(1)
        post_no_recent = int(js['gall_list'][0]['no'])
        res = post_no_recent
        if return_json: res = (res, js)
        return res

    def get_page_no(self, post_no, N_max_search=15, page_init=1, v=False):
        page = page_init
        page_max = page
#        offset = 0
        for j_trial in range(N_max_search):
            if v > 0: print("Retrieving page {:d} ... ".format(page), end='')
            info = self.get_list(page)
            if v > 0: print("done")
            gall_list = info['gall_list']
            if v > 1: print([l['no'] for l in gall_list])
            N_per_list = len(gall_list)
            if v > 0: print("{:d} posts found in the list page {:d}".format(N_per_list, page))
            if N_per_list == 0:
                offset_adjust = int(0.5 * (page - page_max))
                assert offset_adjust > 0
                page = page_max + offset_adjust
                continue
#                offset = 
            elif N_per_list > 0:
                page_max = page
            assert N_per_list > 0
            post_no_last, post_no_first = (int(gall_list[j]['no']) for j in (0, -1))
            if page == 1 and post_no_last < post_no:
                raise ValueError("The given post_no(={:d}) exceeds the most recent post_no(={:d})".format(post_no, post_no_last))
#             assert post_no_last - post_no_first >= N_per_list
            if post_no_last >= post_no and post_no >= post_no_first: break
            elif N_per_list == 0:
                raise ValueError("N_per_list == 0")
            else:
                offset = floor((post_no_last - post_no) / N_per_list)
                assert offset != 0
                page = page + offset
            if page < 1: raise ValueError("Invalid page number: {:d}".format(page))
#            page_max = page
            if v > 0: print()

        if j_trial == N_max_search - 1:
            raise ValueError("Could not find the page number")
        elif j_trial > N_max_search - 1:
            raise ValueError("Unexpected exception")
        return page
