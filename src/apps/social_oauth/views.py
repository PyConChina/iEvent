#coding=utf8

# Porcess after weibo signed in
#

from uliweb import expose, functions

@expose('/oauth/<site>')
def callback(site):
    from socialoauth import socialsites
    from socialoauth.utils import import_oauth_class
    from socialoauth.exception import SocialAPIError
    from uliweb.contrib.auth import login
    from uliweb.utils import date

    code = request.GET.get('code')
    if not code:
        # error occurred
        error("Can't found the code from oauth return data")
    
    socialsites._sites_id_name_table = {}
    socialsites.config(settings.SOCIALOAUTH)

    s = import_oauth_class(socialsites[site])()
    try:
        s.get_access_token(code)
    except SocialAPIError as e:
        print e.site_name      
        print e.url            
        print e.error_msg     
        raise
    
    # we can get uid, name, avatar from s
    # we should store the user info to database

    User = functions.get_model('user')
    user = User.get((User.c.username==s.uid) & (User.c.login_type=='1') & (User.c.login_site==site))
    if not user:
        user = User(username=s.uid, nickname=s.name, image=s.avatar,
            login_type='1', login_site=site)
        user.save()
        login(user)
        #引导用户填写邮箱地址
        return redirect('/user')
    else:
        user.last_login = date.now()