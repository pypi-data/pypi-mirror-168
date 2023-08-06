import django
from django.shortcuts import render
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.apps import apps
from django.db.models import ForeignKey
from django.shortcuts import render, HttpResponseRedirect
from django.shortcuts import HttpResponse, get_object_or_404
from django.http import Http404, HttpResponseForbidden
from django.urls import reverse
import simplejson as json
import copy

def get_fk_name(model):
    ''' Get The First ForeignKey Field Name '''
    fields = model._meta.get_fields()
    for field in fields:
        if isinstance(field, ForeignKey):
            return field.name
    return None

def model_has_inlines(modelname):
    ''' Check if Model has Inline(s) from his Model Admin '''
    inline_list = get_model_inlines(modelname)
    if len(inline_list) > 0:
        return True
    return False

def get_model_inlines(modelname):
    ''' Get Inline Models from Model Admin '''
    inline_list = []
    for k,v in admin.site._registry.items():
        if v.inlines:
            for i in v.inlines:
                if k.__name__.lower() == modelname.lower():
                    inline_list.append(i.model)
    return inline_list

@staff_member_required
def sortable_inlines_detail(request, app, modelparentname, model_id, modelname, fkfield=None):
    ''' Sort Element from Inline Model'''
    preview_field = False
    TargetModelParent = apps.get_model('{}.{}'.format(app, modelparentname))
    TargetModel = apps.get_model('{}.{}'.format(app, modelname))
    parent_instance = TargetModelParent.objects.get(id=model_id)
    ordering_field = TargetModel._meta.ordering[0]
    if fkfield is None:
        # se non indicato proviamo a pescarlo in autonomia
        fkfield = get_fk_name(TargetModel)
    queryset = TargetModel.objects.filter(**{fkfield: parent_instance})
    res = []
    for q in queryset:
        res.append({'ord': getattr(q, ordering_field), 'obj': q })

    fields = TargetModel._meta.get_fields()
    for field in fields:
        if getattr(field, 'attr_class', None) == django.db.models.fields.files.ImageFieldFile:
            preview_field = True

    context = {
        'res': res,
        'parent_instance': parent_instance,
        'ordering_field': ordering_field,
        'app': app,
        'modelname': modelname,
        'targetModel':  { 'name': TargetModel.__name__,
                         'verbose_name_plural': TargetModel._meta.verbose_name_plural,
                        },
        'parentModel' : { 'name': TargetModelParent.__name__,
                         'verbose_name_plural': TargetModelParent._meta.verbose_name_plural,
                        },
        'preview_field': preview_field,
    }
    return render(request, 'adminvisualsortable/sort-inline-models.html', context)

@staff_member_required
def sort_models(request, app, modelname):
    ''' Sort Element from an Inline Model referring from Parent Model'''
    preview_field = False
    TargetModel = apps.get_model('{}.{}'.format(app, modelname))
    ordering_field = TargetModel._meta.ordering[0]
    queryset = TargetModel.objects.all()
    res = []
    idx_list = []
    warning_dups = False
    for q in queryset:
        res.append({'ord': getattr(q, ordering_field), 'obj': q,  'has_sort_inlines': model_has_inlines(modelname) })
        if getattr(q, ordering_field) in idx_list:
            warning_dups = True
        else:
            idx_list.append(getattr(q, ordering_field))
    if warning_dups:
        from django.core.management import call_command
        call_command('reorder', '{}.{}'.format(app.lower(), modelname.lower()))
        return HttpResponseRedirect(request.path)
    fields = TargetModel._meta.get_fields()
    for field in fields:
        if getattr(field, 'attr_class', None) == django.db.models.fields.files.ImageFieldFile:
            preview_field = True
    context = {
        'res': res,
        'ordering_field': ordering_field,
        'modelInstance': TargetModel,
        'app': app,
        'modelname': modelname,
        'targetModel': { 'name': TargetModel.__name__,
                         'verbose_name_plural': TargetModel._meta.verbose_name_plural,
                         'id': TargetModel.id,
                         'app_name': app
                        },
        'preview_field': preview_field,
    }
    return render(request, 'adminvisualsortable/sort-models.html', context)

@staff_member_required
def sortable_inlines(request, app, modelparentname, model_id):
    ''' If one Inline sortable show sortable layout '''
    ''' If more then one show or should show list of possible inlines to sort'''
    inline_list = []
    for k,v in admin.site._registry.items():
        if v.inlines:
            for i in v.inlines:
                if k.__name__.lower() == modelparentname:
                    inline_list.append(i.model)

    if len(inline_list) == 1:
        return HttpResponseRedirect(reverse('adminvisualsortable:sortable inlines detail', kwargs={
            'app': app,
            'modelparentname': modelparentname,
            'model_id': model_id,
            'modelname': inline_list[0].__name__.lower(),
        }))

    else:
        print('AHI AHI')
        # TODO
        pass


####################################################
################      API    #######################
####################################################

@staff_member_required
def api_sort_models(request):
    ''' Sorting API '''
    context_json = {}
    context_json['status'] = 'error'
    context_json['msg'] = 'Errore Generico'
    if request.method != 'POST':
        return HttpResponse(json.dumps(context_json), content_type="application/json")
    data = json.loads(request.body)
    # print(data)
    id_from = data['id_from']
    id_to = data['id_to']
    model_name = data['model_name']
    app = data['app']
    parent_name = data.get('parentModel', None)

    if bool(parent_name) == False:
        TargetModel = apps.get_model('{}.{}'.format(app, model_name))
        from_obj = TargetModel.objects.filter(id=int(id_from)).first()
        to_obj = TargetModel.objects.filter(id=int(id_to)).first()

    if from_obj is None and to_obj is None:
        return HttpResponse(json.dumps(context_json), content_type="application/json")
    ordering_field = TargetModel._meta.ordering[0]
    to_ordering = copy.deepcopy(getattr(to_obj, ordering_field))
    from_ordering = copy.deepcopy(getattr(from_obj, ordering_field))

    #setattr(to_obj, ordering_field, getattr(from_obj, ordering_field))
    #setattr(from_obj, ordering_field, tmp_ordering)
    TargetModel.objects.filter(id=to_obj.id).update(**{ordering_field: from_ordering})
    TargetModel.objects.filter(id=from_obj.id).update(**{ordering_field: to_ordering})
    to_obj.refresh_from_db()
    from_obj.refresh_from_db()
    context_json['id_from'] = from_obj.id
    context_json['from_ord'] = getattr(from_obj, ordering_field)
    context_json['id_to'] = to_obj.id
    context_json['to_ord'] = getattr(to_obj, ordering_field)
    context_json['status'] = 'success'
    context_json['msg'] = 'Ordinamento aggiornato con successo'
    return HttpResponse(json.dumps(context_json), content_type="application/json")
