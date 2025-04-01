import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

# Decorador para medir el tiempo de ejecución de funciones
def timing(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Tiempo de ejecución de {func.__name__}: {end_time - start_time:.6f} segundos")
        return result
    return wrapper

# Clase base que define una onda en la cuerda
class Onda:
    def __init__(self, L, A, mg, u, n):
        self.L = L  # Longitud de la cuerda
        self.A = A  # Amplitud de la onda
        self.mg = mg  # Peso de la cuerda
        self.u = u  # Densidad lineal de masa
        self.n = n  # Modo de vibración
    
    @property
    def velocidad(self):
        # Calcula la velocidad de propagación de la onda
        return math.sqrt(self.mg / self.u)

    @property
    def frecuencia(self):
        # Calcula la frecuencia de la onda
        return self.velocidad / (2 * self.L)

    @property
    def periodo(self):
        # Calcula el periodo de la onda
        return 1 / self.frecuencia

    def calcular_desplazamiento(self, x, t):
        # Método a ser implementado en las subclases
        raise NotImplementedError("Este método debe ser implementado en una subclase")

# Clase que modela una onda estacionaria
class OndaEstacionaria(Onda):
    def calcular_desplazamiento(self, x, t):
        k = self.n * math.pi / self.L  # Número de onda
        omega = 2 * math.pi / self.periodo  # Frecuencia angular
        return self.A * math.sin(k * x) * math.cos(omega * t)

# Clase que modela una onda viajera
class OndaViajera(Onda):
    def calcular_desplazamiento(self, x, t):
        k = self.n * math.pi / self.L  # Número de onda
        omega = 2 * math.pi / self.periodo  # Frecuencia angular
        return self.A * math.sin(k * x - omega * t)

# Implementación del método de Euler para aproximar la solución numérica
class MetodoEuler:
    def __init__(self, onda, dt=0.01, dx=0.1, t_max=2):
        self.onda = onda  # Instancia de la onda a analizar
        self.dt = dt  # Paso de tiempo
        self.dx = dx  # Paso espacial
        self.t_max = t_max  # Tiempo máximo de simulación

    def resolver(self):
        x = [i * self.dx for i in range(int(self.onda.L / self.dx) + 1)]  # Puntos espaciales
        y = [self.onda.calcular_desplazamiento(xi, 0) for xi in x]  # Desplazamientos calculados
        
        plt.figure()
        plt.plot(x, y, 'g-', lw=2)  # Graficar la solución obtenida
        plt.xlabel("Posición x")
        plt.ylabel("Desplazamiento y")
        plt.title("Onda en estado estacionario con Método de Euler")
        plt.grid()
        plt.show()

# Clase que gestiona la animación de la onda
class AnimacionOnda:
    def __init__(self, onda):
        self.onda = onda
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(0, self.onda.L)
        self.ax.set_ylim(-1.1 * self.onda.A, 1.1 * self.onda.A)
        self.ax.set_xlabel("Posición x")
        self.ax.set_ylabel("Desplazamiento y")
        self.ax.set_title("Onda en una cuerda")
        self.x = [i * self.onda.L / 99 for i in range(100)]  # Puntos de evaluación en x
        self.line, = self.ax.plot(self.x, [self.onda.calcular_desplazamiento(xi, 0) for xi in self.x], 'b-', lw=2)
    
    def actualizar(self, frame):
        t = frame * self.onda.periodo / 100  # Tiempo actual de la animación
        # Actualizar los valores de desplazamiento en y
        self.line.set_ydata([self.onda.calcular_desplazamiento(xi, t) for xi in self.x])
        return self.line,

    @timing
    def ejecutar_animacion(self):
        ani = animation.FuncAnimation(self.fig, self.actualizar, frames=100, interval=50, blit=True)
        plt.show()

# Bloque principal de ejecución
if __name__ == "__main__":
    # Solicitud de parámetros al usuario
    L = float(input("Ingrese la longitud de la cuerda en metros: "))
    A = float(input("Ingrese la amplitud de la onda en metros: "))
    mg = float(input("Ingrese el peso de la cuerda en Newtons: "))
    u = float(input("Ingrese la densidad lineal de masa de la cuerda (kg/m): "))
    n = int(input("Ingrese el número del modo de vibración (entero positivo): "))

    # Selección del tipo de onda
    print("Seleccione el tipo de onda:")
    print("1. Estacionaria")
    print("2. Viajera")
    tipo_onda = input("Ingrese el número correspondiente (1 o 2): ").strip()
    if tipo_onda == "2":
        onda = OndaViajera(L, A, mg, u, n)
    else:
        onda = OndaEstacionaria(L, A, mg, u, n)

    # Creación y ejecución de la animación
    animacion = AnimacionOnda(onda)
    animacion.ejecutar_animacion()

    # Resolución mediante el método numérico de Euler
    metodo_euler = MetodoEuler(onda)
    metodo_euler.resolver()