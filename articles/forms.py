from django import forms


class ArticleForm(forms.Form):
    title = forms.CharField()
    content = forms.CharField()

    def clean(self):
        """
        Clean the data such as whitespace and empty fill
        @return: Cleaned data
        """
        cleaned_data = self.cleaned_data  # dictionary
        return cleaned_data
