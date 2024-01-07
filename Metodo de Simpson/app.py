from flask import Flask, request, render_template
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

def simpson_rule(func, a, b, n):
    """Regla de Simpson para integrar 'func' desde 'a' hasta 'b' con 'n' subintervalos"""
    if n % 2 != 0:
        raise ValueError("El número de subintervalos 'n' debe ser par.")

    dx = (b - a) / n
    x = np.linspace(a, b, n + 1)
    y = np.array([eval(func) for x in x])

    # Preparación del gráfico
    plt.figure(figsize=(10, 6))
    x_smooth = np.linspace(a, b, 300)
    y_smooth = np.array([eval(func) for x in x_smooth])
    plt.plot(x_smooth, y_smooth, label='Función f(x)')

    for i in range(0, n, 2):
        xs = np.linspace(x[i], x[i + 2], 100)
        ys = np.array([eval(func) for x in xs])
        plt.fill_between(xs, ys, color='gray', alpha=0.3)

    plt.title('Aproximación de la Integral usando el Método de Simpson')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.legend()

    # Guardar gráfico en un buffer
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    plt.close()

    return dx / 3 * (y[0] + y[-1] + 4 * np.sum(y[1:n:2]) + 2 * np.sum(y[2:n-1:2])), plot_url

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        func = request.form.get('function')
        a = float(eval(request.form.get('a')))
        b = float(eval(request.form.get('b')))
        n = int(request.form.get('n'))

        if n % 2 != 0:
            error = "El número de subintervalos debe ser par."
            return render_template('index.html', error=error)

        try:
            result, plot_url = simpson_rule(func, a, b, n)
            return render_template('result.html', result=result, plot_url=plot_url)
        except Exception as e:
            error = f"Error al calcular la integral: {e}"
            return render_template('index.html', error=error)

    return render_template('index.html')

if __name__ == '__main__':
 #   app.run(host='0.0.0.0', port=80)
    app.run(debug=True)
