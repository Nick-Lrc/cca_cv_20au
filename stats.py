import numpy as np
import os

input_dir = 'result'
log_file = os.path.join(input_dir, 'log.txt')
label_file = os.path.join(input_dir, 'label.txt')
log = open(log_file, 'r')
labels = open(label_file, 'r')

sim = []
dis = []
for entry, label in zip(log, labels):
    entry = entry.strip().split(',')[2:]
    label = int(label.strip())
    if label == 1:
        sim.append(entry)
    else:
        dis.append(entry)

sim = np.array(sim).astype(float)
sim_means = np.mean(sim, axis=0)
sim_stds = np.std(sim, axis=0)
print(f'# similar  pairs: {len(sim)}')
print(f'Means           : {sim_means}')
print(f'Stds            : {sim_stds}')
print(f'Delta Means     : {(sim_means - sim_means[0]) / sim_means[0]}')
print(f'Delta Stds      : {(sim_stds - sim_stds[0]) / sim_stds[0]}')
print()

dis = np.array(dis).astype(float)
dis_means = np.mean(dis, axis=0)
dis_stds = np.std(dis, axis=0)
print(f'# distinct pairs: {len(dis)}')
print(f'Means           : {dis_means}')
print(f'Stds            : {dis_stds}')
print(f'Delta Means     : {(dis_means - dis_means[0]) / dis_means[0]}')
print(f'Delta Stds      : {(dis_stds - dis_stds[0]) / dis_stds[0]}')
