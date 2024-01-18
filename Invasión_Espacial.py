import pygame
import random
import math
from pygame import mixer
import io
# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


#def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    #print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
#if __name__ == '__main__':
 #   print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

pygame.init()

pantalla = pygame.display.set_mode((800,600))

#Titulo e icono
pygame.display.set_caption("Invasión Espacial")
icono = pygame.image.load("ovni.png")
fondo = pygame.image.load("fondo.png")
pygame.display.set_icon(icono)

#Agregar musica
mixer.music.load("fondo.mp3")
mixer.music.set_volume(0.2)
mixer.music.play(-1)

#variables del Jugador
img_jugador = pygame.image.load("cohete.png")
jugador_x = 368
jugador_y = 500
jugador_x_cambio = 0


#variables del enemigo
img_enemigo = []
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 8

for e in range(cantidad_enemigos):
    img_enemigo.append(pygame.image.load("enemigo.png"))
    enemigo_x.append(random.randint(0, 736))
    enemigo_y.append(random.randint(50, 200))
    enemigo_x_cambio.append(1)
    enemigo_y_cambio.append(50)

#variables de la bala
img_bala = pygame.image.load("bala.png")
balas = []
bala_x = 0
bala_y = 500
bala_x_cambio = 0
bala_y_cambio = 10
bala_visible = False

#Puntaje
puntaje = 0
texto_x = 10
texto_y = 10


def fuente_bytes(fuente):
    with open(fuente,"rb") as f:
        ttf_bytes = f.read()
    return io.BytesIO(ttf_bytes)


fuente_como_bytes = fuente_bytes("freesansbold.ttf")


fuente = pygame.font.Font(fuente_como_bytes,32)

#Texto fional juego
fuente_final = pygame.font.Font(fuente_como_bytes,50)

def texto_final():
    mi_fuente_final = fuente_final.render("JUEGO TERMINADO", True,(255,255,255))
    pantalla.blit(mi_fuente_final,(60,200))
#Función mostrar puntaje
def mostrar_puntaje(x,y):
    texto = fuente.render(f"Puntos: {puntaje}", True, (255,255,255))
    pantalla.blit(texto,(x,y))

#Función jugador
def jugador(x,y):
    pantalla.blit(img_jugador,(x,y))



def enemigo(x,y,ene):
    pantalla.blit(img_enemigo[ene],(x,y))

#Función disparar bala
def dispara_bala(x,y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala,(x + 16, y + 10))

#Función detectar colisiones
def hay_colision(x_1,y_1,x_2,y_2):
    distancia = math.sqrt(math.pow(x_1-x_2,2)+ math.pow(y_2-y_1,2))
    if distancia < 27:
        return True
    else:
        return False


#Loop del juego
se_ejecuta = True

while se_ejecuta:

    #RGB
    #pantalla.fill((200, 144, 228))

    #fondo
    pantalla.blit(fondo,(0, 0))


    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            se_ejecuta = False
        #evento presionar teclas
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                jugador_x_cambio = -3

            if evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 3

            if evento.key == pygame.K_SPACE:
                sonido_bala = mixer.Sound("disparo.mp3")
                sonido_bala.set_volume(0.1)
                sonido_bala.play()
                nueva_bala = {
                    "x": jugador_x,
                    "y": jugador_y,
                    "velocidad": -5
                }
                balas.append(nueva_bala)
                #if not bala_visible:
                   # bala_x = jugador_x
                    #dispara_bala(bala_x,bala_y)
            # Movimiento bala
        for bala in balas:
            bala["y"] += bala["velocidad"]
            pantalla.blit(img_bala, (bala["x"] + 16, bala["y"] + 10))
            if bala["y"] < 0:
                balas.remove(bala)
        for bala in balas:
            bala["y"] += bala["velocidad"]
            pantalla.blit(img_bala, (bala["x"] + 16, bala["y"] + 10))
            if bala["y"] < 0:
                balas.remove(bala)

        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0

    #Modificar ubicación del jugador
    jugador_x += jugador_x_cambio
    enemigo_x += enemigo_x_cambio

    # Mantener limites del jugador
    if jugador_x <= 0:
        jugador_x = 0
    elif jugador_x >= 736:
        jugador_x = 736

    # Modificar ubicación del enemigo
    for e in range(cantidad_enemigos):

        #Fin del juego
        if enemigo_y[e] > 500:
            for k in range(cantidad_enemigos):
                enemigo_y[k] = 1000
            texto_final()
            break

        enemigo_x[e] += enemigo_x_cambio[e]


        # Mantener limites del enemigo
        if enemigo_x[e] <= 0:
            enemigo_x_cambio[e] = 1
            enemigo_y[e] += enemigo_y_cambio[e]
        elif enemigo_x[e] >= 736:
            enemigo_x_cambio[e] = -1
            enemigo_y[e] += enemigo_y_cambio[e]

        # colision
        colision = hay_colision(enemigo_x[e], enemigo_y[e], bala_x, bala_y)
        if colision:
            sonido_colision = mixer.Sound("golpe.mp3")
            sonido_colision.play()
            bala_y = 500
            bala_visible = False
            puntaje += 1
            enemigo_x[e] = random.randint(0, 736)
            enemigo_y[e] = random.randint(50, 200)

        for bala in balas:
            colision_bala_enemigo = hay_colision(enemigo_x[e], enemigo_y[e], bala["x"], bala["y"])
            if colision_bala_enemigo:
                sonido_colision = mixer.Sound("Golpe.mp3")
                sonido_colision.play()
                balas.remove(bala)
                puntaje += 1
                enemigo_x[e] = random.randint(0, 736)
                enemigo_y[e] = random.randint(20, 200)
                break
        enemigo(enemigo_x[e], enemigo_y[e], e)

    #Movimiento bala
    if bala_y <= -64:
        bala_y = 500
        bala_visible = False


    if bala_visible:
        dispara_bala(bala_x, bala_y)
        bala_y -= bala_y_cambio


    jugador(jugador_x,jugador_y)
    mostrar_puntaje(texto_x,texto_y)
    pygame.display.update()


