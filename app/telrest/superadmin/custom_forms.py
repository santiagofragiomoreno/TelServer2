from django import forms
from telapi.models import Flat


# form usado en alta_clientes para la persona fisica
class OwnerForm(forms.Form):
    name = forms.CharField(label='Nombre', max_length=100)
    lastname = forms.CharField(label='Apellidos', max_length=100)
    email = forms.EmailField(label='Email', max_length=100)
    dni = forms.CharField(label='DNI', max_length=20, required=False)
    tlf = forms.FloatField(label='Teléfono', max_value=999999999999, required=False)
    direccion = forms.CharField(label='Calle', max_length=100, required=False)
    ciudad = forms.CharField(label='Ciudad', max_length=30, required=False)
    puerta = forms.CharField(label='Puerta', max_length=30, required=False)
    piso = forms.IntegerField(label='Piso', max_value=999, required=False)
    cp = forms.IntegerField(label='CP', max_value=99999999, required=False)


# form usado en alta_clientes para la persona juridica
class JuridicaForm(forms.Form):
    denominacion = forms.CharField(label='Denominación social', max_length=100)
    responsable = forms.CharField(label='Responsable', max_length=100)
    email = forms.EmailField(label='Email', max_length=100)
    cif = forms.CharField(label='CIF', max_length=30, required=False)
    tlf = forms.FloatField(label='Teléfono', max_value=999999999999, required=False)
    direccion = forms.CharField(label='Calle', max_length=100, required=False)
    ciudad = forms.CharField(label='Ciudad', max_length=30, required=False)
    puerta = forms.CharField(label='Puerta', max_length=30, required=False)
    piso = forms.IntegerField(label='Piso', max_value=999, required=False)
    cp = forms.IntegerField(label='CP', max_value=99999999, required=False)


#  class FlatForm(forms.ModelForm):
#      class Meta:
#          model = Flat
#          fields = "__all__"

#  form usado en alta_pisos para el formulario de pisos
class FlatForm(forms.Form):
    name = forms.CharField(label='Nombre del piso', max_length=100)
    address = forms.CharField(label='Direccion', max_length=100)
    floor = forms.IntegerField(label='Piso', max_value=999, required=False)
    door = forms.CharField(label='Puerta', max_length=100, required=False)
    city = forms.CharField(label='Ciudad', max_length=100, required=False)
    postal_code = forms.IntegerField(label='CP', max_value=99999999, required=False)
    guests = forms.IntegerField(label='Nº huéspedes', max_value=99, required=False)
    rooms = forms.IntegerField(label='Nº habitaciones', max_value=99, required=False)
    baths = forms.IntegerField(label='Nº baños', max_value=99, required=False)
    reference = forms.CharField(label='Referencia catastral', max_length=100, required=False)
    meters = forms.IntegerField(label='Nº metros', max_value=99999, required=False)