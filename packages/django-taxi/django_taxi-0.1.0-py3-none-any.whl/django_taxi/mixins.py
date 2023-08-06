from django import forms
from django.contrib.contenttypes.models import ContentType
from django.db import transaction

from .fields import TaxiField, TaxiSingleField
from .models import TermTaxonomy, TermTaxonomyItem


class TaxiModelMixin(forms.ModelForm):
    """
    Mixin used on model forms where a TaxiField is set.
    The mixin is responsible to create and delete
    TermTaxonomyItems for a given instance based on form data.
    """

    taxi_fields = None

    def __init__(self, *args, **kwargs):
        self.taxi_fields = {}
        for field_name, field in self.__class__.base_fields.items():
            if type(field) in [TaxiField, TaxiSingleField]:
                self.taxi_fields[field_name] = field.taxonomy_slug

        # Set initial
        instance = kwargs.get("instance")
        if instance:
            kwargs["initial"] = kwargs.get("initial", {})
            for field in self.taxi_fields:
                kwargs["initial"].update(
                    {
                        field: list(
                            instance.terms.values_list("term_taxonomy__term", flat=True)
                        )
                    }
                )

        super().__init__(*args, **kwargs)

        # Set choices
        for field in self.taxi_fields:
            self.fields[field].choices = self.get_choices(field).values_list(
                "id", "term__name"
            )

    def get_choices(self, field):
        return TermTaxonomy.objects.filter(taxonomy__slug=self.taxi_fields[field])

    def get_existing_term_taxonomy_ids(self, field, instance):
        return list(
            instance.terms.filter(
                term_taxonomy__taxonomy__slug=self.taxi_fields[field]
            ).values_list("term_taxonomy", flat=True)
        )

    def _save_taxi(self):
        instance = self.instance
        content_type = ContentType.objects.get_for_model(instance)
        with transaction.atomic():
            for field, term_taxonomy in self.taxi_fields.items():
                existing = self.get_existing_term_taxonomy_ids(field, instance)
                choices = self.get_choices(field)
                data = self.cleaned_data[field]
                data = [int(data)] if type(data) == str else [int(i) for i in data]
                for choice in choices:
                    if choice.pk in data and choice.pk in existing:
                        # Do nothing, selected and already exists.
                        pass
                    elif choice.pk in data and choice.pk not in existing:
                        # Create the new choice that does not already exist.
                        TermTaxonomyItem(
                            content_type=content_type,
                            object_id=instance.pk,
                            term_taxonomy=choice,
                        ).save()
                    elif choice.pk not in data and choice.pk in existing:
                        # Remove the unselected choice that already exists.
                        TermTaxonomyItem.objects.filter(
                            term_taxonomy=choice,
                            content_type=content_type,
                            object_id=instance.pk,
                        ).delete()
                    elif choice.pk not in data and choice.pk not in existing:
                        # Final case, choice not selected and do not exist.
                        pass

    def _save_m2m_taxi(self):
        self._save_m2m()
        self._save_taxi()

    def save(self, commit=True):
        instance = super().save(commit=commit)
        if commit:
            self._save_taxi()
        else:
            self.save_m2m = self._save_m2m_taxi  # noqa

        return instance
