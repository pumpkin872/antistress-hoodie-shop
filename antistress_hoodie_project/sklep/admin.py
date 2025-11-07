from django.contrib import admin
from .models import Category, Product, ProductVariant, Person, Position

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductVariant)
admin.site.register(Position)

class PersonAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)
    list_display = ['name', 'surname', 'position']
    list_filter = ['position', 'created']

admin.site.register(Person, PersonAdmin)

