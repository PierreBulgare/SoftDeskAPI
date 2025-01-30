from django.contrib import admin
from .models import User, Contributor, Project, Issue, Comment


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'age', 'can_be_contacted', 'can_data_be_shared', 'created_time')
    search_fields = ('username',)
    ordering = ('-created_time',)


@admin.register(Contributor)
class ContributorAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_time')
    search_fields = ('user__username',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'project_type', 'author', 'created_time')
    search_fields = ('name',)
    list_filter = ('project_type',)


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'priority', 'balise', 'status', 'author', 'created_time')
    search_fields = ('title', 'project__name')
    list_filter = ('priority', 'balise', 'status')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'issue', 'author', 'created_time')
    search_fields = ('description',)
