from django.db import models
from django.conf import settings
from problems.models import Problem
from languages.models import Language

class CodeExecution(models.Model):
    STATUS_CHOICES = (
        ('Running', 'Running'),
        ('Completed', 'Completed'),
        ('Error', 'Error'),
        ('Timeout', 'Timeout'),
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, null=True, blank=True)
    code = models.TextField()
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    input_data = models.TextField(blank=True)
    output = models.TextField(blank=True)
    error_message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Running')
    execution_time = models.FloatField(null=True, blank=True)
    memory_usage = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Execution {self.id} by {self.user.username}"