from django import forms


# TO BE USED IN DEBUG TO POPULATE DB'S FOR TEST
class ProductUploadForm(forms.Form):
    name = forms.CharField(max_length=100)
    price = forms.CharField(max_length=100)
    category = forms.CharField(max_length=50)
    description = forms.CharField(max_length=500)
    stock = forms.IntegerField()
    img1 = forms.ImageField()
    img2 = forms.ImageField()
    img3 = forms.ImageField()


class Login(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
