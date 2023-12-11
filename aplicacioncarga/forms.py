from django import forms

class ConsumirServicioForm(forms.Form):
    urlServicio = forms.CharField(label='URL del servicio', max_length=500)
    cantidadHilos = forms.IntegerField(label='Cantidad de hilos')