from crispy_forms.layout import Field
from .models import Dataset
from django import forms
from crispy_forms.helper import FormHelper

class DataSetForm(forms.ModelForm):
    class Meta:
        model = Dataset
        fields = ['row']

    def __init__(self, *args, **kwargs):
        super(DataSetForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['row'].label = False



