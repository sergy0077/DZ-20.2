from django import forms
from catalog.models import Product, Version


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    version = forms.ModelChoiceField(queryset=Version.objects.none(), label='Версия продукта', required=False)

    version_number = forms.CharField(max_length=20, label='Номер версии')
    version_name = forms.CharField(max_length=100, label='Название версии')
    is_active = forms.BooleanField(label='Текущая версия', required=False)

    # поле choices для отображения списка версий в форме
    active_versions = forms.ModelMultipleChoiceField(
        queryset=Version.objects.filter(is_active=True),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.product = self.instance
        if self.product:
            self.fields['active_versions'].queryset = Version.objects.filter(product=self.product, is_active=True)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ProductVersionForm(forms.ModelForm):
    version_number = forms.CharField(max_length=20, label='Номер версии')
    version_name = forms.CharField(max_length=100, label='Название версии')
    is_active = forms.BooleanField(label='Текущая версия', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Product
        fields = '__all__'



