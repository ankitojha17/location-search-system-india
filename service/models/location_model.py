from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)
    state = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'locations'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name}, {self.state}"