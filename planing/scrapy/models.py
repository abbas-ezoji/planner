from django.db import models


# 'event_type', 'details_api', 'title', 'location', 'image'
class points(models.Model):
    type = models.CharField('Type', max_length=1000)
    details = models.CharField('Details', max_length=4000, null=True, blank=True)
    title = models.CharField('Title', max_length=4000)
    location = models.CharField('Location', max_length=4000, null=True, blank=True)
    image = models.URLField('Image', null=True, blank=True)

    def __str__(self):
        return self.title

    # def save(self, *args, **kwargs):
    #     if not self.id:
    #         super().save(*args, **kwargs)


    class Meta:
        verbose_name_plural = 'points'
        ordering = ('type', 'title', 'location')
        # unique_together = ["details"]


