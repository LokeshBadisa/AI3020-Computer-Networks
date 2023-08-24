from utils import generateTable
from tqdm import tqdm
import warnings
warnings.filterwarnings("ignore")

urls = ['ntt.com','google.com']

for url in tqdm(urls):
    generateTable(url,'Wifi',True)