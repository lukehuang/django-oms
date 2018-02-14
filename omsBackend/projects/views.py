# -*- coding: utf-8 -*-
# author: kiven

from rest_framework import viewsets
from projects.models import Project, ProjectComment, ProjectType, BugManager, TestManager
from projects.serializers import (ProjectSerializer,
                                  ProjectCommentSerializer,
                                  ProjectTypeSerializer,
                                  BugManagerSerializer,
                                  TestManagerSerializer)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by('create_time')
    serializer_class = ProjectSerializer
    filter_fields = ['pid']
    search_fields = ['name', 'content', 'type__name']


class ProjectCommentViewSet(viewsets.ModelViewSet):
    queryset = ProjectComment.objects.all().order_by('create_time')
    serializer_class = ProjectCommentSerializer
    filter_fields = ['project__id']


class ProjectTypeViewSet(viewsets.ModelViewSet):
    queryset = ProjectType.objects.all()
    serializer_class = ProjectTypeSerializer


class BugManagerViewSet(viewsets.ModelViewSet):
    queryset = BugManager.objects.all()
    serializer_class = BugManagerSerializer
    filter_fields = ['id', 'project__id', 'test_id']


class TestManagerViewSet(viewsets.ModelViewSet):
    queryset = TestManager.objects.all()
    serializer_class = TestManagerSerializer
    filter_fields = ['id', 'project__id']
