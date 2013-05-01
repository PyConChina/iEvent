#coding=utf8

from uliweb.orm import *

def get_modified_user():
    from uliweb import request
    
    return request.user.id

class HeadLine(Model):
    title = Field(str, max_length=80, verbose_name='标题', required=True)
    description = Field(TEXT, verbose_name='描述', required=True)
    button_link = Field(str, max_length=1024, verbose_name='按钮链接')
    logo = Field(FILE, max_length=1024, verbose_name='LOGO', hint='图片尺寸不应小于397x208')
    active = Field(bool, verbose_name='活动状态')
    create_date = Field(datetime.datetime, verbose_name='创建时间', auto_now_add=True)
    modified_user = Reference('user', verbose_name='修改人', auto_add=True, auto=True, default=get_modified_user)
    modified_date = Field(datetime.datetime, verbose_name='修改时间', auto_now=True, auto_now_add=True)
    
    def __unicode__(self):
        return self.title
    
    class AddForm:
        fields = ['title', 'description', 'button_link']
        
    class EditForm:
        fields = ['title', 'description', 'button_link']
        
    @classmethod
    def OnInit(cls):
        Index('headline_indx', cls.c.active, cls.c.create_date)
    
    