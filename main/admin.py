from django.contrib import admin
from .models import Product, Keyword, Rank


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'num')


class KeywordAdmin(admin.ModelAdmin):
    list_display = ('number', 'product', 'name')


class RankAdmin(admin.ModelAdmin):
    list_display = ('date_searched', 'product', 'keyword', 'rank')


admin.site.register(Product, ProductAdmin)
admin.site.register(Keyword, KeywordAdmin)
admin.site.register(Rank, RankAdmin)

