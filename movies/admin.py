from django import forms
from django.contrib import admin
from .models import Category, Genre, Movie, MovieShots, \
                    Actor, RatingStar, Rating, Reviews
from django.utils.safestring import mark_safe


from ckeditor_uploader.widgets import CKEditorUploadingWidget


class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget(), label="Description")

    class Meta:
        model = Movie
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ("id", "name", "url", )
    list_display_links = ("name", )


class ReviewInline(admin.TabularInline):
    model = Reviews
    extra = 1
    readonly_fields = ("name", "email", )


class MovieShotsInline(admin.TabularInline):
    model = MovieShots
    extra = 1
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height="110"')

    get_image.short_description = "Image"


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):

    list_display = ("title", "category", "url", "draft", )
    list_display_links = ("title", )
    list_filter = ("category", "year", )
    search_fields = ("title", "category__name", )
    actions = ("publish", "unpublish")
    inlines = [MovieShotsInline, ReviewInline, ]
    save_on_top = True
    save_as = True
    list_editable = ("draft", )
    readonly_fields = ("get_image", )
    form = MovieAdminForm
    fieldsets = (
        (None, {
            "fields": (("title", "tagline"),)
        }),
        (None, {
            "fields": ("description", ("poster", "get_image"), )
        }),
        (None, {
            "fields": (("year", "world_premiere", "country"),)
        }),
        ("Actors", {
            "classes": ("collapse",),
            "fields": (("actors", "directors", "genres", "category"),)
        }),
        (None, {
            "fields": (("budget", "fees_in_usa", "fees_in_world"),)
        }),
        ("Options", {
            "fields": (("url", "draft"),)
        }),
    )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="100" height="110"')

    def unpublish(self, request, queryset):
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = '1 field updated'
        else:
            message_bit = f'{row_update} fields updated'

        self.message_user(request, f"{message_bit}")

    def publish(self, request, queryset):
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = '1 field updated'
        else:
            message_bit = f'{row_update} fields updated'

        self.message_user(request, f"{message_bit}")

    get_image.short_description = "Poster"

    publish.short_description = "Publish"
    publish.allowed_permissions = ("change", )

    unpublish.short_description = "Unpublish"
    unpublish.allowed_permissions = ("change", )


@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):

    list_display = ("name", "email", "parent", "movie", "id", )
    readonly_fields = ("name", "email", )


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):

    list_display = ("name", "url", )


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):

    list_display = ("name", "age", "get_image", )
    readonly_fields = ("get_image", )

    def get_image(self, obj):
        return mark_safe(f"<img src='{ obj.image.url }' width='50' height='50'")

    get_image.short_description = "Image"


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):

    list_display = ("movie", "ip", "star", )


@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):

    list_display = ("movie", "title", "get_image", )
    readonly_fields = ("get_image", )

    def get_image(self, obj):
        return mark_safe(f"<img src='{ obj.image.url }' width='50' height='50'")

    get_image.short_description = "Image"


@admin.register(RatingStar)
class RatingStarAdmin(admin.ModelAdmin):

    list_display = ("value", )


admin.site.site_title = "Django Movies"
admin.site.site_header = "Django Movies"
