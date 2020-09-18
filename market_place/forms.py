from django import forms


# TO BE USED IN DEBUG TO POPULATE DB'S FOR TEST
class ProductUploadForm(forms.Form):
    brand = forms.CharField(max_length=100)
    name = forms.CharField(max_length=200)
    price = forms.CharField(max_length=100)
    category = forms.CharField(max_length=50)
    description = forms.CharField(max_length=10000)
    stock = forms.IntegerField()
    img1 = forms.FileField()
    img2 = forms.FileField()
    img3 = forms.FileField()

