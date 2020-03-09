from tablib.core import Dataset
from gimel_session import GimelSession
from gimel_parser import parse


USER_NAME = input('Username: ')
PASSWORD = input('Password: ')
SESSION_FILE = 'calibration.txt'
EXEL_OUTPUT = 'calibration_stats.xlsx'

# Choose the particle type
particle = input('Particle type (see README.txt): ')

# Momentum of the parent particle GeV/c
min_momentum = input("Particle's momentum (GeV/c): ")
min_momentum = int(momentum)

# Step size
step_size = input("Step size (GeV/c): ")
step_size = int(step_size)

# Amount of events
number_of_injections = input("Amount of injections desired: ")
number_of_injections = int(times)



if __name__ == '__main__':
    with GimelSession(user=USER_NAME, password=PASSWORD, output_file=SESSION_FILE) as g:
        g.start_gimmel()

        g.send_particles_ascending_energies(particle, min_momentum, step_size, number_of_injections)
    with open(SESSION_FILE) as f:
        text = f.read()
    events = parse(text)
    dataset = Dataset()
    dataset.headers = ('P', 'Kappa', 'd Kappa', 'Calorimeter Pulse Hight')
    for event in events:
        row = []
        if len(event.tracks.tracks) != 0:
            row.append(event.energy)
            row.append(event.tracks.tracks[0].parameters.akappa)
            row.append(event.tracks.tracks[0].error_matrix['akappa']['akappa'])
            row.append(event.calorimeter.clusters.clusters[0].pulse_height)
            dataset.append(row)

    with open(EXEL_OUTPUT, 'wb') as f:
        f.write(dataset.export('xlsx'))
