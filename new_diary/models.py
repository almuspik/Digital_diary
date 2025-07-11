from django.db import models
from django.contrib.auth.models import User

class DiaryEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='diary_entries')
    title = models.CharField(max_length=100)
    content = models.TextField()
    entry_date = models.DateField()  # This replaces auto_now_add to allow calendar selection

    class Meta:
        unique_together = ('user', 'entry_date')
        ordering = ['-entry_date']

    def __str__(self):
        return f"{self.title} on {self.entry_date} by {self.user.username}"

class Userprofile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=100)
    dob = models.DateField()
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"profile of {self.user.username}"
