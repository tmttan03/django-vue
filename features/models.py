from django.db import models


class Feature(models.Model):
    PRINCIPLES = 'Principles'
    VALUES = 'Values'

    TYPE_CHOICES = (
        (PRINCIPLES, PRINCIPLES),
        (VALUES, VALUES),
    )

    name = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True, null=True)
    feat_type = models.CharField(default=VALUES, max_length=255, choices=TYPE_CHOICES)
    is_deleted = models.BooleanField(default=False)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    # class Meta:
    #     unique_together = ('name', 'feat_type'),

    def __str__(self):
        return "{}".format(self.name)