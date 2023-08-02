import os
import pandas as pd
from datasets import load_dataset
from huggingface_hub import hf_hub_download, snapshot_download
try:
    ipython = get_ipython()
    from tqdm.notebook import tqdm as tqdmn
except:
    from tqdm import tqdm as tqdmn


def DatasetInfo(dataset):
    UNSW_NB15_INFO = '{"normal": {"1": 9597932, "2": 9771699, "3": 9980200, "4": 9979823, "5": 9982881, "6": 9983244, "7": 9984416, "8": 9986659, "9": 9987598, "10": 9672644, "11": 9625429, "12": 9583173, "13": 9618777, "14": 9636038, "15": 9643297, "16": 9623646, "17": 9584978, "18": 9403900}, "exploits": {"1": 219231, "2": 121153, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 208672, "11": 216055, "12": 231463, "13": 226910, "14": 199265, "15": 222618, "16": 216629, "17": 231583, "18": 217538}, "dos": {"1": 66031, "2": 33817, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 46811, "11": 69137, "12": 71735, "13": 57220, "14": 72111, "15": 44221, "16": 70959, "17": 73005, "18": 46603}, "fuzzers": {"1": 61609, "2": 17397, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 26704, "11": 38687, "12": 42034, "13": 44183, "14": 40441, "15": 32462, "16": 38901, "17": 44524, "18": 34134}, "generic": {"1": 28211, "2": 17799, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 25510, "11": 29047, "12": 36914, "13": 29415, "14": 28263, "15": 33660, "16": 28577, "17": 41717, "18": 33750}, "reconnaissance": {"1": 12572, "2": 6820, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 12166, "11": 13541, "12": 24232, "13": 14069, "14": 13001, "15": 13400, "16": 12487, "17": 13645, "18": 14262}, "worms": {"1": 1732, "2": 324, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 1168, "11": 1298, "12": 1214, "13": 1688, "14": 1202, "15": 878, "16": 1780, "17": 1490, "18": 858}, "shellcode": {"1": 1459, "2": 598, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 1262, "11": 1306, "12": 1434, "13": 1396, "14": 1272, "15": 1300, "16": 1332, "17": 1268, "18": 1356}, "backdoor": {"1": 953, "2": 572, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 1418, "11": 1263, "12": 1688, "13": 1809, "14": 1427, "15": 1928, "16": 1473, "17": 1821, "18": 1932}, "analysis": {"1": 388, "2": 1086, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 478, "11": 1520, "12": 2024, "13": 436, "14": 1784, "15": 2224, "16": 650, "17": 2009, "18": 1476}, "total": {"1": 9990118, "2": 9971265, "3": 9980200, "4": 9979823, "5": 9982881, "6": 9983244, "7": 9984416, "8": 9986659, "9": 9987598, "10": 9996833, "11": 9997283, "12": 9995911, "13": 9995903, "14": 9994804, "15": 9995988, "16": 9996434, "17": 9996040, "18": 9755809}}'
    CIC_IDS2017_INFO = '{"BENIGN": {"1": 4822905, "2": 3571097, "3": 3556526, "4": 2575904, "5": 3007086, "6": 2637797, "7": 2612615, "8": 2649076, "9": 2948428, "10": 422225, "11": 4418585, "12": 2651388, "13": 3109436, "14": 2845250, "15": 2558990, "16": 3182740, "17": 1920222, "18": 528653}, "FTP-Patator": {"1": 0, "2": 0, "3": 1953, "4": 12803, "5": 68205, "6": 28602, "7": 0, "8": 0, "9": 0, "10": 0, "11": 0, "12": 0, "13": 0, "14": 0, "15": 0, "16": 0, "17": 0, "18": 0}, "SSH-Patator": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 38680, "7": 124631, "8": 0, "9": 0, "10": 0, "11": 0, "12": 0, "13": 0, "14": 0, "15": 0, "16": 0, "17": 0, "18": 0}, "DoS slowloris": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 47519, "10": 0, "11": 41, "12": 0, "13": 0, "14": 0, "15": 0, "16": 0, "17": 0, "18": 0}, "DoS Slowhttptest": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 19866, "10": 19675, "11": 0, "12": 0, "13": 0, "14": 0, "15": 0, "16": 0, "17": 0, "18": 0}, "DoS Hulk": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 1459567, "11": 786683, "12": 0, "13": 0, "14": 0, "15": 0, "16": 0, "17": 0, "18": 0}, "Heartbleed": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 0, "11": 49296, "12": 0, "13": 0, "14": 0, "15": 0, "16": 0, "17": 0, "18": 0}, "Web Attack \\u2013 Brute Force": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 0, "11": 0, "12": 12370, "13": 17873, "14": 0, "15": 0, "16": 0, "17": 0, "18": 0}, "Web Attack \\u2013 XSS": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 0, "11": 0, "12": 0, "13": 9344, "14": 0, "15": 0, "16": 0, "17": 0, "18": 0}, "Web Attack \\u2013 SQL Injection": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 0, "11": 0, "12": 0, "13": 126, "14": 0, "15": 0, "16": 0, "17": 0, "18": 0}, "Infiltration": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 0, "11": 0, "12": 0, "13": 0, "14": 59754, "15": 0, "16": 0, "17": 0, "18": 0}, "Bot": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 0, "11": 0, "12": 0, "13": 0, "14": 0, "15": 0, "16": 12853, "17": 0, "18": 0}, "PortScan": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 0, "11": 0, "12": 0, "13": 0, "14": 0, "15": 0, "16": 45, "17": 321386, "18": 0}, "DDoS": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 0, "11": 0, "12": 0, "13": 0, "14": 0, "15": 0, "16": 0, "17": 942879, "18": 289211}, "normal": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 0, "11": 0, "12": 0, "13": 0, "14": 0, "15": 0, "16": 0, "17": 0, "18": 0}, "exploits": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 0, "11": 0, "12": 0, "13": 0, "14": 0, "15": 0, "16": 0, "17": 0, "18": 0}, "dos": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 0, "11": 0, "12": 0, "13": 0, "14": 0, "15": 0, "16": 0, "17": 0, "18": 0}, "fuzzers": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 0, "11": 0, "12": 0, "13": 0, "14": 0, "15": 0, "16": 0, "17": 0, "18": 0}, "generic": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 0, "11": 0, "12": 0, "13": 0, "14": 0, "15": 0, "16": 0, "17": 0, "18": 0}, "reconnaissance": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 0, "11": 0, "12": 0, "13": 0, "14": 0, "15": 0, "16": 0, "17": 0, "18": 0}, "worms": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 0, "11": 0, "12": 0, "13": 0, "14": 0, "15": 0, "16": 0, "17": 0, "18": 0}, "shellcode": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 0, "11": 0, "12": 0, "13": 0, "14": 0, "15": 0, "16": 0, "17": 0, "18": 0}, "backdoor": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 0, "11": 0, "12": 0, "13": 0, "14": 0, "15": 0, "16": 0, "17": 0, "18": 0}, "analysis": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 0, "11": 0, "12": 0, "13": 0, "14": 0, "15": 0, "16": 0, "17": 0, "18": 0}, "DoS GoldenEye": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 0, "11": 104513, "12": 0, "13": 0, "14": 0, "15": 0, "16": 0, "17": 0, "18": 0}, "total": {"1": 4822905, "2": 3571097, "3": 3558479, "4": 2588707, "5": 3075291, "6": 2705079, "7": 2737246, "8": 2649076, "9": 3015813, "10": 1901467, "11": 5359118, "12": 2663758, "13": 3136779, "14": 2905004, "15": 2558990, "16": 3195638, "17": 3184487, "18": 817864}}'
    if dataset=='UNSW-NB15':
        df = pd.DataFrame(eval(UNSW_NB15_INFO))
        df = df.rename_axis('File')
    elif dataset=='CIC-IDS2017':
        df = pd.DataFrame(eval(CIC_IDS2017_INFO))
        df = df.rename_axis('File')
    return df


class Dataset:
    def __init__(self, dataset=None, subset=None, files=None):
        self.dataset = dataset
        if subset == 'all':
            subset = ['Network-Flows', 'Packet-Fields', 'Packet-Bytes', 'Payload-Bytes']
        elif isinstance(subset, str):
            subset = [subset]
        self.subset = subset
        if files == 'all':
            files = [i for i in range(1, 19)]
        elif isinstance(files, str):
            files = [files]
        self.files = files
        if self.dataset == 'UNSW-NB15':
            self.flow_file = "UNSW_Flow"
        else:
            self.flow_file = "CICIDS_Flow"

    def download(self, use_cache=True):
        if self.subset == 'all' and self.files == 'all':
            snapshot_download(repo_id=f"rdpahalavan/{self.dataset}", allow_patterns="*.parquet", repo_type="dataset",
                              local_dir=self.dataset, local_dir_use_symlinks=use_cache)
        for subset in self.subset:
            if subset == 'Network-Flows':
                hf_hub_download(repo_id=f"rdpahalavan/{self.dataset}", subfolder=subset,
                                filename=f"{self.flow_file}.parquet", repo_type="dataset", local_dir=self.dataset,
                                local_dir_use_symlinks=use_cache)
                continue
            for file in self.files:
                hf_hub_download(repo_id=f"rdpahalavan/{self.dataset}", subfolder=subset,
                                filename=f"{subset.replace('-', '_')}_File_{file}.parquet", repo_type="dataset",
                                local_dir=self.dataset, local_dir_use_symlinks=use_cache)

    def merge(self, subset=None, files=None):
        if subset is None:
            subset = self.subset
        if files is None:
            files = self.files
        on_columns = ['packet_id', 'flow_id', 'source_ip', 'source_port', 'destination_ip', 'destination_port',
                      'protocol', 'attack_label']
        if 'Network-Flows' in subset:
            flow_df = pd.read_parquet(f"{self.dataset}/Network-Flows/{self.flow_file}.parquet")
            flow_df.drop(columns=on_columns[2:], inplace=True)
        os.makedirs(f"{self.dataset}/{'+'.join(subset)}", exist_ok=True)
        for file in tqdmn(files, desc='Merging Files'):
            k = 0
            for sub in tqdmn(subset, desc='Merging Subsets'):
                if sub != 'Network-Flows':
                    if k == 0:
                        df = pd.read_parquet(f"{self.dataset}/{sub}/{sub.replace('-', '_')}_File_{file}.parquet")
                    else:
                        df = df.merge(
                            pd.read_parquet(f"{self.dataset}/{sub}/{sub.replace('-', '_')}_File_{file}.parquet"),
                            how='inner', on=on_columns)
                    k += 1
            if 'Network-Flows' in subset:
                df = df.merge(flow_df, how='inner', on='flow_id')
            attack_label = df.pop('attack_label')
            df.insert(len(df.columns), 'attack_label', attack_label)
            df.to_parquet(f"{self.dataset}/{'+'.join(subset)}/{'+'.join(subset).replace('-', '_')}_File_{file}.parquet",
                          index=False)
            del df

    def _hex_to_dec(self, hex_str):
        return [int(hex_str[i:i + 2], 16) for i in range(0, len(hex_str), 2)]

    def bytes(self, files=None, max_bytes=None, packet=False, payload=False):
        if files is None:
            files = self.files
        if packet:
            col_name = "packet_hex"
        elif payload:
            col_name = "payload_hex"
        os.makedirs(f"{self.dataset}/{col_name.split('_')[0].capitalize()}-Bytes-{max_bytes}", exist_ok=True)
        for file in tqdmn(files, desc='Extracting Bytes'):
            df = pd.read_parquet(f"{self.dataset}/Packet-Fields/Packet_Fields_File_{file}.parquet")
            df = df.dropna(subset=col_name)
            df.reset_index(drop=True, inplace=True)
            dec_data = df[col_name].apply(lambda x: self._hex_to_dec(str(x)[:int(max_bytes * 2)]))
            max_len = dec_data.apply(len).max()
            df_final = pd.DataFrame(dec_data.tolist(),
                                    columns=[f"{col_name.split('_')[0]}_byte_{i}" for i in range(1, max_len + 1)])
            df_final = pd.concat([df[['packet_id', 'flow_id', 'source_ip', 'source_port', 'destination_ip',
                                      'destination_port', 'protocol']], df_final], axis=1)
            df_final['attack_label'] = df['attack_label']
            df_final.to_parquet(f"{self.dataset}/{col_name.split('_')[0].capitalize()}-Bytes-{max_bytes}/{col_name.split('_')[0].capitalize()}_Bytes_File_{file}.parquet", index=False)
            del df_final
            del df

    def read(self, dataset=None, subset=None, files=None, packets=None, num_proc=None, stream=False):
        if dataset is None:
            dataset = self.dataset
        if subset is None:
            subset = self.subset[0]
        if files is None:
            files = self.files
        if packets is None:
            split = 'train'
        else:
            split = f'train[{packets}]'
        files = [f"{subset.replace('-', '_')}_File_{file}.parquet" for file in files]
        dataset = load_dataset(path=f"rdpahalavan/{dataset}", data_dir=subset, data_files=files, split=split, num_proc=num_proc,
                               streaming=stream)
        return dataset
