from django import forms
from django.forms import Textarea
from .models import Post, Bid


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'set', 'condition', 'author', 'image', 'description', 'place_date', 'finish_date',
                  'min_price', 'user', 'life_cycle')
        exclude = ['user', 'life_cycle']



class PostForm2(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'set', 'condition', 'description', 'finish_date')


# class PlaceBid(forms.ModelForm):
#     class Meta:
#         model = Bid
#         # am = forms.FloatField()
#         fields = ('auct', 'user', 'amount', 'status')


