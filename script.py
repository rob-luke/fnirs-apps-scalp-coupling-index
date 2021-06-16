import numpy as np
import pandas as pd
import mne
import mne_bids
import mne_nirs
import argparse
from mne_bids import BIDSPath, read_raw_bids


print(mne.sys_info())

parser = argparse.ArgumentParser(description='Scalp coupling index')
parser.add_argument('threshold', type=float, help='threshold below which a channel is marked as bad', default=0.7)

args = parser.parse_args()
print(args)

# mne_bids.print_dir_tree("/data")

ids = range(1, 6)
task = "tapping"
for id in ids:
    bids_path = BIDSPath(subject='%02d' % id, task=task,
                         root="/bids_dataset",
                         datatype="nirs", suffix="nirs", extension=".snirf")
    raw = read_raw_bids(bids_path, verbose=True)
    raw = mne.preprocessing.nirs.optical_density(raw)
    sci = mne.preprocessing.nirs.scalp_coupling_index(raw)
    fname_chan = bids_path.update(suffix='channels', extension='.tsv').fpath
    chans = pd.read_csv(fname_chan, sep='\t')
    for idx in range(len(raw.ch_names)):
        assert raw.ch_names[idx] == chans["name"][idx]
    chans["SCI"] = sci
    chans["status"] = sci > args.threshold
    chans.to_csv(fname_chan, sep='\t', index=False)

