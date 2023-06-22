from django.forms.widgets import Widget
from django.template import loader
from django import VERSION
from django.forms import widgets
from django.utils.safestring import mark_safe




from django.forms import widgets

class CountableWidget(widgets.Textarea):
    class Media:
        js = ('admin/js/scripts.js',)
        css = {
            'all':
                ('admin/css/styles.css',)
                }

    def render(self, name, value, attrs=None, **kwargs):
        if VERSION[:2] >= (1, 11):
            final_attrs = self.build_attrs(self.attrs, attrs)
            output = super(CountableWidget, self).render(name, value, final_attrs, **kwargs)
        output += self.get_word_count_template(final_attrs)  
        return mark_safe(output)

    @staticmethod
    def get_word_count_template(attrs):
        count_type = attrs.get('data-count', 'words')
        count_direction = attrs.get('data-count-direction', 'up')
        max_count = attrs.get('data-max-count', '0')

        if count_direction == 'down':
            count_label = ""
            if count_type == "characters":
                count_label = "Characters remaining: "
     
        return (
                 '<span class="text-count" id="%(id)s_counter"> %(label)s'
                 '<span class="text-count-current">%(number)s</span></span>\r\n'
               ) % {'label': count_label,
                   'id': attrs.get('id'),
                   'number': max_count if count_direction == 'down' else '0'}


class ToggleWidget(widgets.CheckboxInput):
    class Media:
        css = {'all': (
            "https://gitcdn.github.io/bootstrap-toggle/2.2.2/css/bootstrap-toggle.min.css", )}
        js = ("https://gitcdn.github.io/bootstrap-toggle/2.2.2/js/bootstrap-toggle.min.js",)


    def __init__(self, attrs=None, *args, **kwargs):
        attrs = attrs or {}

        default_options = {
            'toggle': 'toggle',
            'offstyle': 'danger'
        }
        options = kwargs.get('options', {})
        default_options.update(options)
        for key, val in default_options.items():
            attrs['data-' + key] = val

        super().__init__(attrs)
    def render(self, name, value, attrs=None, **kwargs):
        if VERSION[:2] >= (1, 11):
            final_attrs = self.build_attrs(self.attrs, attrs)
            output = super(ToggleWidget, self).render(name, value, final_attrs, **kwargs)
        
        return mark_safe(output)

import django.http