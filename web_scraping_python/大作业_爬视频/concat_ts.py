import os 

ts_list = []
ts_root = '../911call'

with open('./m3u8/second.txt', 'r') as f: 
    for line in f: 
        if line.startswith('#'): 
            continue
        line = line.strip() 
        ts_list.append(os.path.join(ts_root,line))

s = ' '.join(ts_list)        
os.system(f'cat {s} > 911_s7_1.mp4')

print('\033[1;32m程序完成\n¯\_(ツ)_/¯\033[0m')