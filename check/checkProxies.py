import json
import sys
import uuid
from ruamel.yaml import YAML
from gitRepo import commitPushRActiveProxiesFile, getLatestActiveConfigs
import shutil

sys.path.append('./check/xray_url_decoder/')
sys.path.append('./check/clash_meta_url_decoder/')
sys.path.append('./check/xray_ping/')

from xray_url_decoder.XrayUrlDecoder import XrayUrlDecoder
from xray_ping.XrayPing import XrayPing
from clash_meta_url_decoder.ClashMetaUrlDecoder import ClashMetaDecoder

import argparse # 传递参数
import time # 控制时间
""" 
parser = argparse.ArgumentParser(prog = "checkProxies.py")
parser.add_argument("-n", type = str, nargs = '?', default = "", const = "")


args = parser.parse_args() # 引入序号参数


 """
""" 
def is_good_for_game(config: XrayUrlDecoder):
    return (config.type in ['tcp', 'grpc']) and (config.security in [None, "tls"])

"""  
"""
# for more info, track this issue https://github.com/MetaCubeX/Clash.Meta/issues/801
def is_buggy_in_clash_meta(config: ClashMetaDecoder):
    return config.security == "reality" and config.type == "grpc"
"""
# 根据序号选择文件
#with open("collected-proxies/row-url/all" + args.n + ".txt", 'r') as rowProxiesFile:
with open("./collected-proxies/row-url/all.txt", 'r') as rowProxiesFile:
    configs = []
#    clash_meta_configs = []
#    for_game_proxies = []
    for url in rowProxiesFile:
        if len(url) > 10:
            try:
                cusTag = uuid.uuid4().hex

                # ############# xray ############
                c = XrayUrlDecoder(url, cusTag)
                c_json = c.generate_json_str()
                if c.isSupported and c.isValid:
                    configs.append(c_json)
                """ 
                # ############# clash Meta ##########
                ccm = ClashMetaDecoder(url, cusTag)
                ccm_json = ccm.generate_obj_str()
                if c.isSupported and c.isValid and (not is_buggy_in_clash_meta(ccm)):
                    clash_meta_configs.append(json.loads(ccm_json))

                if is_good_for_game(c):
                    for_game_proxies.append(url) """
            except:
                print("There is error with this proxy => " + url)
    # getLatestGoodForGame()
    # with open("collected-proxies/row-url/for_game.txt", 'w') as forGameProxiesFile:
    #     for forGame in for_game_proxies:
    #         forGameProxiesFile.write(forGame)
    # commitPushForGameProxiesFile()

    # xrayping 不需要序号参数
    delays = XrayPing(configs)

    # 序号传给get
    # getLatestActiveConfigs(args.n)

#    with open("collected-proxies/xray-json/actives_all" + args.n + ".txt", 'w') as activeProxiesFile:
    with open("./collected-proxies/xray-json/actives_all.txt", 'w') as activeProxiesFile:
        for active in delays.actives:
            activeProxiesFile.write(json.dumps(active['proxy']) + "\n")
    
    """
    yaml = YAML()
    with open("collected-proxies/clash-meta/all.yaml", 'w') as allClashProxiesFile:
        yaml.dump({"proxies": clash_meta_configs}, allClashProxiesFile)

    """

    """ with open("collected-proxies/xray-json/actives_all.txt", 'w') as activeProxiesFile:
        for active in delays.actives:
            activeProxiesFile.write(json.dumps(active['proxy']) + "\n")

    with open("collected-proxies/xray-json/actives_under_1000ms.txt", 'w') as active1000ProxiesFile:
        for active in delays.realDelay_under_1000:
            active1000ProxiesFile.write(json.dumps(active['proxy']) + "\n")

    with open("collected-proxies/xray-json/actives_under_1500ms.txt", 'w') as active1500ProxiesFile:
        for active in delays.realDelay_under_1500:
            active1500ProxiesFile.write(json.dumps(active['proxy']) + "\n")

    with open("collected-proxies/xray-json/actives_no_403_under_1000ms.txt", 'w') as active1000no403ProxiesFile:
        for active in delays.no403_realDelay_under_1000:
            active1000no403ProxiesFile.write(json.dumps(active['proxy']) + "\n")

    with open("collected-proxies/xray-json/actives_for_ir_server_no403_u1s.txt",
              'w') as active1000no403ForServerProxiesFile:
        for active in delays.no403_realDelay_under_1000:
#            if active['proxy']["streamSettings"]["network"] not in ["ws", "grpc"]:
            active1000no403ForServerProxiesFile.write(json.dumps(active['proxy']) + "\n")

 """
#time_n = int(args.n) - 1
#time.sleep(time_n * 200)

# commitPushRActiveProxiesFile(args.n)
def is_duplicated_config(proxy: str, seen_lines: set[str]):
    isDuplicated = False

    configs: list[XrayUrlDecoder] = []
    for url in seen_lines:
        if len(url) > 10:
            try:
                configs.append(XrayUrlDecoder(url))
            except:
                pass

    try:
        c_str = XrayUrlDecoder(proxy).generate_json_str()
        for conf in configs:
            if conf.is_equal_to_config(c_str):
                isDuplicated = True
    except:
        pass

    return isDuplicated


def keep_only_lines_and_remove_duplicates(file_path, lines_to_keep):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    if lines_to_keep is None:
        new_lines = lines
    else:
        lines_to_keep = set(lines_to_keep)  # Convert to a set for faster lookup
        new_lines = [line for i, line in enumerate(lines, start=1) if i in lines_to_keep]

    unique_lines = []
    seen_lines = set()
    for line in new_lines:
        if line not in seen_lines:
            if not is_duplicated_config(line, seen_lines):
                unique_lines.append(line)
            seen_lines.add(line)

    new_content = '\n'.join(line.rstrip() for line in unique_lines if line.strip())

    with open(file_path, 'w') as file:
        file.write(new_content)


# getLatestActiveConfigs()
# getLatestRowProxies()

lineNumberOfFounds = []
with open("collected-proxies/xray-json/actives_all.txt", 'r') as activeProxiesFile:
    for activeConfig in activeProxiesFile:
        if len(activeConfig) < 10: continue

        with open("collected-proxies/row-url/all.txt", 'r') as rowProxiesFile:
            # remove if it's not in active proxies
            for (index, rowProxyUrl) in enumerate(rowProxiesFile):
                if len(rowProxyUrl) < 10: continue

                try:
                    config = XrayUrlDecoder(rowProxyUrl)
                    if config.isSupported and config.isValid and config.is_equal_to_config(activeConfig):
                        lineNumberOfFounds.append(index + 1)
                except:
                    pass

shutil.copyfile("collected-proxies/row-url/all.txt", "collected-proxies/row-url/actives_now.txt")

keep_only_lines_and_remove_duplicates("collected-proxies/row-url/actives_now.txt", lineNumberOfFounds)
