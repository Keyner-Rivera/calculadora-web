# myapp/forms.py
from django import forms

# Opciones para el select de métodos
METHOD_CHOICES = (
    ('bisection', 'Método de Bisección'),
    ('newton_raphson', 'Método de Newton-Raphson'),
    ('modified_newton_raphson', 'Método de Newton-Raphson Modificado'),
)

class RootFinderForm(forms.Form):
    function = forms.CharField(label='Ingresa la ecuación (ej: x^3 - 2*x^2 + 3*x - 4)', max_length=200)
    method = forms.ChoiceField(label='Selecciona el método numérico', choices=METHOD_CHOICES)

    # Campos para el Método de Bisección (ocultos por defecto, mostrados con JS)
    bisection_a = forms.FloatField(label='Intervalo a', required=False)
    bisection_b = forms.FloatField(label='Intervalo b', required=False)

    # Campos para Newton-Raphson (ocultos por defecto, mostrados con JS)
    newton_raphson_initial_guess = forms.FloatField(label='Valor inicial (x₀)', required=False)
    newton_raphson_derivative = forms.CharField(label="Derivada f'(x)", max_length=200, required=False)

    # Campos para Newton-Raphson Modificado (ocultos por defecto, mostrados con JS)
    modified_newton_raphson_initial_guess = forms.FloatField(label='Valor inicial (x₀)', required=False)
    modified_newton_raphson_derivative = forms.CharField(label="Primera derivada f'(x)", max_length=200, required=False)
    modified_newton_raphson_second_derivative = forms.CharField(label="Segunda derivada f''(x)", max_length=200, required=False)

    # Campos comunes a todos los métodos
    tolerance = forms.FloatField(label='Tolerancia', initial=0.0001)
    max_iterations = forms.IntegerField(label='Máximo de Iteraciones', initial=100)

    # Sobreescribe el método clean para validar campos específicos según el método seleccionado
    def clean(self):
        cleaned_data = super().clean()
        method = cleaned_data.get('method')

        if method == 'bisection':
            if not cleaned_data.get('bisection_a'):
                self.add_error('bisection_a', 'Este campo es requerido para Bisección.')
            if not cleaned_data.get('bisection_b'):
                self.add_error('bisection_b', 'Este campo es requerido para Bisección.')
        elif method == 'newton_raphson':
            if not cleaned_data.get('newton_raphson_initial_guess'):
                self.add_error('newton_raphson_initial_guess', 'Este campo es requerido para Newton-Raphson.')
            if not cleaned_data.get('newton_raphson_derivative'):
                self.add_error('newton_raphson_derivative', 'Este campo es requerido para Newton-Raphson.')
        elif method == 'modified_newton_raphson':
            if not cleaned_data.get('modified_newton_raphson_initial_guess'):
                self.add_error('modified_newton_raphson_initial_guess', 'Este campo es requerido para Newton-Raphson Modificado.')
            if not cleaned_data.get('modified_newton_raphson_derivative'):
                self.add_error('modified_newton_raphson_derivative', 'Este campo es requerido para Newton-Raphson Modificado.')
            if not cleaned_data.get('modified_newton_raphson_second_derivative'):
                self.add_error('modified_newton_raphson_second_derivative', 'Este campo es requerido para Newton-Raphson Modificado.')

        return cleaned_data