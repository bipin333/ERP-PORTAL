from django.db import models

# Create your models here.
class Notice(models.Model):
    notice_text = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.notice_text[:50] + "..."

    class Meta:
        ordering = ['-created_at']