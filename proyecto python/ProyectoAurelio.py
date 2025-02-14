# !/usr/bin/python3
from tkinter import PhotoImage, Label, Frame
import tkinter
import pygame
import random
pygame.font.init()
# Recordar mover los archivos a la terminal para que se cargue de manera
# correcta.
# Realmente no copié y pegué nada, ni ningún código de internet, pero me
# inspiré en lo sisguientes vídeos para darme una idea de lo que tenía que
# hacer para que el código plasmara de forma adecuada lo que yo quería hacer
# como proyecto, seguidamente adjunto los links:
# link 1:
# https://www.youtube.com/watch?v=UZolOCW6Sg8&list=
# PL8KnQ7ULK8ejkYsjtWmUneJ-Q3p7gQIOQ
# link 2:
# https://www.youtube.com/watch?v=jrUJ8EsnctI&t=83s
# Configuraciones de la ventana principal
ventana = tkinter.Tk()
ventana.title("Operetion Moon Light")
ventana.geometry("650x650+200+0")
ventana.config(cursor="star")


# Imagen para el fondo del juego
fondo = PhotoImage(file="space3.gif")
ventanafondo = Label(ventana, image=fondo).place(x=0, y=0)

# Configuarciones del marco de la ventana principal de juego
marco = Frame()
marco.pack()
marco.pack(side="top")
marco.config(bg="Brown")
marco.config(width=400, height=500)
marco.config(relief="groove")
marco.config(bd=25)
marco.config(cursor="star")


# Funcion para el boton de inicio el cual comienza el juego
def iniciar():
    # Seleccionar .play()
    ventana.withdraw()
    juego()  # Funcion donde esta almacenada el juego
    # Se debe actualizar la fuente cada vez que se
    # Inicia el juego para evitar problemas
    pygame.font.init()


# Boton para iniciar el juego
botoninicio = tkinter.Button(marco, text="iniciar juego", command=iniciar)
botoninicio.place(x=15, rely=0.2)
botoninicio.config(bd=18, relief="groove")
botoninicio.config(bg="goldenrod", font="20")
botoninicio.place(relwidth=0.9, relheight=0.15)


# Función para salir del juego
def salir():
    ventana.destroy()  # Eliminar la ventana principal


# Botón para salir del juego
botonsalir = tkinter.Button(marco, text="Cerrar", command=salir)
botonsalir.place(x=15, rely=0.65)
botonsalir.config(bd=18, relief="groove")
botonsalir.config(bg="red", font="20")
botonsalir.place(relwidth=0.9, relheight=0.15)


def juego():  # Función que almacena el juego
    # Programación del juego
    juego = pygame.display.set_mode((650, 650))
    pygame.display.set_caption("Operation moon light")

    # Sprites
    naveprincipal = pygame.image.load("nave2.png")
    E1imagen = pygame.image.load("enemigo1.png")
    E2imagen = pygame.image.load("enemigo2.png")
    J1imagen = pygame.image.load("jefe1.png")
    laser_imagen = pygame.image.load("LaserRojo.png")
    laserjefeimagen = pygame.image.load("LaserRojo.png")
    fondojuego = pygame.image.load("space.gif")
    lunaimagen = pygame.image.load("sephirot.png")
    # Sonidos
    pygame.mixer.init()
    sonidolaser = pygame.mixer.Sound("blaster.mp3")
    ambiente = pygame.mixer.Sound("Musica.mp3")
    golpe = pygame.mixer.Sound("8-bit-explosion_F.wav")
    ambiente.play()
    # Variables
    fps = 60  # Frames por segundo que actualiza el juego
    abrir = True   # Mantiene la venta de juego abierta
    Reloj = pygame.time.Clock()  # Reloj para obtener los milisegundos juego
    # Carga la letra del juego
    fuenteletra = pygame.font.match_font("Arial", 15)
    segundo = 0  # Tiempo inicial
    b = True  # Necesaria para sumar los puntos extra y curar solo una vez
    # Indica cuanto debe curar, se actualiza en base al daño
    # recibido mas adelante
    curar = 0

    class Jugador(pygame.sprite.Sprite):  # Clase para el jugador
        def __init__(self):
            # Obtiene las caracteristica de la clase Sprite de pygame
            super().__init__()
            # Imagen del jugador
            self.image = pygame.transform.scale(naveprincipal, (70, 70))
            self.rect = self.image.get_rect()  # Obtiene rectángulo (sprite)
            self.rect.x = 325  # Posición inicial x
            self.rect.y = 600  # Posición inicial y
            # Tiempo de enfreamiento entre disparos en milisegundos
            self.enfriamiento = 300
            self.ultimoLaser = 0  # Mide el tiempo entre disparos
            self.salud = 50  # Salud del jugador
            # Tiempo de invencibilidad desde el ultimo golpe recibido
            self.invencible = 1000
            self.ultimogolpe = 0  # Mide el tiempo desde el ultimo golpe

        def update(self):  # Actualización del estado del jugador
            # Velocidad predeterminada/sirve para parar
            teclas = pygame.key.get_pressed()  # Lee el teclado
            # Movimiento y limites de la pantalla
            if teclas[pygame.K_RIGHT] and 650 > self.rect.right:
                self.rect.x += 7
            if teclas[pygame.K_LEFT] and self.rect.left > 0:
                self.rect.x -= 7
            if teclas[pygame.K_UP] and self.rect.top > 0:
                self.rect.y -= 7
            if teclas[pygame.K_DOWN] and 650 > self.rect.bottom:
                self.rect.y += 7
            # Permite disparar al presionar el espacio
            if teclas[pygame.K_SPACE]:
                # Mide el tiempo en milisegundos
                tiempoactual = pygame.time.get_ticks()
                # Ordena una acción despues de un tiempo x
                if tiempoactual - self.ultimoLaser > self.enfriamiento:
                    jugador.disparar()
                    # Indica un nuevo tiempo de referencia
                    self.ultimoLaser = tiempoactual

        def disparar(self):  # Función que permite el disparo del jugador
            laser = Laser(self.rect.x + 35, self.rect.top + 25)
            disparos.add(laser)

    class Enemigo1(pygame.sprite.Sprite):  # Clase para el primer enemigo
        def __init__(self):
            super().__init__()
            # Imagen del enemigo
            self.image = pygame.transform.scale(E1imagen, (70, 70))
            self.rect = self.image.get_rect()  # Obtiene el rectángulo
            self.rect.y = 50  # Posicion x
            self.rect.x = 325  # Posicion y
            self.velocidadx = 4  # Velocidad de movimiento izquierda-derecha
            self.velocidady = 0  # Velocidad de movimiento arriba-abajo
            self.enfriamiento = 2000  # Tiempo entre embestidas
            self.ultimoataque = 0  # Tiempo para generar el numero la embestida
            self.derecha = True  # Moviento a la derecha
            self.izquierda = False  # Movimiento a la izquierda
            self.salud = 15  # Salud del enemigo

        def update(self):
            # Valor de la embestida(si es divisible entre 3 activa el ataque)
            embestida = 1
            embestir = True  # Embestida se activada
            tiempoactual = pygame.time.get_ticks()
            # Actualiza la posicon en y segun la velocidad
            self.rect.y += self.velocidady
            if tiempoactual - self.ultimoataque > self.enfriamiento:
                # Genera el numero aleatorio
                embestida = random.randrange(0, 11)
                self.ultimoataque = tiempoactual
            # Al volver de la embestida retoma el movimiento horizontal
            if self.rect.top in range(40, 51):
                self.velocidady = 0
                self.velocidadx = 4
                embestir = True
            if self.derecha:
                self.rect.x += self.velocidadx
            if self.izquierda:
                self.rect.x -= self.velocidadx
            # Desactiva el movimiento a la derecha y activa el izquierdo
            if self.rect.right > 650:
                self.derecha = False
                self.izquierda = True
            # Desactiva el movimiento a la izquierda y activa el derecho
            if 0 > self.rect.left:
                self.derecha = True
                self.izquierda = False
            # Si el numero aleatorio es divisible entre 3 embiste
            if embestida % 3 == 0 and embestir:
                self.velocidadx = 0
                self.velocidady = 18
                E1.salud -= 1
                self.rect.y += self.velocidady
                embestir = False
            # Al llegar abajo de la pantalla, se devuelve arriba
            if self.rect.bottom > 650:
                self.velocidady *= -1

    class Enemigo2(pygame.sprite.Sprite):  # Clase para el segundo enemigo
        def __init__(self):
            super().__init__()
            # Imagen del enemigo 2
            self.image = pygame.transform.scale(E2imagen, (70, 70))
            self.rect = self.image.get_rect()  # Obtiene el rectángulo
            self.rect.y = 50   # Posición x
            self.rect.x = 325   # Posición y
            self.velocidadx = 4  # Velocidad de movimiento izquierda-derecha
            self.velocidady = 0  # Velocidad de movimiento arriba-abajo
            self.enfriamiento = 2000  # Tiempo entre embestidas
            self.ultimoataque = 0  # Tiempo para generar el numero embestida
            self.derecha = True  # Moviento a la derecha
            self.izquierda = False  # Movimiento a la izquierda
            self.salud = 20  # Salud del enemigo 2

        def update(self):
            # Valor de la embestida(si es divisible entre 2 activa el ataque)
            embestida = 1
            embestir = True  # Embestida activada
            tiempoactual = pygame.time.get_ticks()
            # Actualiza la posicon en y segun la velocidad
            self.rect.y += self.velocidady
            if tiempoactual - self.ultimoataque > self.enfriamiento:
                # Genera el numero aleatorio
                embestida = random.randrange(0, 5)
                self.ultimoataque = tiempoactual
                # Al volver de la embestida retoma el movimiento horizontal
            if self.rect.top in range(40, 51):
                self.velocidady = 0
                self.velocidadx = 4
                embestir = True
            if self.derecha:
                self.rect.x += self.velocidadx
            if self.izquierda:
                self.rect.x -= self.velocidadx
            # Desactiva el movimiento a la derecha y activa el izquierdo
            if self.rect.right > 650:
                self.derecha = False
                self.izquierda = True
            # Desactiva el movimiento a la izquierda y activa el derecho
            if 0 > self.rect.left:
                self.derecha = True
                self.izquierda = False
            # Si el número aleatorio es divisible entre 3 embiste
            if embestida % 3 == 0 and embestir:
                self.velocidadx = 0
                self.velocidady = 18
                E2.salud -= 1
                self.rect.y += self.velocidady
                embestir = False
            # Al llegar abajo de la pantalla, devuelvase hacia arriba
            if self.rect.bottom > 650:
                self.velocidady *= -1

    class OVNI(pygame.sprite.Sprite):  # Clase del primer jefe
        def __init__(self):
            super().__init__()
            # Imagen del jefe 1
            self.image = pygame.transform.scale(J1imagen, (175, 100))
            self.image.set_colorkey((0, 0, 0))  # Elimina el fondo del jefe1
            self.salud = 30
            self.rect = self.image.get_rect()
            self.rect.y = 50
            self.rect.x = 325
            self.teletransporte = 2000  # Tiempo entre teletransportes
            # Tiempo desde el ultimo teletransporte
            self.ultimoteletransporte = 0
            self.enfriamiento1 = 100  # Tiempo entre disparos
            self.rafaga = 1000  # Tiempo entre rafagas de disparos
            self.ultimarafaga = 0  # Tiempo desde la ultima rafaga
            self.ultimodisparo1 = 0  # Tiempo desde el ultimo disaparo
            self.disparo = True  # Activa el disparo
            self.contar = 0  # Cuenta el número de disparos por rafaga

        def update(self):
            tiempoactual = pygame.time.get_ticks()
            if tiempoactual - self.ultimoteletransporte > self.teletransporte:
                # Cambia a una posición en x aleatoria
                self.rect.x = random.randrange(20, 530, 30)
                self.ultimoteletransporte = tiempoactual
            if tiempoactual - self.ultimarafaga > self.rafaga:
                self.disparo = True  # Activa el disparo cada segundo
                self.ultimarafaga = tiempoactual
            if tiempoactual - self.ultimodisparo1 > self.enfriamiento1 \
                    and self.disparo:
                ovni.disparar()
                self.ultimodisparo1 = tiempoactual
                self.contar += 1  # Cuenta los disparos en esta rafaga
                sonidolaser.play()
                # Desactiva el disparo despues de 3 disparos seguidos
                if self.contar > 2:
                    self.disparo = False
                    self.contar = 0  # Reinicia el contador de disparos

        def disparar(self):  # Permite disparar al ovni
            laserovni = Laserjefe(self.rect.x + 90, self.rect.bottom - 30)
            laserdeljefe.add(laserovni)

    class Luna(pygame.sprite.Sprite):  # Clase del ultimo jefe
        def __init__(self):
            super().__init__()
            self.image = pygame.transform.scale(lunaimagen, (100, 100))
            self.image.set_colorkey((247, 247, 247))
            self.salud = 50
            self.rect = self.image.get_rect()
            self.rect.y = 50
            self.rect.x = 325
            self.derecha = True
            self.izquierda = False
            self.velocidadx = 4
            self.velocidady = 0
            self.disparo = True
            self.desactivardisparo = True  # Desactiva el disparo al embestir
            self.embestir = True
            self.enfriamientoD = 100  # Enfriamiento entre disparos
            self.enfriamientoE = 6000  # Enfriamiento entre embestidas
            self.rafaga = 1000  # Enfriamiento entre rafagas
            self.ultimarafaga = 0  # Tiempo desde la ultima rafaga
            self.ultimodisparo = 0  # Tiempo desde el ultio disparo
            self.ultimaembestida = 0  # Tiempo desde la ultima embestida
            self.contador = 0
            self.contadorE = 0  # Contador de embestidas
            self.azar = 0  # Nùmero al azar para decidir las embestidas

        def update(self):
            tiempoactual = pygame.time.get_ticks()
            self.rect.y += self.velocidady
            if self.derecha:
                self.rect.x += self.velocidadx
            if self.izquierda:
                self.rect.x -= self.velocidadx
            if self.rect.right > 650:
                self.derecha = False
                self.izquierda = True
            if 0 > self.rect.left:
                self.derecha = True
                self.izquierda = False
            if tiempoactual - self.ultimarafaga > self.rafaga and \
                    self.desactivardisparo:
                self.disparo = True
                self.ultimarafaga = tiempoactual
            if tiempoactual - self.ultimodisparo > self.enfriamientoD and \
                    self.disparo:
                luna.disparar()
                self.contador += 1
                self.ultimodisparo = tiempoactual
                sonidolaser.play()
                if self.contador > 2:
                    self.disparo = False
                    self.contador = 0
            if tiempoactual - self.ultimaembestida > self.enfriamientoE and \
                    self.embestir:
                self.desactivardisparo = False
                self.embestir = False
                self.velocidadx = 0
                self.velocidady = 18
                self.rect.y += self.velocidady
                # Genera el numero random para determinar la embestida
                self.azar = random.randrange(0, 11)
                self.ultimaembestida = tiempoactual
            # Si azar es par realiza una embestida
            if self.rect.top > 660 and self.azar % 2 == 0:
                self.rect.y = 50
            # Si azar es impar realiza dos embestidas
            if self.rect.top > 660 and self.azar % 2 != 0:
                self.rect.y = 51
                # Posición en x aletoria para la segunda embestida
                self.rect.x = random.randrange(20, 550, 50)
                self.contadorE += 1
                # Si se hacen 2 embestidas, para de embestir
                if self.contadorE > 1:
                    self.rect.y = 50
                    self.contadorE = 0  # Reinica el contador de embestidas
            # Al volver a la parte superior retoma el movimiento es x
            if self.rect.y == 50:
                self.velocidady = 0
                self.velocidadx = 4
                self.embestir = True
                self.desactivardisparo = True

        def disparar(self):
            laserluna = Laserjefe(self.rect.x + 50, self.rect.bottom - 30)
            laserdeljefe.add(laserluna)

    class Laser(pygame.sprite.Sprite):  # Clase para los disaparos del jugador
        def __init__(self, x, y):
            super().__init__()
            # Imagen del laser
            self.image = pygame.transform.scale(laser_imagen, (30, 30))
            self.rect = self.image.get_rect()
            self.rect.bottom = y
            self.rect.centerx = x

        def update(self):
            self.rect.y -= 10
            if self.rect.bottom == 0:
                # Al llegar a la parte superior de la pantalla se borran
                self.kill()

    class Laserjefe(pygame.sprite.Sprite):  # Clase para los laseres del jefe
        def __init__(self, x, y):
            super().__init__()
            self.image = pygame.transform.scale(laserjefeimagen, (60, 30))
            self.rect = self.image.get_rect()
            self.rect.top = y
            self.rect.centerx = x

        def update(self):
            self.rect.y += 8
            if self.rect.bottom == 650:
                self.kill()

    # Función para excribir texto en pantalla
    def muestra_texto(pantalla, fuente, texto, dimensiones, x, y):
        # Fuenta a utilizar y las dimensiones de la misma
        tipoletra = pygame.font.Font(fuente, dimensiones)
        # Contenido y color del texto
        formato = tipoletra.render(texto, True, (0, 255, 0))
        # Obtiene el rectangulo donde se escribe le texto
        rectangulo = formato.get_rect()
        rectangulo.center = (x, y)  # Posición del mensaje
        pantalla.blit(formato, rectangulo)

    # Sprites del jugador
    sprites = pygame.sprite.Group()
    jugador = Jugador()  # Genera el jugador
    sprites.add(jugador)
    # Sprite de los disparos
    disparos = pygame.sprite.Group()
    # Sprite de los disparos del jefe
    laserdeljefe = pygame.sprite.Group()

    E1 = Enemigo1()  # Genera el primer enemigo
    enemy1 = pygame.sprite.Group()

    ovni = OVNI()  # Genera el segundo jefe
    jefe2 = pygame.sprite.Group()

    E2 = Enemigo2()  # Genera el segundo enemigo
    enemy2 = pygame.sprite.Group()

    luna = Luna()  # Genera el ultimo jefe
    jefefinal = pygame.sprite.Group()

    while abrir:  # Bucle principal del juego
        teclas = pygame.key.get_pressed()
        juego.blit(fondojuego, (0, 0))  # Añade el fondo al juego
        Reloj.tick(fps)  # administra los fps
        # Añade los datos a la pantalla del juego
        muestra_texto(juego, fuenteletra,
                      ("tiempo:{}".format(segundo)),
                      15, 50, 20)
        muestra_texto(juego, fuenteletra,
                      ("vida:{}".format(jugador.salud)),
                      15, 325, 20)
        for event in pygame.event.get():
            # Si se presiona la x o la tecla ESC se cierra el juego
            if event.type == pygame.QUIT or teclas[pygame.K_ESCAPE]:
                abrir = False
        # Actualiza los diferentes grupos de sprites
        sprites.update()
        enemy1.update()
        jefe2.update()
        enemy2.update()
        jefefinal.update()
        disparos.update()
        laserdeljefe.update()
        # Dibuja en pantalla los sprites
        sprites.draw(juego)
        enemy1.draw(juego)
        jefe2.draw(juego)
        enemy2.draw(juego)
        jefefinal.draw(juego)
        disparos.draw(juego)
        laserdeljefe.draw(juego)
        # Colisiones del juego
        impactosenemigo1 = pygame.sprite.groupcollide(
            enemy1, disparos, False, True)
        impactosnave_enemigo1 = pygame.sprite.spritecollide(
            jugador, enemy1, False)
        impactosonvi = pygame.sprite.groupcollide(
            jefe2, disparos, False, True)
        impactoslaser = pygame.sprite.groupcollide(
            sprites, laserdeljefe, False, True)
        impactosenemigo2 = pygame.sprite.groupcollide(
            enemy2, disparos, False, True)
        impactosnave_enemigo2 = pygame.sprite.spritecollide(
            jugador, enemy2, False)
        impactosluna = pygame.sprite.groupcollide(
            jefefinal, disparos, False, True)
        impactosnave_luna = pygame.sprite.spritecollide(
            jugador, jefefinal, False)
        tiempoinvencible = pygame.time.get_ticks()

        # Si se colisiona con el enemigo1 y no se es invencible
        if impactosnave_enemigo1 and \
                tiempoinvencible - jugador.ultimogolpe > jugador.invencible:
            jugador.salud -= 10
            jugador.ultimogolpe = tiempoinvencible

        if impactosenemigo1:  # Si se golpea al enemigo 1
            E1.salud -= 1
            golpe.play()

        if impactoslaser:  # Si el jugador es golpeado por el lase del jefe
            jugador.salud -= 3

        if impactosonvi:  # Si el jefe es golpeado por el jugador
            ovni.salud -= 1
            golpe.play()

        # Si se colisiona con el enemigo2 y no se es invecible
        if impactosnave_enemigo2 and \
                tiempoinvencible - jugador.ultimogolpe > jugador.invencible:
            jugador.salud -= 20
            jugador.ultimogolpe = tiempoinvencible

        if impactosenemigo2:  # Si se golpea al enemigo2
            E2.salud -= 1
            golpe.play()

        # Si el jefe final golpea al jugador y el jugador no es invencible
        if impactosnave_luna and \
                tiempoinvencible - jugador.ultimogolpe > jugador.invencible:
            jugador.salud -= 10
            jugador.ultimogolpe = tiempoinvencible

        if impactosluna:  # Si el laser del jugador golpea el jefe final
            luna.salud -= 1
            golpe.play()

        if E1.salud != 0:  # Si el jefe 1 esta vivo
            enemy1.add(E1)
            muestra_texto(juego, fuenteletra, ("Nivel 1"), 15, 425, 20)
        if 0 >= E1.salud:  # Al morir el jefe 1
            E1.kill()

        # Generar al jefe2 al morir el enemigo1
        if 0 >= E1.salud and ovni.salud != 0:
            jefe2.add(ovni)

        if 0 >= ovni.salud:  # Al morir el jefe 2
            ovni.kill()
            if b:
                curar = (50 - jugador.salud)
                jugador.salud += curar
            b = False  # Desactiva la cura

        # Generar al enemigo2 al morir el jefe 2
        if 0 >= ovni.salud and E2.salud != 0:
            enemy2.add(E2)
            muestra_texto(juego, fuenteletra, ("Nivel 2"), 15, 425, 20)
        if 0 >= E2.salud:  # Al morir el enemigo2
            E2.kill()

        # Generear al jefe final al morir el jefe 2
        if 0 >= E2.salud and luna.salud != 0:
            jefefinal.add(luna)
        if 0 >= luna.salud:  # Al morir el jefe final
            luna.kill()
            # Texto al ganar el juego
            muestra_texto(juego, fuenteletra, ("Bien,"
                                               "pero aún se siente el mal"
                                               "..."), 50, 325, 325)
        if 0 >= jugador.salud:  # Si el jugador muere
            jugador.kill()
            # Texto al perder el juego
            muestra_texto(juego, fuenteletra, ("Gameover"), 50, 325, 325)

        # Reloj
        i = 1  # Contador para los segundos
        segundo = (pygame.time.get_ticks() // 1000)
        if i == segundo:
            i += 1
        # Actualiza la pantalla
        pygame.display.update()
    pygame.quit()
    # Regresa a la ventana principal
    ventana.state(newstate="normal")


ventana.mainloop()
