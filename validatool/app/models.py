from django.db import models
from django.conf import settings


# Create your models here.

class Validation(models.Model):
    title = models.CharField(max_length=200)
    guiding_text = models.TextField()
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                          through="Participation",
                                          through_fields=('validation', 'user'))
    answers_per_item = models.IntegerField(default=3)

    def __str__(self):
        return "{} - {}".format(self.id, self.title)


class Item(models.Model):
    validation = models.ForeignKey(Validation, on_delete=models.CASCADE)
    payload = models.JSONField()

    def __str__(self):
        return "Item {} from Validation {}".format(self.id, self.validation.id)


class Participation(models.Model):
    validation = models.ForeignKey(Validation, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    current_item = models.ForeignKey(Item, blank=True, null=True, default=None, on_delete=models.RESTRICT)

    def __str__(self):
        return "{} -> {} (Current item: {})".format(self.user, self.validation, self.current_item)


class Answer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    validation = models.ForeignKey(Validation, on_delete=models.DO_NOTHING)
    answer_data = models.JSONField()
    answer_timestamp = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def get_validated_num():
        #TODO: Implement this
        pass

    def __str__(self):
        return "Answer {} - {} - User {}".format(self.id, self.item, self.user)
