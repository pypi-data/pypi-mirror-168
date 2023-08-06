from django.db import models
from django.utils.translation import gettext_lazy
from modelcluster.models import ClusterableModel
from wagtail.snippets.models import register_snippet

from wagtail_localize.fields import SynchronizedField, TranslatableField


try:
    from wagtail.admin.panels import FieldPanel
    from wagtail.fields import RichTextField
    from wagtail.models import Page, TranslatableMixin
except ImportError:
    from wagtail.admin.edit_handlers import FieldPanel
    from wagtail.core.fields import RichTextField
    from wagtail.core.models import Page, TranslatableMixin


class TestPage(Page):
    test_charfield = models.CharField(
        gettext_lazy("char field"), max_length=255, blank=True, null=True, default=""
    )
    test_textfield = models.TextField(blank=True)
    test_richtextfield = RichTextField(blank=True)
    test_synchronized_charfield = models.CharField(max_length=255, blank=True)

    translatable_fields = [
        TranslatableField("test_charfield"),
        TranslatableField("test_textfield"),
        TranslatableField("test_richtextfield"),
        SynchronizedField("test_synchronized_charfield"),
    ]


@register_snippet
class TestSnippet(TranslatableMixin, ClusterableModel):
    field = models.TextField(gettext_lazy("field"))

    translatable_fields = [
        TranslatableField("field"),
    ]

    panels = [
        FieldPanel("field"),
    ]
