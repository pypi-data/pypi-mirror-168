import pathlib
from pathlib import Path
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.conf import settings
from adminvisualsortable.views import get_fk_name, get_model_inlines
from django.db.models import ForeignKey

class AdminVisualSortableInlineMixin:
    is_adminvisualsortable = True

class AdminVisualSortableMixin:
    @property
    def change_list_template(self):
        opts = self.model._meta
        app_label = opts.app_label
        return str(Path('change_list.html'))

class AdminVisualSortableBaseMixin:
    is_adminvisualsortable = True
    change_form_template =  str(Path('change_form.html'))

    def has_sort_elements(self, object_id):
        TargetModel = self.model.__name__
        inline_list = get_model_inlines(TargetModel)
        for ModelInline in inline_list:
            fields = ModelInline._meta.get_fields()
            for f in fields:
                if f.related_model == self.model:
                    if ModelInline.objects.filter(**{f.name:object_id}).count() > 0:
                        return True
            if ModelInline.objects.filter(fk_chenonsappiamo=object_id).count() > 0:
                return True
        return False

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['is_adminvisualsortable'] = self.is_adminvisualsortable
        extra_context['has_sort_elements'] = self.has_sort_elements(object_id)
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context,
        )