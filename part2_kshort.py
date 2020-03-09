from tablib.core import Dataset
from gimel_session import GimelSession
from gimel_parser import parse
import math as m
import matplotlib.pyplot as plt
import subprocess as sp


USER_NAME = input('Username: ')
PASSWORD = input('Password: ')
SESSION_FILE = 'kappa.txt'
RAW_OUTPUT = 'kappa_raw.xlsx'

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
        g.send_particle_in_bulk('k-short', momentum, times)
    with open(SESSION_FILE) as f:
        text = f.read()
    events = parse(text)
    raw = Dataset()

    raw.headers = ('Event ID','P Parent Particle',
                    'Kappa1', 'd Kappa1', 'tandip1', 'd tandip1',
                    'Kappa2', 'd Kappa2', 'tandip2', 'd tandip2',
                    'Vertex x', 'd Vertex x', 'Vertex y', 'd Vertex y',
                    'Vertex z', 'd Vertex z', 'Phi', 'd Phi')

    for event in events:
        sp.call('cls',shell=True)
        event_id += 1
        progress = int(100*event_id/times)
        print('Processing..', str(progress)+'% completed.')

        if len(event.raw.strip()) == 0:
            event_id -= 1

        elif len(event.tracks.tracks) >= 2 and len(event.verteces.verteces) > 0:

            row_raw = []
            row_raw.append(number_of_decays + 1)
            row_raw.append(momentum)

            if event.verteces.verteces[0].phi < 0.01 and len(event.verteces.verteces) > 1:
                kappa1 = event.tracks.tracks[1].parameters.akappa
                dkappa1 = event.tracks.tracks[1].error_matrix['akappa']['akappa']
                tandip1 = event.tracks.tracks[1].parameters.tandip
                dtandip1 = event.tracks.tracks[1].error_matrix['tandip']['tandip']
                kappa2 = event.tracks.tracks[2].parameters.akappa
                dkappa2 = event.tracks.tracks[2].error_matrix['akappa']['akappa']
                tandip2 = event.tracks.tracks[2].parameters.tandip
                dtandip2 = event.tracks.tracks[2].error_matrix['tandip']['tandip']

                x = event.verteces.verteces[1].x
                dx = event.verteces.verteces[1].d_x
                y = event.verteces.verteces[1].y
                dy = event.verteces.verteces[1].d_y
                z = event.verteces.verteces[1].z
                dz = event.verteces.verteces[1].d_z
                phi = event.verteces.verteces[1].phi
                dphi = event.verteces.verteces[1].d_phi

            else:
                kappa1 = event.tracks.tracks[0].parameters.akappa
                dkappa1 = event.tracks.tracks[0].error_matrix['akappa']['akappa']
                tandip1 = event.tracks.tracks[0].parameters.tandip
                dtandip1 = event.tracks.tracks[0].error_matrix['tandip']['tandip']
                kappa2 = event.tracks.tracks[1].parameters.akappa
                dkappa2 = event.tracks.tracks[1].error_matrix['akappa']['akappa']
                tandip2 = event.tracks.tracks[1].parameters.tandip
                dtandip2 = event.tracks.tracks[1].error_matrix['tandip']['tandip']

                x = event.verteces.verteces[0].x
                dx = event.verteces.verteces[0].d_x
                y = event.verteces.verteces[0].y
                dy = event.verteces.verteces[0].d_y
                z = event.verteces.verteces[0].z
                dz = event.verteces.verteces[0].d_z
                phi = event.verteces.verteces[0].phi
                dphi = event.verteces.verteces[0].d_phi

            row_raw.append(kappa1)
            row_raw.append(dkappa1)
            row_raw.append(tandip1)
            row_raw.append(dtandip1)
            row_raw.append(kappa2)
            row_raw.append(dkappa2)
            row_raw.append(tandip2)
            row_raw.append(dtandip2)

            row_raw.append(x)
            row_raw.append(dx)
            row_raw.append(y)
            row_raw.append(dy)
            row_raw.append(z)
            row_raw.append(dz)
            row_raw.append(phi)
            row_raw.append(dphi)

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
