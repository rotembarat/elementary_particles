from tablib.core import Dataset
from gimel_session import GimelSession
from gimel_parser import parse
import math as m
import matplotlib.pyplot as plt
import subprocess as sp


USER_NAME = input('Username: ')
PASSWORD = input('Password: ')
SESSION_FILE = 'pi0.txt'
RAW_OUTPUT = 'pi0_raw.xlsx'

# Momentum of the parent particle GeV/c
momentum = input("Parent particle's momentum (GeV/c): ")
momentum = int(momentum)

# Amount of events
times = input("Amount of injections desired: ")
times = int(times)

number_of_decays = 0
event_id = 0
progress = 0


if __name__ == '__main__':
    with GimelSession(user=USER_NAME, password=PASSWORD, output_file=SESSION_FILE) as g:
        g.start_gimmel()

        #  Insert the name of the particle here:
        g.send_particle_in_bulk('pi-0', momentum, times)
    with open(SESSION_FILE) as f:
        text = f.read()
    events = parse(text)
    raw = Dataset()

    raw.headers = ('Event ID','P Parent Particle',
                    'Cluster1 y', 'Cluster1 z', 'Pulse Height 1',
                    'Cluster2 y', 'Cluster2 z', 'Pulse Height 2')

    for event in events:
        sp.call('cls',shell=True)
        event_id += 1
        progress = int(100*event_id/times)
        print('Processing..', str(progress)+'% completed.')

        if len(event.raw.strip()) == 0:
            event_id -= 1

#        elif len(event.calorimeter.clusters.clusters) == 1 and len(event.tracks.tracks) == 0:
#            number_of_decays += 1

        elif len(event.calorimeter.clusters.clusters) == 2 and len(event.tracks.tracks) == 0:

            row_raw = []
            row_raw.append(number_of_decays + 1)
            row_raw.append(momentum)

            y1 = event.calorimeter.clusters.clusters[0].y.value
            z1 = event.calorimeter.clusters.clusters[0].z.value
            y2 = event.calorimeter.clusters.clusters[1].y.value
            z2 = event.calorimeter.clusters.clusters[1].z.value
            ph1 = event.calorimeter.clusters.clusters[0].pulse_height
            ph2 = event.calorimeter.clusters.clusters[1].pulse_height

            row_raw.append(y1)
            row_raw.append(z1)
            row_raw.append(ph1)
            row_raw.append(y2)
            row_raw.append(z2)
            row_raw.append(ph2)

            raw.append(row_raw)
            number_of_decays += 1

        with open(RAW_OUTPUT, 'wb') as f:
            f.write(raw.export('xlsx'))

    if (progress < 98):
        print('Something went wrong. Please run the program again.')
    else:
        print('Execution completed.')
        print(event_id, 'event(s) were simulated.')
        print('There were', number_of_decays, 'interesting events out of', event_id, 'events.')
