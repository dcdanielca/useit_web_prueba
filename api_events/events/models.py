from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Comment(models.Model):
    body = models.TextField()
    creator = models.ForeignKey(User, blank=True, on_delete= models.CASCADE)
    date = models.DateField()
    responses = models.ManyToManyField('self', blank=True, related_name='comment')

    def __str__(self):
        return '(Comment: %s)' % (self.id)

class Event(models.Model):
    name = models.CharField(max_length=30, unique = True)
    description = models.CharField(max_length=30)
    picture = models.ImageField(upload_to="events/pictures")
    date = models.DateField()
    time = models.TimeField()
    creator = models.ForeignKey(User, on_delete = models.CASCADE)
    comments = models.ManyToManyField(Comment, blank=True)

    def __str__(self):
        return self.name


class Interaction(models.Model):
    OPTION_CHOICES = [
        ('Assist', 'Assist'),
        ('Interested', 'Interested'),
        ('Refuse', 'Refuse'),
    ]

    eventId = models.ForeignKey(Event, on_delete = models.CASCADE)
    userId = models.ForeignKey(User, on_delete = models.CASCADE)
    option = models.CharField(
       max_length=20,
       choices=OPTION_CHOICES
   )

    class Meta:
        unique_together = ('eventId', 'userId',)

    def __str__(self):
        return'(Interaction: %s)' % (self.id)

