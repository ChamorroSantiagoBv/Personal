import time
import numpy as np 
import sys

# Imprimir con demora
def imprimir_con_retraso(s):
    # Imprimir una letra a la vez
    for c in s:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.05)

# Crear la clase
class Pokemon:
    def __init__(self, nombre, tipos, movimientos, EVs, puntos_de_salud='============='):
        # Guardar las variables como atributos
        self.nombre = nombre
        self.tipos = tipos 
        self.movimientos = movimientos
        self.ataque = EVs['ataque']
        self.defensa = EVs['defensa']
        self.puntos_de_salud = puntos_de_salud
        self.barras = 20  # Amount of puntos_de_salud barras

    def impresa(self, Pokemon2):
        '''Imprimir información de lucha'''
        print("-----BATALLA DE POKÉMON-----")
        print(f"\n{self.nombre}")
        print("tipo/", self.tipos)
        print("ataque/", self.ataque)
        print("defensa/", self.defensa)
        print("Nv./", 3 * (1 + np.mean([self.ataque, self.defensa])))
        print("\nVS")
        print(f"\n{Pokemon2.nombre}")
        print("tipo/", Pokemon2.tipos)
        print("ataque/", Pokemon2.ataque)
        print("defensa/", Pokemon2.defensa)
        print("Nv./", 3 * (1 + np.mean([Pokemon2.ataque, Pokemon2.defensa])))
        time.sleep(2)

    def ventaja(self, Pokemon2):
        '''Considerar la ventaja de tipo
        Actualizar poderes de ataque y defensa
        Devuelve dos cadenas de información'''
        
        cadena_1_ataque = ''
        cadena_2_ataque = ''

        version = ['fuego', 'agua', 'planta']
        for i, k in enumerate(version):

            if self.tipos == k:
                # Son del mismo tipo
                if Pokemon2.tipos == k:
                    cadena_1_ataque = '\nNo es muy efectivo...'
                    cadena_2_ataque = '\nNo es muy efectivo...'

                # Pokemon2 es FUERTE
                elif Pokemon2.tipos == version[(i + 1) % 3]:
                    Pokemon2.ataque *= 2
                    Pokemon2.defensa *= 2
                    self.ataque /= 2
                    self.defensa /= 2
                    cadena_1_ataque = '\nNo es muy efectivo...'
                    cadena_2_ataque = '\n¡Es muy eficaz!'

                # Pokemon2 es DÉBIL 
                elif Pokemon2.tipos == version[(i + 2) % 3]:
                    self.ataque *= 2
                    self.defensa *= 2
                    Pokemon2.ataque /= 2
                    Pokemon2.defensa /= 2
                    cadena_1_ataque = '\n¡Es muy eficaz!'
                    cadena_2_ataque = '\nNo es muy efectivo...'
        
        return cadena_1_ataque, cadena_2_ataque

    def turno(self, Pokemon2, cadena_1_ataque, cadena_2_ataque):
        '''Empieza con Pokemon1, elige ataque y calcula
        los nuevos puntos de salud.
        Haz lo mismo con Pokemon2. Siga hasta que los puntos de salud de
        los pokemon sean < 0
        Actualiza los datos.
        '''
        while (self.barras > 0) and (Pokemon2.barras > 0):

            # Imprimir los puntos_de_salud de cada Pokemon
            print(f"\n{self.nombre}\t\tPS\t{self.puntos_de_salud}")
            print(f"\n{Pokemon2.nombre}\t\tPS\t{Pokemon2.puntos_de_salud}")

            # POKEMON 1
            print(f"¡Adelante {self.nombre}!")
            for i, x in enumerate(self.movimientos):
                print(f"{i + 1}.", x)
            index = int(input('Elige un movimiento: '))
            imprimir_con_retraso(f"\n¡{self.nombre} usó {self.movimientos[index - 1]}!")
            time.sleep(1)
            imprimir_con_retraso(cadena_1_ataque)

            # Determinar el daño
            Pokemon2.barras -= self.ataque
            Pokemon2.puntos_de_salud = ""

            # Agregar barras adicionales más defensa boost
            for j in range(int(Pokemon2.barras + .1 * Pokemon2.defensa)):
                Pokemon2.puntos_de_salud += "="

            time.sleep(1)
            print(f"\n{self.nombre}\t\tPS\t{self.puntos_de_salud}")
            print(f"\n{Pokemon2.nombre}\t\tPS\t{Pokemon2.puntos_de_salud}")
            time.sleep(.5)

            # Comprueba si Pokémon se debilitó
            if Pokemon2.barras <= 0:
                imprimir_con_retraso("\n..." + Pokemon2.nombre + ' se debilitó')
                break

            # POKEMON 2
            print(f"¡Adelante {Pokemon2.nombre}!")
            for i, x in enumerate(Pokemon2.movimientos):
                print(f"{i + 1}.", x)
            index = int(input('Elige un movimiento: '))
            imprimir_con_retraso(f"\n¡{Pokemon2.nombre} usó {Pokemon2.movimientos[index - 1]}!")
            time.sleep(1)
            imprimir_con_retraso(cadena_2_ataque)

            # Determinar el daño
            self.barras -= Pokemon2.ataque
            self.puntos_de_salud = ""

            # Agregar barras adicionales más defensa boost
            for j in range(int(self.barras + .1 * self.defensa)):
                self.puntos_de_salud += "="

            time.sleep(1)
            print(f"\n{self.nombre}\t\tPS\t{self.puntos_de_salud}")
            print(f"\n{Pokemon2.nombre}\t\tPS\t{Pokemon2.puntos_de_salud}")
            time.sleep(.5)

            # Comprueba si Pokémon se debilitó
            if self.barras <= 0:
                imprimir_con_retraso("\n..." + self.nombre + ' se debilitó')
                break

    def lucha(self, Pokemon2):
        '''Permitir que dos pokemon luchen entre ellos'''

        # Imprimir información de lucha
        self.impresa(Pokemon2)

        # Considerar la ventaja de tipo
        cadena_1_ataque, cadena_2_ataque = self.ventaja(Pokemon2)

        # Ahora para la lucha real ...
        # Continúa mientras Pokémon aún tenga puntos_de_salud
        self.turno(Pokemon2, cadena_1_ataque, cadena_2_ataque)

        # Recibir dinero (premio)
        money = np.random.choice(5000)
        imprimir_con_retraso(f"\nEl oponente te pagó ${money}.\n") 

if __name__ == '__main__':
    # Crear Pokémon
    Charizard = Pokemon('Charizard', 'fuego', ['Llamarada', 'Vuelo', 'Blast Burn', 'Puño Fuego'], {'ataque': 12, 'defensa': 8})
    Blastoise = Pokemon('Blastoise', 'agua', ['Pistola Agua', 'Rayo Burbuja', 'Hydro Pump', 'Surf'], {'ataque': 10, 'defensa': 10})
    Venusaur = Pokemon('Venusaur', 'planta', ['Vine Whip', 'Razor Leaf', 'Earthquake', 'Frenzy Plant'], {'ataque': 8, 'defensa': 12})

    Charmander = Pokemon('Charmander', 'fuego', ['Ember', 'Scratch', 'Tackle', 'Puño Fuego'], {'ataque': 4, 'defensa': 2})
    Squirtle = Pokemon('Squirtle', 'agua', ['Rayo Burbuja', 'Tackle', 'Headbutt', 'Surf'], {'ataque': 3, 'defensa': 3})
    Bulbasaur = Pokemon('Bulbasaur', 'planta', ['Vine Whip', 'Razor Leaf', 'Tackle', 'Leech Seed'], {'ataque': 2, 'defensa': 4})

    Charmeleon = Pokemon('Charmeleon', 'fuego', ['Ember', 'Scratch', 'Llamarada', 'Puño Fuego'], {'ataque': 6, 'defensa': 5})
    Wartortle = Pokemon('Wartortle', 'agua', ['Rayo Burbuja', 'Pistola Agua', 'Headbutt', 'Surf'], {'ataque': 5, 'defensa': 5})
    Ivysaur = Pokemon('Ivysaur', 'planta', ['Vine Whip', 'Razor Leaf', 'Bullet Seed', 'Leech Seed'], {'ataque': 4, 'defensa': 6})

    Charizard.lucha(Blastoise)  # Hazlos luchar
