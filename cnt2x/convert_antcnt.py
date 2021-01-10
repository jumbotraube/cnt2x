import numpy as np
import libeep
import os
import scipy.io
import sys

def load(filename):
    print("Loading " + filename)
    cnt = libeep.read_cnt(filename)

    n_chan = cnt.get_channel_count()
    n_times = cnt.get_sample_count()
    data = np.empty((n_chan+1, n_times), dtype=np.double)
    x = np.asarray(cnt.get_samples(0,n_times))
    x.shape  = (n_times,n_chan) 
    data[:-1] = x.transpose()

    data_dict = {
        'data': data, 
        'fs': cnt.get_sample_frequency(),
        'trigger_names': [cnt.get_trigger(t)[0] for t in range(cnt.get_trigger_count())],
        'trigger_values': [cnt.get_trigger(t)[1] for t in range(cnt.get_trigger_count())]
    }

    return data_dict

def write_csv(data_dict, filename):
    print("Writing " + filename + '.csv')
    header = "sampling_frequency={}".format(data_dict['fs'])
    np.savetxt(filename + '.csv', data_dict['data'], delimiter=',', header=header)

def write_pyc(data_dict, filename):
    print("Writing " + filename + '.pyc')
    np.save(filename, data_dict['data'], allow_pickle=False)

def write_mat(data_dict, filename):
    print("Writing " + filename + '.mat')
    scipy.io.savemat(filename, data_dict, do_compression=True)

if __name__ == "__main__":
    infile = sys.argv[1]
    head, tail = os.path.split(infile)
    filename, extension = os.path.splitext(os.path.basename(tail))
    if os.path.isfile(infile) and extension == '.cnt':
        if os.path.isfile(filename + '.csv') or os.path.isfile(filename + '.mat') or os.path.isfile(filename + '.npy'):
            print('File "{}" exists already with extension .csv, .mat or .npy! Remove manually, will not overwrite.'.format(filename))
        else:
            data = load(infile)
            write_csv(data, os.path.join(head, filename))
            write_pyc(data, os.path.join(head, filename))
            write_mat(data, os.path.join(head, filename))
    else:
        print("File {} does not exist or is not a cnt file! Aborting.".format(infile))