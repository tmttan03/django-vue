import datetime
from datetime import datetime as dtime, timedelta

from django.conf import settings
from django.shortcuts import get_object_or_404, _get_queryset
from django.utils import timezone


class Query(object):
    """Query Helper for Model Serializers."""

    def __init__(self, *args, **kwargs):
        return super(Query, self).__init__(*args, **kwargs)

    @property
    def _model(self):
        try:
            return self.serializer_class.Meta.model
        except Exception as e:
            raise Exception("Model Serializer not found")

    def _get(self, _model, **kwargs):
        """ get an object based on the keyword arguments
            raise an HTTP404 if not found.
        """
        return get_object_or_404(_model, **kwargs)

    def _filter(self, _model, **kwargs):
        """ get the list of objects based on the
            keyword arguments.
        """
        return _model.objects.filter(**kwargs)


class PermissionHelper(object):
    """Permissions Helper."""

    def check_get_query_result_if_exists(self, model, *args, **kwargs):
        """
            Checks if the query exists, return True if it exists, else false
        """
        # Allows dynamic get querysets
        queryset = _get_queryset(model)

        try:
            # Put the args and kwargs in the filter for filtering
            exists = queryset.get(*args, **kwargs)
            return True
        except queryset.model.DoesNotExist as e:
            # If queryset does not exist. Return False
            return False


class TZ(object):
    """Timezone Manager of Calculated Time and Date."""

    def __init__(self, *args, **kwargs):
        return super(TZ, self).__init__(*args, **kwargs)

    def get_server_time(self):
        """Global Server DateTime Configuration."""
        return dict(
            # current timezone aware date and time.
            datetime=timezone.now(),
            # current timezone
            tz=settings.TIME_ZONE
        )

    def last_n_months(self, month_num=1):
        """Get Month based on the Input."""
        return [
            timezone.now() - datetime.timedelta(days=month_num*30),
            timezone.now()
        ]

    def dt_range(self, start, interval=7):
        given_date = dtime.strptime(start, "%Y-%m-%d").date()
        # compute the start of the week value
        start_of_week = given_date - timedelta(days=given_date.weekday())
        #compute the end of the week value
        end_of_week = start_of_week + timedelta(days=interval)

        return start_of_week, end_of_week


def get_object_or_None(klass, *args, **kwargs):
    """
        Uses get() to return an object or None if the object does not exist.
        klass may be a Model, Manager, or QuerySet object. All other passed
        arguments and keyword arguments are used in the get() query.
        Note: Like with get(), a MultipleObjectsReturned will be raised if more than one
        object is found.
    """
    queryset = _get_queryset(klass)

    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None
