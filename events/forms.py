from django import forms
from events.models import Events, Category


class EventForm(forms.ModelForm):
    class Meta:
        model = Events
        fields = ['name','description','start_date','end_date','time','location','category','image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full p-3 rounded-xl bg-white/10 border border-white/20 '
                         'text-white placeholder-purple-300 backdrop-blur-md '
                         'focus:ring-2 focus:ring-purple-500 focus:outline-none',
                'placeholder': 'Event Name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full p-3 h-32 rounded-xl bg-white/10 border border-white/20 '
                         'text-white placeholder-purple-300 backdrop-blur-md '
                         'focus:ring-2 focus:ring-purple-500 focus:outline-none',
                'placeholder': 'Event Description'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'w-full p-3 rounded-xl bg-white/10 border border-white/20 '
                         'text-white backdrop-blur-md focus:ring-2 '
                         'focus:ring-purple-500 focus:outline-none',
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'w-full p-3 rounded-xl bg-white/10 border border-white/20 '
                         'text-white backdrop-blur-md focus:ring-2 '
                         'focus:ring-purple-500 focus:outline-none',
                'type': 'date'
            }),
            'time': forms.TimeInput(attrs={
                'class': 'w-full p-3 rounded-xl bg-white/10 border border-white/20 '
                         'text-white backdrop-blur-md focus:ring-2 '
                         'focus:ring-purple-500 focus:outline-none',
                'type': 'time'
            }),
            'location': forms.TextInput(attrs={
                'class': 'w-full p-3 rounded-xl bg-white/10 border border-white/20 '
                         'text-white placeholder-purple-300 backdrop-blur-md '
                         'focus:ring-2 focus:ring-purple-500 focus:outline-none',
                'placeholder': 'Event Location'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full p-3 rounded-xl bg-white/10 border border-white/20 '
                         'text-white backdrop-blur-md focus:ring-2 '
                         'focus:ring-purple-500 focus:outline-none'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'w-full p-3 rounded-xl bg-white/10 border border-white/20 '
                         'text-white backdrop-blur-md focus:ring-2 '
                         'focus:ring-purple-500 focus:outline-none'
            }),
        }
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "w-full p-3 rounded-xl bg-white/10 border border-white/20 text-white placeholder-purple-300 backdrop-blur-md focus:ring-2 focus:ring-purple-500 focus:outline-none",
                "placeholder": "Category Name"
            }),
            "description": forms.Textarea(attrs={
                "class": "w-full p-3 h-32 rounded-xl bg-white/10 border border-white/20 text-white placeholder-purple-300 backdrop-blur-md focus:ring-2 focus:ring-purple-500 focus:outline-none",
                "placeholder": "Description"
            }),
        }