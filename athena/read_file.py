import numpy as np
import sys
sys.path.append('/mnt/sw/nix/store/6plcgbnkn9w8nf1y0dzmjs1jbjbzi4ma-openvdb-10.0.0/lib64/python3.9/site-packages') # Put your path to openvdb here
### PUT THE athena_read.py in your path
import athena_read
import pyopenvdb as vdb

path = '/mnt/home/wwong/ceph/Simulations/Athena/blast3d/Blast.out1.'
#path = '/mnt/home/wwong/ceph/Simulations/Athena/collapse/Collapse.out2.'
output_name = '/mnt/home/wwong/ceph/Visualization/Tutorial/Athena/collapse'
N_res = 128
N_frames = 51

field = ['rho', 'press', 'vel1', 'vel2', 'vel3']
data = {}
for name in field:
	data[name] = []

for index in range(N_frames):
	data_prim = athena_read.athdf(path+str(index).zfill(5)+'.athdf')
	data['rho'].append(data_prim['rho']) # density at cell center
	data['press'].append(data_prim['press']) # pressure at cell center
	data['vel1'].append(data_prim['vel1']) # x velocity at cell center
	data['vel2'].append(data_prim['vel2']) # y velocity at cell center
	data['vel3'].append(data_prim['vel3']) # z velocity at cell center

for i in range(len(data['rho'])):
	dataCube = []

	for name in field:
		dataCube.append(vdb.FloatGrid())
		dataCube[-1].copyFromArray(data[name][i])
		dataCube[-1].name = name
		dataCube[-1].transform = vdb.createLinearTransform(voxelSize=1/(N_res))
		vdb.write(output_name+'_'+str(i)+'.vdb', grids=dataCube)
