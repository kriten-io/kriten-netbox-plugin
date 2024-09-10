from django.urls import path

from netbox.views.generic import ObjectChangeLogView
from . import models, views


urlpatterns = (

    # Kriten Clusters
    path('kriten-clusters/', views.KritenClusterListView.as_view(), name='kritencluster_list'),
    path('kriten-clusters/add/', views.KritenClusterEditView.as_view(), name='kritencluster_add'),
    path('kriten-clusters/<int:pk>/', views.KritenClusterView.as_view(), name='kritencluster'),
    path('kriten-clusters/<int:pk>/edit/', views.KritenClusterEditView.as_view(), name='kritencluster_edit'),
    path('kriten-clusters/<int:pk>/delete/', views.KritenClusterDeleteView.as_view(), name='kritencluster_delete'),
    path('kriten-clusters/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='kritencluster_changelog', kwargs={
        'model': models.KritenCluster
    }),

    # Kriten Runners
    path('kriten-runners/', views.KritenRunnerListView.as_view(), name='kritenrunner_list'),
    path('kriten-runners/add/', views.KritenRunnerEditView.as_view(), name='kritenrunner_add'),
    path('kriten-runners/<int:pk>/', views.KritenRunnerView.as_view(), name='kritenrunner'),
    path('kriten-runners/<int:pk>/edit/', views.KritenRunnerEditView.as_view(), name='kritenrunner_edit'),
    path('kriten-runners/<int:pk>/delete/', views.KritenRunnerDeleteView.as_view(), name='kritenrunner_delete'),
    path('kriten-runners/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='kritenrunner_changelog', kwargs={
        'model': models.KritenRunner
    }),

    # Kriten Tasks
    path('kriten-tasks/', views.KritenTaskListView.as_view(), name='kritentask_list'),
    path('kriten-tasks/add/', views.KritenTaskEditView.as_view(), name='kritentask_add'),
    path('kriten-tasks/<int:pk>/', views.KritenTaskView.as_view(), name='kritentask'),
    path('kriten-tasks/<int:pk>/edit/', views.KritenTaskEditView.as_view(), name='kritentask_edit'),
    path('kriten-tasks/<int:pk>/delete/', views.KritenTaskDeleteView.as_view(), name='kritentask_delete'),
    path('kriten-tasks/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='kritentask_changelog', kwargs={
        'model': models.KritenTask
    }),

    # Kriten Jobs
    path('kriten-jobs/', views.KritenJobListView.as_view(), name='kritenjob_list'),
    path('kriten-jobs/add/', views.KritenJobEditView.as_view(), name='kritenjob_add'),
    path('kriten-jobs/<int:pk>/', views.KritenJobView.as_view(), name='kritenjob'),
    path('kriten-jobs/<int:pk>/edit/', views.KritenJobEditView.as_view(), name='kritenjob_edit'),
    path('kriten-jobs/<int:pk>/delete/', views.KritenJobDeleteView.as_view(), name='kritenjob_delete'),
    path('kriten-jobs/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='kritenjob_changelog', kwargs={
        'model': models.KritenJob
    }),
    
)