# fNIRS App: Scalp Coupling Index 

[![build](https://github.com/rob-luke/fnirs-apps-scalp-coupling-index/actions/workflows/ghregistry.yml/badge.svg?branch=main)](https://github.com/rob-luke/fnirs-apps-scalp-coupling-index/actions/workflows/ghregistry.yml)

This [*fNIRS App*](http://fnirs-apps.org) will calculate the scalp coupling index for each channel in your BIDS dataset.

This app evaluates the channel quality of your data using the scalp coupling index metric.
The extracted metric is saved as a column in the `channels.tsv` BIDS file.
If a threshold is specified, then the status column in `channels.tsv` will also be set.

If you prefer a visual report of the data quality see: [fNIRS App: Quality Reports](https://github.com/rob-luke/fnirs-apps-quality-reports)

**Feedback is welcome!!** Please let me know your experience with this app by raising an issue.  

## Usage

To run the app you must have [docker installed](https://docs.docker.com/get-docker/). See here for details about [installing fNIRS Apps](http://fnirs-apps.org/details/). You do NOT need to have MATLAB or python installed, and you do not need any scripts.

To run the app you must inform it where the `bids_dataset` to be formatted resides.
This is done by passing the app the location of the dataset using the `-v` command.
To run this app use the command:

```bash
docker run -v /path/to/data/:/bids_dataset ghcr.io/rob-luke/fnirs-apps-scalp-coupling-index/app
```

You can also specify additional parameters by passing arguments to the app. A complete list of arguments is provided below.
A more complete example that only runs on participant 3 and also specifies a threshold, below which channels are marked as bad, can be set as:

```bash
docker run -v /path/to/data/:/bids_dataset ghcr.io/rob-luke/fnirs-apps-scalp-coupling-index/app \
  --threshold 0.7 \
  --participant_label 0.6
```

## Arguments

|                   | Required | Default | Note                                                   |
|-------------------|----------|---------|--------------------------------------------------------|
| threshold         | optional | []      | If not present then the status column is not modified. |
| participant_label | optional | []      | Participants to process. Default is to process all.    |
| task_label        | optional | []      | Tasks to process. Default is to process all.           |


## Updating

To update to the latest version run.

```bash
docker pull ghcr.io/rob-luke/fnirs-apps-scalp-coupling-index/app
```

Or to run a specific version:

```bash
docker run -v /path/:/bids_dataset ghcr.io/rob-luke/fnirs-apps-scalp-coupling-index/app:v1.4.2
```


Acknowledgements
----------------

This package uses MNE-Python, MNE-BIDS, and MNE-NIRS under the hood. Please cite those package accordingly.

MNE-Python: https://mne.tools/dev/overview/cite.html

MNE-BIDS: https://github.com/mne-tools/mne-bids#citing

MNE-NIRS: https://github.com/mne-tools/mne-nirs#acknowledgements
