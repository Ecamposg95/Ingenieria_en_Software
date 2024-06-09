# charts.py
import matplotlib.pyplot as plt

def generate_pie_chart():
    labels = ['A', 'B', 'C']
    values = [200, 34, 120]
    explode = [0.1 if value == max(values) else 0 for value in values]

    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct='%1.1f%%', explode=explode, startangle=90, colors=['#ff9999','#66b3ff','#99ff99','#ffcc99'])
    ax.set_title('Distribución de valores para A, B, y C')
    plt.savefig('pie_improved22.png')
    plt.close()
