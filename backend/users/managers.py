from django.db import models



class LogsAuthorizedManager(models.Manager):
    
    def get_queryset(self):
        from backend.users.models import Log
        return super().get_queryset().filter(
            action_description__in=[Log.REGISTER_SUCCESS_USER]
        )
             