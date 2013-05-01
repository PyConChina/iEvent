#coding=utf8
from uliweb import expose, functions, settings
from uliweb.i18n import gettext_lazy as _

@expose('/admin/headlines')
class HeadLineAdminView(object):
    def __begin__(self):
        return functions.require_login()
        
    def __init__(self):
        self.model = functions.get_model('headline')
        
    def _get_query_view(self, url):
        """
        Return a query view object
        """
        from uliweb.form import IntField
        from uliweb.contrib.generic.forms import QueryForm
        
        id = IntField(label=_('ID'))
        fields = [('id', id),]
        layout = [('id',)]
        query = functions.QueryView(self.model, ok_url=url, fields=fields, layout=layout, form_cls=QueryForm)
        return query
        
    def _get_fields(self):
        """
        Return list fields info, and it'll be used in angularjs template
        """
        view = functions.ListView(self.model)
        return view.table_info['fields_list']
        
    @expose('')
    def list(self):
        query = self._get_query_view(url_for(self.__class__.list))
        c = query.run()
        
        condition = None
        
        if c.get('id'):
            condition = (self.model.c.id == c['id']) & condition

        def _logo(value, obj):
            return functions.get_href(obj.logo)
        
        fields_convert_map = {'logo':_logo}
        
        view = functions.ListView(self.model, 
#            pageno=page, #get page info from request
#            rows_per_page=rows, #get rows info from request
            pagination=True,
            condition=condition,
            order_by=self.model.c.create_date.desc(),
            fields_convert_map=fields_convert_map,
        )
        
        
        
        if 'data' in request.values:
            return json(view.json())
        
        result = view.run()
        result['view'] = view
        
        
        return result
    
    def add(self):
        def pre_save(data):
            data['active'] = True
            
        def post_created_form(fcls, model):
            pass
            
        def post_save(obj, data):
            pass
    
        def success_data(obj, data):
            d = obj.to_dict()
            return d
        
        def get_url(id):
            return url_for(self.__class__.list)
        
        template_data = {'layout':'siteman_layout.html'}
        
        view = functions.AddView(self.model,
            ok_url=get_url,
            pre_save=pre_save,
            post_save=post_save,
            post_created_form=post_created_form,
            template_data=template_data,
            success_data=True,
            )
#        response.template = 'GenericView/add.html'
        return view.run(json_result=False)
        
    def view(self, id):
        """
        Show the detail of object. Template will receive an `object` variable 
        """
        obj = self.model.get_or_notfound(int(id))
        
        fields_convert_map = {}
        template_data = {}
        
        view = functions.DetailView(self.model, 
            obj=obj,
            template_data=template_data,
            fields_convert_map=fields_convert_map,
        )
#        response.template = 'GenericView/view.html'
        return view.run()
        
    def edit(self, id):
        def success_data(obj, data):
            d = obj.to_dict()
            d['logo'] = functions.get_href(obj.logo)
            return d
           
        def post_created_form(fcls, model, obj):
            pass
        
        template_data = {}
        
        obj = self.model.get_or_notfound(int(id))
        view = functions.EditView(self.model, 
            ok_url=url_for(self.__class__.list),
            obj=obj, 
            template_data=template_data,
            post_created_form=post_created_form,
            success_data=True,
            )
#        response.template = 'GenericView/edit.html'
        return view.run(json_result=True)
        
    def delete(self, id):
        def pre_delete(obj):
            pass
            
        obj = self.model.get_or_notfound(int(id))
        view = functions.DeleteView(self.model, 
            ok_url=url_for(self.__class__.list),
            obj=obj,
            pre_delete=pre_delete,
        )
        return view.run(json_result=True)
    
    def active(self, id):
        """
        切換在首页显示状态
        """
        obj = self.model.get(int(id))
        if not obj:
            return json({'success':False, 'message':'找不到对应的记录'})
        else:
            obj.active = not obj.active
            obj.save()
            return json({'success':True, 'data':{'active':obj.active}})
        
    def upload_logo(self, id):
        """
        上传logo处理
        """
        from uliweb.form import Form, ImageField
        class ImageForm(Form):
            file = ImageField()
           
        obj = self.model.get(int(id))
        if not obj:
            return json({'success':False, 'message':'记录没有找到'})
        
        form = ImageForm()
        if form.validate(request.files):
            fname = functions.save_file(form.data['file'].filename, form.data['file'].file)
            obj.logo = fname
            obj.save()
            return json({'success':True, 'data':{'logo':functions.get_href(fname)}})
        else:
            return json({'success':False, 'message':form.error['file']})