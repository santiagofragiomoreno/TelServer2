from django import forms
class Settings_forms(forms.Form):
    is_lastname = forms.BooleanField(label='Apellidos', required=False)
    is_phone = forms.BooleanField(label='Telefono', required=False)
    is_city = forms.BooleanField(label='Ciudad',  required=False)
    is_import = forms.BooleanField(label='Importe de la reserva', required=False)
    is_origin = forms.BooleanField(label='Origen de la reserva', required=False)
    is_code = forms.BooleanField(label='Código de reserva', required=False)
    is_capacity = forms.BooleanField(label='Aforo', required=False)
    is_cancelation = forms.BooleanField(label='Coste de cancecion', required=False)
    is_observation = forms.BooleanField(label='Observaciones', required=False)
    is_pay = forms.BooleanField(label='Pasarela de pago', required=False)

class Settings_alerts(forms.Form):
    max_temperature = forms.IntegerField(label='Temperatura maxima', max_value=30, required=False)
    min_temperature = forms.IntegerField(label='Temperatura minima', max_value=15, required=False)
    start_time = forms.IntegerField(label='Hora de inicio', max_value=24, required=False)
    end_time = forms.IntegerField(label='Hora de fin', max_value=24, required=False)
    max_capacity = forms.IntegerField(label='Aforo maximo permitido', max_value=10, required=False)
    listening_time = forms.IntegerField(label='Tiempo de escucha para la alarma', max_value=15, required=False)

class Settings_checkout(forms.Form):
    price_time = forms.IntegerField(label='Tiempo (min)', max_value=30, required=False)
    time_price = forms.IntegerField(label='Precio (€)', max_value=15, required=False)