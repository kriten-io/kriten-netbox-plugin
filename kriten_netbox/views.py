import requests
from datetime import datetime

from django.contrib import messages
from django.db.models import Count, ProtectedError, RestrictedError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse

from utilities.forms import ConfirmationForm, restrict_form_fields
from utilities.htmx import htmx_partial
from utilities.views import GetReturnURLMixin, get_viewname
from netbox.views import generic
from . import filtersets, forms, models, tables, services

def no_cascade_delete(self, request, *args, **kwargs):
    """
    GET request handler.

    Args:
        request: The current request

    Override GET method to set modified versions of confirmation.
    Kriten doesn't allow auto deletion of dependent objects.
    """
    obj = self.get_object(**kwargs)
    form = ConfirmationForm(initial=request.GET)

    try:
        dependent_objects = self._get_dependent_objects(obj)
    except ProtectedError as e:
        return self._handle_protected_objects(obj, e.protected_objects, request, e)
    except RestrictedError as e:
        return self._handle_protected_objects(obj, e.restricted_objects, request, e)

    if dependent_objects:
        delete_form = 'kriten_netbox/delete_form.html'
        object_delete = 'kriten_netbox/object_delete.html'
    else:
        delete_form = 'htmx/delete_form.html'
        object_delete = self.template_name

    # If this is an HTMX request, return only the rendered deletion form as modal content
    if htmx_partial(request):
        viewname = get_viewname(self.queryset.model, action='delete')
        form_url = reverse(viewname, kwargs={'pk': obj.pk})
        return render(request, delete_form, {
            'object': obj,
            'object_type': self.queryset.model._meta.verbose_name,
            'form': form,
            'form_url': form_url,
            'dependent_objects': dependent_objects,
            **self.get_extra_context(request, obj),
        })

    return render(request, object_delete, {
        'object': obj,
        'form': form,
        'return_url': self.get_return_url(request, obj),
        'dependent_objects': dependent_objects,
        **self.get_extra_context(request, obj),
    })

# KritenClusters
class KritenClusterView(generic.ObjectView):
    queryset = models.KritenCluster.objects.all()

    def get_extra_context(self, request, instance):
        table = tables.KritenTaskTable(instance.tasks.all())
        table.configure(request)
        runners_table = tables.KritenRunnerTable(instance.runners.all())
        runners_table.configure(request)

        return {
            'tasks_table': table,
            'runners_table': runners_table
        }


class KritenClusterListView(generic.ObjectListView):
    queryset = models.KritenCluster.objects.annotate(
        task_count=Count(('tasks'),distinct=True), runner_count=Count(('runners'), distinct=True)
    )
    table = tables.KritenClusterTable


class KritenClusterEditView(generic.ObjectEditView):
    queryset = models.KritenCluster.objects.all()
    form = forms.KritenClusterForm


class KritenClusterDeleteView(generic.ObjectDeleteView):
    queryset = models.KritenCluster.objects.all()
    def get(self, request, *args, **kwargs):
        response = no_cascade_delete(self, request, *args, **kwargs)
        return response

# KritenRunners
class KritenRunnerView(generic.ObjectView):
    queryset = models.KritenRunner.objects.all()

    def get_extra_context(self, request, instance):
        table = tables.KritenTaskTable(instance.tasks.all())
        table.configure(request)

        return {
            'tasks_table': table,
        }


class KritenRunnerListView(generic.ObjectListView):
    queryset = models.KritenRunner.objects.annotate(
        task_count=Count('tasks')
    )
    table = tables.KritenRunnerTable
    filterset = filtersets.KritenRunnerFilterSet
    filterset_form = forms.KritenRunnerFilterForm


class KritenRunnerEditView(generic.ObjectEditView):
    queryset = models.KritenRunner.objects.all()
    form = forms.KritenRunnerForm


class KritenRunnerDeleteView(generic.ObjectDeleteView):
    queryset = models.KritenRunner.objects.all()
    def get(self, request, *args, **kwargs):
        response = no_cascade_delete(self, request, *args, **kwargs)
        return response

# KritenTasks
class KritenTaskView(generic.ObjectView):
    queryset = models.KritenTask.objects.all()

    def get_extra_context(self, request, instance):
        table = tables.KritenJobTable(instance.kritenjobs.all())
        table.configure(request)

        return {
            'kritenjobs_table': table,
        }


class KritenTaskListView(generic.ObjectListView):
    #queryset = models.KritenTask.objects.all()
    queryset = models.KritenTask.objects.annotate(
        job_count=Count('kritenjobs')
    )
    table = tables.KritenTaskTable
    filterset = filtersets.KritenTaskFilterSet
    filterset_form = forms.KritenTaskFilterForm


class KritenTaskEditView(generic.ObjectEditView):
    queryset = models.KritenTask.objects.all()
    form = forms.KritenTaskForm


class KritenTaskDeleteView(generic.ObjectDeleteView):
    queryset = models.KritenTask.objects.all()
    def get(self, request, *args, **kwargs):
        response = no_cascade_delete(self, request, *args, **kwargs)
        return response
    

# KritenJobs
class KritenJobView(generic.ObjectView):
    queryset = models.KritenJob.objects.all()
    def get(self, request, **kwargs):
        """
        GET request handler. `*args` and `**kwargs` are passed to identify the object being queried.

        Args:
            request: The current request
        """
        instance = self.get_object(**kwargs)

        if instance.completed:
            # No need to get data
            pass
        else:
            kriten_task_name = instance.kriten_task.name
            kriten_url = instance.kriten_task.kriten_cluster.kriten_url
            kriten_token = instance.kriten_task.kriten_cluster.api_token
            kriten_job_name = instance.name
            headers = {
                "Content-Type": "application/json",
                "Token": kriten_token
            }
            job_url = f"{kriten_url}/api/v1/jobs/{kriten_job_name}"
            job_request = requests.request("GET",job_url, headers=headers)
            if job_request.status_code == 200:
                job_details = job_request.json()
                date_fmt = '%a %b %d %H:%M:%S %Z %Y'
                instance.owner = job_details.get('owner')
                instance.start_time = datetime.strptime(job_details.get('startTime'), date_fmt)
                # completionTime not returned if job fails
                if job_details.get('completionTime'):
                    instance.completion_time = datetime.strptime(job_details.get('completionTime'), date_fmt)
                instance.failed = job_details.get('failed')
                instance.completed = job_details.get('completed')
                instance.stdout = job_details.get('stdout')
                #if instance.completed:
                instance.save()

        return render(request, self.get_template_name(), {
            'object': instance,
            'tab': self.tab,
            **self.get_extra_context(request, instance),
        })


class KritenJobListView(generic.ObjectListView):
    queryset = models.KritenJob.objects.all()
    table = tables.KritenJobTable
    filterset = filtersets.KritenJobFilterSet
    filterset_form = forms.KritenJobFilterForm
    # actions = {
    #     "bulk_delete": {"delete"},
    # }


class KritenJobEditView(LoginRequiredMixin, generic.ObjectEditView):
    queryset = models.KritenJob.objects.all()
    form = forms.KritenJobForm
    template_name = 'kriten_netbox/kritenjobform.html'


class KritenJobDeleteView(generic.ObjectDeleteView):
    queryset = models.KritenJob.objects.all()
