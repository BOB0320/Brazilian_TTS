from django.db import models
from personal_sessions.models import Sessions
from enum import IntEnum
from django.contrib.auth.models import User

class Status(IntEnum):
    '''
    Enum to store the status of the voice data
    '''
    PENDING = 0
    SUCCESS = 1
    FAILED = 2

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class VoiceModel(models.Model):
    '''
    Model to store the voice data
    '''
    session_id = models.ForeignKey(Sessions, null=False, on_delete=models.CASCADE)
    voice = models.FileField(upload_to='voice',blank=True, null=True)
    status = models.IntegerField(choices=Status.choices(), default=Status.PENDING)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.voice.name


