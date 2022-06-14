
import argparse
import carla
import random
import time
import numpy as np

class GbufferStream:
    def __init__(self, world_ref : carla.World, bp_tag : str, buf_opts: dict, callback):
        self.blueprint = world_ref.get_blueprint_library().find(bp_tag)
        for k, v in buf_opts.items():
            self.blueprint.set_attribute(k, v)
        self.callback = callback
        self.world_ref = world_ref

    def spawn(self, transform, attach_to):
        self.stream = self.world_ref.spawn_actor(self.blueprint, transform, attach_to = attach_to)
        self.stream.listen(self.callback)

    def set_attributes(options):
        for k, v in options.items():
            self.blueprint.set_attribute(k, v)

def collect_gbuffer(client):

    vehicle = None
    vehicle_list = []
    stream_list = []

    try:
        gbuffers = []
        # Getting the world and
        world = client.get_world()
        original_settings = world.get_settings()

        traffic_manager = client.get_trafficmanager(8000)
        settings = world.get_settings()
        traffic_manager.set_synchronous_mode(True)
        settings.synchronous_mode = True
        settings.fixed_delta_seconds = 0.05
        world.apply_settings(settings)

        # Instanciating the vehicle to which we attached the sensors
        bp = world.get_blueprint_library().filter('charger_2020')[0]
        vehicle = world.spawn_actor(bp, random.choice(world.get_map().get_spawn_points()))
        vehicle_list.append(vehicle)
        vehicle.set_autopilot(True)

        normal_buffer = GbufferStream(world, "camera.sensor.gbuffer", )

        while True:
            world.tick()

    finally:
        client.apply_batch([carla.command.DestroyActor(x) for x in vehicle_list])

        world.apply_settings(original_settings)



if __name__ == "__main__":

    argparser = argparse.ArgumentParser(
        description='Save Gbuffer from CarlaUE4')
    argparser.add_argument(
        '--host',
        metavar='H',
        default='127.0.0.1',
        help='IP of the host server (default: 127.0.0.1)')

    argparser.add_argument(
        '-p', '--port',
        metavar='P',
        default=2000,
        type=int,
        help='TCP port to listen to (default: 2000)')

    argparser.add_argument(
        '--res',
        metavar='WIDTHxHEIGHT',
        default='1280x720',
        help='window resolution (default: 1280x720)')

    args = argparser.parse_args()

    args.width, args.height = [int(x) for x in args.res.split('x')]

    try:
        client = carla.Client(args.host, args.port)
        client.set_timeout(5.0)
        collect_gbuffer(client)

    except KeyboardInterrupt:
        print('\nCancelled by user. Bye!')
    pass