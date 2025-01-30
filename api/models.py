import uuid
from django.contrib.auth.models import AbstractBaseUser
from django.db import models


class User(AbstractBaseUser):
    username = models.CharField(max_length=100, unique=True)
    age = models.PositiveIntegerField(null=False, blank=False)
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "username"

    def __str__(self):
        return self.username
    

class Contributor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contributor_user')
    projects = models.ManyToManyField('Project', related_name='contributor_projects')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Project(models.Model):
    PROJECT_TYPE = [
        ('back-end', 'back-end'),
        ('front-end', 'front-end'),
        ('iOS', 'iOS'),
        ('Android', 'Android')
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    project_type = models.CharField(max_length=15, choices=PROJECT_TYPE)
    author = models.ForeignKey(Contributor, on_delete=models.CASCADE, related_name='project_author')
    contributors = models.ManyToManyField('Contributor', related_name='project_contributors')
    issues = models.ManyToManyField('Issue', related_name='project_issues')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Issue(models.Model):
    PRIORITY = [
        ('LOW', 'LOW'),
        ('MEDIUM', 'MEDIUM'),
        ('HIGH', 'HIGH')
    ]
    BALISE = [
        ('BUG', 'BUG'),
        ('FEATURE', 'FEATURE'),
        ('TASK', 'TASK')
    ]
    STATUS = [
        ('To Do', 'To Do'),
        ('In Progress', 'In Progress'),
        ('Finished', 'Finished')
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='issue_project')
    priority = models.CharField(max_length=15, choices=PRIORITY)
    balise = models.CharField(max_length=15, choices=BALISE)
    status = models.CharField(max_length=15, choices=STATUS)
    author = models.ForeignKey(Contributor, on_delete=models.CASCADE, related_name='issue_author')
    comments = models.ManyToManyField('Comment', related_name='issue_comments')
    created_time = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    description = models.TextField()
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comment_issue')
    author = models.ForeignKey(Contributor, on_delete=models.CASCADE, related_name='comment_author')
    created_time = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.description
