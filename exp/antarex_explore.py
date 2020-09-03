import pandas as pd
import numpy as np
import os
import sys
import glob

data_dir = '/home/gabriel/Research/Aspide/EDE/data/Antarex/'
CPU_mono = 'CPU-MEM_mono'
CPU_multi = 'CPU-MEM_multi'
HDD_mono = 'HDD_mono'
HDD_multi = 'HDD_multi'

path_vmstat = "{}{}/results/ldms/csv/vmstat".format(data_dir, CPU_mono)
path_meminfo = "{}{}/results/ldms/csv/meminfo".format(data_dir, CPU_mono)
path_edac = "{}{}/results/ldms/csv/edac".format(data_dir, CPU_mono)
path_procdiskstats = "{}{}/results/ldms/csv/procdiskstats".format(data_dir, CPU_mono)
path_procsensors = "{}{}/results/ldms/csv/procsensors".format(data_dir, CPU_mono)
path_procstat = "{}{}/results/ldms/csv/procstat".format(data_dir, CPU_mono)
labels_CPU_MONO = "/home/gabriel/Research/Aspide/EDE/data/Antarex/CPU-MEM_mono/results/labels_injection-mono_workload-129.132.24.206_30000.csv"
# path_vmstat_2 = "{}{}/results_hdd-multi/ldms/csv/vmstat".format(data_dir, HDD_multi)

df = pd.read_csv(path_vmstat)
df_mem = pd.read_csv(path_meminfo)
df_edac = pd.read_csv(path_edac)
df_procdisk = pd.read_csv(path_procdiskstats)
df_procsensors = pd.read_csv(path_procsensors)
df_procstat = pd.read_csv(path_procstat)
df_labels = pd.read_csv(labels_CPU_MONO)


df_list = [df, df_mem, df_edac, df_procsensors, df_procstat, df_labels]
# df2 = pd.read_csv(path_vmstat_2)

print("Length of vm stat {}".format(len(df)))
print("Length of mem info {}".format(len(df_mem)))
print("Length of edac {}".format(len(df_edac)))
print("Length of proc disk {}".format(len(df_procdisk)))
print("Length of proc sensor {}".format(len(df_procsensors)))
print("Length of proc stat {}".format(len(df_procstat)))
print("length of labels {}".format(len(df_labels)))


print("Memory usage vm stat {}".format(df.memory_usage(index=True).sum()/1024/1024))
print("Memory usage mem info {}".format(df_mem.memory_usage(index=True).sum()/1024/1024))
print("Memory usage edac {}".format(df_edac.memory_usage(index=True).sum()/1024/1024))
print("Memory usage proc disk {}".format(df_procdisk.memory_usage(index=True).sum()/1024/1024))
print("Memory usage proc sensors {}".format(df_procsensors.memory_usage(index=True).sum()/1024/1024))
print("Memory usage proc stat {}".format(df_procstat.memory_usage(index=True).sum()/1024/1024))
print("Memory usage labels {}".format(df_labels.memory_usage(index=True).sum()/1024/1024))

print("Start and end times for dataframes:")
print(df['#Time'].iloc[0], df['#Time'].iloc[-1])
print(df_mem['#Time'].iloc[0], df_mem['#Time'].iloc[-1])
print(df_edac['#Time'].iloc[0], df_edac['#Time'].iloc[-1])
print(df_procdisk['#Time'].iloc[0], df_procdisk['#Time'].iloc[-1])
print(df_procsensors['#Time'].iloc[0], df_procsensors['#Time'].iloc[-1])
print(df_procstat['#Time'].iloc[0], df_procstat['#Time'].iloc[-1])
print(df_labels['#Time'].iloc[0], df_labels['#Time'].iloc[-1])


for d in df_list:
    print(d.columns)

# Round down time index
df['#Time'] = df['#Time'].apply(np.ceil)

print(df['#Time'].iloc[0])
# Check if unique
print(df['#Time'].is_unique)
# print(len(df2))
cdf = pd.concat(df_list, axis=1)


# print(cdf.head(10))


# fss

# cdf.to_csv("concat_all.csv")
