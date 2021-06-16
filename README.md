# fNIRS App: Scalp Coupling Index

Portable fNIRS neuroimaging pipelines that work with BIDS datasets. See http://fnirs-apps.org

This app evaluates the channel quality of your data using the scalp coupling index metric.
The extrated metric is saved as a column in the `channels.tsv` BIDS file.
If a threshold is specified, then the status column in `channels.tsv` will also be set.

## Usage

```bash
docker run -v /path/to/data/:/bids_dataset ghcr.io/rob-luke/fnirs-apps-scalp-coupling-index/app
```


## Arguments

|           | Required | Default | Note                                                   |
|-----------|----------|---------|--------------------------------------------------------|
| threshold | optional | NA      | If not present then the status column is not modified. |
|           |          |         |                                                        |



Acknowledgements
----------------

This package uses MNE-Python, MNE-BIDS, and MNE-NIRS under the hood. Please cite those package accordingly.

MNE-Python: https://mne.tools/dev/overview/cite.html

MNE-BIDS: https://github.com/mne-tools/mne-bids#citing

MNE-NIRS: https://github.com/mne-tools/mne-nirs#acknowledgements
