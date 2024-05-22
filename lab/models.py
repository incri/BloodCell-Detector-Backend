from django.db import models
from uuid import uuid4

# Create your models here.

class Patient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField()


    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    
    class Meta:
        ordering = ['first_name', 'last_name']



class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)



class BloodTest(models.Model):
    DETECTION_STATUS_PENDING = 'P'
    DETECTION_STATUS_COMPLETED = 'C'
    DETECTION_STATUS_FAILED = 'F'

    DETECTION_STATUS_CHOICES = [(DETECTION_STATUS_PENDING, 'Pending'),
                                (DETECTION_STATUS_COMPLETED, 'Completed'),
                                (DETECTION_STATUS_FAILED, 'Failed'),
                                ]
    
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)    
    title = models.CharField(max_length=255)
    description = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    detection_status = models.CharField(max_length=1, 
                                        choices=DETECTION_STATUS_CHOICES, 
                                        default=DETECTION_STATUS_PENDING,)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='blood_tests')

    
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ['created_at']



class Result(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)    
    bloodtest = models.ForeignKey(BloodTest, on_delete=models.CASCADE, related_name='results')
    description = models.TextField()
    created_at = models.DateField(auto_now_add=True)