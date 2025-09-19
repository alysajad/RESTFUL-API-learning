from django.db import models

# Create your models here.
class Employee(models.Model):
    emp_id=models.CharField(max_length=20)
    emp_name=models.CharField(max_length=100)
    designation=models.CharField(max_length=100)
    salary=models.IntegerField()

    def __str__(self):
        return self.emp_name