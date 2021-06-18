# fNIRS App: Scalp Coupling Index 

[![build](https://github.com/rob-luke/fnirs-apps-scalp-coupling-index/actions/workflows/ghregistry.yml/badge.svg?branch=main)](https://github.com/rob-luke/fnirs-apps-scalp-coupling-index/actions/workflows/ghregistry.yml)

Portable fNIRS neuroimaging pipelines that work with BIDS datasets. See http://fnirs-apps.org

This app evaluates the channel quality of your data using the scalp coupling index metric.
The extrated metric is saved as a column in the `channels.tsv` BIDS file.
If a threshold is specified, then the status column in `channels.tsv` will also be set.

## Usage

```bash
docker run -v /path/to/data/:/bids_dataset ghcr.io/rob-luke/fnirs-apps-scalp-coupling-index/app
```

By default the app will process all subject and tasks.
You can modify the behaviour of the script using the options below.

## Arguments

|                   | Required | Default | Note                                                   |
|-------------------|----------|---------|--------------------------------------------------------|
| threshold         | optional | []      | If not present then the status column is not modified. |
| participant_label | optional | []      | Participants to process. Default is to process all.    |
| task_label        | optional | []      | Tasks to process. Default is to process all.           |


For example, to process only participant 6 you would run


```bash
docker run -v /path/to/data/:/bids_dataset ghcr.io/rob-luke/fnirs-apps-scalp-coupling-index/app --participant_label 06
```


## Updating

To update to the latest version run.

```bash
docker pull ghcr.io/rob-luke/fnirs-apps-scalp-coupling-index/app
```


Acknowledgements
----------------

This package uses MNE-Python, MNE-BIDS, and MNE-NIRS under the hood. Please cite those package accordingly.

MNE-Python: https://mne.tools/dev/overview/cite.html

MNE-BIDS: https://github.com/mne-tools/mne-bids#citing

MNE-NIRS: https://github.com/mne-tools/mne-nirs#acknowledgements
