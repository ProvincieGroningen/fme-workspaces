import requests, lxml.html, json, datetime, os.path

username = 'gebruikersnaam'
password = 'wachtwoord'
url_home = 'https://ovbureau.haltescan.nl'
url_auth = 'https://ovbureau.haltescan.nl/auth/login'
path_out = 'c:\\Temp'

s = requests.session()

login_headers = {"Host": "ovbureau.haltescan.nl",
                 "Connection": "keep-alive",
                 "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
                 "Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
                 "Accept-Encoding": "gzip, deflate, br",
                 "Accept-Language": "en-US,en;q=0.9"}

login = s.get(url_home, headers = login_headers, timeout = 5)

login_html = lxml.html.fromstring(login.text)

data = {"username": username, "password": password}
                 
form_headers = {"Accept": "application/json, text/javascript, */*; q=0.01",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.9",
                "Connection": "keep-alive",
                "Content-length": str(len(str(data))),
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "DNT": "1",
                "Cookie": "haltescan-dev=" + s.cookies["haltescan-dev"],
                "Host": "ovbureau.haltescan.nl",
                "Origin": "https://ovbureau.haltescan.nl",
                "Referer": "https://ovbureau.haltescan.nl/",
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
                "X-CSRF-Token": str(login_html.xpath(r'//form//input[@name="csrf_token"]/@value')[0]),
                "X-Requested-With": "XMLHttpRequest"}

response = s.post(url_auth, data = json.dumps(data), headers = form_headers, timeout = 5)

f = s.get("https://ovbureau.haltescan.nl/batch/quays/xlsx?filetype=xlsx&type=basic&delimiter=%3B&from_mutation_date=&location=provinceId.0&category=&status=")

filename = datetime.datetime.now().strftime('Haltescan%Y%m%d%H%M%S.xlsx')

open(os.path.join(path_out, filename), 'wb').write(f.content)