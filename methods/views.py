# myapp/views.py
from django.shortcuts import render
from .forms import RootFinderForm
from .models import CalculationHistory
from sympy import sympify, Symbol, lambdify, diff # Asegúrate de que 'diff' esté importado si lo usas en otro lado
import numpy as np

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import urllib, base64

def numerical_methods_calculator(request):
    form = RootFinderForm()
    result = None
    error = None
    graph = None
    iterations_data = None  # Variable para almacenar los datos de las iteraciones
    method_name = None      # Variable para el nombre clave del método (ej. 'bisection')
    method_name_display = None # Variable para el nombre legible del método (ej. 'Bisección')

    if request.method == 'POST':
        form = RootFinderForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            function_str = data['function']
            selected_method = data['method']
            tolerance = data['tolerance']
            max_iterations = data['max_iterations']

            # Inicializar variables para el historial
            a_val, b_val = None, None
            initial_guess_val = None
            derivative_expr_str, second_derivative_expr_str = None, None
            
            # Asignar el nombre interno y el nombre de display del método
            method_name = selected_method 
            if selected_method == 'bisection':
                method_name_display = 'Bisección'
            elif selected_method == 'newton_raphson':
                method_name_display = 'Newton-Raphson'
            elif selected_method == 'modified_newton_raphson':
                method_name_display = 'Newton-Raphson Modificado'
            
            x = Symbol('x')
            
            # El bloque try-except ahora engloba toda la lógica de cálculo y graficado
            try:
                f_expr = sympify(function_str)
                f = lambdify(x, f_expr, 'numpy')

                # Lista para almacenar los datos de cada iteración
                current_iterations_log = []

                if selected_method == 'bisection':
                    a = data['bisection_a']
                    b = data['bisection_b']
                    a_val, b_val = a, b # Guardar para el historial

                    if f(a) * f(b) >= 0:
                        error = "La función no cambia de signo en el intervalo dado. (Bisección)"
                    else:
                        # Se puede usar 'prev_c' si se quisiera calcular el error aproximado basado en (c_k - c_{k-1})
                        # Sin embargo, para bisección, el error está inherentemente limitado por (b-a)/2^(n+1)
                        # Aquí usaremos la longitud del intervalo como una medida de la precisión.
                        
                        for i in range(max_iterations):
                            c = (a + b) / 2
                            f_c = f(c)

                            # Error aproximado para Bisección: (b-a)/2 en cada iteración
                            # Opcionalmente, puedes usar el error relativo absoluto si 'c' no es cero
                            approx_error = abs(b - a) / 2.0 if c != 0 else abs(b - a) / 2.0 # O más simple (b-a)/2

                            # Guardar los datos de la iteración actual
                            current_iterations_log.append({
                                'iteration': i + 1,
                                'a': a,
                                'b': b,
                                'x_n': c,
                                'f_x_n': f_c,
                                'approx_error': approx_error,
                            })

                            if abs(f_c) < tolerance or approx_error < tolerance:
                                result = c
                                break
                            
                            if f_c * f(a) < 0:
                                b = c
                            else:
                                a = c
                            
                            if i == max_iterations - 1: # Si llegamos a la última iteración y no convergimos
                                if result is None:
                                    result = c # La última 'c' es la mejor aproximación
                                    error = f"El método de Bisección no convergió en {max_iterations} iteraciones. Última aproximación: {c:.6f}"
                
                elif selected_method == 'newton_raphson':
                    initial_guess = data['newton_raphson_initial_guess']
                    derivative_str = data['newton_raphson_derivative']
                    initial_guess_val = initial_guess # Guardar para historial
                    derivative_expr_str = derivative_str # Guardar para historial

                    df_expr = sympify(derivative_str)
                    df = lambdify(x, df_expr, 'numpy')

                    x0 = float(initial_guess)
                    
                    for i in range(max_iterations):
                        f_x0 = f(x0)
                        df_x0 = df(x0)

                        if abs(df_x0) < 1e-10: # Evitar división por cero
                            error = "La derivada es demasiado cercana a cero, no se puede continuar. (Newton-Raphson)"
                            # Guardar la última iteración conocida antes del error fatal
                            current_iterations_log.append({
                                'iteration': i + 1,
                                'x_n': x0,
                                'f_x_n': f_x0,
                                'approx_error': None, # No se puede calcular un error útil si la derivada es cero
                            })
                            break
                        
                        x1 = x0 - (f_x0 / df_x0)
                        
                        approx_error = abs((x1 - x0) / x1) if x1 != 0 else abs(x1 - x0) # Error relativo o absoluto
                        
                        # Guardar los datos de la iteración actual
                        current_iterations_log.append({
                            'iteration': i + 1,
                            'x_n': x0, # Guardar la x_n de la iteración actual antes de actualizarla
                            'f_x_n': f_x0,
                            'approx_error': approx_error,
                        })

                        if abs(x1 - x0) < tolerance:
                            result = x1
                            break
                        
                        x0 = x1 # Actualizar x0 para la siguiente iteración

                        if i == max_iterations - 1: # Si llegamos a la última iteración y no convergimos
                            if result is None:
                                result = x0 # La última aproximación es la mejor
                                error = f"El método de Newton-Raphson no convergió en {max_iterations} iteraciones. Última aproximación: {x0:.6f}"

                elif selected_method == 'modified_newton_raphson':
                    initial_guess = data['modified_newton_raphson_initial_guess']
                    derivative_str = data['modified_newton_raphson_derivative']
                    second_derivative_str = data['modified_newton_raphson_second_derivative']
                    initial_guess_val = initial_guess # Guardar para historial
                    derivative_expr_str = derivative_str # Guardar para historial
                    second_derivative_expr_str = second_derivative_str # Guardar para historial

                    df_expr = sympify(derivative_str)
                    df = lambdify(x, df_expr, 'numpy')
                    d2f_expr = sympify(second_derivative_str)
                    d2f = lambdify(x, d2f_expr, 'numpy')

                    x0 = float(initial_guess)
                    
                    for i in range(max_iterations):
                        f_x0 = f(x0)
                        df_x0 = df(x0)
                        d2f_x0 = d2f(x0)

                        denominator = (df_x0**2) - (f_x0 * d2f_x0)
                        if abs(denominator) < 1e-10: # Evitar división por cero
                            error = "El denominador es demasiado cercano a cero, no se puede continuar. (Newton-Raphson Modificado)"
                            # Guardar la última iteración conocida antes del error fatal
                            current_iterations_log.append({
                                'iteration': i + 1,
                                'x_n': x0,
                                'f_x_n': f_x0,
                                'approx_error': None,
                            })
                            break
                        
                        x1 = x0 - (f_x0 * df_x0) / denominator
                        
                        approx_error = abs((x1 - x0) / x1) if x1 != 0 else abs(x1 - x0)
                        
                        # Guardar los datos de la iteración actual
                        current_iterations_log.append({
                            'iteration': i + 1,
                            'x_n': x0, # Guardar la x_n de la iteración actual antes de actualizarla
                            'f_x_n': f_x0,
                            'approx_error': approx_error,
                        })

                        if abs(x1 - x0) < tolerance:
                            result = x1
                            break
                        
                        x0 = x1 # Actualizar x0 para la siguiente iteración

                        if i == max_iterations - 1: # Si llegamos a la última iteración y no convergimos
                            if result is None:
                                result = x0 # La última aproximación es la mejor
                                error = f"El método de Newton-Raphson Modificado no convergió en {max_iterations} iteraciones. Última aproximación: {x0:.6f}"
                
                # Una vez que la raíz es encontrada o el bucle termina, asignamos los datos de las iteraciones
                iterations_data = current_iterations_log

                # --- LÓGICA PARA GENERAR LA GRÁFICA ---
                if not error and result is not None: # Solo graficamos si no hubo error y se encontró una raíz
                    x_min_plot, x_max_plot = -10, 10
                    if selected_method == 'bisection':
                        a_plot, b_plot = data['bisection_a'], data['bisection_b']
                        padding = (abs(b_plot - a_plot)) * 0.5 if abs(b_plot - a_plot) > 0 else 5
                        x_min_plot, x_max_plot = min(a_plot, b_plot) - padding, max(a_plot, b_plot) + padding
                    elif result is not None:
                        x_min_plot, x_max_plot = result - 5, result + 5
                    
                    # Asegurar que el rango no sea demasiado pequeño si la función es muy plana o el resultado está lejos
                    if x_min_plot == x_max_plot:
                        x_min_plot -= 5
                        x_max_plot += 5

                    x_vals = np.linspace(x_min_plot, x_max_plot, 400)
                    y_vals = f(x_vals)
                    
                    # Evitar y_vals infinitos o NaN que rompen el gráfico
                    y_vals = np.nan_to_num(y_vals, nan=np.nan, posinf=np.nan, neginf=np.nan)
                    valid_indices = ~np.isnan(y_vals)
                    x_vals_clean = x_vals[valid_indices]
                    y_vals_clean = y_vals[valid_indices]

                    if len(y_vals_clean) > 1 : # Necesitamos al menos dos puntos para trazar
                        plt.figure(figsize=(8, 5))
                        plt.plot(x_vals_clean, y_vals_clean, label=f'f(x) = {function_str}', color='b')
                        plt.axhline(0, color='gray', linewidth=0.8, linestyle='--')
                        plt.title("Gráfica de la Función")
                        plt.xlabel("x")
                        plt.ylabel("f(x)")
                        plt.grid(True)
                        
                        # Ajustar límites en Y dinámicamente, evitando extremos si hay asíntotas
                        y_median = np.median(y_vals_clean)
                        y_std = np.std(y_vals_clean)
                        y_plot_min = y_median - 3 * y_std
                        y_plot_max = y_median + 3 * y_std
                        # Si la raíz está fuera de este rango, ajustar para incluirla
                        if result is not None and f(result) is not None:
                            f_result = f(result)
                            if not (np.isinf(f_result) or np.isnan(f_result)):
                                y_plot_min = min(y_plot_min, f_result - abs(f_result)*0.1 if f_result !=0 else -1)
                                y_plot_max = max(y_plot_max, f_result + abs(f_result)*0.1 if f_result !=0 else 1)
                        
                        # Asegurar que y_min no sea mayor que y_max
                        if y_plot_min >= y_plot_max:
                            y_plot_min = min(y_vals_clean) -1
                            y_plot_max = max(y_vals_clean) +1 if max(y_vals_clean) > min(y_vals_clean) else min(y_vals_clean) +1


                        plt.ylim(y_plot_min, y_plot_max)
                        
                        if result is not None:
                            f_result_val = f(result)
                            if not (np.isinf(f_result_val) or np.isnan(f_result_val)): # Solo graficar si f(result) es un número válido
                                plt.plot(result, f_result_val, 'ro', label=f'Raíz ≈ {result:.4f}')

                        plt.legend()
                        buf = io.BytesIO()
                        plt.savefig(buf, format='png')
                        buf.seek(0)
                        string = base64.b64encode(buf.read())
                        graph = urllib.parse.quote(string)
                        plt.close()
                    else:
                        error = (error + " No se pudo generar la gráfica (datos insuficientes o inválidos)." if error else 
                                 "No se pudo generar la gráfica (datos insuficientes o inválidos).")

            except Exception as e:
                # Este except captura cualquier error durante la evaluación de la función, el cálculo de los métodos o la generación de la gráfica
                error = f"Error en la operación: {e}. Por favor, revise la función, sus derivadas o los parámetros iniciales."

            # --- GUARDAR EN EL HISTORIAL ---
            # Asegurarse de que 'result' sea None si hubo un error fatal que impide un resultado válido.
            # Si el error indica "no convergió", la última aproximación (que se asigna a 'result') sí es un resultado válido para guardar.
            history_entry = CalculationHistory(
                function_expression=function_str,
                method_name=method_name_display, # Usar el nombre legible
                tolerance=tolerance,
                max_iterations=max_iterations,
                a_value=a_val,
                b_value=b_val,
                initial_guess_value=initial_guess_val,
                derivative_expression=derivative_expr_str,
                second_derivative_expression=second_derivative_expr_str,
                # Guardar result_value solo si no hay un error que lo invalide completamente
                result_value=result if not error or "no convergió" in error else None, 
                error_message=error
            )
            history_entry.save()
            # ---------------------------------

        else: # Si el formulario no es válido (ej. campos vacíos o mal formato)
            # Puedes decidir si quieres loggear estos errores del formulario también
            # Por ahora, simplemente no se hace nada especial, el formulario se renderizará con sus errores.
            pass

    # --- OBTENER HISTORIAL PARA MOSTRAR ---
    # Ordenar por 'calculated_at' de forma descendente para mostrar las más recientes primero
    history_entries = CalculationHistory.objects.all().order_by('-calculated_at') 
    # ---------------------------------------

    context = {
        'form': form,
        'result': result,
        'error': error,
        'graph': graph,
        'history_entries': history_entries,
        'iterations_data': iterations_data,       # <-- Datos para la tabla de iteraciones
        'method_name': method_name,               # <-- Nombre clave del método para lógica en HTML
        'method_name_display': method_name_display, # <-- Nombre legible del método para el título
    }
    return render(request, 'home.html', context)