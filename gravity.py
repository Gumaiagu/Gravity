#!/home/gustavo/Documentos/phisics/.venv/bin/python3
import pygame
from numpy import array, add
from math import sqrt

WINDOW_SIZE = array((1900, 1000))
ZOOM = 5

GRAVITACIONAL_CONST = 10


window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Phisics")


def distance(pos1: array, pos2: array):
    return sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)


class ScreenAjuster:
    def __init__(self):
        self.center_of_mass = array((0, 0))


class Object:
    def __init__(self, radius: float, color: tuple[int, int, int], position: array, initial_velocity: array=None, mass: float = 1):
        self.position = position
        self.color = color
        self.radius = radius * ZOOM
        self.velocity: array = array((.0, .0)) if initial_velocity is None else initial_velocity
        self.mass = mass

    def destroied(self, obj, objs: list):
        objects_distance = distance(self.position, obj.position)
        if self.radius + obj.radius > objects_distance:
            self.position += (self.radius + obj.radius)/2 * (obj.position - self.position)/objects_distance
            self.radius = sqrt(self.radius**2 + obj.radius**2)
            self.color = array(add(self.color, obj.color))
            self.color = (1 if all(self.color >= 255) else 0) + self.color%255
            self.velocity = (self.mass*self.velocity + obj.mass*obj.velocity)/(self.mass + obj.mass)
            objs.remove(obj)


    def do_gravity(self, objs, before_update):
        g_force = 0
        for index, obj in enumerate(objs):
            if not obj is self:
                self.destroied(obj, objs)
                g_force -=  (self.position - before_update[index]) * GRAVITACIONAL_CONST * obj.mass/ distance(self.position, before_update[index])**3
        self.velocity += g_force
        self.position += self.velocity

    def draw(self, screen_ajuster: ScreenAjuster):
        pygame.draw.circle(window, self.color, WINDOW_SIZE/2 + (self.position - screen_ajuster.center_of_mass)/ZOOM, self.radius/ZOOM, 170, 0)


def get_energy(objs):
    systems_energy = 0
    for position_on_the_list, obj in enumerate(objs):
        systems_energy += obj.mass * (obj.velocity[0]**2 + obj.velocity[1]**2)/2
        for i in range(position_on_the_list+1, len(objs)):
            interacting_object = objs[i]
            if not obj is interacting_object:
                systems_energy -= GRAVITACIONAL_CONST * obj.mass * interacting_object.mass / distance(obj.position, interacting_object.position)
    return systems_energy


def draw(screen_ajuster: ScreenAjuster, objs: list[Object]):
    window.fill((0, 0, 0))
    for obj in objs:
        obj.draw(screen_ajuster)
    pygame.display.update()


def update(screen_ajuster: ScreenAjuster, objs: list[Object], systems_energy):
    n = 0
    d = 0
    before_update = list(map(lambda x: x.position, objs))
    for obj in objs:
        n += obj.mass*obj.position
        d += obj.mass
        obj.do_gravity(objs, before_update)
    if not systems_energy is None:
        new_systems_energy = get_energy(objs)
        if systems_energy != new_systems_energy:
            print(f'ERROR! Energy not preserved, the energy lost is {-new_systems_energy + systems_energy}')
    screen_ajuster.center_of_mass = n/d


def main():
    pygame.init()

    screen_ajuster = ScreenAjuster()

    objects_in_scene = []
    objects_in_scene.append(Object(5, (255, 0, 0), array((-2000., 700.)), array((.5, -.3)), mass=10))
    objects_in_scene.append(Object(5, (139, 93, 245), array((0., 0.)), mass=50))
    #objects_in_scene.append(Object(5, (255, 0, 0), array((-2000., 700.)), array((-.5, -1.)), mass=10))
    #objects_in_scene.append(Object(5, (255, 0, 0), array((0., 0.)), mass=1000))
    #objects_in_scene.append(Object(5, (255, 0, 0), array((3000., 500.)), array((.0, 1)), mass=1))

    systems_energy = None
    # Uncomment the next line if you want to see the energy lost
    #systems_energy = get_energy(objects_in_scene)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        update(screen_ajuster, objects_in_scene, systems_energy)
        draw(screen_ajuster, objects_in_scene)
    pygame.quit()


main()
