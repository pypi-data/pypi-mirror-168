from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Manager, QuerySet
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class MetaMixin(models.Model):
    """
    Adds a json meta field not used by this library but may be used
    for programmatically adding additional metadata to an instance.
    """

    meta = models.JSONField(default=dict, null=True, blank=True)

    class Meta:
        abstract = True


class Taxonomy(MetaMixin, models.Model):
    """
    The main model that relate to and populate a single field on a model form.
    """

    name = models.CharField(max_length=128, verbose_name=_("Name"))
    slug = models.SlugField()
    parent = models.ForeignKey(
        "Taxonomy",
        null=True,
        blank=True,
        related_name="children",
        on_delete=models.SET_NULL,
        verbose_name=_("Parent"),
    )

    class Meta:
        verbose_name = _("Taxonomy")
        verbose_name_plural = _("Taxonomies")

    def save(self, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(**kwargs)

    def __str__(self):
        return self.name


class Term(MetaMixin, models.Model):
    """
    The smallest atomic value that might be used in one or multiple taxonomies.
    """

    name = models.CharField(max_length=128, verbose_name=_("Name"))
    slug = models.SlugField()

    class Meta:
        verbose_name = _("Term")
        verbose_name_plural = _("Terms")

    def save(self, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(**kwargs)

    def __str__(self):
        return self.name


class TermTaxonomy(MetaMixin, models.Model):
    """
    Choices in a modelform field that specify a taxonomy.
    """

    term = models.ForeignKey(
        Term,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="taxonomies",
        verbose_name=_("Term"),
    )
    taxonomy = models.ForeignKey(
        Taxonomy,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="terms",
        verbose_name=_("Taxonomy"),
    )

    class Meta:
        verbose_name = _("Term Taxonomy")
        verbose_name_plural = _("Term Taxonomies")

    def __str__(self):
        return f"{self.term}"


class TermTaxonomyQuerySet(QuerySet):
    def taxonomy_slug(self, slug: str) -> QuerySet:
        return self.filter(term_taxonomy__taxonomy__slug=slug)


class TermTaxonomyManager(Manager):
    pass


class TermTaxonomyItem(MetaMixin, models.Model):
    """
    Relates a term taxonomy selected and saved choice with any model instance as a generic relation.
    """

    term_taxonomy = models.ForeignKey(
        TermTaxonomy,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        verbose_name=_("Taxi"),
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    objects = TermTaxonomyManager().from_queryset(TermTaxonomyQuerySet)()

    class Meta:
        verbose_name = _("Term Taxonomy Item")
        verbose_name_plural = _("Term Taxonomy Items")

    def __str__(self):
        return f"{self.term_taxonomy.term}"
