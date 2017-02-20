from django.db import models


class Project(models.Model):
    code = models.CharField(max_length=4, primary_key=True)
    name = models.CharField(max_length=30)
    host = models.CharField(max_length=20)
    work_dir = models.CharField(max_length=20)
    branch = models.CharField(max_length=20)
    test_c = models.CharField(max_length=20)
    prod_c = models.CharField(max_length=20)

    class Meta:
        db_table = 'project'
        ordering = ('code',)
