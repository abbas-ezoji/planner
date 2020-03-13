from django.db import models
import math


class attractions(models.Model):
    country = models.CharField('Country', max_length=100)
    iso3 = models.CharField('iso3', max_length=10)
    phoneCode = models.CharField('Phone Code', max_length=10)
    title = models.CharField('Title', max_length=5000)
    fullTitle = models.CharField('Full Title', max_length=5000, null=True, blank=True)
    address = models.CharField('Address', max_length=5000, null=True, blank=True)
    cost = models.CharField('Cost', max_length=50, null=True, blank=True)
    description = models.TextField('Description', null=True, blank=True)
    latt = models.DecimalField('Latitude', null=True, blank=True, max_digits=9, decimal_places=6)
    long = models.DecimalField('Longitude', null=True, blank=True, max_digits=9, decimal_places=6)
    rq_time = models.IntegerField('Require Time', null=True, blank=True)
    vis_time = models.CharField('Visit Time Range', max_length=50, null=True, blank=True)
    vis_time_from = models.IntegerField('Visit Time From', null=True, blank=True)
    vis_time_to = models.IntegerField('Visit Time To', null=True, blank=True)
    province = models.CharField('Provice', max_length=100, null=True, blank=True)
    city = models.CharField('City', max_length=100, null=True, blank=True)

    image = models.URLField('Image', null=True, blank=True)

    def __str__(self):
        return self.fullTitle

    # def save(self, *args, **kwargs):
    #     if not self.id:
    #         super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Attractions'
        ordering = ('latt', 'long')
        # unique_together = ["details"]


class travelType(models.Model):
    title = models.CharField(max_length=200)
    tags = models.CharField(max_length=1000)
    comment = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Travel Types'


class distance_mat(models.Model):
    origin = models.ForeignKey(attractions, related_name='distance_mat', on_delete=models.CASCADE)
    destination = models.ForeignKey(attractions, related_name='destination', on_delete=models.CASCADE)
    travel_type = models.ForeignKey(travelType, on_delete=models.CASCADE)
    ecl_dist = models.DecimalField('Euclidean Distance', null=True, blank=True, max_digits=9, decimal_places=6)
    len_meter = models.FloatField('Lenght Of Meters', null=True, blank=True)
    len_time = models.FloatField('Lenght Of Time', null=True, blank=True)

    def __str__(self):
        return self.origin.title + ' - ' + self.destination.title

    class Meta:
        verbose_name_plural = 'Distance matrix'

    def save(self, *args, **kwargs):
        if not self.id:
            super().save(*args, **kwargs)

        '''
            CREATE OR REPLACE PROCEDURE pln_update_ecl_dist()
            LANGUAGE plpgsql    
            AS $$
            BEGIN
                    update plan_distance_mat
                    set ecl_dist = t.ecl_dist
                    from	
                        (select 
                             m.id
                             ,sqrt(power(o.latt-d.latt, 2) + power(o.long-d.long, 2)) as ecl_dist
                            from
                                plan_distance_mat m
                                join plan_attractions o on o.id = m.origin_id
                                join plan_attractions d on d.id = m.destination_id
                        ) t 
                    where t.id = plan_distance_mat.id;
                    
                COMMIT;
            END;
            $$;

        '''

        ogn_latt = self.origin.latt
        ogn_long = self.origin.long
        dst_latt = self.destination.latt
        dst_long = self.destination.long

        ecl_dist = math.sqrt(((dst_latt-ogn_latt)**2) + ((dst_long-ogn_long)**2))
        self.ecl_dist = ecl_dist
        super(distance_mat, self).save(*args, **kwargs)
