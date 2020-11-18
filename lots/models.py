from django.conf import settings
from django.db import models
from time import strftime
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone
# Create your models here. makemigrations/migrate

class Post(models.Model):

    DAMAGED = 'D'
    HEAVILYPLAYED = 'HP'
    MODERATLYPLAYED = 'MP'
    LIGHTLYPLAYED = 'LP'
    NEARMINT = 'NM'
    CARD_CONDITION_CHOICES = [
        (DAMAGED, 'Damaged'),
        (HEAVILYPLAYED, 'Heavily Played'),
        (MODERATLYPLAYED, 'Moderately Played'),
        (LIGHTLYPLAYED, 'Lightly Played'),
        (NEARMINT, 'Near Mint'),
    ]
    LOT_LIFE_CYCLE = [
        ('EX', 'exist'),
        ('BN', 'banned'),
        ('FN', 'finished'),

    ]
    title = models.CharField(max_length=100, null=False)
    set = models.CharField(max_length=50, null=False)
    condition = models.CharField(
        max_length=2,
        choices=CARD_CONDITION_CHOICES,
        default=NEARMINT,
    )
    author = models.CharField(max_length=100, null=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    # user = models.ManyToManyField(settings.AUTH_USER_MODEL)
    image = models.FileField(null=False, upload_to='upload/')
    min_price = models.FloatField()
    description = models.TextField(max_length=1024)
    place_date = models.DateTimeField(null=False, default=timezone.now)
    finish_date = models.DateTimeField(null=False, default=timezone.now() + timezone.timedelta(hours=24))
    life_cycle = models.CharField(max_length=2, choices=LOT_LIFE_CYCLE, default='EX')

class Bid(models.Model):
    STATUS_ = (
        ('W', 'Wining'),
        ('L', 'Losing'),
    )
    auct = models.ForeignKey(Post,  on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    status = models.CharField(max_length=1, choices=STATUS_)
    expire = models.FloatField(default=0)


