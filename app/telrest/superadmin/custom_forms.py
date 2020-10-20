from django import forms


class OwnerForm(forms.Form):
    # selector IMPLEMENTAR
    # type = forms.ChoiceField(label='Tipo de persona', choices=(('1', 'Física'), ('2', 'Jurídica'),))

    # form para persona fisica

    name = forms.CharField(label='Nombre', max_length=100)
    lastname = forms.CharField(label='Apellidos', max_length=100)
    email = forms.EmailField(label='Email', max_length=100)
    dni = forms.CharField(label='DNI', max_length=20, required=False)
    tlf = forms.FloatField(label='Teléfono', max_value=15, required=False)
    direccion = forms.CharField(label='Calle', max_length=100, required=False)
    ciudad = forms.CharField(label='Ciudad', max_length=30, required=False)
    puerta = forms.CharField(label='Puerta', max_length=30, required=False)
    piso = forms.IntegerField(label='Piso', max_value=10, required=False)
    cp = forms.IntegerField(label='CP', max_value=10, required=False)
    pais = forms.CharField(label='País', max_length=30, required=False)

    # form para persona juridica

    # denominacion = forms.CharField(label='Denominación social', max_length=100)
    # responsable = forms.CharField(label='Responsable', max_length=100)
    # emailj = forms.EmailField(label='Email', max_length=100)
    # cif = forms.CharField(label='CIF', max_length=20, required=False)
    # tlfj = forms.FloatField(label='Teléfono', max_value=15, required=False)
    # callej = forms.CharField(label='Calle', max_length=100, required=False)
    # ciudadj = forms.CharField(label='Ciudad', max_length=30, required=False)
    # cpj = forms.IntegerField(label='CP', max_value=10, required=False)
    # paisj = forms.CharField(label='País', max_length=30, required=False)
