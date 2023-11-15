import tool,json,re,urllib,sys
from urllib.parse import urlparse, parse_qs, unquote
def parse(data):
    info = data[:]
    server_info = urlparse(info)
    try:
        netloc = tool.b64Decode(server_info.netloc).decode('utf-8')
    except:
        netloc = server_info.netloc
    _netloc = netloc.split("@")
    netquery = dict(
        (k, v if len(v) > 1 else v[0])
        for k, v in parse_qs(server_info.query).items()
    )
    node = {
        'tag': unquote(server_info.fragment) or tool.genName()+'_vless',
        'type': 'vless',
        'server': re.sub(r"\[|\]", "", _netloc[1].rsplit(":", 1)[0]),
        'server_port': int(_netloc[1].rsplit(":", 1)[1]),
        'uuid': _netloc[0].split(':', 1)[-1],
        'packet_encoding': netquery.get('packetEncoding', 'xudp')
    }
    if netquery.get('flow'):
        node['flow'] = 'xtls-rprx-vision'
    if netquery.get('security', '') not in ['none', '']:
        node['tls'] = {
            'enabled': True,
            'insecure': True
        }
        if netquery.get('sni', '') not in ['none', '']:
            node['tls']['server_name'] = netquery['sni']
        if netquery.get('fp'):
            node['tls']['utls'] = {
                'enabled': True,
                'fingerprint': netquery.get('fp', 'chrome')
            }
        if netquery['security'] == 'reality':
            node['tls']['reality'] = {
                'enabled': True,
                'public_key': netquery.get('pbk'),
            }
            if netquery.get('sid'):
                node['tls']['reality']['short_id'] = netquery['sid']
            node['tls']['utls'] = {
                'enabled': True,
                'fingerprint': netquery.get('fp', 'chrome')
            }
    if netquery.get('type'):
        if netquery['type'] == 'http':
            node['transport'] = {
                'type':'http'
            }
        if netquery['type'] == 'ws':
            node['transport'] = {
                'type':'ws',
                "path": netquery.get('path', '').rsplit("?")[0],
                "headers": {
                    "Host": netquery.get('sni', netquery.get('host', ''))
                }
            }
            if '?ed=' in netquery.get('path'):
                node['transport']['early_data_header_name'] = 'Sec-WebSocket-Protocol'
                node['transport']['max_early_data'] = int(netquery.get('path').rsplit("?ed=")[1])
        if netquery['type'] == 'grpc':
            node['transport'] = {
                'type':'grpc',
                'service_name':netquery.get('serviceName', '')
            }
    if netquery.get('protocol'):
        node['multiplex'] = {
            'enabled': True,
            'protocol': netquery['protocol'],
            'max_streams': int(netquery.get('max_streams', '0'))
        }
        if netquery.get('max_connections'):
            node['multiplex']['max_connections'] = int(netquery['max_connections'])
        if netquery.get('min_streams'):
            node['multiplex']['min_streams'] = int(netquery['min_streams'])
        if netquery.get('padding') == 'True':
            node['multiplex']['padding'] = True
    return node
