#!/home/gustavo/Documentos/phisics/.venv/bin/python3
import pygame
from numpy import array, add
from pandas import read_csv
from math import sqrt

WINDOW_SIZE = array((1900, 1000))
ZOOM = 14
SHOW_ENERGY_LOST = False
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

    def destroied(self, obj, objects_in_scene: list):
        objects_distance = distance(self.position, obj.position)
        if self.radius + obj.radius > objects_distance:
            self.position += (self.radius + obj.radius)/2 * (obj.position - self.position)/objects_distance
            self.radius = sqrt(self.radius**2 + obj.radius**2)
            self.color = add(self.color, obj.color)
            self.color = tuple(map(lambda x: min(x, 255), self.color))
            self.velocity = (self.mass*self.velocity + obj.mass*obj.velocity)/(self.mass + obj.mass)
            self.mass += obj.mass
            objects_in_scene.remove(obj)


    def do_gravity(self, objects_in_scene, before_update):
        g_force = 0
        for index, obj in enumerate(objects_in_scene):
            if not obj is self:
                distance_between_objects = distance(self.position, before_update[index])
                if distance_between_objects != 0:
                    g_force -=  (self.position - before_update[index]) * GRAVITACIONAL_CONST * obj.mass / distance_between_objects**3
                self.destroied(obj, objects_in_scene)
        self.velocity += g_force
        self.position += self.velocity

    def draw(self, screen_ajuster: ScreenAjuster):
        pygame.draw.circle(window, self.color, WINDOW_SIZE//2 + (self.position - screen_ajuster.center_of_mass)//ZOOM, self.radius//ZOOM, 170, 0)


def get_energy(objects_in_scene):
    systems_energy = 0
    for position_on_the_list, obj in enumerate(objects_in_scene):
        systems_energy += obj.mass * (obj.velocity[0]**2 + obj.velocity[1]**2)/2
        for i in range(position_on_the_list+1, len(objects_in_scene)):
            interacting_object = objects_in_scene[i]
            if not obj is interacting_object:
                systems_energy -= GRAVITACIONAL_CONST * obj.mass * interacting_object.mass / distance(obj.position, interacting_object.position)
    return systems_energy


def draw(screen_ajuster: ScreenAjuster, objects_in_scene: list[Object]):
    window.fill((0, 0, 0))
    for obj in objects_in_scene:
        obj.draw(screen_ajuster)
    pygame.display.update()


def update(screen_ajuster: ScreenAjuster, objects_in_scene: list[Object], systems_energy):
    center_of_mass_numerator = 0
    systems_mass = 0

    before_update = list(map(lambda x: x.position, objects_in_scene))
    for obj in objects_in_scene:
        obj.do_gravity(objects_in_scene, before_update)

    for obj in objects_in_scene:
        center_of_mass_numerator += obj.mass*obj.position
        systems_mass += obj.mass

    if not systems_energy is None:
        new_systems_energy = get_energy(objects_in_scene)
        if systems_energy != new_systems_energy:
            print(f'ERROR! Energy not preserved, the energy lost is {-new_systems_energy + systems_energy}')

    if len(objects_in_scene) > 1:
        screen_ajuster.center_of_mass = center_of_mass_numerator/systems_mass


def main():
    pygame.init()

    screen_ajuster = ScreenAjuster()

    objects_in_scene = []
    objects_in_csv = read_csv('config.csv').values
    for object in objects_in_csv:
        objects_in_scene.append(Object(float(object[0]), pygame.Color(object[6])[:3], array((float(object[1]), float(object[2]))), array((float(object[3]), float(object[4]))), mass=float(object[5])))

    # Another cool config:
    #objects_in_scene.append(Object(5, (255, 0, 0), array((-2000., 700.)), array((-.5, -1.)), mass=10))
    #objects_in_scene.append(Object(5, (255, 0, 0), array((0., 0.)), mass=1000))
    #objects_in_scene.append(Object(5, (255, 0, 0), array((3000., 500.)), array((.0, 1)), mass=1))

    systems_energy = get_energy(objects_in_scene) if SHOW_ENERGY_LOST else None

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        update(screen_ajuster, objects_in_scene, systems_energy)
        draw(screen_ajuster, objects_in_scene)
    pygame.quit()


main()
