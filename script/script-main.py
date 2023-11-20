#import requirement libraries
import os
import wget
import json

import math
import string
import random

import jdatetime
from datetime import datetime, timezone, timedelta

#import web-based libraries
import html
import requests
from bs4 import BeautifulSoup

#import regex and encoding libraries
import re
import base64

import glob
import csv
#import custom python script
from title import check_modify_config, config_sort, create_internet_protocol
#去重操作依赖
import urllib.parse
# 优选域名/IP
rewrite_domain_cn = "cdn.sethost.eu.org"
rewrite_domain_80 = "cf.yumy.gay"
rewrite_domain_443 = "globalpotplayer.cn"
rewrite_domain = rewrite_domain_443
"""
# Create the geoip-lite folder if it doesn't exist
if not os.path.exists('./script/geoip-lite'):
    os.mkdir('./script/geoip-lite')

if os.path.exists('./script/geoip-lite/geoip-lite-country.mmdb'):
    os.remove('./script/geoip-lite/geoip-lite-country.mmdb')

# Download the file and rename it
url = 'https://git.io/GeoLite2-Country.mmdb'
filename = 'geoip-lite-country.mmdb'
wget.download(url, filename)

# Move the file to the geoip folder
os.rename(filename, os.path.join('./script/geoip-lite', filename))
"""

# Clean up unmatched file
with open("./script/base64/splitted/no-match", "w") as no_match_file:
    no_match_file.write("#Non-Adaptive Configurations\n")


# Load and read last date and time update
with open('./script/last update', 'r') as file:
    last_update_datetime_file = file.readline()
    last_update_datetime = last_update_datetime_file.strip()
    last_update_datetime = datetime.strptime(last_update_datetime, '%Y-%m-%d %H:%M:%S.%f%z')
# Write the current date and time update
with open('./script/last update', 'w') as file:
    current_datetime_update = datetime.now(tz = timezone(timedelta(hours=8), 'Asia/Beijing'))
    file.write(f'{current_datetime_update}')

print(f"Latest Update: {last_update_datetime.strftime('%a, %d %b %Y %X %Z')}\nCurrent Update: {current_datetime_update.strftime('%a, %d %b %Y %X %Z')}")


def json_load(path):
    # Open and read the json file
    with open(path, 'r') as file:
        # Load json file content into list
        list_content = json.load(file)
    # Return list of json content
    return list_content


def tg_channel_messages(channel_user):
    try:
        # Retrieve channels messages
        response = requests.get(f"https://t.me/s/{channel_user}")
        soup = BeautifulSoup(response.text, "html.parser")
        # Find all telegram widget messages
        div_messages = soup.find_all("div", class_="tgme_widget_message")
        # Return list of all messages in channel
        return div_messages
    except Exception as exc:
        pass

def find_matches(text_content):
    # Initialize configuration type patterns
    pattern_telegram_user = r'(?:@)(\w{4,})'
    pattern_url = r'(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))'
 #   pattern_vless = r"(?<![\w-])(vless://(?:(?!=reality)[^\s<>#])+(?=[\s<>#]))"
 #   pattern_vless = r"(?<![\w-])(vless://(?:(?!=reality|&type=http|&type=grpc)[^\s<>#])+(?=[\s<>#]))"
    pattern_vless = r"(?<![\w-])(vless://(?:(?!=reality|&type=http|&type=grpc|&type=tcp)[^\s<>#])+(?=[\s<>#]))"
    pattern_tuic = r"(?<![\w-])(tuic://[^\s<>#]+)"
    pattern_hysteria = r"(?<![\w-])(hysteria://[^\s<>#]+)"
    pattern_hysteria_ver2 = r"(?<![\w-])(hy2://[^\s<>#]+)"
    pattern_juicity = r"(?<![\w-])(juicity://[^\s<>#]+)"

    # Find all matches of patterns in text
    matches_usersname = re.findall(pattern_telegram_user, text_content, re.IGNORECASE)
    matches_url = re.findall(pattern_url, text_content, re.IGNORECASE)
    matches_vless = re.findall(pattern_vless, text_content, re.IGNORECASE)
    matches_tuic = re.findall(pattern_tuic, text_content)
    matches_hysteria = re.findall(pattern_hysteria, text_content)
    matches_hysteria_ver2 = re.findall(pattern_hysteria_ver2, text_content)
    matches_juicity = re.findall(pattern_juicity, text_content)

    # Iterate over matches to subtract titles
    for index, element in enumerate(matches_vless):
        matches_vless[index] = (re.sub(r"#[^#]+$", "", html.unescape(element))+ f"#VLESS")

    for index, element in enumerate(matches_tuic):
        matches_tuic[index] = (re.sub(r"#[^#]+$", "", html.unescape(element))+ f"#TUIC")

    for index, element in enumerate(matches_hysteria):
        matches_hysteria[index] = (re.sub(r"#[^#]+$", "", html.unescape(element))+ f"#HYSTERIA")

    for index, element in enumerate(matches_hysteria_ver2):
        matches_hysteria_ver2[index] = (re.sub(r"#[^#]+$", "", html.unescape(element))+ f"#HYSTERIA")

    for index, element in enumerate(matches_juicity):
        matches_juicity[index] = (re.sub(r"#[^#]+$", "", html.unescape(element))+ f"#JUICITY")

    matches_vless = [x for x in matches_vless if "…" not in x]
    matches_tuic = [x for x in matches_tuic if "…" not in x]
    matches_hysteria = [x for x in matches_hysteria if "…" not in x]
    matches_hysteria_ver2 = [x for x in matches_hysteria_ver2 if "…" not in x]
    matches_juicity = [x for x in matches_juicity if "…" not in x]

    # Extend hysteria versions
    matches_hysteria.extend(matches_hysteria_ver2)
    
    return matches_usersname, matches_url, matches_vless, matches_tuic, matches_hysteria, matches_juicity


def tg_message_time(div_message):
    # Retrieve channel message info
    div_message_info = div_message.find('div', class_='tgme_widget_message_info')
    # Retrieve channel message datetime
    message_datetime_tag = div_message_info.find('time')
    message_datetime = message_datetime_tag.get('datetime')

    # Change message datetime type into object and convert into Beijing datetime
    datetime_object = datetime.fromisoformat(message_datetime)
    datetime_object = datetime.astimezone(datetime_object, tz = timezone(timedelta(hours=8), 'Asia/Beijing'))

    # Retrieve now datetime based on Beijing timezone
    datetime_now = datetime.now(tz = timezone(timedelta(hours=8), 'Asia/Beijing'))

    # Return datetime object, current datetime based on Beijing datetime and delta datetime
    return datetime_object, datetime_now, datetime_now - datetime_object


def tg_message_text(div_message, content_extracter):
    # Retrieve message text class from telegram messages widget
    div_message_text = div_message.find("div", class_="tgme_widget_message_text")
    text_content = div_message_text.prettify()
    if content_extracter == 'url':
        text_content = re.sub(r"<code>([^<>]+)</code>", r"\1",re.sub(r"\s*", "", text_content),)
    elif content_extracter == 'config':
        text_content = re.sub(r"<code>([^<>]+)</code>", r"\1",
                              re.sub(r"<a[^<>]+>([^<>]+)</a>", r"\1",re.sub(r"\s*", "", text_content),),)
    
    # Return text content
    return text_content


# Load telegram channels usernames
# telegram_channels = json_load('./script/source/telegram channels.json')
telegram_channels = json_load('./script/source/telegram channels-0.json')

# Initial channels messages array
channel_messages_array = list()
removed_channel_array = list()
channel_check_messages_array = list()

# Iterate over all public telegram chanels and store twenty latest messages
for channel_user in telegram_channels:
    try:
        print(f'{channel_user}')
        # Iterate over Telegram channels to Retrieve channel messages and extend to array
        div_messages = tg_channel_messages(channel_user)
        
        # Append destroyed Telegram channels
        if len(div_messages) == 0:
            removed_channel_array.append(channel_user)
        # Check configuation Telegram channels
        channel_check_messages_array.append((channel_user, div_messages))
        
        for div_message in div_messages:
            datetime_object, datetime_now, delta_datetime_now = tg_message_time(div_message)
            if datetime_object > last_update_datetime:
                print(f"\t{datetime_object.strftime('%a, %d %b %Y %X %Z')}")
                channel_messages_array.append((channel_user, div_message))
    except Exception as exc:
        continue

# Print out total new messages counter
print(f"\nTotal New Messages From {last_update_datetime.strftime('%a, %d %b %Y %X %Z')} To {current_datetime_update.strftime('%a, %d %b %Y %X %Z')} : {len(channel_messages_array)}\n")


# Initial arrays for protocols
array_usernames = list()
array_url = list()
array_vless = list()
array_tuic = list()
array_hysteria = list()
array_juicity = list()

for channel_user, message in channel_messages_array:
    try:
        # Iterate over channel messages to extract text content
        url_text_content = tg_message_text(message, 'url')
        config_text_content = tg_message_text(message, 'config')
        # Iterate over each message to extract configuration protocol types and subscription links
        matches_username, matches_url, _ , _ , _ , _ , _ , _ , _ , _ = find_matches(url_text_content)
        _ , _ , matches_vless, matches_tuic, matches_hysteria, matches_juicity = find_matches(config_text_content)

        # Extend protocol type arrays and subscription link array
        array_usernames.extend([element.lower() for element in matches_username if len(element) >= 5])
        array_url.extend(matches_url)
        array_vless.extend(matches_vless)
        array_tuic.extend(matches_tuic)
        array_hysteria.extend(matches_hysteria)
        array_juicity.extend(matches_juicity)

    except Exception as exc:
        continue


# Initialize Telegram channels list without configuration
channel_without_config = set()

for channel_user, messages in channel_check_messages_array:
    # Initialize Channel Configs Counter
    total_config = 0

    for message in messages:
        try:
            # Iterate over channel messages to extract text content
            url_text_content = tg_message_text(message, 'url')
            config_text_content = tg_message_text(message, 'config')
            # Iterate over each message to extract configuration protocol types and subscription links
            matches_username, matches_url, _ , _ , _ , _ , _ , _ , _ , _ = find_matches(url_text_content)
            _ , _ , matches_vless, matches_tuic, matches_hysteria, matches_juicity = find_matches(config_text_content)
            total_config = total_config + len(matches_vless) + len(matches_tuic) + len(matches_hysteria) + len(matches_juicity)

        except Exception as exc:
            continue

    if total_config == 0:
        channel_without_config.add(channel_user)


def tg_username_extract(url):
    telegram_pattern = r'((http|Http|HTTP)://|(https|Https|HTTPS)://|(www|Www|WWW)\.|https://www\.|)(?P<telegram_domain>(t|T)\.(me|Me|ME)|(telegram|Telegram|TELEGRAM)\.(me|Me|ME)|(telegram|Telegram|TELEGRAM).(org|Org|ORG)|telesco.pe|(tg|Tg|TG).(dev|Dev|DEV)|(telegram|Telegram|TELEGRAM).(dog|Dog|DOG))/(?P<username>[a-zA-Z0-9_+-]+)'
    matches_url = re.match(telegram_pattern, url)
    return matches_url.group('username')


# Split Telegram usernames and subscription url links
tg_username_list = set()
url_subscription_links = set()

for url in array_url:
    try:
        tg_user = tg_username_extract(url)
        if tg_user not in ['proxy', 'img', 'emoji', 'joinchat'] and '+' not in tg_user and '-' not in tg_user and len(tg_user)>=5:
            tg_user = ''.join([element for element in list(tg_user) if element in string.ascii_letters + string.digits + '_'])
            tg_username_list.add(tg_user.lower())
    except:
        url_subscription_links.add(url.split("\"")[0])
        continue

for index, tg_user in enumerate(array_usernames):
    tg_user = ''.join([element for element in list(tg_user) if element in string.ascii_letters + string.digits + '_'])
    array_usernames[index] = tg_user


# Retrive and update channels from telegram proxies Repository
# url = 'https://raw.githubusercontent.com/yyyr-otz/tele-providers-collector/master/vless-tuic-hy2/telegram channels.json'
# filename = 'telegram proxies channel.json'
# wget.download(url, filename)

tg_username_list.update(array_usernames)
# telegram_proxies_channel = json_load('./script/telegram proxies channel.json')
# tg_username_list.update(telegram_proxies_channel)
# os.remove('./script/telegram proxies channel.json')


# Subtract and get new telegram channels
new_telegram_channels = tg_username_list.difference(telegram_channels)

# Initial channels messages array
new_channel_messages = list()

# Iterate over all public telegram chanels and store twenty latest messages
for channel_user in new_telegram_channels:
    try:
        print(f'{channel_user}')
        # Iterate over Telegram channels to Retrieve channel messages and extend to array
        div_messages = tg_channel_messages(channel_user)
        channel_messages = list()
        for div_message in div_messages:
            datetime_object, datetime_now, delta_datetime_now = tg_message_time(div_message)
            print(f"\t{datetime_object.strftime('%a, %d %b %Y %X %Z')}")
            channel_messages.append(div_message)
        new_channel_messages.append((channel_user, channel_messages))
    except:
        continue

# Messages Counter
print(f"\nTotal New Messages From New Channels {last_update_datetime.strftime('%a, %d %b %Y %X %Z')} To {current_datetime_update.strftime('%a, %d %b %Y %X %Z')} : {len(new_channel_messages)}\n")


# Initial arrays for protocols
new_array_vless = list()
new_array_tuic = list()
new_array_hysteria = list()
new_array_juicity = list()

# Initialize array for channelswith configuration contents
new_array_channels = list()

for channel, messages in new_channel_messages:
    # Set Iterator to estimate each channel configurations
    total_config = 0
    new_array_url = set()
    new_array_usernames = set()

    for message in messages:
        try:
            # Iterate over channel messages to extract text content
            url_text_content = tg_message_text(message, 'url')
            config_text_content = tg_message_text(message, 'config')
            # Iterate over each message to extract configuration protocol types and subscription links
            matches_username, matches_url, _ , _ , _ , _ , _ , _ , _ , _ = find_matches(url_text_content)
            _ , _ , matches_vless, matches_tuic, matches_hysteria, matches_juicity = find_matches(config_text_content)
            total_config = total_config + len(matches_vless) + len(matches_tuic) + len(matches_hysteria) + len(matches_juicity)

            # Extend protocol type arrays and subscription link array
            new_array_usernames.update([element.lower() for element in matches_username if len(element) >= 5])
            new_array_url.update(matches_url)
            new_array_vless.extend(matches_vless)
            new_array_tuic.extend(matches_tuic)
            new_array_hysteria.extend(matches_hysteria)
            new_array_juicity.extend(matches_juicity)

        except Exception as exc:
            continue

    # Append to channels that conatins configurations
    if total_config != 0:
        new_array_channels.append(channel)

    # Split Telegram usernames and subscription url links
    tg_username_list_new = set()

    for url in new_array_url:
        try:
            tg_user = tg_username_extract(url)
            if tg_user not in ['proxy', 'img', 'emoji', 'joinchat'] and '+' not in tg_user and '-' not in tg_user and len(tg_user)>=5:
                tg_user = ''.join([element for element in list(tg_user) if element in string.ascii_letters + string.digits + '_'])
                tg_username_list_new.add(tg_user.lower())
        except:
            url_subscription_links.add(url.split("\"")[0])
            continue

    new_array_usernames = list(new_array_usernames)
    for index, tg_user in enumerate(new_array_usernames):
        tg_user = ''.join([element for element in list(tg_user) if element in string.ascii_letters + string.digits + '_'])
        new_array_usernames[index] = tg_user

    # Subtract and get new telegram channels
    tg_username_list_new.update([element.lower() for element in new_array_usernames])
    tg_username_list_new = tg_username_list_new.difference(telegram_channels)
    tg_username_list_new = tg_username_list_new.difference(new_telegram_channels)
    updated_new_channel = set(list(map(lambda element : element[0], new_channel_messages)))
    tg_username_list_new = tg_username_list_new.difference(updated_new_channel)

    # Iterate over all public telegram chanels and store twenty latest messages
    for channel_user in tg_username_list_new:
        try:
            print(f'{channel_user}')
            # Iterate over Telegram channels to Retrieve channel messages and extend to array
            div_messages = tg_channel_messages(channel_user)
            channel_messages = list()
            for div_message in div_messages:
                datetime_object, datetime_now, delta_datetime_now = tg_message_time(div_message)
                print(f"\t{datetime_object.strftime('%a, %d %b %Y %X %Z')}")
                channel_messages.append(div_message)
            # new_channel_messages.append((channel_user, channel_messages))
        except:
            continue


# Extend new configurations into list previous ones
array_vless.extend(new_array_vless)
array_tuic.extend(new_array_tuic)
array_hysteria.extend(new_array_hysteria)
array_juicity.extend(new_array_juicity)

"""
print("New Telegram Channels Found")
for channel in new_array_channels:
    print('\t{value}'.format(value = channel))

print("Destroyed Telegram Channels Found")
for channel in removed_channel_array:
    print('\t{value}'.format(value = channel))


print("No Config Telegram Channels Found")

Traceback_time_str = current_datetime_update.strftime('%m-%d %H:%M')
Traceback_file_name = "./script/source/channels no proxy/"+Traceback_time_str

with open(Traceback_file_name,'w') as file:
    file.write('channels no proxy')

for channel in channel_without_config:
    with open(Traceback_file_name,'a') as file:
        file.write('\n{value}'.format(value = channel))
    print('\t{value}'.format(value = channel))
"""
# Extend new channels into previous channels
telegram_channels.extend(new_array_channels)
#telegram_channels = [channel for channel in telegram_channels if channel not in removed_channel_array and channel not in channel_without_config]
telegram_channels = [channel for channel in telegram_channels if channel not in removed_channel_array]
telegram_channels = list(set(telegram_channels))
telegram_channels = sorted(telegram_channels)

with open('./script/source/telegram channels.json', 'w') as telegram_channels_file:
    json.dump(telegram_channels, telegram_channels_file, indent = 4)


def html_content(html_address):
    # Retrieve subscription link content
    response = requests.get(html_address, timeout = 10)
    soup = BeautifulSoup(response.text, 'html.parser').text
    return soup


def is_valid_base64(string_value):
    try:
        # Decode the string using base64
        byte_decoded = base64.b64decode(string_value)
        # Encode the decoded bytes back to base64 and compare to the original string
        return base64.b64encode(byte_decoded).decode("utf-8") == string_value
    except:
        return False


def decode_string(content):
    # Decode strings and append to array
    if is_valid_base64(content):
            content = base64.b64decode(content).decode("utf-8")
    return content



# Update url subscription links
url_subscription_links = list(url_subscription_links)

new_tg_username_list = set()
new_url_subscription_links = set()

for url in url_subscription_links:
    try:
        tg_user = tg_username_extract(url)
        if tg_user not in ['proxy', 'img', 'emoji', 'joinchat']:
            new_tg_username_list.add(tg_user.lower())
    except:
        new_url_subscription_links.add(url.split("\"")[0])
        continue

# Chnage type of url subscription links into list to be hashable
new_url_subscription_links = list(new_url_subscription_links)


accept_chars = ['sub', 'subscribe', 'token', 'workers', 'worker', 'dev', 'txt', 'vless']
avoid_chars = ['github', 'githubusercontent', 'gist', 'git', 'google', 'play', 'apple', 'microsoft']

new_subscription_links = set()

for index, element in enumerate(new_url_subscription_links):
    acc_cond = [char in element.lower() for char in accept_chars]
    avoid_cond = [char in element.lower() for char in avoid_chars]
    if any(acc_cond):
        if not any(avoid_cond):
            new_subscription_links.add(element)


# Load subscription links
subscription_links = json_load('./script/source/subscription links.json')
# subscription_links.extend(new_subscription_links)

# Initial links contents array decoded content array
array_links_content = list()
array_links_content_decoded = list()

raw_array_links_content = list()
raw_array_links_content_decoded = list()

channel_array_links_content = list()
channel_array_links_content_decoded = list()

for url_link in subscription_links:
    try:
        # Retrieve subscription link content
        links_content = html_content(url_link)
        array_links_content.append((url_link, links_content))
        if 'soroushmirzaei' not in url_link:
            raw_array_links_content.append((url_link, links_content))
        elif 'soroushmirzaei' in url_link and 'channels' in url_link:
            channel_array_links_content.append((url_link, links_content))
    except:
        continue


# Separate encoded and unencoded strings
decoded_contents = list(map(lambda element : (element[0], decode_string(element[1])), array_links_content))
# Separate encoded and unencoded strings
raw_decoded_contents = list(map(lambda element : (element[0], decode_string(element[1])), raw_array_links_content))
# Separate encoded and unencoded strings
channel_decoded_contents = list(map(lambda element : (element[0], decode_string(element[1])), channel_array_links_content))

for url_link, content in decoded_contents:
    try:
        # Split each link contents into array and split by lines
        link_contents = content.splitlines()
        link_contents = [element for element in link_contents if element not in ['\n','\t','']]
        # Iterate over link contents to subtract titles
        for index, element in enumerate(link_contents):
            link_contents[index] = re.sub(r"#[^#]+$", "", element)
        array_links_content_decoded.append((url_link, link_contents))
    except:
        continue


for url_link, content in raw_decoded_contents:
    try:
        # Split each link contents into array and split by lines
        link_contents = content.splitlines()
        link_contents = [element for element in link_contents if element not in ['\n','\t','']]
        # Iterate over link contents to subtract titles
        for index, element in enumerate(link_contents):
            link_contents[index] = re.sub(r"#[^#]+$", "", element)
        raw_array_links_content_decoded.append((url_link, link_contents))
    except:
        continue


for url_link, content in channel_decoded_contents:
    try:
        # Split each link contents into array and split by lines
        link_contents = content.splitlines()
        link_contents = [element for element in link_contents if element not in ['\n','\t','']]
        # Iterate over link contents to subtract titles
        for index, element in enumerate(link_contents):
            link_contents[index] = re.sub(r"#[^#]+$", "", element)
        channel_array_links_content_decoded.append((url_link, link_contents))
    except:
        continue


new_subscription_urls = set()

matches_usernames = list()
matches_url = list()
matches_vless = list()
matches_tuic = list()
matches_hysteria = list()
matches_juicity = list()

raw_matches_usernames = list()
raw_matches_url = list()
raw_matches_vless = list()
raw_matches_tuic = list()
raw_matches_hysteria = list()
raw_matches_juicity = list()

channel_matches_usernames = list()
channel_matches_url = list()
channel_matches_vless = list()
channel_matches_tuic = list()
channel_matches_hysteria = list()
channel_matches_juicity = list()

for url_link, content in array_links_content_decoded:
    # Merge all subscription links content and find all protocols matches base on protocol pattern
    content_merged = "\n".join(content)
    match_user, match_url, match_vless, match_tuic, match_hysteria, match_juicity = find_matches(content_merged)

    if len(match_vless) + len(match_tuic) + len(match_hysteria) + len(match_juicity) != 0:
        new_subscription_urls.add(url_link)

    matches_usernames.extend(match_user)
    matches_url.extend(match_url)
    matches_vless.extend(match_vless)
    matches_tuic.extend(match_tuic)
    matches_hysteria.extend(match_hysteria)
    matches_juicity.extend(match_juicity)

for url_link, content in raw_array_links_content_decoded:
    # Merge all subscription links content and find all protocols matches base on protocol pattern
    raw_content_merged = "\n".join(content)
    match_user, match_url, match_vless, match_tuic, match_hysteria, match_juicity = find_matches(raw_content_merged)

    raw_matches_usernames.extend(match_user)
    raw_matches_url.extend(match_url)
    raw_matches_vless.extend(match_vless)
    raw_matches_tuic.extend(match_tuic)
    raw_matches_hysteria.extend(match_hysteria)
    raw_matches_juicity.extend(match_juicity)

for url_link, content in channel_array_links_content_decoded:
    # Merge all subscription links content and find all protocols matches base on protocol pattern
    raw_content_merged = "\n".join(content)
    match_user, match_url, match_vless, match_tuic, match_hysteria, match_juicity = find_matches(raw_content_merged)

    channel_matches_usernames.extend(match_user)
    channel_matches_url.extend(match_url)
    channel_matches_vless.extend(match_vless)
    channel_matches_tuic.extend(match_tuic)
    channel_matches_hysteria.extend(match_hysteria)
    channel_matches_juicity.extend(match_juicity)

# Save New Subscription Links
# with open('./script/source/subscription links.json', 'w') as subscription_file:
#    json.dump(sorted(new_subscription_urls), subscription_file, indent = 4)


def remove_duplicate_modified(array_configuration):
    # Initialize list for sorted configs
    country_config_dict = dict()

    for config in array_configuration:
        try:
            if config.startswith('vless'):
                pattern = r"vless://(?P<id>[^@]+)@\[?(?P<ip>[a-zA-Z0-9\.:-]+?)\]?:(?P<port>[0-9]+)/?\?(?P<params>[^#]+)#?(?P<title>(?<=#).*)?"
                vless_match = re.match(pattern, config, flags=re.IGNORECASE)
                ip = vless_match.group("ip")
                port = vless_match.group("port")
                id = vless_match.group("id")
                param = vless_match.group("params")

                # Split configuration parameters and initialize dict for parameters
                array_params_input = param.split("&")
                dict_params = {}

                # Iterate over parameters and split based on key value
                for pair in array_params_input:
                    try:
                        key, value = pair.split("=")
                        key = re.sub(r"servicename", "serviceName", re.sub(r"headertype", "headerType", re.sub(r"allowinsecure", "allowInsecure", key.lower()),),)
                        dict_params[key.lower()] = value.lower() if type(value) == str else value
                    except:
                        pass

                dict_params = {k: v for k, v in sorted(dict_params.items(), key=lambda item: item[0])}
                non_title_config = f"VL-{ip}:{port}"
                country_config_dict[non_title_config] = config

            
            if config.startswith('tuic'):
                pattern = r"tuic://(?P<id>[^:]+):(?P<pass>[^@]+)@\[?(?P<ip>[a-zA-Z0-9\.:-]+?)\]?:(?P<port>[0-9]+)/?\?(?P<params>[^#]+)#?(?P<title>(?<=#).*)?"
                tuic_match = re.match(pattern, config, flags=re.IGNORECASE)
                ip = tuic_match.group("ip")
                port = tuic_match.group("port")
                id = tuic_match.group("id")
                password = tuic_match.group("pass")
                non_title_config = f"TUIC-{ip}:{port}"
                country_config_dict[non_title_config] = config


            if config.startswith('hysteria'):
                pattern = r"hysteria://\[?(?P<ip>[a-zA-Z0-9\.:-]+?)\]?:(?P<port>[0-9]+)/?\?(?P<params>[^#]+)#?(?P<title>(?<=#).*)?"
                hysteria_match = re.match(pattern, config, flags=re.IGNORECASE)
                ip = hysteria_match.group("ip")
                port = hysteria_match.group("port")
                non_title_config = f"HYSTERIA1-{ip}:{port}"
                country_config_dict[non_title_config] = config


            if config.startswith('hy2'):
                pattern = r"hy2://(?P<pass>[^@]+)@\[?(?P<ip>[a-zA-Z0-9\.:-]+?)\]?:(?P<port>[0-9]+)/?\?(?P<params>[^#]+)#?(?P<title>(?<=#).*)?"
                hysteria_match = re.match(pattern, config, flags=re.IGNORECASE)
                ip = hysteria_match.group("ip")
                port = hysteria_match.group("port")
                password = hysteria_match.group("pass")
                non_title_config = f"HYSTERIA2-{ip}:{port}"
                country_config_dict[non_title_config] = config

        except:
            continue

    return list(country_config_dict.values())
    

def remove_duplicate(vless_array, tuic_array, hysteria_array, juicity_array, vmess_decode_dedup = True):
    # Remove duplicate configurations of telegram channels
    vless_array = list(set(vless_array))
    tuic_array = list(set(tuic_array))
    hysteria_array = list(set(hysteria_array))
    juicity_array = list(set(juicity_array))

    return vless_array, tuic_array, hysteria_array, juicity_array



def modify_config(vless_array, tuic_array, hysteria_array, check_port_connection = True):
    # Checkout connectivity and modify title and protocol type address and resolve IP address
    vless_array, vless_tls_array, vless_non_tls_array, vless_tcp_array, vless_ws_array = check_modify_config(array_configuration = vless_array, protocol_type = "VLESS", check_connection = True)
    tuic_array, _, _, _, _, = check_modify_config(array_configuration = tuic_array, protocol_type = "TUIC", check_connection = False)
    hysteria_array, _, _, _, _, = check_modify_config(array_configuration = hysteria_array, protocol_type = "HYSTERIA", check_connection = False)

    # Initialize security and netowrk array
    tls_array = list()
    non_tls_array = list()

    tcp_array = list()
    ws_array = list()


    for array in [vless_tls_array]:
        tls_array.extend(array)
    for array in [vless_non_tls_array]:
        non_tls_array.extend(array)

    for array in [vless_tcp_array]:
        tcp_array.extend(array)
    for array in [vless_ws_array]:
        ws_array.extend(array)

    return vless_array, tuic_array, hysteria_array, tls_array, non_tls_array, tcp_array, ws_array


# Remove Duplicate Configurations
configs_list_array = [array_vless, array_tuic, array_hysteria, matches_vless, matches_tuic, matches_hysteria, raw_matches_vless, raw_matches_tuic, raw_matches_hysteria, channel_matches_vless, channel_matches_tuic, channel_matches_hysteria]
array_removed_duplicate_list_configurations = list()

for array in configs_list_array:
    print(f"Before Removing Duplicates : {len(array)}", end = '\t')
    array = remove_duplicate_modified(array)
    print(f"After Removing Duplicates : {len(array)}")
    array_removed_duplicate_list_configurations.append(array)

# Dedicate removed array of the list of elements
array_vless, array_tuic, array_hysteria, matches_vless, matches_tuic, matches_hysteria, raw_matches_vless, raw_raw_matches_tuic, raw_matches_hysteria, channel_matches_vless, channel_channel_matches_tuic, channel_matches_hysteria = array_removed_duplicate_list_configurations


# Remove duplicate configurations of telegram channels and subscription links contents
array_vless, array_tuic, array_hysteria, array_juicity = remove_duplicate(array_vless, array_tuic, array_hysteria, array_juicity)
matches_vless, matches_tuic, matches_hysteria, matches_juicity = remove_duplicate(matches_vless, matches_tuic, matches_hysteria, matches_juicity)
raw_matches_vless, raw_raw_matches_tuic, raw_matches_hysteria, raw_matches_juicity = remove_duplicate(raw_matches_vless, raw_raw_matches_tuic, raw_matches_hysteria, raw_matches_juicity)
channel_matches_vless, channel_channel_matches_tuic, channel_matches_hysteria, channel_matches_juicity = remove_duplicate(channel_matches_vless, channel_channel_matches_tuic, channel_matches_hysteria, channel_matches_juicity)

# Checkout connectivity and modify title and protocol type address and resolve IP address
array_vless, array_tuic, array_hysteria, array_tls, array_non_tls, array_tcp, array_ws = modify_config(array_vless, array_tuic, array_hysteria)
matches_vless, matches_tuic, matches_hysteria, matches_tls, matches_non_tls, matches_tcp, matches_ws = modify_config(matches_vless, matches_tuic, matches_hysteria)
raw_matches_vless, raw_matches_tuic, raw_matches_hysteria, raw_matches_tls, raw_matches_non_tls, raw_matches_tcp, raw_matches_ws = modify_config(raw_matches_vless, raw_matches_tuic, raw_matches_hysteria, check_port_connection = True)
channel_matches_vless, channel_matches_tuic, channel_matches_hysteria, channel_matches_tls, channel_matches_non_tls, channel_matches_tcp, channel_matches_ws = modify_config(channel_matches_vless, channel_matches_tuic, channel_matches_hysteria, check_port_connection = True)


# Extend channel subscription links contents to telegram channel contents
array_vless_channels = array_vless
array_tuic_channels = array_tuic
array_hysteria_channels = array_hysteria
array_juicity_channels = array_juicity

array_vless_channels.extend(channel_matches_vless)
array_tuic_channels.extend(channel_matches_tuic)
array_hysteria_channels.extend(channel_matches_hysteria)
array_juicity_channels.extend(channel_matches_juicity)

# Remove duplicate configurations after modifying telegram channels and subscription links contents
array_vless_channels, array_tuic_channels, array_hysteria_channels, array_juicity_channels = remove_duplicate(array_vless_channels, array_tuic_channels, array_hysteria_channels, array_juicity_channels)
channel_matches_vless, channel_channel_matches_tuic, channel_matches_hysteria, channel_matches_juicity = remove_duplicate(channel_matches_vless, channel_channel_matches_tuic, channel_matches_hysteria, channel_matches_juicity)

# Extend channel subscription links contents to telegram channel contents based on networks and security
array_tls_channels = array_tls
array_non_tls_channels = array_non_tls
array_tcp_channels = array_tcp
array_ws_channels = array_ws

array_tls_channels.extend(channel_matches_tls)
array_non_tls_channels.extend(channel_matches_non_tls)
array_tcp_channels.extend(channel_matches_tcp)
array_ws_channels.extend(channel_matches_ws)
array_tls_channels = list(set(array_tls_channels))
array_non_tls_channels = list(set(array_non_tls_channels))
array_tcp_channels = list(set(array_tcp_channels))
array_ws_channels = list(set(array_ws_channels))


# Extend subscription links contents to telegram channel contents
array_vless.extend(matches_vless)
array_tuic.extend(matches_tuic)
array_hysteria.extend(matches_hysteria)
array_juicity.extend(matches_juicity)

# Remove duplicate configurations after modifying telegram channels and subscription links contents
array_vless, array_tuic, array_hysteria, array_juicity = remove_duplicate(array_vless, array_tuic, array_hysteria, array_juicity)
matches_vless, matches_tuic, matches_hysteria, matches_juicity = remove_duplicate(matches_vless, matches_tuic, matches_hysteria, matches_juicity)
raw_matches_vless, raw_raw_matches_tuic, raw_matches_hysteria, raw_matches_juicity = remove_duplicate(raw_matches_vless, raw_raw_matches_tuic, raw_matches_hysteria, raw_matches_juicity)

# Extend subscription links contents to telegram channel contents
array_tls.extend(matches_tls)
array_non_tls.extend(matches_non_tls)
array_tcp.extend(matches_tcp)
array_ws.extend(matches_ws)

# Remove duplicate configurations after modifying telegram channels and subscription links contents
array_tls = list(set(array_tls))
array_non_tls = list(set(array_non_tls))
array_tcp = list(set(array_tcp))
array_ws = list(set(array_ws))

raw_matches_tls = list(set(raw_matches_tls))
raw_matches_non_tls = list(set(raw_matches_non_tls))
raw_matches_tcp = list(set(raw_matches_tcp))
raw_matches_ws = list(set(raw_matches_ws))


# Remove Duplicate Configurations
array_list_configurations = [array_vless, array_tuic, array_hysteria, matches_vless, matches_tuic, matches_hysteria, raw_matches_vless, raw_raw_matches_tuic, raw_matches_hysteria, channel_matches_vless, channel_channel_matches_tuic, channel_matches_hysteria]
array_removed_duplicate_list_configurations = list()

for array in array_list_configurations:
    print(f"Before Removing Duplicates : {len(array)}", end = '\t')
    array = remove_duplicate_modified(array)
    print(f"After Removing Duplicates : {len(array)}")
    array_removed_duplicate_list_configurations.append(array)

# Dedicate removed array of the list of elements 
array_vless, array_tuic, array_hysteria, matches_vless, matches_tuic, matches_hysteria, raw_matches_vless, raw_raw_matches_tuic, raw_matches_hysteria, channel_matches_vless, channel_channel_matches_tuic, channel_matches_hysteria = array_removed_duplicate_list_configurations


# Combine all configurations into one mixed configuration array and shuffle
array_mixed = array_tuic + array_hysteria + array_juicity
# array_mixed = config_sort(array_mixed)



"""
# Define chunk size for splitted arrays
chunk_size = math.ceil(len(array_mixed)/10)
chunks = list()

# Split and get chunks of mixed configurations array 
for i in range(0, len(array_mixed), chunk_size):
    chunk = array_mixed[i : i + chunk_size]
    chunks.append(chunk)
"""

def create_title(title, port):
    uuid_ranks = ['abcabca','abca','abca','abcd','abcabcabcabc']
    for index, value in enumerate(uuid_ranks):
        char_value = list(value)
        random.shuffle(char_value)
        uuid_ranks[index] = ''.join(char_value)

    uuid = '-'.join(uuid_ranks)

    # Define configurations based on protocol
    vless_config_title = f"vless://{uuid}@127.0.0.1:{port}?security=tls&type=tcp#{title}"


    return vless_config_title


# Define update date and time based on Beijing timezone and calendar
datetime_update = jdatetime.datetime.now(tz = timezone(timedelta(hours=8), 'Asia/Beijing'))
datetime_update_str = datetime_update.strftime("\U0001F504 更新时间 \U0001F4C5 %a %m月%d日 \U0001F551 %H:%M").upper()
# Define update time based on protocol type
vless_update = create_title(datetime_update_str, port = 1080)

# Define develooper sign
dev_sign = "\U0001F468\U0001F3FB\u200D\U0001F4BB 由YYYR收集,鸣谢代码原作者,请勿用于违法用途 \U0001F970"
# Define develooper based on protocol type
vless_dev_sign = create_title(dev_sign, port = 8080)

# Adds update time into protocol type lists 

array_vless = config_sort(array_vless)
""" 
# 插入反代IP
def IP_reweite(array_configuration, rewrite_ip):
    for config in array_configuration:
          former_ip = r'(?<=@).*?(?=:)'
          proxy_rewrite = re.sub(former_ip, rewrite_ip, config)
          former_id = r'(?<=((VL-WS-TLS))).*?(?=$)|(?<=((VL-WS-NONE))).*?(?=$)'
          proxy_rewrite = re.sub(former_id, " \U0001F680 优选IP-" + rewrite_ip, config)
    return list(set(config))

array_vless_rewrite = IP_reweite(array_vless, rewrite_domain)
array_ws_rewrite = IP_reweite(array_ws, rewrite_domain)
array_tls_rewrite = IP_reweite(array_tls, rewrite_domain)
array_tls_rewrite = IP_reweite(array_tls, rewrite_domain)
array_non_tls_rewrite = IP_reweite(array_non_tls, rewrite_domain)

 """
# array_vless_rewrite.insert(0, vless_update)
array_vless.insert(0, vless_update)
array_tuic.insert(0, vless_update)
array_hysteria.insert(0, vless_update)
array_juicity.insert(0, vless_update)

# array_vless_rewrite.append(vless_dev_sign)
array_vless.append(vless_dev_sign)
array_tuic.append(vless_dev_sign)
array_hysteria.append(vless_dev_sign)
array_juicity.append(vless_dev_sign)

# Split and save mixed array based on internet protocol 全部节点-IP类型
array_mixed_ipv4, array_mixed_ipv6 = create_internet_protocol(array_mixed)
with open("./script/base64/layers/ipv4", "w", encoding="utf-8") as file:
    array_mixed_ipv4.insert(0, vless_update)
    array_mixed_ipv4.append(vless_dev_sign)
    file.write(base64.b64encode("\n".join(array_mixed_ipv4).encode("utf-8")).decode("utf-8"))

with open("./script/base64/layers/ipv6", "w", encoding="utf-8") as file:
    array_mixed_ipv6.insert(0, vless_update)
    array_mixed_ipv6.append(vless_dev_sign)
    file.write(base64.b64encode("\n".join(array_mixed_ipv6).encode("utf-8")).decode("utf-8"))


# Save all mixed array and subscription links content 全部节点
with open("./script/base64/splitted/mixed", "w", encoding="utf-8") as file:
    array_mixed.insert(0, vless_update)
    array_mixed.append(vless_dev_sign)
    file.write(base64.b64encode("\n".join(array_mixed).encode("utf-8")).decode("utf-8"))

with open("./script/raw/protocols/mixed.txt", "w", encoding="utf-8") as file:
    array_mixed.insert(0, vless_update)
    array_mixed.append(vless_dev_sign)
    file.write("\n".join(array_mixed).encode("utf-8").decode("utf-8"))


# Save configurations into files splitted based on configuration type 全部节点-协议类型
# with open("./script/base64/protocols/vless-CDN", "w", encoding="utf-8") as file:
#     file.write(base64.b64encode("\n".join(array_vless_rewrite).encode("utf-8")).decode("utf-8"))
with open("./script/base64/protocols/vless", "w", encoding="utf-8") as file:
    file.write(base64.b64encode("\n".join(array_vless).encode("utf-8")).decode("utf-8"))
with open("./script/base64/protocols/tuic", "w", encoding="utf-8") as file:
    file.write(base64.b64encode("\n".join(array_tuic).encode("utf-8")).decode("utf-8"))
with open("./script/base64/protocols/hysteria", "w", encoding="utf-8") as file:
    file.write(base64.b64encode("\n".join(array_hysteria).encode("utf-8")).decode("utf-8"))
with open("./script/base64/protocols/juicity", "w", encoding="utf-8") as file:
    file.write(base64.b64encode("\n".join(array_juicity).encode("utf-8")).decode("utf-8"))

""" #
with open("./script/base64/protocols/vless-CDN", "w", encoding="utf-8") as file:
    rewrite_ip = rewrite_domain
    vless_former = "\n".join(array_vless)
 #   print(vless_former)
#    former_ip = r'(?<=@).*?(?=:)'
    ip_rewrite = re.sub(r'(?<=@).*?(?=:)', rewrite_ip, vless_former)
#    print(ip_rewrite)
#    former_id = r'(?<=((VL-WS-TLS))).*?(?=$)|(?<=((VL-WS-NONE))).*?(?=$)'
    id_rewrite = re.sub(r'(?<=((VL-WS-TLS ))).*MS|(?<=((VL-WS-NONE))).*MS', "\U0001F680 优选IP" + rewrite_ip, ip_rewrite)
#    print(id_rewrite)
    file.write(base64.b64encode((id_rewrite).encode("utf-8")).decode("utf-8"))
 """
# with open("./script/raw/protocols/vless-CDN.txt", "w") as file:
#     file.write("\n".join(array_vless_rewrite).encode("utf-8").decode("utf-8"))
with open("./script/raw/protocols/vless.txt", "w") as file:
    file.write("\n".join(array_vless).encode("utf-8").decode("utf-8"))
with open("./script/raw/protocols/tuic.txt", "w") as file:
    file.write("\n".join(array_tuic).encode("utf-8").decode("utf-8"))
with open("./script/raw/protocols/hysteria.txt", "w") as file:
    file.write("\n".join(array_hysteria).encode("utf-8").decode("utf-8"))
with open("./script/raw/protocols/juicity.txt", "w") as file:
    file.write("\n".join(array_juicity).encode("utf-8").decode("utf-8"))
with open("./script/raw/protocols/vless-CDN.txt", "w") as file:
    rewrite_ip = rewrite_domain
    vless_former = "\n".join(array_vless).encode("utf-8").decode("utf-8")
#    print(vless_former)
#    former_ip = r'(?<=@).*?(?=:)'
#    # 替换优选IP
    #ip_rewrite = re.sub(r'(?<=[a-z0-9]{12}@).*?(?=:[0-9])', rewrite_ip, vless_former)
#    print(ip_rewrite)
#    former_id = r'(?<=((VL-WS-TLS))).*?(?=$)|(?<=((VL-WS-NONE))).*?(?=$)'
#    id_rewrite = re.sub(r'(?<=((TLS ))).*MS|(?<=((NONE))).*MS|(?<=((NA))).*MS', "\U0001F680 优选IP: " + rewrite_ip, ip_rewrite)
#    print(id_rewrite)
    # 替换加速端口
    port_80 = re.sub(r'(?<=[0-9\]]:)8080(?=\?)|(?<=[0-9\]]:)8880(?=\?)|(?<=[0-9\]]:)2052(?=\?)|(?<=[0-9\]]:)2082(?=\?)|(?<=[0-9\]]:)2086(?=\?)|(?<=[0-9\]]:)2095(?=\?)', "80", vless_former)
    port_443 =  re.sub(r'(?<=[0-9\]]:)8443(?=\?)|(?<=[0-9\]]:)2053(?=\?)|(?<=[0-9\]]:)2083(?=\?)|(?<=[0-9\]]:)2087(?=\?)|(?<=[0-9\]]:)2096(?=\?)', "843", port_80)
#    # 替换优选IP
    ip_rewrite = re.sub(r'(?<=[a-z0-9]{12}@).*?(?=:[0-9])', rewrite_ip, port_443)

    file.write((ip_rewrite).encode("utf-8").decode("utf-8"))
    print ("节点已替换优选ip:" + rewrite_ip +",保存至./script/raw/protocols/vless-CDN.txt")

# 追加vless-sub
vless_sub_url = "https://vless-sub.n7p8ri7j.workers.dev/sub/" + rewrite_domain + "?max=20000&provider=yyyr-otz&original=0&merge=1&fp=edge"
with open('./script/raw/protocols/vless-CDN.txt', "a") as vless_sub_file:
    vless_sub_b64 = requests.get(vless_sub_url, allow_redirects=True).text.encode("utf-8").decode("utf-8")
    vless_sub_raw = base64.b64decode(vless_sub_b64).decode("utf-8")
    vless_sub_unurl = urllib.parse.unquote(vless_sub_raw,  'utf-8')
#    print (vless_sub_unurl )
    vless_sub_file.write("\n" + vless_sub_unurl.encode("utf-8").decode("utf-8"))
    print ("vless-sub已下载……")
""" #定义url解码字典
url_table = {
'%20':' ',
'%22':'"',
'%23':'#',
'%25':'%',
'%26':'&',
'%28':'(',
'%29':')',
'%2B':'+',
'%2C':',',
'%2F':'/',
'%3A':':',
'%3B':';',
'%3C':'<',
'%3D':'=',
'%3E':'>',
'%3F':'?',
'%40':'@',
'%7C':'|'
}
 """
# 优选节点重命名
with open("./script/raw/protocols/vless-CDN.txt", "r") as file:
#    former_id = r'encryptio.*.$'
    file_code = file.read().encode("utf-8").decode("utf-8")
    with open("./script/raw/protocols/vless-CDN.txt", "w") as f:
        print("vless-sub已追加……")
#        print(file_code)
    #url解码
    #    unurl_proxy = ""
    #    for char in file_code:
    #        if char in url_table:
    #            unurl_proxy += url_table[char]
    #        else:
    #            unurl_proxy += char
    #    url1 = file_code.replace("%20"," ")
    #    url2 = url1.replace("%23","#")
    #    url3 = url2.replace("%26","&")
    #    url4 = url3.replace("%2C",",")
    #    url5 = url4.replace("%2F","/")
    #    url6 = url5.replace("%3A",":")
    #    url7 = url6.replace("%3D","=")
    #    url8 = url7.replace("%3F","?")
    #    url9 = url8.replace("%40","@")
    #    url10 = url9.replace("%7C","|")
    #    url11 = url10.replace("%25","%")
    #    print("url已解码……")
    #    print(url11)
    # 去掉节点前缀
        id_rewrite_1 = re.sub(r'#?(?<=#).*?(?=VL)',"# \U0001F512 ", file_code)
        print("节点前缀已统一……")
#        print(id_rewrite_1)
    # 去掉末尾ping
        id_rewrite_2 = re.sub(r'#?(?<=((-TLS ))).*MS|#?(?<=(-(NONE ))).*MS|#?(?<=((-NA ))).*MS|#?(?<=((-TLS ))).*-ip|#?(?<=(-(NONE ))).*-ip|#?(?<=((-NA ))).*-ip',"\U0001F680 优选IP: " + rewrite_ip, id_rewrite_1)
        print("节点后缀已统一……")
#        print(id_rewrite_2)
        id_rewrite_3 = re.sub(r'优选IP.*.ip|优选IP.*.$', "优选IP: " + rewrite_ip, id_rewrite_2)
        id_rewrite_4 = re.sub(r' CDN-ip', "", id_rewrite_3)
        f.write(id_rewrite_4.encode("utf-8").decode("utf-8"))


# 定义去重函数
def remove_duplicate_lines(file_path):
    lines = set()
    with open(file_path, 'r') as file:
        for line in file:
            lines.add(line)
    lines = list(lines)
    with open(file_path, 'w') as file:
        for line in lines:
            file.write(line)
    return True
# 优选节点去重
if remove_duplicate_lines("./script/raw/protocols/vless-CDN.txt"):
    print("优选节点./script/raw/protocols/vless-CDN.txt"+"去重完成")

# 优选节点传递到check
with open("./script/raw/protocols/vless-CDN.txt", "r") as file:
    with open("./collected-proxies/row-url/all.txt", "a") as f:
        f.write("\n" + file.read())
    print("待测节点./collected-proxies/row-url/all.txt"+"追加完成")


# 对待测节点去重 
if remove_duplicate_lines("./collected-proxies/row-url/all.txt"):
    print("待测节点./collected-proxies/row-url/all.txt"+"去重完成")
"""        
# 待测节点分割
with open("./collected-proxies/row-url/all.txt", "r") as file:
    file = file.readlines()
    num_part = 3
    start = 0
    num_lines = len(file)
    part_size = ( num_lines // num_part ) + 1
    end = part_size
    for i in range(num_part):
        part_name = "./collected-proxies/row-url/all_" + str(i+1)
        with open(part_name, 'w') as part_f:
            part_f.write(''.join(file[start:end]))
        start = start + part_size
        end = end + part_size
    print(os.listdir("./collected-proxies/row-url/"))
"""
# 优选节点base64编码
with open("./script/raw/protocols/vless-CDN.txt", "r") as file:
    with open("./script/base64/protocols/vless-CDN", "w", encoding="utf-8") as f:
            f.write(base64.b64encode(file.read().encode("utf-8")).decode("utf-8"))
            print ("./script/raw/protocols/vless-CDN.txt"+"base编码为"+"./script/base64/protocols/vless-CDN")
  
"""
# 遍历当前目录下所有扩展名为.txt的文件
for b64_file in glob.glob(os.path.join(r"./script/base64/protocols/", "*")):
    print (b64_file+"开始解码")
    with open(b64_file, "r") as b64_txt:
        raw_file = base64.b64decode(b64_txt.read()).decode("utf-8")
        # raw_file = base64.urlsafe_b64decode(data.read())
        # 将解码后的内容写入新文件
        raw_path = os.path.join(r"./script/raw/protocols/" , os.path.basename(b64_file))
        with open(raw_path + ".txt", "w") as rawf:
            print (raw_file)
            rawf.write(raw_file)
            print (raw_path+"写入完成")
"""
# Adds update time into protocol type lists 全部节点-加密类型
array_tls = config_sort(array_tls)
array_non_tls = config_sort(array_non_tls)
array_tcp = config_sort(array_tcp)
array_ws = config_sort(array_ws)

array_tls.insert(0, vless_update)
array_non_tls.insert(0, vless_update)
array_tcp.insert(0, vless_update)
array_ws.insert(0, vless_update)

array_tls.append(vless_dev_sign)
array_non_tls.append(vless_dev_sign)
array_tcp.append(vless_dev_sign)
array_ws.append(vless_dev_sign)

# Save configurations into files splitted based on configuration type
with open("./script/base64/security/tls", "w", encoding="utf-8") as file:
    file.write(base64.b64encode("\n".join(array_tls).encode("utf-8")).decode("utf-8"))
with open("./script/base64/security/non-tls", "w", encoding="utf-8") as file:
    file.write(base64.b64encode("\n".join(array_non_tls).encode("utf-8")).decode("utf-8"))
with open("./script/base64/networks/tcp", "w", encoding="utf-8") as file:
    file.write(base64.b64encode("\n".join(array_tcp).encode("utf-8")).decode("utf-8"))
with open("./script/base64/networks/ws", "w", encoding="utf-8") as file:
    file.write(base64.b64encode("\n".join(array_ws).encode("utf-8")).decode("utf-8"))


readme = '''## Introduction-Just Vless-WS
The script aggregates Vless ( just ws ) from Telegram public channels. It cleans up the configurations based on the open and closed ports, removes duplicate configurations, resolves configurations addresses based on IP address, and redefines configuration titles based on server and protocol type properties such as network and security type, IP address and port.

![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/yyyr-otz/tele-providers-collector/master?label=Last%20Commit&color=%2338914b)
![GitHub](https://img.shields.io/github/license/yyyr-otz/tele-providers-collector/master?label=License&color=yellow)
[![节点索引](https://github.com/yyyr-otz/tele-providers-collector/actions/workflows/proxies-script.yml/badge.svg?branch=master)](https://github.com/yyyr-otz/tele-providers-collector/actions/workflows/proxies-script.yml)
[![节点索引](https://github.com/yyyr-otz/tele-providers-collector/actions/workflows/proxies-script.yml/badge.svg?branch=master&event=workflow_dispatch)](https://github.com/yyyr-otz/tele-providers-collector/actions/workflows/proxies-script.yml)
[![节点索引](https://github.com/yyyr-otz/tele-providers-collector/actions/workflows/proxies-script.yml/badge.svg?branch=master&event=schedule)](https://github.com/yyyr-otz/tele-providers-collector/actions/workflows/proxies-script.yml)

## Protocol Type Subscription Links

| **Protocol Type** | **Mixed Configurations** |
|:----:|:----:|
| **Juicity Configurations [Preview]** | [Subscription Link](https://raw.githubusercontent.com/yyyr-otz/tele-providers-collector/master/script/base64/protocols/juicity) |
| **Hysteria Configurations [Preview]** | [Subscription Link](https://raw.githubusercontent.com/yyyr-otz/tele-providers-collector/master/script/base64/protocols/hysteria) |
| **Tuic Configurations [Preview]** | [Subscription Link](https://raw.githubusercontent.com/yyyr-otz/tele-providers-collector/master/script/base64/protocols/tuic) |
| **Vless Configurations** | [Subscription Link](https://raw.githubusercontent.com/yyyr-otz/tele-providers-collector/master/script/base64/protocols/vless) |
| **Vless (CDN) Configurations** | [Subscription Link](https://raw.githubusercontent.com/yyyr-otz/tele-providers-collector/master/script/base64/protocols/vless-sub) |
| **Mixed Type Configurations** | [Subscription Link](https://raw.githubusercontent.com/yyyr-otz/tele-providers-collector/master/script/base64/splitted/mixed) |

## Network Type Subscription Links

| **Network Type** | **Mixed Configurations** |
|:----:|:----:|
| **WebSocket Protocol (WS)** | [Subscription Link](https://raw.githubusercontent.com/yyyr-otz/tele-providers-collector/master/script/base64/networks/ws) |
 | **Transmission Control Protocol (TCP)** | [Subscription Link](https://raw.githubusercontent.com/yyyr-otz/tele-providers-collector/master/script/base64/networks/tcp) |

## Security Type Subscription Links

| **Security Type** | **Mixed Configurations** |
|:----:|:----:|
| **Transport Layer Security (TLS)** | [Subscription Link](https://raw.githubusercontent.com/yyyr-otz/tele-providers-collector/master/script/base64/security/tls) |
| **Non Transport Layer Security (Non-TLS)** | [Subscription Link](https://raw.githubusercontent.com/yyyr-otz/tele-providers-collector/master/script/base64/security/non-tls) |

## Internet Protocol Type Subscription Links

| **Internet Protocol Type** | **Mixed Configurations** |
|:----:|:----:|
| **Internet Protocol Version 4 (IPV4)** | [Subscription Link](https://raw.githubusercontent.com/yyyr-otz/tele-providers-collector/master/script/base64/layers/ipv4) |
| **Internet Protocol Version 6 (IPV6)** | [Subscription Link](https://raw.githubusercontent.com/yyyr-otz/tele-providers-collector/master/script/base64/layers/ipv6) |

'''

# 更新readme
with open('./script/readme-script.md', 'w') as file:
    file.write(f"## Latest Update: {last_update_datetime.strftime('%a, %d %b %Y %X %Z')}\n## Current Update: {current_datetime_update.strftime('%a, %d %b %Y %X %Z')}"+ '\n' + readme)


# 下载vless-sub
""" 
vless_sub_url = 'https://vless-sub.n7p8ri7j.workers.dev/sub/cdn.sethost.eu.org?max=20000&provider=yyyr-otz&original=0&merge=1&fp=edge'
with open('./script/base64/protocols/vless-sub', "w", encoding="utf-8") as vless_sub_file:
    vless_sub = requests.get(vless_sub_url, allow_redirects=True).text.encode("utf-8").decode("utf-8")
    vless_sub_file.write(vless_sub)       

"""
"""
# 遍历当前目录下所有扩展名为.txt的文件
for b64_file in glob.glob(os.path.join(r"./script/base64/protocols/", "*")):
    print (b64_file+"开始解码")
    with open(b64_file, "r") as b64_txt:
        raw_file = base64.b64decode(b64_txt.read()).decode("utf-8")
        # raw_file = base64.urlsafe_b64decode(data.read())
        # 将解码后的内容写入新文件
        raw_path = os.path.join(r"./script/raw/protocols/" , os.path.basename(b64_file))
        with open(raw_path + ".txt", "w") as rawf:
            print (raw_file)
            rawf.write(raw_file)
            print (raw_path+"写入完成")
"""
