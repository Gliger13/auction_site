from datetime import timedelta

from django import forms
from django.core.exceptions import NON_FIELD_ERRORS
from django.utils import timezone

from lots.models import Lot, Bet
from users.models import User


class LotsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.lot = None
        super(LotsForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if type(visible.field.widget) == forms.Textarea:
                visible.field.widget.attrs['class'] = 'uk-textarea input-form'
            else:
                visible.field.widget.attrs['class'] = 'uk-input input-form'

    text_description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 4,
            'cols': 3,
        })
    )

    tags = forms.CharField(
        label="Tags. Separate tags by ';'",
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 4,
            'cols': 3,
        })
    )

    base_price = forms.IntegerField(
        widget=forms.NumberInput(),
        required=True,
    )
    image = forms.FileField(
        widget=forms.FileInput
    )

    class Meta:
        model = Lot
        fields = [
            'heading',
            'text_description',
            'tags',
            'base_price',
            'min_price_step',

        ]

    def is_valid(self):
        return super(LotsForm, self).is_valid()

    def save(self, commit=True):
        if self.cleaned_data.get('expires_at'):
            self.instance.expires_at = self.cleaned_data.get('expires_at')
        else:
            self.instance.expires_at = timezone.now().replace(microsecond=0) + timedelta(days=3)
        self.instance.current_price = self.cleaned_data.get('base_price')
        self.instance.save()
        return super().save(commit)


class SetBitForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SetBitForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'uk-input uk-form-width-medium'

    set_price = forms.IntegerField(
        widget=forms.NumberInput,
        required=True
    )

    class Meta:
        model = Bet
        fields = [
            'set_price'
        ]

    def is_valid(self):
        return super(SetBitForm, self).is_valid()

    def clean_lot(self, lot):
        set_price = int(self.data['set_price'])
        if (
                set_price > lot.current_price and
                lot.min_price_step <= set_price - lot.current_price or
                set_price == lot.current_price == lot.base_price
        ):
            lot.current_price = set_price
            lot.save()
            return True
        else:
            return False


class FilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(FilterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if type(visible.field.widget) == forms.Select:
                visible.field.widget.attrs['class'] = 'uk-select'
            elif type(visible.field.widget) != forms.TextInput:
                visible.field.widget.attrs['class'] = 'uk-input field-input'

    CHOICES = [
        ('price_lth', 'Price: Low to High'),
        ('price_htl', 'Price: High to Low'),
        ('created_lth', 'Created: High to Low'),
        ('created_htl', 'Created: Low to High'),
        ('time_left_lth', 'Time left: High to Low'),
        ('time_left_htl', 'Time left: Low to High'),
    ]

    search = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'uk-search-input uk-search uk-search-large search'
            }
        ),
        required=False,
    )

    min_price = forms.IntegerField(
        widget=forms.NumberInput,
        required=False,
    )

    max_price = forms.IntegerField(
        widget=forms.NumberInput,
        required=False,
    )

    by_author = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'uk-input'
            }
        ),
        required=False,
    )

    order_by = forms.ChoiceField(
        choices=CHOICES,
        widget=forms.Select,
        required=False,
    )

    class Meta:
        fields = [
            'search',
            'min_price',
            'max_price',
            'by_author',
            'order_by',
        ]

    def clean_by_author(self):
        author = self.data.get('by_author')
        if author:
            user = User.objects.filter(username=self.data.get('by_author'))
            if not user.exists():
                self.errors[NON_FIELD_ERRORS] = "User with this username is not found"
            else:
                return author
