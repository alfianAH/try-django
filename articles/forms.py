from django import forms

from .models import Article


class ArticleModelForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content']

    def clean(self):
        data = self.cleaned_data
        title = data.get("title")

        # Query all the database and filter the title
        qs = Article.objects.filter(title__icontains=title)

        # If the query has results, ...
        if qs.exists():
            # Print the error
            self.add_error("title", "\"{}\" is already in use".format(title))

        return data


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
