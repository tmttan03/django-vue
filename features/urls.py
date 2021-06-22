from django.urls import path, re_path
from .api import FeatureViewSet


urlpatterns = [
    path('', FeatureViewSet.as_view({
        'get': 'get',
    }), name="feature_list"),

    path('values/', FeatureViewSet.as_view({
        'get': 'get_values',
    }), name="values_list"),

    path('principles/', FeatureViewSet.as_view({
        'get': 'get_principles',
    }), name="principles_list"),

    path('add/', FeatureViewSet.as_view({
        'post': 'add',
    }), name="add_feature"),

    path('update/', FeatureViewSet.as_view({
        'put': 'update',
    }), name="update_feature"),

    path('delete/', FeatureViewSet.as_view({
        'post': 'delete'
    }), name='delete_feature')
]