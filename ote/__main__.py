#!/usr/bin/env python3

import html2text
import json
import os.path
import random
import re
import requests
import string
import sys
import time
import webbrowser

reader = html2text.HTML2Text()
reader.ignore_links = False


def create_email(username='', secure=False):
    domains = ['esiix.com', 'wwjmp.com', '1secmail.com', '1secmail.org', '1secmail.net']
    domain = random.choice(domains)
    if secure:
        ''.join(random.choices(string.ascii_lowercase + string.digits, k=20)), domain
    elif username:
        username, domain
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10)), domain

def check_inbox(username, domain):
    return requests.get(f'https://www.1secmail.com/api/v1/?action=getMessages&login={username}&domain={domain}').json()

def get_email(username, domain, ID):
    return requests.get(f'https://www.1secmail.com/api/v1/?action=readMessage&login={username}&domain={domain}&id={ID}').json()['body']

def entropy(string):
    digits = re.findall(r'\d', string)
    lowerAlphas = re.findall(r'[a-z]', string)
    upperAlphas = re.findall(r'[A-Z]', string)
    entropy = len(set(digits + lowerAlphas + upperAlphas))
    if not digits:
        entropy = entropy/2
    return entropy

def is_random(string):
    if re.match(r'[/=][A-Fa-f0-9]{14,}[/&]?', string):
        return True
    elif re.match(r'[/=][A-Za-z0-9+/_=]{30,}[/&]?', string):
        return True
    else:
        long_strings = re.findall(r'[/=][A-Za-z0-9+/_=]+[/&]?', string)
        for long_string in long_strings:
            if entropy(long_string) > 10:
                return True
    return False

def get_otp_link(links):
    for link in links:
        if is_random(link):
            return link

def get_otp(text):
    digits = re.search(r'[\s*](\d{4,10})[\s*]', text)
    sep_digits = re.search(r'[\s*]((?:\d-){3,8}\d)[\s*]', text)
    if digits:
        return digits.group(1)
    elif sep_digits:
        return sep_digits.group(1)

def handle_email(email):
    no_links_text = reader.handle(email)
    otp = get_otp(no_links_text)
    reader.ignore_links = False
    links_text = reader.handle(email)
    links = re.findall(r'https?://[^/]+\.[^/]+/[^\s)]+', links_text)
    otp_link = get_otp_link(links)
    if otp and otp_link:
        if email.find(otp) > email.find(otp_link):
            return otp_link
        return otp
    elif otp_link:
        return otp_link
    return otp

def start_process(username, domain):
    emails = check_inbox(username, domain)
    last_id = int(emails[-1]['id']) if emails else 0
    while True:
        emails = check_inbox(username, domain)
        if emails:
            ID = int(emails[-1]['id'])
            if ID <= last_id:
                continue
            email_body = get_email(username, domain, ID)
            otp = handle_email(email_body)
            if otp:
                print(otp)
                inp = input('> ')
                if inp.strip().lower() == 'f':
                    print(f'https://www.1secmail.com/mailbox/?action=readMessage&id={ID}&login={username}&domain={domain}')
                    break
                elif inp.strip().lower() == 'q':
                    quit()
                elif inp.strip().lower() == 'o' and otp.startswith(o):
                    webbrowser.open(otp)
                    break
                elif inp.strip().lower() == 'i':
                    webbrowser.open(f'https://www.1secmail.com/?login={username}&domain={domain}')
                    break
            else:
                print(f'https://www.1secmail.com/mailbox/?action=readMessage&id={ID}&login={username}&domain={domain}')
                break
        time.sleep(5)

def get_config_path():
    config_path = '.otp'
    if sys.platform.startswith('linux'):
        config_path = os.getenv('XDG_CONFIG_HOME', os.path.expanduser("~/.config")) + "/.otp"
    return config_path

def save_config(username, domain):
    config_path = get_config_path()
    with open(config_path, 'w+') as file:
        json.dump({'username': username, 'domain': domain}, file)
    print(f'configuration saved to {config_path}')

def load_config():
    config_path = get_config_path()
    if not os.path.isfile(config_path):
        return '', ''
    with open(config_path, 'r') as config_file:
        data = json.load(config_file)
        return data['username'], data['domain']

def main():
    if len(sys.argv) > 1:
        if sys.argv[1].strip().lower() == 'init':
            username, domain = create_email(secure=True)
            if len(sys.argv) > 2:
                username, domain = create_email(sys.argv[2])
            save_config(username, domain)
        else:
            quit('invalid arguments\n\nExamples:\n> otp\n> otp init\n> otp init myusername')
    else:
        username, domain = load_config()
        if not username:
            username, domain = create_email()
        print(f'{username}@{domain}')
        try:
            start_process(username, domain)
        except KeyboardInterrupt:
            pass

if __name__ == "__main__":
    main()
