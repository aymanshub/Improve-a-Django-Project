from django.forms import forms, ModelForm, DateField, CharField, ValidationError, ModelMultipleChoiceField, BooleanField
from django.forms.widgets import SelectDateWidget, HiddenInput
from datetime import date
from .models import Menu, Item


def min_selection(selected_items):
    """
    Custom validator for minimum menu items
    """
    if len(selected_items) < 2:
        raise ValidationError('Please select more!\n'
                              'a season should include at least two items')


class MenuForm(ModelForm):
    """
    Used for creating new or editing existing menu
    """
    season = CharField(
        required=True,
        error_messages={'required': 'Season field is required'}
    )

    items = ModelMultipleChoiceField(
        required=True,
        queryset=Item.objects.all().order_by('id'),
        validators=[min_selection],
        error_messages={'required': 'Please select items (at least two)'}
    )

    cur_year = date.today().year
    year_range = tuple([i for i in range(cur_year-5, cur_year + 10)])
    expiration_date = DateField(
        required=False,
        widget=SelectDateWidget(
            empty_label=("Choose Year", "Choose Month", "Choose Day"),
            years=year_range
        ),
        error_messages={'invalid': 'Incorrect date'}
    )

    created_date = DateField(widget=HiddenInput)

    def clean_expiration_date(self):
        expiration_date = self.cleaned_data['expiration_date']
        if expiration_date and expiration_date < date.today():
            raise ValidationError("Expiration date should be equal to"
                                  " or greater than today (" + date.today().strftime('%B-%d-%Y') + ")")
        return expiration_date

    def clean_season(self):
        season = self.cleaned_data['season']

        if Menu.objects\
                .exclude(expiration_date__lt=date.today())\
                .exclude(pk=self.instance.id)\
                .filter(season__iexact=season):
            raise ValidationError("An active menu with the exact season name exists."
                                  " Please choose another name.")
        return season

    class Meta:
        model = Menu
        fields = ['season', 'items', 'created_date', 'expiration_date']


class DeleteForm(forms.Form):
    """
    Used for menu deletion confirmation/cancellation
    """
    season = CharField(label='Are you sure you want to remove menu:', disabled=True)
