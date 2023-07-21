# NIDS Datasets (nids-datasets)

The `nids-datasets` package offers an efficient and straightforward way to download, subset, and interact with cybersecurity datasets specifically curated for Network Intrusion Detection Systems (NIDS). The package includes functionality for the UNSW-NB15 and CIC-IDS2017 datasets, both of which have been enhanced to include packet-level information from the raw PCAP files. 

## Installation

Install the `nids-datasets` package using pip:

```shell
pip install nids-datasets
```

To import the package into your Python script:

```python
from nids_datasets import Dataset, DatasetInfo
```

## Dataset Information

The `nids-datasets` package currently supports two datasets: UNSW-NB15 and CIC-IDS2017. The UNSW-NB15 dataset has 10 unique class labels while the CIC-IDS2017 dataset has 24 unique class labels. Each class label represents a different type of cyber threat.

- **Labels for UNSW-NB15 based dataset:** 'normal', 'exploits', 'dos', 'fuzzers', 'generic', 'reconnaissance', 'worms', 'shellcode', 'backdoor', 'analysis'
- **Labels for CIC-IDS2017 based dataset:** 'BENIGN', 'FTP-Patator', 'SSH-Patator', 'DoS slowloris', 'DoS Slowhttptest', 'DoS Hulk', 'Heartbleed', 'Web Attack – Brute Force', 'Web Attack – XSS', 'Web Attack – SQL Injection', 'Infiltration', 'Bot', 'PortScan', 'DDoS', 'normal', 'exploits', 'dos', 'fuzzers', 'generic', 'reconnaissance', 'worms', 'shellcode', 'backdoor', 'analysis', 'DoS GoldenEye'

## Subsets of the Dataset

The datasets are divided into four subsets:

1. Network Flows - Contains flow-level data.
2. Packet Fields - Contains packet header information.
3. Packet Bytes - Contains packet byte information in the range (0-255).
4. Payload Bytes - Contains payload byte information in the range (0-255).

Each subset contains data stored in parquet files, an efficient and performant data storage format that maintains the schema along with the data.

## Getting Information on the Datasets

The `DatasetInfo` method provides an overview of the dataset in a pandas dataframe format. It displays the number of packets for each class label across all 18 files in the dataset. This method allows you to visualize the dataset structure and can guide you in selecting specific files for download and analysis.

```python
df = DatasetInfo(dataset='UNSW-NB15') # or dataset='CIC-IDS2017'
df
```

## Downloading the Datasets

The `Dataset` class allows you to specify the dataset, subset, and files that you are interested in. This information is used to download the selected files. You can specify 'all' for downloading all subsets or files.

```python
dataset = 'UNSW-NB15' # or 'CIC-IDS2017'
subset = ['Network-Flows', 'Packet-Fields', 'Payload-Bytes'] # or 'all' for all subsets
files = [3, 5, 10] # or 'all' for all files

data = Dataset(dataset=dataset, subset=subset, files=files)
data.download()
```

After downloading, you can load the parquet files using pandas:

```python
import pandas as pd
df = pd.read_parquet('UNSW-NB15/Packet-Fields/Packet_Fields_File_10.parquet')
```

## Merging Subsets

If you wish to join or merge all data of each packet across all four subsets into a single file, use the `merge()` method. This will produce a combined file that includes both flow-level information and packet-level information for each packet, providing a comprehensive view of the dataset.

```python
data.merge()
```

## Extracting Bytes

To retrieve all bytes (up to 65535 bytes) from the Packet-Bytes and Payload-Bytes subsets, use the `Bytes()` method. This function requires files in the Packet-Fields subset to operate. You can pass the `max_bytes` parameter to specify the number of bytes you want to extract.

```python
data.bytes(payload=True, max_bytes=2500) # use max_bytes to pass how many bytes you want
```

## Reading the Files

The `read()` method offers a flexible way to read the downloaded files. It uses the Hugging Face `load_dataset` method and can be used to read one or multiple files from a single subset at a time. The method defaults to the dataset, subset, and files provided when the `Dataset` object was initialized if no parameters are passed.

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

Please ensure you have sufficient disk space and RAM when performing these operations. Large subsets and high byte values could require significant system resources.
