from .models import Review
from django import forms
CHOICE = [(1,1),
    (2,2),
    (3,3),
    (4,4),
    (5,5),
    (6,6),
    (7,7),
    (8,8),
    (9,9),
    (10,10)]
    
class ReviewForm(forms.ModelForm):
    score = forms.ChoiceField(choices=CHOICE,widget=forms.RadioSelect(attrs={'class': 'special'}))
    class Meta:
        model = Review
        fields =('content','score')