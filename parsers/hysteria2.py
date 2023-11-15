import tool,json,re,urllib,sys
from urllib.parse import urlparse, parse_qs, unquote

def parse(data):
    info = data[:]
    server_info = urlparse(info)
    netquery = dict(
        (k, v if len(v) > 1 else v[0])
        for k, v in parse_qs(server_info.query).items()
    )
    node = {
        'tag': unquote(server_info.fragment) or tool.genName()+'_hysteria2',
        'type': 'hysteria2',
        'server': re.sub(r"\[|\]", "", server_info.netloc.split("@")[1].rsplit(":", 1)[0]),
        'server_port': int(server_info.netloc.rsplit(":", 1)[1].split(",")[0]),
        "password": server_info.netloc.split("@")[0].rsplit(":", 1)[-1],
        'up_mbps': int(netquery.get('upmbps', '10').split('M')[0]),
        'down_mbps': int(netquery.get('downmbps', '50').split('M')[0]),
        'tls': {
            'enabled': True,
            'server_name': netquery.get('sni', re.sub(r"\[|\]", "", server_info.netloc.split("@")[1].rsplit(":", 1)[0]))
        }
    }
    if netquery.get('insecure') and netquery['insecure'] == '1' or netquery.get('allowInsecure') and netquery['allowInsecure'] == '1':
        node['tls']['insecure'] = True
    node['tls']['alpn'] = (netquery.get('alpn') or "h3").strip('{}').split(',')
    if netquery.get('obfs', '') not in ['none', '']:
        node['obfs'] = {
            'type': netquery['obfs'],
            'password': netquery['obfs-password'],
        }
    return (node)
