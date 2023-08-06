from django import forms
from django.contrib.contenttypes.fields import GenericRelation


class TaxiBaseField:
    taxonomy_slug = None

    def __init__(self, taxonomy_slug: str, *args, **kwargs):
        self.taxonomy_slug = taxonomy_slug
        super().__init__(*args, **kwargs)


class TaxiField(TaxiBaseField, forms.MultipleChoiceField):
    widget = forms.CheckboxSelectMultiple


class TaxiSingleField(TaxiBaseField, forms.ChoiceField):
    widget = forms.Select


class TaxiRelation(GenericRelation):
    taxonomy = f"django_taxi.TermTaxonomyItem"

    def __init__(self, taxonomy: str = None, **kwargs):
        if taxonomy:
            self.taxonomy = taxonomy
        super().__init__(self.taxonomy, **kwargs)
