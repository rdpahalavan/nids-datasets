# NIDS Datasets (nids-datasets)

The `nids-datasets` package is a Python-based toolkit developed to provide an efficient and seamless experience to researchers working with Network Intrusion Detection Systems (NIDS). Specifically, the package aids in downloading, managing, and interacting with popular NIDS datasets, namely UNSW-NB15 and CIC-IDS2017.

## Introduction

The field of cybersecurity has been continuously evolving and expanding, and one of its critical components is the detection and prevention of network intrusions. Network Intrusion Detection Systems (NIDS) are an essential part of this cyber defense infrastructure. They monitor network traffic for suspicious activities and issue alerts when such activities are discovered. 

To build and improve these systems, it's necessary to work with comprehensive datasets that capture different types of network traffic, including various kinds of attacks. The `nids-datasets` package provides an interface to interact with two of the most widely used datasets in this domain: UNSW-NB15 and CIC-IDS2017.

## Features

The package provides several features:

- Downloading datasets: `nids-datasets` allows for the easy download of large and complex datasets.
- Subsetting: You can choose to download specific parts (or "subsets") of the datasets.
- Parsing and reading data: The package provides utility functions for reading the downloaded datasets.
- Merging subsets: You can merge subsets into a single, comprehensive dataset for analysis.
- Byte extraction: You can extract and analyze byte sequences from the datasets.

## Installation

Install the `nids-datasets` package using pip:

```shell
pip install nids-datasets
```

Import the package in your Python script:

```python
from nids_datasets import Dataset, DatasetInfo
```

## Dataset Information

The `nids-datasets` package currently supports two datasets: UNSW-NB15 and CIC-IDS2017. Each of these datasets contains a mix of normal traffic and different types of attack traffic, which are identified by their respective labels. The UNSW-NB15 dataset has 10 unique class labels, and the CIC-IDS2017 dataset has 24 unique class labels. 

- UNSW-NB15 Labels: 'normal', 'exploits', 'dos', 'fuzzers', 'generic', 'reconnaissance', 'worms', 'shellcode', 'backdoor', 'analysis'
- CIC-IDS2017 Labels: 'BENIGN', 'FTP-Patator', 'SSH-Patator', 'DoS slowloris', 'DoS Slowhttptest', 'DoS Hulk', 'Heartbleed', 'Web Attack – Brute Force', 'Web Attack – XSS', 'Web Attack – SQL Injection', 'Infiltration', 'Bot', 'PortScan', 'DDoS', 'normal', 'exploits', 'dos', 'fuzzers', 'generic', 'reconnaissance', 'worms', 'shellcode', 'backdoor', 'analysis', 'DoS GoldenEye'

## Subsets of the Dataset

Each dataset consists of four subsets:

1. Network Flows - Contains flow-level data.
2. Packet Fields - Contains packet header information.
3. Packet Bytes - Contains packet byte information in the range (0-255).
4. Payload Bytes - Contains payload byte information in the range (0-255).

Each subset contains data stored in parquet files, an efficient and performant data storage format that maintains the schema along with the data. You can choose to download all subsets or select specific subsets depending on your analysis requirements.

## Getting Information on the Datasets

The `DatasetInfo` function provides a summary of the dataset in a pandas dataframe format. It displays the number of packets for each class label across all 18 files in the dataset. This overview can guide you in selecting specific files for download and analysis.

```python
df = DatasetInfo(dataset='UNSW-NB15') # or dataset='CIC-IDS2017'
df
```

## Downloading the Datasets

The `Dataset` class allows you to specify the dataset, subset, and files that you are interested in. The specified data will then be downloaded.

```python
dataset = 'UNSW-NB15' # or 'CIC-IDS2017'
subset = ['Network-Flows', 'Packet-Fields', 'Payload-Bytes'] # or 'all' for all subsets
files = [3, 5, 10] # or 'all' for all files

data = Dataset(dataset=dataset, subset=subset, files=files)
data.download()
```

You can then load the parquet files using pandas:

```python
import pandas as pd
df = pd.read_parquet('UNSW-NB15/Packet-Fields/Packet_Fields_File_10.parquet')
```

## Merging Subsets

The `merge()` method allows you to merge all data of each packet across all subsets, providing both flow-level and packet-level information in a single dataset.

```python
data.merge()
```

## Extracting Bytes

If you need to work with more than the first 1500-1600 bytes of the packets, you can use the `bytes()` method:

```python
data.bytes(payload=True, max_bytes=2500)
```

## Reading the Datasets

The `read()` method allows you to read files using Hugging Face's `load_dataset` method:

```python
dataset = data.read(dataset='UNSW-NB15', subset='Packet-Fields', files=[1,2])
```

For scenarios where you want to process one packet at a time, you can use the `stream=True` parameter:

```python
dataset = data.read(dataset='UNSW-NB15', subset='Packet-Fields', files=[1,2], stream=True)
print(next(iter(dataset)))
```

The `read()` method returns a dataset that you can convert to a pandas dataframe or save to a CSV, parquet, or any other desired file format:

```python
df = dataset.to_pandas()
dataset.to_csv('file_path_to_save.csv')
dataset.to_parquet('file_path_to_save.parquet')
```

## Notes

The size of these datasets is large, and depending on the subset(s) selected and the number of bytes extracted, the operations can be resource-intensive. Therefore, it's recommended to ensure you have sufficient disk space and RAM when using this package.
