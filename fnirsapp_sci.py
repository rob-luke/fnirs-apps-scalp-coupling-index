#!/usr/bin/env python3
import pandas as pd
import numpy as np
import mne
import argparse
from mne_bids import BIDSPath, read_raw_bids, get_entity_vals
from mne_nirs.preprocessing import peak_power
from glob import glob
import os.path as op
import os
from pathlib import Path
import subprocess
from mne.utils import logger
from datetime import datetime
import json
import hashlib
from pprint import pprint

__version__ = "v0.3.4"


def run(command, env={}):
    merged_env = os.environ
    merged_env.update(env)
    process = subprocess.Popen(command, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT, shell=True,
                               env=merged_env)
    while True:
        line = process.stdout.readline()
        line = str(line, 'utf-8')[:-1]
        print(line)
        if line == '' and process.poll() != None:
            break
    if process.returncode != 0:
        raise Exception("Non zero return code: %d" % process.returncode)

parser = argparse.ArgumentParser(description='Scalp coupling index')
parser.add_argument('--input-datasets', default="/bids_dataset", type=str,
                    help='The directory with the input dataset '
                    'formatted according to the BIDS standard.')
parser.add_argument('--threshold', type=float, default=1.0,
                    help='Threshold below which a channel is marked as bad.')
parser.add_argument('--subject-label',
                    help='The label(s) of the participant(s) that should be '
                    'analyzed. The label corresponds to '
                    'sub-<subject-label> from the BIDS spec (so it does '
                    'not include "sub-"). If this parameter is not provided '
                    'all subjects should be analyzed. Multiple participants '
                    'can be specified with a space separated list.',
                    nargs="+")
parser.add_argument('--session-label',
                    help='The label(s) of the session(s) that should be '
                    'analyzed. The label corresponds to '
                    'ses-<session-label> from the BIDS spec (so it does '
                    'not include "ses-"). If this parameter is not provided '
                    'all sessions should be analyzed. Multiple sessions '
                    'can be specified with a space separated list.',
                    nargs="+")
parser.add_argument('--task-label',
                    help='The label(s) of the tasks(s) that should be '
                    'analyzed. If this parameter is not provided '
                    'all tasks should be analyzed. Multiple tasks '
                    'can be specified with a space separated list.',
                    nargs="+")
parser.add_argument('--h-freq', type=float, default=1.5,
                    help='High frequency limit for metrics.')
parser.add_argument('--h-trans-bandwidth', type=float, default=0.3,
                    help='High frequency width of the transition band.')
parser.add_argument('-v', '--version', action='version',
                    version='BIDS-App Scalp Coupling Index version '
                    f'{__version__}')
args = parser.parse_args()

def create_report(app_name=None, pargs=None):

    exec_rep = dict()
    exec_rep["ExecutionStart"] = datetime.now().isoformat()
    exec_rep["ApplicationName"] = app_name
    exec_rep["ApplicationVersion"] = __version__
    exec_rep["Arguments"] = vars(pargs)

    return exec_rep

exec_files = dict()
exec_rep =create_report(app_name="fNIRS-Apps: Scalp Coupling Index", pargs=args)

mne.set_log_level("INFO")
logger.info("\n")

########################################
# Extract parameters
########################################

if args.threshold == 1.0:
    print("No threshold was set, so the status column will not be modified")
else:
    print(f"Using specified threshold: {args.threshold}")

logger.info("Extracting subject metadata.")
subs = []
if args.subject_label:
    logger.info("    Subject data provided as input argument.")
    subs = args.subject_label
else:
    logger.info("    Subject data will be extracted from data.")
    subs = get_entity_vals(args.input_datasets, 'subject')
logger.info(f"        Subjects: {subs}")


logger.info("Extracting session metadata.")
sess = []
if args.session_label:
    logger.info("    Session data provided as input argument.")
    sess = args.session_label
else:
    logger.info("    Session data will be extracted from data.")
    sess = get_entity_vals(args.input_datasets, 'session')
if len(sess) == 0:
    sess = [None]
logger.info(f"        Sessions: {sess}")


logger.info("Extracting tasks metadata.")
tasks = []
if args.task_label:
    logger.info("    Task data provided as input argument.")
    tasks = args.task_label
else:
    logger.info("    Session data will be extracted from data.")
    tasks = get_entity_vals(args.input_datasets, 'task')
logger.info(f"        Tasks: {tasks}")


########################################
# Main script
########################################

logger.info(" ")

for sub in subs:
    for task in tasks:
        for ses in sess:

            logger.info(f"Processing: sub-{sub}/ses-{ses}/task-{task}")
            exec_files[f"sub-{sub}_ses-{ses}_task-{task}"] = dict()

            b_path = BIDSPath(subject=sub, task=task, session=ses,
                              root=f"{args.input_datasets}",
                              datatype="nirs", suffix="nirs",
                              extension=".snirf")
            try:
                exec_files[f"sub-{sub}_ses-{ses}_task-{task}"]["FileName"] = str(b_path.fpath)
                exec_files[f"sub-{sub}_ses-{ses}_task-{task}"]["FileHash"] = hashlib.md5(open(b_path.fpath, 'rb').read()).hexdigest()

                raw = read_raw_bids(b_path, verbose=True)
                raw = mne.preprocessing.nirs.optical_density(raw)

                sci = mne.preprocessing.nirs.scalp_coupling_index(raw, h_freq=args.h_freq, h_trans_bandwidth=args.h_trans_bandwidth)
                dist = mne.preprocessing.nirs.source_detector_distances(raw.info)
                _, pps, _ = peak_power(raw, h_freq=args.h_freq, h_trans_bandwidth=args.h_trans_bandwidth)
                pps = np.mean(pps, axis=1)

                fname_chan = b_path.update(suffix='channels',
                                           extension='.tsv').fpath
                chans = pd.read_csv(fname_chan, sep='\t')
                for idx in range(len(raw.ch_names)):
                    assert raw.ch_names[idx] == chans["name"][idx]
                chans["SCI"] = sci
                chans["SD_Distance"] = dist
                chans["PeakPower"] = pps
                if args.threshold < 1.0:
                    logger.info("    Setting status channel")
                    chans["status"] = sci > args.threshold
                chans.to_csv(fname_chan, sep='\t', index=False)
            except FileNotFoundError:
                print(f"Unable to process {b_path.fpath}")

exec_rep["Files"] = exec_files
exec_path = f"{args.input_datasets}/execution"
exec_rep["ExecutionEnd"] = datetime.now().isoformat()

Path(exec_path).mkdir(parents=True, exist_ok=True)
with open(f"{exec_path}/{exec_rep['ExecutionStart'].replace(':', '-')}-fnirsapp_sci.json", "w") as fp:
    json.dump(exec_rep, fp)

pprint(exec_rep)