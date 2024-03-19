from django import forms


class ResultTable(forms.Form):
    code = forms.CharField(widget=forms.Textarea(attrs={"class": "input-field"}))

    # class Meta:
    #     model = Code
    #     fields = ["code"]
        # widgets = {
        #     'code': forms.TextInput(attrs={'class': 'input-box'}),
        # }
