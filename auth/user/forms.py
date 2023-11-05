from django.forms import ModelForm
from .models import User, ChildrenOrphanage, Visit, Donation, Review
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class AddOrphanageForm(ModelForm):
    class Meta:
        model = ChildrenOrphanage
        fields = '__all__'


class AddUserForm(ModelForm):
    class Meta:
        model = User
        fields = '__all__'


class ReviewForm(ModelForm):
    rating = forms.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = Review
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        rating = cleaned_data.get('rating')
        if not rating:
            self.add_error('rating', "Rating is required.")
        cleaned_data['rating'] = rating
        return cleaned_data
class VisitForm(ModelForm):
    class Meta:
        model = Visit
        fields = '__all__'

class DonationForm(ModelForm):
    class Meta:
        model = Donation
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        donated_item = cleaned_data.get('donated_item')
        amount = cleaned_data.get('amount')

        if donated_item != 'money' and amount:
            self.add_error('amount', "Amount should only be specified for money donations.")

        return cleaned_data

class EditOrphanageForm(ModelForm):
    class Meta:
        model = ChildrenOrphanage
        fields = '__all__'

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')