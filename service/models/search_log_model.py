from django.db import models

class SearchLog(models.Model):
    query = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default='PENDING') 
    is_processed = models.BooleanField(default=False) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.query} - {self.status}"