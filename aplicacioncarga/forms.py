from django import forms

class ConsumirServicioForm(forms.Form):
    urlServicio = forms.CharField(label='URL del servicio', max_length=500 ,required=True)
    cantidadHilos = forms.IntegerField(label='Cantidad de hilos', required=True)