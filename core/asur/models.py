from django.db import models

class UploadedFile(models.Model):
    file = models.FileField(upload_to='static/uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.file.name}, {self.uploaded_at}'

