import os
import re
import json
import pandas as pd
import shutil
from PIL import Image
import ipwhois
import socket
from ipwhois import IPWhois
import geopandas as gpd
from geopandas import GeoDataFrame
from shapely.geometry import Point
import matplotlib.pyplot as plt
from ip2geotools.databases.noncommercial import DbIpCity
import warnings
warnings.filterwarnings("ignore")

def generateTable(url,mode,isVis=False):
    data = os.popen(f'traceroute -I {url}').read()
    generatecsv(data,url.split('.',1)[0],isVis,mode)

def GetLocation(ip):
    res = DbIpCity.get(ip, api_key="free")
    return res.latitude,res.longitude

def make_gif(frame_folder,name):
    D = {}
    for i in os.scandir(f"{frame_folder}"):
        D[int(i.name.split(".",1)[0])]=i
    frames = [Image.open(f"{frame_folder}/"+D[i].name) for i in range(0,len(D))]
    frame_one = frames[0]
    frame_one.save(f'{name}.gif', format="GIF", append_images=frames,
               save_all=True, duration=1000, loop=0)
    
def visualize(L,name):
    # print(L)
    L = L.dropna()
    if os.path.exists('./gifs'):
        shutil.rmtree('./gifs')
    os.mkdir('gifs')
    for i in range(L.shape[0]):
        plt.figure(figsize=(16,11))
        geometry = [Point(xy) for xy in zip(L.iloc[0:i]['longitude'], L.iloc[0:i]['latitude'])]
        gdf = GeoDataFrame(L.iloc[0:i], geometry = geometry)
        world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
        gdf.plot(ax = world.plot(figsize = (10, 10)), color = 'red', markersize = 10)
        plt.plot(L.iloc[0:i]['longitude'], L.iloc[0:i]['latitude'],color='red')
        for j in range(i):
            plt.annotate(j+1,(L.iloc[j,1], L.iloc[j,0]))
        plt.savefig(f'./gifs/{i}.jpg')
    make_gif('./gifs/',name)
    shutil.rmtree('./gifs')


def generatecsv(s,websitename,isVis:False,mode):
    data = re.findall('\(.*?\)', s)
    bogon_count=0
    locations = pd.DataFrame(columns=['latitude','longitude'])

    df = pd.DataFrame(columns=["ip","AS Number","Range","Location","Organization"])
    
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    df.loc[len(df)]={'ip':IPAddr,'AS Number':'  ','Range':'  ','Location':mode,'Organization':'  '}
    loc = GetLocation(IPAddr)
    locations.loc[len(locations)] = {'latitude':loc[0],'longitude':loc[1]}
    for i in data[1:]:
        
        ipinfo = os.popen(f'ipinfo {i[1:-1]} -j')
        processed = ipinfo.read()
        ipinfo.close()

        try: 
            obj = IPWhois(i[1:-1])
            obj = obj.lookup_whois()
        except ipwhois.exceptions.IPDefinedError:
            obj = {'nets':[{'range':' '}]}

        json_object = json.loads(processed) 

        if 'org' not in json_object.keys():
            json_object['org'] = " "

        if 'bogon' in json_object.keys():
            new_row = {'ip':json_object['ip'],'AS Number':" ",\
                    "Range": " ","Location":" ","Organization":" "
                    }
            
            bogon_count = bogon_count+1
            #To remove bogon ips, uncomment below line:
            #continue
        else:
            new_row = {'ip':json_object['ip'],'AS Number':json_object['org'].split(" ",1)[0],\
                    "Range":obj['nets'][0]['range'],
                            'Location':json_object['city']+', '+\
                                json_object['region']+', '+json_object['country_name'],\
                                    'Organization':json_object['org'].split(" ",1)[1]}
        
        df.loc[len(df)] = new_row
        if 'bogon' in json_object.keys():
            continue
        loc = GetLocation(json_object['ip'])
        locations.loc[len(locations)] = {'latitude':loc[0],'longitude':loc[1]}
    print(f'{websitename}')
    print("Bogon Count: "+str(bogon_count))
    print(df)
    df.to_csv(f'{websitename}.csv',index=False)
    if isVis:
        visualize(locations,f'{websitename}')