# need to install https://github.com/yueyoum/social-oauth

def get_oauth_login_url(site):
    """
    Get oauth login url according site
    """
    
    from uliweb import settings
    from socialoauth import socialsites
    from socialoauth.utils import import_oauth_class

    socialsites._sites_id_name_table = {}
    socialsites.config(settings.SOCIALOAUTH)
    
    _s = import_oauth_class(socialsites[site])()
    return _s.authorize_url
    