from django.db import models

class CalculationHistory(models.Model):
    # Campos comunes a todas las operaciones
    function_expression = models.CharField(max_length=255, help_text="La expresión de la función utilizada")
    method_name = models.CharField(max_length=50, help_text="Nombre del método numérico (Bisección, Newton-Raphson, etc.)")
    tolerance = models.FloatField(help_text="La tolerancia utilizada para el cálculo")
    max_iterations = models.IntegerField(help_text="El número máximo de iteraciones permitidas")
    calculated_at = models.DateTimeField(auto_now_add=True, help_text="Fecha y hora del cálculo")

    # Campos específicos para cada método (pueden ser nulos si no se usan)
    # Bisección
    a_value = models.FloatField(null=True, blank=True, help_text="Valor 'a' para Bisección")
    b_value = models.FloatField(null=True, blank=True, help_text="Valor 'b' para Bisección")

    # Newton-Raphson y Modificado Newton-Raphson
    initial_guess_value = models.FloatField(null=True, blank=True, help_text="Valor de estimación inicial (x₀)")
    derivative_expression = models.CharField(max_length=255, null=True, blank=True, help_text="Expresión de la primera derivada")
    second_derivative_expression = models.CharField(max_length=255, null=True, blank=True, help_text="Expresión de la segunda derivada")

    # Resultados
    result_value = models.FloatField(null=True, blank=True, help_text="La raíz aproximada encontrada")
    error_message = models.TextField(null=True, blank=True, help_text="Mensaje de error si el cálculo falló")

    def __str__(self):
        return f"Cálculo de {self.method_name} para f(x)='{self.function_expression}' @ {self.calculated_at.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        ordering = ['-calculated_at'] # Ordenar por fecha de cálculo descendente