def get_user_image(user, size=20):
    """
    Get one's portrait from gravatar.com
    This code copies from http://blog.gravatar.com/2008/01/17/gravatars-in-python-25/
    
    if the user is loginned via weibo, then use image directly, it should be
    the image url
    """
    from uliweb import functions
    import urllib, hashlib
     
    if user:
        if user.login_type == '0': #login type
            email = user.email or "Someone@somewhere.com"
            default = functions.url_for_static('images/user50x50.jpg', _external=True)
     
            # construct the url 
            gravatar_url = "http://www.gravatar.com/avatar.php?"
            gravatar_url += urllib.urlencode({'gravatar_id':hashlib.md5(email.lower()).hexdigest(), 'default':default, 'size':str(size)})
            
            return gravatar_url
        if user.login_type == '1': #weibo
            return user.image
    else:
        return functions.url_for_static('images/user%dx%d.jpg' % (size, size), _external=True)