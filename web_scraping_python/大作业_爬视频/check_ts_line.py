with open('./m3u8/second.txt', 'r') as f: 
    content = f.readlines() 

# print(content)
print(type(content))
ts = []
for i in content: 
    if i.startswith('#'): 
        continue
    # print(i)
    ts.append(i)
print(len(ts))    


# import requests 

# resp = requests.get('https://91mjww.com/vplay/MzM5NDgtMS0w.html')
# print(resp.text)