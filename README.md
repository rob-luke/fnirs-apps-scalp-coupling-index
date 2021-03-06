# fNIRS App: Scalp Coupling Index 

![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/rob-luke/fnirs-apps-scalp-coupling-index?color=green&label=version&sort=semver)
[![build](https://github.com/rob-luke/fnirs-apps-scalp-coupling-index/actions/workflows/ghregistry.yml/badge.svg?branch=main)](https://github.com/rob-luke/fnirs-apps-scalp-coupling-index/actions/workflows/ghregistry.yml)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4999132.svg)](https://doi.org/10.5281/zenodo.4999132)


This [*fNIRS App*](http://fnirs-apps.org) will calculate the scalp coupling index for each channel in your BIDS dataset.

This app evaluates the channel quality of your data using the scalp coupling index metric.
The extracted metric is saved as a column in the `channels.tsv` BIDS file.
If a threshold is specified, then the status column in `channels.tsv` will also be set.
Additionally the peak power metric is extracted, and the average value across the measurement is stored per channel in the `channels.tsv` BIDS file.

If you prefer a visual report of the data quality see: [fNIRS App: Quality Reports](https://github.com/rob-luke/fnirs-apps-quality-reports)

**Feedback is welcome!!** Please let me know your experience with this app by raising an issue.  


The metrics computed in this program are from the following manuscripts. Please cite these accordingly:

* Pollonini L et al., “PHOEBE: a method for real time mapping of
  optodes-scalp coupling in functional near-infrared spectroscopy” in
  Biomed. Opt. Express 7, 5104-5119 (2016).
* Hernandez, Samuel Montero, and Luca Pollonini. "NIRSplot: a tool for
  quality assessment of fNIRS scans." Optics and the Brain.
  Optical Society of America, 2020.


## Usage

To run the app you must have [docker installed](https://docs.docker.com/get-docker/). See here for details about [installing fNIRS Apps](http://fnirs-apps.org/overview//). You do NOT need to have MATLAB or python installed, and you do not need any scripts. See this [tutorial for an introduction to fNIRS Apps](http://fnirs-apps.org/tutorial/).

To run the app you must inform it where the `bids_dataset` resides.
This is done by passing the location of the dataset using the `-v` command to the app.
To run this app use the command:

```bash
docker run -v /path/to/data/:/bids_dataset ghcr.io/rob-luke/fnirs-apps-scalp-coupling-index/app
```

You can also specify additional parameters by passing arguments to the app. A complete list of arguments is provided below.
A more complete example that only runs on participant 6 and also specifies a threshold, below which channels are marked as bad, can be set as:

```bash
docker run -v /path/to/data/:/bids_dataset ghcr.io/rob-luke/fnirs-apps-scalp-coupling-index/app \
  --threshold 0.7 \
  --subject-label 06
```

## Arguments

|                   | Required | Default | Note                                                   |
|-------------------|----------|---------|--------------------------------------------------------|
| threshold         | optional | []      | If not present then the status column is not modified. |
| subject-label     | optional | []      | Subjects to process. Default is to process all.        |
| task-label        | optional | []      | Tasks to process. Default is to process all.           |
| h-freq            | optional | 1.5     | High frequency limit for metrics (Hz).                 |
| h-trans-bandwidth | optional | 0.3     | Width of the high frequency transition band (Hz).      |

For arguments `h-freq` and `h-trans-bandwidth` detailed explanations can be found in the [MNE-NIRS documentation](https://mne.tools/mne-nirs/main/generated/mne.preprocessing.nirs.scalp_coupling_index.html#mne.preprocessing.nirs.scalp_coupling_index).


## Updating

To update to the latest version run.

```bash
docker pull ghcr.io/rob-luke/fnirs-apps-scalp-coupling-index/app
```

Or to run a specific version:

```bash
docker run -v /path/:/bids_dataset ghcr.io/rob-luke/fnirs-apps-scalp-coupling-index/app:v1.4.2
```

## Additional information

#### Boutiques

This app is [boutiques compatible](https://boutiques.github.io).
In addition to the methods described above, this app can also be run using [boutiques bosh command](https://boutiques.github.io/doc/index.html).
You can see an example usage of this app with boutiques at https://github.com/rob-luke/fnirs-apps-demo.



Acknowledgements
----------------

This app is directly based on BIDS Apps and BIDS Execution. Please cite those projects when using this app.

BIDS Apps: https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1005209

BIDS Execution: https://github.com/bids-standard/bids-specification/issues/313

This app uses MNE-Python, MNE-BIDS, and MNE-NIRS under the hood. Please cite those package accordingly.

MNE-Python: https://mne.tools/dev/overview/cite.html

MNE-BIDS: https://github.com/mne-tools/mne-bids#citing

MNE-NIRS: https://github.com/mne-tools/mne-nirs#acknowledgements
