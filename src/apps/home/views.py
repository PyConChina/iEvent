#coding=utf-8
from uliweb import expose, functions

@expose('/')
def index():
    Head = functions.get_model('headline')
    objects = Head.filter(Head.c.active==True).order_by(Head.c.create_date.desc())
    return {'objects':objects}
