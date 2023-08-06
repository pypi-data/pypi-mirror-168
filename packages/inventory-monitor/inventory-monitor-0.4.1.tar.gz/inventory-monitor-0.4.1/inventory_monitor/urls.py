from django.urls import path
from . import models, views
from netbox.views.generic import ObjectChangeLogView


urlpatterns = (
    path('probes/', views.ProbeListView.as_view(), name='probe_list'),
    path('probes/add/', views.ProbeEditView.as_view(), name='probe_add'),
    path('probes/<int:pk>/', views.ProbeView.as_view(), name='probe'),
    path('probes/<int:pk>/edit/', views.ProbeEditView.as_view(), name='probe_edit'),
    path('probes/<int:pk>/delete/',
         views.ProbeDeleteView.as_view(), name='probe_delete'),
    path('probes/<int:pk>/changelog/', ObjectChangeLogView.as_view(),
         name='probe_changelog', kwargs={'model': models.Probe}),
    path("probes/delete/", views.ProbeBulkDeleteView.as_view(),
         name="probe_bulk_delete",),
)
