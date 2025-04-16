from django.db import models


class ErrorLog(models.Model):
    path = models.CharField(max_length=500)
    method = models.CharField(max_length=10)
    status_code = models.IntegerField()
    error_message = models.TextField()
    traceback = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.created_at}] {self.method} {self.path} ({self.status_code})"
