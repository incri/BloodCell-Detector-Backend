from django.db import models

# Create your models here.
class BloodTest(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ['created_at']


class Patient(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField()

    def __str__(self) -> str:
        return self.first_name + self.last_name
    
    class Meta:
        ordering = ['first_name', 'last_name']

class Address(models.Model):
    street = models.CharField(max_length=255)
    cit = models.CharField(max_length=255)
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, primary_key=True)

class Detection(models.Model):
    DETECTION_STATUS_PENDING = 'P'
    DETECTION_STATUS_COMPLETED = 'C'
    DETECTION_STATUS_FAILED = 'F'

    DETECTION_STATUS_CHOICES = [(DETECTION_STATUS_PENDING, 'Pending'),
                                (DETECTION_STATUS_COMPLETED, 'Completed'),
                                (DETECTION_STATUS_FAILED, 'Failed'),
                                ]
    
    started_at = models.DateTimeField(auto_now_add=True)
    detection_status = models.CharField(max_length=1, 
                                        choices=DETECTION_STATUS_CHOICES, 
                                        default=DETECTION_STATUS_PENDING,)
    
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT)
    


    