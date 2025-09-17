from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users'


class Model(models.Model):
    name = models.CharField(max_length=255)
    version = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    parameters = models.JSONField(default=dict, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='models')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'models'
        unique_together = ['name', 'version']
    
    def __str__(self):
        return f"{self.name} v{self.version}"


class RobotType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    specifications = models.JSONField(default=dict, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'robot_types'
    
    def __str__(self):
        return self.name


class Dataset(models.Model):
    name = models.CharField(max_length=255)
    version = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    file_path = models.CharField(max_length=500, blank=True)
    size_mb = models.FloatField(null=True, blank=True)
    num_samples = models.IntegerField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='datasets')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'datasets'
        unique_together = ['name', 'version']
    
    def __str__(self):
        return f"{self.name} v{self.version}"


class Run(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    model = models.ForeignKey(Model, on_delete=models.CASCADE, related_name='runs')
    robot_type = models.ForeignKey(RobotType, on_delete=models.CASCADE, related_name='runs')
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='runs')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    hyperparameters = models.JSONField(default=dict, blank=True)
    metrics = models.JSONField(default=dict, blank=True)
    logs = models.TextField(blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='runs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'runs'
    
    def __str__(self):
        return f"Run {self.id} - {self.model} on {self.robot_type}"


class Evaluation(models.Model):
    run = models.ForeignKey(Run, on_delete=models.CASCADE, related_name='evaluations')
    metric_name = models.CharField(max_length=100)
    metric_value = models.FloatField()
    details = models.JSONField(default=dict, blank=True)
    evaluated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='evaluations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'evaluations'
        unique_together = ['run', 'metric_name']
    
    def __str__(self):
        return f"{self.metric_name}: {self.metric_value} for Run {self.run_id}"