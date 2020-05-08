from django.db import models
import math


class country(models.Model):
    name = models.CharField('Country Name', max_length=100)
    iso3 = models.CharField('IOS3', max_length=10, null=True, blank=True)
    phoneCode = models.CharField('Phone Code', max_length=10, null=True, blank=True)
    safarzoon_id = models.IntegerField('Id in safarzoon.com', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '0 Country'


class province(models.Model):
    name = models.CharField('Province Name', max_length=100)
    phoneCode = models.CharField('Phone Code', max_length=10, null=True, blank=True)
    country = models.ForeignKey(country, null=True, blank=True, on_delete=models.CASCADE)
    safarzoon_id = models.IntegerField('Id in safarzoon.com', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '1 Province'


class city(models.Model):
    name = models.CharField('City Name', max_length=100)
    phoneCode = models.CharField('Phone Code', max_length=10, null=True, blank=True)
    latt = models.DecimalField('Latitude', null=True, blank=True, max_digits=9, decimal_places=6)
    long = models.DecimalField('Longitude', null=True, blank=True, max_digits=9, decimal_places=6)
    province = models.ForeignKey(province, null=True, blank=True, on_delete=models.CASCADE)
    safarzoon_id = models.IntegerField('Id in safarzoon.com', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '2 City'


class department(models.Model):
    title = models.CharField('Title', max_length=50, null=True, blank=True)
    comments = models.TextField('Comments', null=True, blank=True)

    def __str__(self):
        return self.title


class category(models.Model):
    department = models.ForeignKey(department, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField('Title', max_length=50, null=True, blank=True)
    comments = models.TextField('Comments', null=True, blank=True)

    def __str__(self):
        return self.department.title + ' -> ' + self.title


class tags(models.Model):
    category = models.ForeignKey(category, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField('Tag Title', max_length=50, null=True, blank=True)
    comments = models.TextField('Comments', null=True, blank=True)

    def __str__(self):
        # return self.category.department.title + ' -> ' + self.category.title + ' -> ' + self.title
        return self.title


TYPE_CHOISES = (
    (0, ("Attraction")),
    (1, ("Fooding")),
    (2, ("Resting")),
    (3, ("Healthing")),
    (4, ("Others"))
)


class attraction(models.Model):
    country = models.ForeignKey(country, on_delete=models.CASCADE, null=True, blank=True)
    province = models.ForeignKey(province, on_delete=models.CASCADE, null=True, blank=True)
    city = models.ForeignKey(city, on_delete=models.CASCADE, null=True, blank=True)
    type = models.IntegerField('Selection Type', default=0, choices=TYPE_CHOISES)
    tags = models.ManyToManyField(tags, null=True, blank=True)
    phoneCode = models.CharField('Phone Code', max_length=10, null=True, blank=True)
    title = models.CharField('Title', max_length=200, null=True, blank=True)
    fullTitle = models.TextField('Full Title', null=True, blank=True)
    address = models.CharField('Address', max_length=2000, null=True, blank=True)
    cost = models.CharField('Cost', max_length=50, null=True, blank=True)
    description = models.TextField('Description', null=True, blank=True)
    latt = models.DecimalField('Latitude', null=True, blank=True, max_digits=9, decimal_places=6)
    long = models.DecimalField('Longitude', null=True, blank=True, max_digits=9, decimal_places=6)
    rq_time = models.IntegerField('Require Time', null=True, blank=True)
    vis_time = models.CharField('Visit Time Range', max_length=50, null=True, blank=True)
    vis_time_from = models.IntegerField('Visit Time From', null=True, blank=True)
    vis_time_to = models.IntegerField('Visit Time To', null=True, blank=True)
    like_no = models.IntegerField('Likes', default=0, null=True, blank=True)
    view_no = models.IntegerField('Views', default=0, null=True, blank=True)
    image = models.URLField('Image', null=True, blank=True)
    safarzoon_id = models.IntegerField('Id in safarzoon.com', null=True, blank=True)

    def __str__(self):
        return self.title   + ' - ' + (str((self.like_no*60)+(self.view_no*40)) if self.like_no is not None else '') #+(' -> const' if self.type > 0 else '')

    # def save(self, *args, **kwargs):
    #     if not self.id:
    #         super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = '4 Attractions'
        ordering = ('latt', 'long')
        # unique_together = ["details"]


class constraint(models.Model):
    title = models.CharField('Title', max_length=200, null=True, blank=True)
    type = models.IntegerField('Selection Type', default=1, choices=TYPE_CHOISES)
    tags = models.ManyToManyField(tags, null=True, blank=True)
    description = models.TextField('Description', null=True, blank=True)
    rq_time = models.IntegerField('Require Time', null=True, blank=True)
    vis_time_from = models.IntegerField('Visit Time From', null=True, blank=True)
    vis_time_to = models.IntegerField('Visit Time To', null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '4 Constraints'


class travelType(models.Model):
    title = models.CharField(max_length=200)
    tags = models.CharField(max_length=1000)
    comment = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '5 Travel Types'


class distance_mat(models.Model):
    origin = models.ForeignKey(attraction, related_name='distance_mat', on_delete=models.CASCADE)
    destination = models.ForeignKey(attraction, related_name='destination', on_delete=models.CASCADE)
    travel_type = models.ForeignKey(travelType, on_delete=models.CASCADE)
    ecl_dist = models.FloatField('Euclidean Distance', null=True, blank=True, )
    len_meter = models.FloatField('Lenght Of Meters', null=True, blank=True)
    len_time = models.FloatField('Lenght Of Time', null=True, blank=True)
    rout = models.TextField('Routing Json', null=True, blank=True)

    def __str__(self):
        return self.origin.title + ' - ' + self.destination.title

    class Meta:
        verbose_name_plural = '6 Distance matrix'

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

        ecl_dist = math.sqrt(((dst_latt - ogn_latt) ** 2) + ((dst_long - ogn_long) ** 2))
        self.ecl_dist = ecl_dist
        super(distance_mat, self).save(*args, **kwargs)


class plan(models.Model):
    city = models.ForeignKey(city, on_delete=models.CASCADE)
    present_id = models.CharField(max_length=1000, null=True, blank=True)
    day = models.IntegerField('Day Of Tour', null=True, blank=True)
    all_days = models.IntegerField('Total days', null=True, blank=True)
    coh_fullTime = models.FloatField('Coefficient of Fill full time Cost', null=True, blank=True)
    coh_lengthTime = models.FloatField('Coefficient of distance length time Cost', null=True, blank=True)
    coh_countPoints = models.FloatField('Coefficient of count of points Cost', null=True, blank=True)
    coh_minRqTime = models.FloatField('Coefficient of diff min required Time Cost', null=True, blank=True)
    cost_fullTime = models.FloatField('Fill full time Cost', null=True, blank=True)
    cost_lengthTime = models.FloatField('Distance length time Cost', null=True, blank=True)
    cost_countPoints = models.FloatField('Count of points Cost', null=True, blank=True)
    cost_minRqTime = models.FloatField('Diff min required Time Cost', null=True, blank=True)
    cost_rate = models.FloatField('Selection attraction rate Cost', null=True, blank=True)
    start_time = models.CharField('Start Time of Day', max_length=20, null=True, blank=True)
    end_time = models.CharField('End Time of Day', max_length=20, null=True, blank=True)
    dist_len = models.FloatField('Length of distance times', null=True, blank=True)
    points_len = models.IntegerField('Count of points used', null=True, blank=True)
    duration_len = models.FloatField('Length of duration points', null=True, blank=True)
    tags = models.CharField(max_length=1000, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    # first_latt = models.DecimalField('Latitude', null=True, blank=True, max_digits=9, decimal_places=6)
    # first_long = models.DecimalField('Longitude', null=True, blank=True, max_digits=9, decimal_places=6)

    def __str__(self):
        return str(self.day) + ' day ' + self.city.name

    class Meta:
        verbose_name_plural = '7 Plan'


class plan_details(models.Model):
    plan = models.ForeignKey(plan, on_delete=models.CASCADE)
    order = models.IntegerField()
    point = models.ForeignKey(attraction, on_delete=models.CASCADE)
    len_time = models.IntegerField()
    from_time = models.IntegerField(null=True, blank=True)
    dist_to = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return '%d: %s' % (self.order, self.point.title)

    class Meta:
        verbose_name_plural = '7.1 Plan details'
        ordering = ('plan__day', 'order',)


class airport(models.Model):
    city = models.ForeignKey(city, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField('Name', max_length=1000, null=True, blank=True)
    icao = models.CharField('ICAO', max_length=10, null=True, blank=True)
    iata = models.CharField('IATA', max_length=10, null=True, blank=True)
    type = models.CharField('Type', max_length=20, null=True, blank=True)
    url = models.CharField('Address url', max_length=100, null=True, blank=True)
    area_code = models.CharField('Area code', max_length=100, null=True, blank=True)
    country_code = models.CharField('Country code', max_length=100, null=True, blank=True)
    city_en = models.CharField('City En', max_length=100, null=True, blank=True)
    airport_en = models.CharField('AirPort name', max_length=100, null=True, blank=True)

    def __str__(self):
        return self.airport_en

    class Meta:
        verbose_name_plural = '3 Airports'
        ordering = ('city', 'airport_en',)
