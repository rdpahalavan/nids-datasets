# NIDS Datasets

The `nids-datasets` package provides functionality to download and utilize specially curated and extracted datasets from the original CIC-IDS2017 and UNSW-NB15 datasets. These datasets, which initially were only flow datasets, have been enhanced to include packet-level information from the raw PCAP files. The dataset contains both packet-level and flow-level data for over 230 million packets, with 179 million packets from UNSW-NB15 and 54 million packets from CIC-IDS2017.

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

The `nids-datasets` package currently supports two datasets: [UNSW-NB15](https://research.unsw.edu.au/projects/unsw-nb15-dataset) and [CIC-IDS2017](https://www.unb.ca/cic/datasets/ids-2017.html). Each of these datasets contains a mix of normal traffic and different types of attack traffic, which are identified by their respective labels. The UNSW-NB15 dataset has 10 unique class labels, and the CIC-IDS2017 dataset has 24 unique class labels. 

- UNSW-NB15 Labels: 'normal', 'exploits', 'dos', 'fuzzers', 'generic', 'reconnaissance', 'worms', 'shellcode', 'backdoor', 'analysis'
- CIC-IDS2017 Labels: 'BENIGN', 'FTP-Patator', 'SSH-Patator', 'DoS slowloris', 'DoS Slowhttptest', 'DoS Hulk', 'Heartbleed', 'Web Attack – Brute Force', 'Web Attack – XSS', 'Web Attack – SQL Injection', 'Infiltration', 'Bot', 'PortScan', 'DDoS', 'normal', 'exploits', 'dos', 'fuzzers', 'generic', 'reconnaissance', 'worms', 'shellcode', 'backdoor', 'analysis', 'DoS GoldenEye'

## Subsets of the Dataset

Each dataset consists of four subsets:

1. Network-Flows - Contains flow-level data.
2. Packet-Fields - Contains packet header information.
3. Packet-Bytes - Contains packet byte information in the range (0-255).
4. Payload-Bytes - Contains payload byte information in the range (0-255).

Each subset contains 18 files (except Network-Flows, which has one file), where the data is stored in parquet format. In total, this package provides access to 110 files. You can choose to download all subsets or select specific subsets or specific files depending on your analysis requirements.

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

The directory structure after downloading files:

```
UNSW-NB15
│
├───Network-Flows
│   └───UNSW_Flow.parquet
│
├───Packet-Fields
│   ├───Packet_Fields_File_3.parquet
│   ├───Packet_Fields_File_5.parquet
│   └───Packet_Fields_File_10.parquet
│
└───Payload-Bytes
    ├───Payload_Bytes_File_3.parquet
    ├───Payload_Bytes_File_5.parquet
    └───Payload_Bytes_File_10.parquet
```

You can then load the parquet files using pandas:

```python
import pandas as pd
df = pd.read_parquet('UNSW-NB15/Packet-Fields/Packet_Fields_File_10.parquet')
```

## Merging Subsets

The `merge()` method allows you to merge all data of each packet across all subsets, providing both flow-level and packet-level information in a single file.

```python
data.merge()
```

The merge method, by default, uses the details specified while instantiating the `Dataset` class. You can also pass subset=list of subsets and files=list of files you want to merge.

The directory structure after merging files:

```
UNSW-NB15
│
├───Network-Flows
│   └───UNSW_Flow.parquet
│
├───Packet-Fields
│   ├───Packet_Fields_File_3.parquet
│   ├───Packet_Fields_File_5.parquet
│   └───Packet_Fields_File_10.parquet
│
├───Payload-Bytes
│   ├───Payload_Bytes_File_3.parquet
│   ├───Payload_Bytes_File_5.parquet
│   └───Payload_Bytes_File_10.parquet
│
└───Network-Flows+Packet-Fields+Payload-Bytes
    ├───Network_Flows+Packet_Fields+Payload_Bytes_File_3.parquet
    ├───Network_Flows+Packet_Fields+Payload_Bytes_File_5.parquet
    └───Network_Flows+Packet_Fields+Payload_Bytes_File_10.parquet
```

## Extracting Bytes

Packet-Bytes and Payload-Bytes subset contains the first 1500-1600 bytes. To retrieve all bytes (up to 65535 bytes) from the Packet-Bytes and Payload-Bytes subsets, use the `Bytes()` method. This function requires files in the Packet-Fields subset to operate. You can specify how many bytes you want to extract by passing the max_bytes parameter.

```python
data.bytes(payload=True, max_bytes=2500)
```

Use packet=True to extract packet bytes. You can also pass files=list of files to retrieve bytes.

The directory structure after extracting bytes:

```
UNSW-NB15
│
├───Network-Flows
│   └───UNSW_Flow.parquet
│
├───Packet-Fields
│   ├───Packet_Fields_File_3.parquet
│   ├───Packet_Fields_File_5.parquet
│   └───Packet_Fields_File_10.parquet
│
├───Payload-Bytes
│   ├───Payload_Bytes_File_3.parquet
│   ├───Payload_Bytes_File_5.parquet
│   └───Payload_Bytes_File_10.parquet
│
├───Network-Flows+Packet-Fields+Payload-Bytes
│   ├───Network_Flows+Packet_Fields+Payload_Bytes_File_3.parquet
│   ├───Network_Flows+Packet_Fields+Payload_Bytes_File_5.parquet
│   └───Network_Flows+Packet_Fields+Payload_Bytes_File_10.parquet
│
└───Payload-Bytes-2500
    ├───Payload_Bytes_File_3.parquet
    ├───Payload_Bytes_File_5.parquet
    └───Payload_Bytes_File_10.parquet
```

## Reading the Datasets

The `read()` method allows you to read files using Hugging Face's `load_dataset` method, one subset at a time. The dataset and files parameters are optional if the same details are used to instantiate the `Dataset` class.

```python
dataset = data.read(dataset='UNSW-NB15', subset='Packet-Fields', files=[1,2])
```

The `read()` method returns a dataset that you can convert to a pandas dataframe or save to a CSV, parquet, or any other desired file format:

```python
df = dataset.to_pandas()
dataset.to_csv('file_path_to_save.csv')
dataset.to_parquet('file_path_to_save.parquet')
```

For scenarios where you want to process one packet at a time, you can use the `stream=True` parameter:

```python
dataset = data.read(dataset='UNSW-NB15', subset='Packet-Fields', files=[1,2], stream=True)
print(next(iter(dataset)))
```

## Notes

The size of these datasets is large, and depending on the subset(s) selected and the number of bytes extracted, the operations can be resource-intensive. Therefore, it's recommended to ensure you have sufficient disk space and RAM when using this package.
