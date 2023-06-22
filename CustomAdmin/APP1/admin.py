from django.contrib import admin
from APP1.models import *
from django.contrib import messages
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter, NumericRangeFilter
from django_admin_listfilter_dropdown.filters import DropdownFilter, ChoiceDropdownFilter, RelatedDropdownFilter,SimpleDropdownFilter,RelatedFieldListFilter,AllValuesFieldListFilter
from django.contrib.auth.models import Group, User
from admin_auto_filters.filters import AutocompleteFilter
from APP1.forms import *
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from django.utils.html import escape

admin.site.site_header = "Admin Panel"
admin.site.index_title = "Customization Project Portal"
admin.site.site_title = "Customized Admin Panel"
# admin.site.login_template="admin.login.html"
# admin.site.login_form=AdminAuthenticationForm
#admin.site.index_template="admin.home.html"

class BookInline(admin.TabularInline):
    model = Book  

class GradeFilter(admin.SimpleListFilter):
    title = 'Rating'
    parameter_name = 'rating'

    def lookups(self, request, model_admin):
        return (
            ('Yes', '>=3'),
            ('No', '<=2'),
        )

    def queryset(self, request, queryset):
        print("queryset",queryset)
        value = self.value()
        if value == 'Yes':
            return queryset.filter(rating__gt=3)
        elif value == 'No':
            return queryset.exclude(rating__gt=2)
        return queryset


class BookFilter(AutocompleteFilter):
    title = 'Authors' # display title
    field_name = 'authors' # name of the foreign key field

class PublisherAdmin(admin.ModelAdmin):
    list_display = ["name","address","city","state_province","country","website","dob"]
    list_display_links =["city","name"]
    list_filter=[('city',DropdownFilter)]
    inlines = [BookInline]
    list_editable=["dob"]


    
class AuthorAdmin(admin.ModelAdmin):
    feilds='__all__'
    list_display = ["first_name","last_name","email","Average_Rating","Books_Written","books_count","dob"]
    list_display_links = None
    list_per_page = 10
    list_editable=["email"]

    def books_count(self, obj):
        return obj.book_set.count()

    search_fields=["first_name","last_name"]

    def has_add_permission(self, request,obj=None):
        return False
    def has_change_permission(self,request, obj=None):
         return False

    def has_delete_permission(self,request, obj=None):
         return False
    def has_view_permission(self,request,obj=None):
        return True

    def Average_Rating(self, obj):
        from django.db.models import Avg
        result = Book.objects.filter(authors=obj).aggregate(Avg("rating"))
        return result["rating__avg"]
    def Books_Written(self,obj):
       
        from django.utils.http import urlencode
        count = obj.book_set.count()

        ### FORMAT "admin:%(app)s_%(model)s_%(page)"
        #https://realpython.com/customize-django-admin-python/#providing-links-to-other-object-pages
        url = (
            reverse("admin:APP1_book_changelist")
            + "?"
            + urlencode({"authors__id": f"{obj.id}"})
        )
        
        return format_html('<a href="{}">{} Books</a>', url, count)
        
    Books_Written.short_description = "Books Written"
                

from advanced_filters.admin import AdminAdvancedFiltersMixin

class BooksAdmin(AdminAdvancedFiltersMixin,admin.ModelAdmin):
    list_display = ['title','publisher','publication_date','rating','get_authors','delete','createdon','modifiedby']
    ordering = ('-id',)
    advanced_filter_fields = ('title', 'rating',)

    
    def delete(self, obj):
        view_name = "admin:{}_{}_delete".format(obj._meta.app_label, obj._meta.model_name)
        link = reverse(view_name, args=[obj.id])
        html = '<input type="button" onclick="location.href=\'{}\'" value="Delete" />'.format(link)
        return format_html(html)




    list_display_links = None
    date_hierarchy='publication_date'
    search_fields=["publisher__state_province","authors__email","publisher"]
    list_filter=[('publication_date', DateRangeFilter),
                ('publisher', RelatedDropdownFilter),BookFilter,GradeFilter
        ]
    radio_fields = {"publisher": admin.HORIZONTAL}

    
    #Multi Select By Passing Id's Cant use Both at a time disable one option to use another
    raw_id_fields = ("authors",)
    #Multi Select By Choosing 
    #filter_horizontal=['authors']

    # Feild or Feildsets any one can be used but not both
    fieldsets = (
        (None, {
            'fields': ('title', 'publisher', 'publication_date', 'rating')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('authors',),
        }),)

    def get_authors(self, instance):
        return [author for author in instance.authors.all()]










from django.contrib import admin
from admin_auto_filters.filters import AutocompleteFilter


class ArtistFilter(AutocompleteFilter):
    title = 'Artist' # display title
    field_name = 'artist' # name of the foreign key field

    

class ArtistAdmin(admin.ModelAdmin):
    list_display =['name_colored','immortal',]
    search_fields = ['name'] # this is required for django's autocomplete functionality
    actions=['mark_immortal','mark_mortal']

    def name_colored(self, obj):
        if obj.immortal:
            print("TRUE")
            color_code = '00FF00'
        else:
            print("FALSE")
            color_code = 'FF0000'
        html = '<span style="color: #{};">{}</span>'.format(color_code, obj.name)
        return format_html(html)
    name_colored.admin_order_field = 'name'
    name_colored.short_description = 'name'


    def mark_immortal(self, request, queryset):
         queryset.update(immortal=False)
    def mark_mortal(self, request, queryset):
         queryset.update(immortal=True)
         
    def get_actions(self, request):
        actions = super().get_actions(request)
        if request.user.username[0].upper() != 'J':
            if 'delete_selected' in actions:
                del actions['delete_selected']
        return actions


class AlbumAdmin(admin.ModelAdmin):
    change_list_template='change_list_form.html'
    
    fields=['name','cover','image','artist']
    list_display =['name','artist','cover','get_image']
    list_display_links = ['name']
    list_filter = [ArtistFilter]
    autocomplete_fields = ["artist"]

    def get_image(self,obj):
        return format_html('<img src="{}" width="100",height="80" />'.format('http://127.0.0.1:8000/media/'+str(obj.image)))




admin.site.register(Artist,ArtistAdmin)
admin.site.register(Album,AlbumAdmin)
admin.site.register(Publisher,PublisherAdmin)
admin.site.register(Author,AuthorAdmin)
admin.site.register(Book,BooksAdmin)


