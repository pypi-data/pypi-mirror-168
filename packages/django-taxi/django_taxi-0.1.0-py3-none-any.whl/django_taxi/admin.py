from django.contrib import admin

from .models import Taxonomy, Term, TermTaxonomy, TermTaxonomyItem


@admin.register(Taxonomy)
class TaxonomyAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "parent",
    )
    fields = (
        "name",
        "slug",
        "parent",
    )
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "slug")


@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
    )
    fields = (
        "name",
        "slug",
    )
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "slug")


@admin.register(TermTaxonomy)
class TermTaxonomyAdmin(admin.ModelAdmin):
    fields = (
        "taxonomy",
        "term",
    )
    autocomplete_fields = (
        "taxonomy",
        "term",
    )
    search_fields = (
        "taxonomy__name",
        "term__name",
    )
    list_select_related = ("taxonomy", "term")


@admin.register(TermTaxonomyItem)
class TermTaxonomyItemAdmin(admin.ModelAdmin):
    list_display = (
        "term_taxonomy",
        "content_type",
        "object_id",
    )
    list_filter = ("term_taxonomy__taxonomy", "content_type")
    fields = ("term_taxonomy", "content_type", "object_id")
    autocomplete_fields = ("term_taxonomy",)
    search_fields = (
        "term_taxonomy__term__name",
        "term_taxonomy__taxonomy__name",
        "object_id",
    )
    list_select_related = (
        "term_taxonomy__term",
        "term_taxonomy__taxonomy",
        "content_type",
    )
