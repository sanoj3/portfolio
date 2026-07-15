from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fname = models.CharField(max_length=150)
    lname = models.CharField(max_length=150)
    email = models.EmailField()
    location = models.TextField()
    experience = models.PositiveBigIntegerField(help_text="years of Experience")
    resume = models.FileField(upload_to='resume/')
    profile_pic = models.ImageField(upload_to='profile_pic/')
    bio = models.TextField()
    description = models.TextField()
    stack_description = models.TextField(blank=True)
    github = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.user.username
    

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=255)
    description = models.TextField()
    github = models.URLField(blank=True, null=True)
    livedemo = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title
    
class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='projectImages')
    image = models.ImageField(upload_to='project_image/')

    def __str__(self):
        return self.project.title
    
class Skill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    

class ProjectFeature(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='features')
    name = models.TextField()

    def __str__(self):
        return self.name
    
class Technology(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title
    
class ProjectTechnology(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    technology = models.ForeignKey(Technology, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.project.title} - {self.technology.title}"
    
class Education(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    degree = models.CharField(max_length=200)
    institution = models.CharField(max_length=250)
    year = models.CharField(max_length=20)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.degree
    

class Experience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    duration = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.company
    


class Certificate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    organization = models.CharField(max_length=200)
    year = models.CharField(max_length=20)
    certificate = models.ImageField(upload_to='certificate/')

    def __str__(self):
        return self.title
    


