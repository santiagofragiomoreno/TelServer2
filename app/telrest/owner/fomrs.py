from django import forms
class Settings_forms(forms.Form):
    is_lastname = forms.BooleanField(label='Apellidos', required=False)
    is_phone = forms.BooleanField(label='Telefono', required=False)
    is_city = forms.BooleanField(label='Ciudad',  required=False)
    is_birthdate = forms.BooleanField(label='Fecha de nacimiento',  required=False)
    is_import = forms.BooleanField(label='Importe de la reserva', required=False)
    is_origin = forms.BooleanField(label='Origen de la reserva', required=False)
    is_code = forms.BooleanField(label='Código de reserva', required=False)
    is_capacity = forms.BooleanField(label='Aforo', required=False)
    is_cancelation = forms.BooleanField(label='Coste de cancecion', required=False)
    is_observation = forms.BooleanField(label='Observaciones', required=False)
    is_pay = forms.BooleanField(label='Pasarela de pago', required=False)

class Settings_alerts(forms.Form):
    max_temperature = forms.IntegerField(label='Temperatura maxima', max_value=30, min_value=0,required=False)
    min_temperature = forms.IntegerField(label='Temperatura minima', max_value=15,min_value=0, required=False)
    start_time = forms.IntegerField(label='Hora de inicio', max_value=24, min_value=0,required=False)
    end_time = forms.IntegerField(label='Hora de fin', max_value=24,min_value=0, required=False)
    max_capacity = forms.IntegerField(label='Aforo maximo permitido', max_value=10,min_value=0, required=False)
    listening_time = forms.IntegerField(label='Tiempo de escucha para la alarma', max_value=15,min_value=0, required=False)

class Settings_checkout(forms.Form):
    price_time = forms.IntegerField(label='Tiempo (min)', max_value=30, required=False,min_value=0)
    time_price = forms.IntegerField(label='Precio (€)', max_value=15, required=False,min_value=0)

class Client(forms.Form):
    name = forms.CharField(label='Nombre', max_length=100,required=True)
    lastname = forms.CharField(label='Apellidos', max_length=100,required=False)
    email = forms.EmailField(label='Email', max_length=100)
    dni = forms.CharField(label='DNI', max_length=20, required=False)
    tlf = forms.IntegerField(label='Teléfono', max_value=999999999, required=False)
    direction = forms.CharField(label='Calle', max_length=100, required=False)
    city = forms.CharField(label='Ciudad', max_length=30, required=False)
    country = forms.CharField(label='Pais', max_length=30, required=False)
    cp = forms.IntegerField(label='CP', max_value=99999, required=False)

class Reservation(forms.Form):
    guest = forms.IntegerField(label='Huespedes', max_value=10, required=False,min_value=0)
    import_price = forms.IntegerField(label='Importe de la reserva', max_value=10, required=False,min_value=0)
    origin = forms.CharField(label='Pais de origen de la reserva', max_length=30, required=False)
    code = forms.CharField(label='Código de reserva', max_length=999999999, required=False)
    cancelation = forms.IntegerField(label= 'Coste de cancecion', max_value=10, required=False,min_value=0)
    observation = forms.CharField(label='Observaciones', max_length=65535, required=False)

    #is_pay = forms.BooleanField(label='Pasarela de pago', required=False)
    #TODO Preguntar a marc como va a ser la pasarela de pago y que opciones ponemos, ira seguramente con un select o radiobutton
    # que segun la opcion seleccionada te habra con js un submenu o algo asi para rellenar datos 

NUMS= [
    ('flat.name', 'PISO'),
    ('state', 'ESTADO'),
    ('date_access_start', 'FECHA DE INICIO'),
    ('date_access_end', 'FECHA DE FIN'),
    ('auth_user.username', 'NOMBRE'),
    ('auth_user.last_name', 'APELLIDOS'),
    ('auth_user.tlf', 'TELEFONO'),

    ]
class Filter(forms.Form):
    NUMS = forms.ChoiceField(choices=NUMS, widget=forms.RadioSelect)