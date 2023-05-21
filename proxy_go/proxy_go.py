# fetches and check proxies and prints them in console 

import requests
import atexit
import argparse
import logging
from tqdm import tqdm


logging.basicConfig(level=logging.INFO,format='%(message)s')
logger=logging.getLogger()

anonymity=["elite","anonymous","transparent","all"]
# protocols=["http","socks4","socks5"]
# country= iso2 codes | all
def get_proxies(protocol:str="http",timeout:float=10000,country:str="all",anonymity_level:int=3):
    proxy_url=f"https://api.proxyscrape.com/v2/?request=displayproxies&protocol={protocol}&timeout={timeout}&country={country}&ssl=all&anonymity={anonymity[min(anonymity_level,3)]}"
    response = requests.get(proxy_url)
    proxy_list=str(response.content).split("\\r\\n")[0:-1]
    logger.info(f"# got {len(proxy_list)} proxies")
    return proxy_list

good_proxies=[]

def print_good_proxies():
    for proxy in good_proxies:
        print(f"{proxy['protocol']} {proxy['ip']} {proxy['port']} # SSL: {proxy['secure']}")

def exit_handler():
    print_good_proxies()

atexit.register(exit_handler)

def segregate(proxy: str,protocol:str="http")->bool:
    proxies={"https":protocol+"://"+proxy,"http":protocol+"://"+proxy}
    try:
        response=requests.get("https://ifconfig.me/ip",proxies=proxies,timeout=args.timeout/1000)
        # print(response.content)
        if(proxy.split(":")[0]==response.content.decode()):
            good_proxies.append({
                "ip":proxy.split(":")[0],
                "port":proxy.split(":")[1],
                "secure":True,
                "protocol":protocol
            })
            return True
    except requests.exceptions.SSLError:
        if(args.unsecure):
            response=requests.get("http://ifconfig.me/ip",proxies=proxies,timeout=args.timeout/1000)
            # print(response.content)
            if(proxy.split(":")[0]==response.content.decode()):
                logger.info("# adding unsecure proxy")
                good_proxies.append({
                "ip":proxy.split(":")[0],
                "port":proxy.split(":")[1],
                "secure":False,
                "protocol":protocol
            })
            return True
    except Exception as detail:
        return False
    return False
    

parser= argparse.ArgumentParser()

parser.add_argument('-p','--protocol',type=str,default="http:1",help='protocol:count protocols=["http","socks4","socks5"]')
parser.add_argument('-t','--timeout',type=float,default=10000,help='in millisecond')
parser.add_argument('-c','--country',type=str,default="all",help='# country= iso2 codes | all')
parser.add_argument('-a','--anonymity',type=int,default=3,help=' 0 -> highest anonymus')
parser.add_argument('-u','--unsecure',action='store_true',help='inclute proxy which does not support ssl')




args=parser.parse_args()

# display all args
logger.info(''.join(f'# {k}={v}\n' for k, v in vars(args).items()))

protocol_requirements=[]

for protocol_requirement in args.protocol.split(","):
    protocol_and_count=protocol_requirement.split(":")
    protocol_requirements.append({"protocol":protocol_and_count[0],"count":int(protocol_and_count[1])})



for protocol_requirement in protocol_requirements:
    logger.info(f"# fetching {protocol_requirement['protocol']} proxies")
    proxies = get_proxies(protocol=protocol_requirement["protocol"],timeout=args.timeout,country=args.country,anonymity_level=args.anonymity)
    initial_count=len(good_proxies)
    i=0
    progress_bar=tqdm(total=protocol_requirement['count'],desc=f"scanned {protocol_requirement['protocol']} {i}/{len(proxies)} found {len(good_proxies)-initial_count} working")
    while(len(good_proxies)-initial_count<protocol_requirement["count"] and i<len(proxies)):
        if(segregate(proxies[i],protocol_requirement['protocol'])):
            progress_bar.set_description(f"scanned {protocol_requirement['protocol']} {i}/{len(proxies)} found {len(good_proxies)-initial_count} working")
            progress_bar.update(1)
        i+=1
    progress_bar.close()

