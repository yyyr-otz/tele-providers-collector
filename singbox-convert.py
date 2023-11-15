import json, os, tool, time, requests, sys, urllib.parse, urllib.request, importlib, argparse, yaml, ruamel.yaml
import glob, base64
import re
from datetime import datetime
from urllib.parse import urlparse
from parsers.clash2base64 import clash2v2ray

from inputimeout import inputimeout, TimeoutOccurred

import b64
import pybase64
from base64io import Base64IO

"""
# 在actions中下载
vless_sub_url = 'https://vless-sub.n7p8ri7j.workers.dev/sub/cdn.sethost.eu.org?max=20000&provider=yyyr-otz&original=0&merge=1&fp=edge'
with open('./protocols/vless-sub', "w", encoding="utf-8") as vless_sub_file:
    vless_sub = requests.get(vless_sub_url, allow_redirects=True).text
    print(vless_sub)
    print("vless-sub读取成功")
    vless_sub_raw = base64.b64decode(vless_sub).decode("utf-8")
    print(vless_sub_raw)
    vless_sub_file.write(vless_sub_raw)
    print("vless-sub下载成功")
"""
"""
# b64解码-补全4字节
def decode_base64(data):
    """"""Decode base64, padding being optional.
    :param data: Base64 data as an ASCII byte string
    :returns: The decoded byte string.
    """"""
    missing_padding = len(data) % 4
    if missing_padding != 0:
        data += b'='* (4 - missing_padding)
    return base64.urlsafe_b64decode(data)
"""
"""
# 遍历当前目录下所有扩展名为.txt的文件
for b64_path in glob.glob(os.path.join(r"./protocols/", "*")):
    print (b64_path+"开始解码")
    raw_path = os.path.join(r"./raw/protocols/" , os.path.basename(b64_path))
    with open("b64_path", "rb") as encoded_source, open("raw_path", "wb") as target:
        with Base64IO(encoded_source) as source:
            for line in source:
                print(line)
                target.write(line)
"""
"""
    with open(b64_file, "r") as b64_txt:
        raw_file = pybase64.standard_b64decode(b64_txt.read())
        # raw_file = base64.urlsafe_b64decode(data.read())
        # 将解码后的内容写入新文件
        print (b64_file+"解码成功")
        print (raw_file)
       
        with open(raw_path,"w") as rawf:
            rawf.write(raw_file)
            print (raw_path+"写入完成")
"""
parsers_mod = {}
providers = None
color_code = [31, 32, 33, 34, 35, 36, 91, 92, 93, 94, 95, 96]


def loop_color(text):
    text = '\033[1;{color}m{text}\033[0m'.format(color=color_code[0], text=text)
    color_code.append(color_code.pop(0))
    return text


def init_parsers():
    b = os.walk('parsers')
    for path, dirs, files in b:
        for file in files:
            f = os.path.splitext(file)
            if f[1] == '.py':
                parsers_mod[f[0]] = importlib.import_module('parsers.' + f[0])


def get_template():
    template_dir = 'config_template'  # 配置模板文件夹路径
    template_files = os.listdir(template_dir)  # 获取文件夹中的所有文件
    template_list = [os.path.splitext(file)[0] for file in template_files if
                     file.endswith('.json')]  # 移除扩展名并过滤出以.json结尾的文件
    template_list.sort()  # 对文件名进行排序
    return template_list


def load_json(path):
    return json.loads(tool.readFile(path))


def process_subscribes(subscribes):
    nodes = {}
    for subscribe in subscribes:
        if 'enabled' in subscribe and not subscribe['enabled']:
            continue
        _nodes = get_nodes(subscribe['url'])
        if _nodes and len(_nodes) > 0:
            add_prefix(_nodes, subscribe)
            add_emoji(_nodes, subscribe)
            if not nodes.get(subscribe['tag']):
                nodes[subscribe['tag']] = []
            nodes[subscribe['tag']] += _nodes
        else:
            print('没有在此订阅下找到节点，跳过')
            # print('Không tìm thấy proxy trong link thuê bao này, bỏ qua')
    tool.proDuplicateNodeName(nodes)
    return nodes


def nodes_filter(nodes, filter, group):
    for a in filter:
        if a.get('for') and group not in a['for']:
            continue
        nodes = action_keywords(nodes, a['action'], a['keywords'])
    return nodes


def action_keywords(nodes, action, keywords):
    # filter将按顺序依次执行
    # "filter":[
    #         {"action":"include","keywords":[""]},
    #         {"action":"exclude","keywords":[""]}
    #     ]
    temp_nodes = []
    flag = False
    if action == 'exclude':
        flag = True
    '''
    # 空关键字过滤
    '''
    # Join the patterns list into a single pattern, separated by '|'
    combined_pattern = '|'.join(keywords)

    # If the combined pattern is empty or only contains whitespace, return the original nodes
    if not combined_pattern or combined_pattern.isspace():
        return nodes

    # Compile the combined regex pattern
    compiled_pattern = re.compile(combined_pattern)

    for node in nodes:
        name = node['tag']
        # Use regex to check for a match
        match_flag = bool(compiled_pattern.search(name))

        # Use XOR to decide if the node should be included based on the action
        if match_flag ^ flag:
            temp_nodes.append(node)

    return temp_nodes


def add_prefix(nodes, subscribe):
    if subscribe.get('prefix'):
        for node in nodes:
            node['tag'] = subscribe['prefix'] + node['tag']


def add_emoji(nodes, subscribe):
    if subscribe.get('emoji'):
        for node in nodes:
            node['tag'] = tool.rename(node['tag'])
            

def get_nodes(url):
    if url.startswith('sub://'):
        url = tool.b64Decode(url[6:]).decode('utf-8')
    urlstr = urlparse(url)
    if '://' not in url and url.startswith('http'):
        try:
            content = tool.b64Decode(url).decode('utf-8')
            data = parse_content(content)
            processed_list = []
            for item in data:
                if isinstance(item, tuple):
                    processed_list.extend([item[0], item[1]])  # 处理shadowtls
                else:
                    processed_list.append(item)
            return processed_list
        except:
            return None
    if not urlstr.scheme:
        content = get_content_form_file(url)
    else:
        content = get_content_from_url(url)
    # print (content)
    if type(content) == dict:
        if 'proxies' in content:
            share_links = []
            for proxy in content['proxies']:
                share_links.append(clash2v2ray(proxy))
            data = '\n'.join(share_links)
            data = parse_content(data)
            processed_list = []
            for item in data:
                if isinstance(item, tuple):
                    processed_list.extend([item[0], item[1]])  # 处理shadowtls
                else:
                    processed_list.append(item)
            return processed_list
        elif 'outbounds' in content:
            outbounds = []
            excluded_types = {"selector", "urltest", "direct", "block", "dns"}
            filtered_outbounds = [outbound for outbound in content['outbounds'] if outbound.get("type") not in excluded_types]
            outbounds.extend(filtered_outbounds)
            return outbounds
    else:
        data = parse_content(content)
        processed_list = []
        for item in data:
            if isinstance(item, tuple):
                processed_list.extend([item[0], item[1]])  # 处理shadowtls
            else:
                processed_list.append(item)
        return processed_list


def parse_content(content):
    # firstline = tool.firstLine(content)
    # # print(firstline)
    # if not get_parser(firstline):
    #     return None
    nodelist = []
    for t in content.splitlines():
        t = t.strip()
        if len(t) == 0:
            continue
        factory = get_parser(t)
        if not factory:
            continue
        node = factory(t)
        if node:
            nodelist.append(node)
    return nodelist


def get_parser(node):
    proto = tool.get_protocol(node)
    if providers.get('exclude_protocol'):
        eps = providers['exclude_protocol'].split(',')
        if len(eps) > 0:
            eps = [protocol.strip() for protocol in eps]
            if proto in eps:
                return None
    if not proto or proto not in parsers_mod.keys():
        return None
    return parsers_mod[proto].parse


def get_content_from_url(url, n=6):
    UA = ''
    print('处理: \033[31m' + url + '\033[0m')
    print('Đang tải link đăng ký: \033[31m' + url + '\033[0m')
    prefixes = ["vmess://", "vless://", "ss://", "ssr://", "trojan://", "tuic://", "hysteria://", "hysteria2://",
                "hy2://", "wg://", "http2://", "socks://"]
    if any(url.startswith(prefix) for prefix in prefixes):
        response_text = tool.noblankLine(url)
        return response_text
    for subscribe in providers["subscribes"]:
        if 'enabled' in subscribe and not subscribe['enabled']:
            continue
        if subscribe['url'] == url:
            UA = subscribe.get('User-Agent', '')
    response = tool.getResponse(url, custom_user_agent=UA)
    concount = 1
    while concount <= n and not response:
        print('连接出错，正在进行第 ' + str(concount) + ' 次重试，最多重试 ' + str(n) + ' 次...')
        print('Lỗi kết nối, đang thử lại '+ str(concount) + '/' + str(n) + '...')
        response = tool.getResponse(url)
        concount = concount + 1
        time.sleep(1)
    if not response:
        print('获取错误，跳过此订阅')
        print('Lỗi khi tải link đăng ký, bỏ qua link đăng ký này')
        print('----------------------------')
        return None
    response_text = response.text
    response_encoding = response.encoding
    if response_text.isspace():
        print('没有从订阅链接获取到任何内容')
        print('Không nhận được proxy nào từ link đăng ký')
        return None
    if any(response_text.startswith(prefix) for prefix in prefixes):
        response_text = tool.noblankLine(response_text)
        return response_text
    elif 'proxies' in response_text:
        yaml_content = response.content.decode('utf-8')
        #yaml = ruamel.yaml.YAML()
        try:
            #response_text = dict(yaml.load(yaml_content))
            response_text = yaml.safe_load(yaml_content)
            return response_text
        except:
            pass
    elif 'outbounds' in response_text:
        try:
            response_text = json.loads(response.text)
            return response_text
        except:
            pass
    else:
        try:
            response_text = tool.b64Decode(response_text)
            response_text = response_text.decode(encoding="utf-8")
            # response_text = bytes.decode(response_text,encoding=response_encoding)
        except:
            pass
            # traceback.print_exc()
    return response_text


def get_content_form_file(url):
    print('处理: \033[31m' + url + '\033[0m')
    print('Đang tải link đăng ký: \033[31m' + url + '\033[0m')
    encoding = tool.get_encoding(url)
    file_extension = os.path.splitext(url)[1]  # 获取文件的后缀名
    if file_extension.lower() == '.yaml':
        with open(url, 'rb') as file:
            content = file.read()
        yaml_data = dict(yaml.safe_load(content))
        share_links = []
        for proxy in yaml_data['proxies']:
            share_links.append(clash2v2ray(proxy))
        node = '\n'.join(share_links)
        processed_list = tool.noblankLine(node)
        return processed_list
    else:
        data = tool.readFile(url)
        data = bytes.decode(data, encoding='utf-8')
        data = tool.noblankLine(data)
        return data


def save_config(path, nodes):
    if 'auto_backup' in providers and providers['auto_backup']:
        now = datetime.now().strftime('%Y%m%d%H%M%S')
        if os.path.exists(path):
            os.rename(path, f'{path}.{now}.bak')
    if os.path.exists(path):
        os.remove(path)
        print(f"已删除文件，并重新保存：\033[33m{path}\033[0m")
        print(f"File cấu hình đã được lưu vào: \033[33m{path}\033[0m")
    else:
        print(f"文件不存在，正在保存：\033[33m{path}\033[0m")
        print(f"File không tồn tại, đang lưu tại: \033[33m{path}\033[0m")
    tool.saveFile(path,json.dumps(nodes, indent=2, ensure_ascii=False))


def set_proxy_rule_dns(config):
    # dns_template = {
    #     "tag": "remote",
    #     "address": "tls://1.1.1.1",
    #     "detour": ""
    # }
    config_rules = config['route']['rules']
    outbound_dns = []
    dns_rules = config['dns']['rules']
    asod = providers["auto_set_outbounds_dns"]
    for rule in config_rules:
        if rule['outbound'] not in ['block', 'dns-out']:
            if rule['outbound'] != 'direct':
                outbounds_dns_template = \
                    list(filter(lambda server: server['tag'] == asod["proxy"], config['dns']['servers']))[0]
                dns_obj = outbounds_dns_template.copy()
                dns_obj['tag'] = rule['outbound'] + '_dns'
                dns_obj['detour'] = rule['outbound']
                if dns_obj not in outbound_dns:
                    outbound_dns.append(dns_obj)
            if rule.get('type') and rule['type'] == 'logical':
                dns_rule_obj = {
                    'type': 'logical',
                    'mode': rule['mode'],
                    'rules': [],
                    'server': rule['outbound'] + '_dns' if rule['outbound'] != 'direct' else asod["direct"]
                }
                for _rule in rule['rules']:
                    child_rule = pro_dns_from_route_rules(_rule)
                    if child_rule:
                        dns_rule_obj['rules'].append(child_rule)
                if len(dns_rule_obj['rules']) == 0:
                    dns_rule_obj = None
            else:
                dns_rule_obj = pro_dns_from_route_rules(rule)
            if dns_rule_obj:
                dns_rules.append(dns_rule_obj)
    # 清除重复规则
    _dns_rules = []
    for dr in dns_rules:
        if dr not in _dns_rules:
            _dns_rules.append(dr)
    config['dns']['rules'] = _dns_rules
    config['dns']['servers'].extend(outbound_dns)


def pro_dns_from_route_rules(route_rule):
    dns_route_same_list = ["inbound", "ip_version", "network", "protocol", 'domain', 'domain_suffix', 'domain_keyword',
                           'domain_regex', 'geosite', "source_geoip", "source_ip_cidr", "source_port",
                           "source_port_range", "port", "port_range", "process_name", "process_path", "package_name",
                           "user", "user_id", "clash_mode", "invert"]
    dns_rule_obj = {}
    for key in route_rule:
        if key in dns_route_same_list:
            dns_rule_obj[key] = route_rule[key]
    if len(dns_rule_obj) == 0:
        return None
    if route_rule.get('outbound'):
        dns_rule_obj['server'] = route_rule['outbound'] + '_dns' if route_rule['outbound'] != 'direct' else \
            providers["auto_set_outbounds_dns"]['direct']
    return dns_rule_obj


def pro_node_template(data_nodes, config_outbound, group):
    if config_outbound.get('filter'):
        data_nodes = nodes_filter(data_nodes, config_outbound['filter'], group)
    return [node.get('tag') for node in data_nodes]


def combin_to_config(config, data):
    config_outbounds = config["outbounds"] if config.get("outbounds") else None
    temp_outbounds = []
    if config_outbounds:
        # 提前处理all模板
        for po in config_outbounds:
            # 处理出站
            if po.get("outbounds"):
                if '{all}' in po["outbounds"]:
                    o1 = []
                    for item in po["outbounds"]:
                        if item.startswith('{') and item.endswith('}'):
                            _item = item[1:-1]
                            if _item == 'all':
                                o1.append(item)
                        else:
                            o1.append(item)
                    po['outbounds'] = o1
                t_o = []
                check_dup = []
                for oo in po["outbounds"]:
                    # 避免添加重复节点
                    if oo in check_dup:
                        continue
                    else:
                        check_dup.append(oo)
                    # 处理模板
                    if oo.startswith('{') and oo.endswith('}'):
                        oo = oo[1:-1]
                        if data.get(oo):
                            nodes = data[oo]
                            t_o.extend(pro_node_template(nodes,po,oo))
                        else:
                            if oo == 'all':
                                for group in data:
                                    nodes = data[group]
                                    t_o.extend(pro_node_template(nodes,po,group))
                    else:
                        t_o.append(oo)
                if len(t_o) == 0:
                    print('发现 {} 出站下的节点数量为 0 ，会导致sing-box无法运行，请检查config模板是否正确。'.format(
                        po['tag']))
                    print('Sing-Box không chạy được vì không tìm thấy bất kỳ proxy nào trong outbound của {}. Vui lòng kiểm tra xem mẫu cấu hình có đúng không!!'.format(
                        po['tag']))
                    sys.exit()
                po['outbounds'] = t_o
                if po.get('filter'):
                    del po['filter']
    for group in data:
        temp_outbounds.extend(data[group])
    config['outbounds'] = config_outbounds + temp_outbounds
    # 自动配置路由规则到dns规则，避免dns泄露
    dns_tags = [server.get('tag') for server in config['dns']['servers']]
    asod = providers.get("auto_set_outbounds_dns")
    if asod and asod.get('proxy') and asod.get('direct') and asod['proxy'] in dns_tags and asod['direct'] in dns_tags:
        set_proxy_rule_dns(config)
    return config


def updateLocalConfig(local_host, path):
    header = {
        'Content-Type': 'application/json'
    }
    r = requests.put(local_host + '/configs?force=false', json={"path": path}, headers=header)
    print(r.text)


def display_template(tl):
    print_str = ''
    for i in range(len(tl)):
        print_str += loop_color('{index}、{name} '.format(index=i + 1, name=tl[i]))
    print(print_str)



def select_config_template(tl):
    print ('Nhập số để chọn mẫu cấu hình tương ứng (nhấn Enter để chọn mẫu cấu hình đầu tiên theo mặc định): ')

    try:
        uip = inputimeout(prompt='输入序号，载入对应config模板（超时默认选择第一个）：', timeout=3)

        if uip == '':
            return 0
        uip = int(uip)
        if uip < 1 or uip > len(tl):
            print('输入了错误信息！重新输入')
            print('Nhập thông tin không chính xác! Vui lòng nhập lại')
            return select_config_template(tl)
        else:
            return uip-1
#    except:
#        print('输入了错误信息！重新输入')
#        print('Nhập thông tin không chính xác! Vui lòng nhập lại')
#        return select_config_template(tl)
    except TimeoutOccurred:
        return 0


if __name__ == '__main__':
    init_parsers()
    providers = load_json('providers.json')
    if providers.get('config_template'):
        config_template_path = providers['config_template']
        print ('选择: \033[33m' + config_template_path + '\033[0m')
        print ('Mẫu cấu hình sử dụng: \033[33m' + config_template_path + '\033[0m')
        response = requests.get(providers['config_template'])
        response.raise_for_status()
        config = response.json()
    else:
        template_list = get_template()
        if len(template_list) < 1:
            print('没有找到模板文件')
            print('Không tìm thấy file mẫu')
            sys.exit()
        display_template(template_list)
        uip = select_config_template(template_list)
        config_template_path = 'config_template/' + template_list[uip] + '.json'
        print ('选择: \033[33m' + template_list[uip] + '.json\033[0m')
        print ('Mẫu cấu hình sử dụng: \033[33m' + template_list[uip] + '.json\033[0m')
        config = load_json(config_template_path)
    nodes = process_subscribes(providers["subscribes"])
    if providers.get('Only-nodes'):
        combined_contents = []
        for sub_tag, contents in nodes.items():
            # 遍历每个机场的内容
            for content in contents:
                # 将内容添加到新列表中
                combined_contents.append(content)
        final_config = combined_contents #只返回节点信息
    else:
        final_config = combin_to_config(config, nodes) #节点信息添加到模板
    save_config(providers["save_config_path"], final_config)
    # updateLocalConfig('http://127.0.0.1:9090',providers['save_config_path'])
