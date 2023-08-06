#-*- coding: utf-8 -*-
from django import template
from django.urls import reverse
from django.conf import settings

register = template.Library()

@register.filter(name='get_child_sortable_list')
def get_child_sortable_list(value):
    try:
        value_list = value.split('/')
        obj_id = value_list[-3]
        model_name = value_list[-4]
        app_name = value_list[-5]
    except ValueError:
        return None
    except IndexError:
        return None

    return reverse('adminvisualsortable:sortable inlines', kwargs={'app': app_name, 'modelparentname': model_name, 'model_id': obj_id })


@register.filter(name='get_parent_visualorder_url')
def get_parent_visualorder_url(value):
    obj = value
    return '{}/adminvisualsortable/{}/{}/'.format(settings.HOST, obj._meta.app_label, obj.__class__.__name__.lower())


@register.filter(name='get_parent_admin_url_detail')
def get_parent_admin_url_detail(value):
    obj = value
    return '{}/admin/{}/{}/{}'.format(settings.HOST, obj._meta.app_label, obj.__class__.__name__.lower(), obj.id)


@register.filter(name='get_parent_admin_url_list')
def get_parent_admin_url_list(value):
    model = value
    modelname = model['name'].lower()
    app = model['app_name']
    return '{}/admin/{}/{}/'.format(settings.HOST, app, modelname)