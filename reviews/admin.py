from django.contrib import admin


from .models import Place, Review


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0


class PlaceAdmin(admin.ModelAdmin):
    inlines = [ReviewInline]
    search_fields = ['name']


admin.site.register(Place, PlaceAdmin)
