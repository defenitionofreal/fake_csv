from .forms import DataSetForm
from django.shortcuts import render, get_object_or_404, redirect

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from django.db import transaction
from django.utils import timezone

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin

from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Schema, Column, Dataset
from django.forms.models import inlineformset_factory
from .forms import DataSetForm

from .tasks import write_csv
# Create your views here.


column_formset = inlineformset_factory(
    Schema,
    Column,
    fields=['name', 'column_type', 'range_from', 'range_to', 'order'],
    labels={'name': 'Column name', 'column_type': 'Type',
                    'order': 'Order', 'range_from': 'From', 'range_to': 'To'},
    extra=1,
    can_delete=True,
    can_order=False,
)


def dashboard(request):
    schema = Schema.objects.filter(user=request.user.pk)
    context = {'schema': schema}
    return render(request, 'data_schemas.html', context)


class SchemaCreateView(LoginRequiredMixin, CreateView, SuccessMessageMixin):
    model = Schema
    fields = ['name', 'column_separator', 'string_character']
    success_url = reverse_lazy('Data Schemas')
    success_message = 'Created successfully!'
    template_name = 'new_schema.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["columns"] = column_formset(self.request.POST)
        else:
            data["columns"] = column_formset()
        return data

    def form_valid(self, form):
        form.instance.user = self.request.user
        context = self.get_context_data()
        columns = context["columns"]
        if not columns.is_valid():
            return super().form_invalid(form)
        self.object = form.save()
        columns.instance = self.object
        columns.save()
        return super().form_valid(form)


class SchemaUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Schema
    fields = ['name', 'column_separator', 'string_character']
    template_name = 'new_schema.html'
    pk_url_kwarg = "pk"
    success_url = reverse_lazy('Data Schemas')
    success_message = 'Updated successfully!'

    def get_context_data(self, **kwargs):
        data = super(SchemaUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['columns'] = column_formset(self.request.POST,
                                             instance=self.object)
        else:
            data['columns'] = column_formset(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        columns = context['columns']
        with transaction.atomic():
            form.instance.modified = timezone.now()
            self.object = form.save()
            if columns.is_valid():
                columns.instance = self.object
                columns.save()
        return super(SchemaUpdateView, self).form_valid(form)

    def get_initial(self):
        initial = super(SchemaUpdateView, self).get_initial()
        initial['user'] = self.request.user
        return initial


def del_schema(request, pk):
    schema = get_object_or_404(Schema, pk=pk, user=request.user)
    schema.delete()
    messages.success(request, 'Deleted successfully!')
    return redirect('Data Schemas')


class DataSetView(LoginRequiredMixin, FormMixin, ListView):
    model = Dataset
    form_class = DataSetForm
    template_name = 'data_sets.html'
    pk_url_kwarg = "pk"

    def dispatch(self, request, *args, **kwargs):
        self.schema_id = kwargs["pk"]
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(schema_id=self.schema_id)

    def form_valid(self, form):
        form.instance.schema_id = self.schema_id
        form.instance.is_ready = False
        dataset = form.save()
        write_csv.delay(dataset.id)
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return self.request.path

    def get_context_data(self, **kwargs):
        context = super(DataSetView, self).get_context_data(**kwargs)
        context['dataset'] = Dataset.objects.filter(schema_id=self.schema_id)
        return context
