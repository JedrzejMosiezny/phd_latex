import os, sys
import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt
import math

path_gen = 'D:/01_Dokumenty/01_PUT/01_DOKTORAT/11_CFX/05_PhD runs/R67_fluent/peak_R67_hgt_512k/trn_des_v01/' #ścieżka do katalogu z interesującymi nas plikami
path_data = 'D:/01_Dokumenty/01_PUT/01_DOKTORAT/11_CFX/05_PhD runs/R67_fluent/peak_R67_hgt_512k/trn_des_v01/data/' #ścieżka do katalogu z interesującymi nas plikami
path_post = 'D:/01_Dokumenty/01_PUT/01_DOKTORAT/11_CFX/05_PhD runs/R67_fluent/peak_R67_hgt_512k/trn_des_v01/post/' #ścieżka do katalogu z interesującymi nas plikami
path_plots = 'D:/01_Dokumenty/01_PUT/01_DOKTORAT/11_CFX/05_PhD runs/R67_fluent/peak_R67_hgt_512k/trn_des_v01/post/plots/' #ścieżka do katalogu z interesującymi nas plikami

os.chdir(path_post)

acupress = pd.read_csv('exp_acupress.csv', sep=',', skiprows=0, index_col=0) #wczytaj pierwszą kolumnę
acupress = pd.DataFrame(data = acupress)
#print(acupress)

mean_p = []
dev_p = []
p_rms = []
dblev =[]

for index, row in acupress.iterrows():
    row = acupress.iloc[index]
    mean = np.mean(row)
    mean_p.append(mean)

for column in acupress:
    acu_col = acupress.loc[:, column]
    dev = acu_col.sub(mean_p,fill_value=0)
    dev_p.append(dev)
    
dev_p = pd.DataFrame(data = dev_p)
dev_p = dev_p.T
dev_p.to_csv('exp_dev_p.csv', sep=',')

os.chdir(path_plots)
for index, row in dev_p.iterrows():
    row = dev_p.iloc[index]
    rms = np.sqrt(np.mean(np.square(row)))
    p_rms.append(rms)
    db = 20 * math.log10(rms/0.00002)
    dblev.append(db)

    fig, ax1 = plt.subplot(index, figsize=(7,6))
    ax1.plot(row, 'b-')

'''
    fig = plt.figure(index, figsize=(7,6))
    plt.plot(row)
    plt.axhline(y=rms, color='r', linestyle='-')
    plt.title('Acoustic pressure at point '+str(index))
    plt.xlabel('Time 1e-06')
    plt.ylabel('[Pa]')
    plt.xlim((0,340))
    plt.ylim((-3000,3000))
    plt.text(120, 7000, 'some text')
    plt.grid(True)
    plt.savefig('Ap_point_'+str(index)+'.png')
    plt.close()
'''
os.chdir(path_post)
p_rms = pd.DataFrame(data = p_rms)
p_rms.to_csv('p_rms.csv', sep=',')
dblev = pd.DataFrame(data = dblev)
dblev.to_csv('dblev.csv', sep=',')