# coding:utf-8
'''
生成随机headers
引用案例
from plugins.hander_random import requests_headers
print(requests_headers())
'''

import random

# 生成随机refener
def random_referer():
    dominio = ['Adzuna', 'Bixee', 'CareerBuilder', 'Craigslist', 'Dice', 'Eluta.ca', 'Hotjobs', 'JobStreet', 'Incruit', 'Indeed', 'Glassdoor', 'LinkUp', 'Monster', 'Naukri', 'Yahoo', 'Legal', 'GoogleScholar', 'Lexis', 'Manupatra', 'Quicklaw', 'WestLaw', 'Medical', 'Bing Health', 'Bioinformatic', 'CiteAb', 'EB-eye', 'Entrez', 'mtv', 'ubuntu', 'GenieKnows', 'GoPubMed', 'Healia', 'Healthline', 'Nextbio', 'PubGene', 'Quertle', 'Searchmedica', 'WebMD', 'News', 'BingNews', 'Daylife', 'GoogleNews', 'aol', 'microsoft', 'MagPortal', 'Newslookup', 'Nexis', 'Topix', 'Trapit', 'YahooNews', 'People', 'Comfibook', 'Ex.plode', 'InfoSpace', 'PeekYou', 'Spock', 'Spokeo', 'WorldwideHelpers', 'iPhone', 'Zabasearch', 'ZoomInfo', 'Fizber', 'HotPads', 'Realtor', 'Redfin', 'Rightmove', 'Trulia', 'Zillow', 'Zoopla', 'StuRents', 'globo', 'sbt', 'band', 'cnn', 'blog.inurl.com.br']
    gTLD = ['aero', 'arpa', 'biz', 'com', 'coop', 'edu', 'gov', 'info', 'int', 'mil', 'museum', 'name', 'net', 'org', 'pro', 'tel']
    arquivo = ['admin', 'index', 'wp-admin', 'info', 'shop', 'file', 'out', 'open', 'news', 'add', 'profile', 'search', 'open', 'photo', 'insert', 'view']
    ext = ['exe', 'php', 'asp', 'aspx', 'jsf', 'html', 'htm', 'lua', 'log', 'cgi', 'sh', 'css', 'py', 'sql', 'xml', 'rss']
    pasta = ['App_Files', 'Assets', 'CFFileServlet', 'CFIDE', 'Communication', 'Computers', 'CoreAdminHome', 'CoreHome', 'Crawler', 'Creator', 'DECOM', 'Dashboard', 'Drives', 'Dynamic', 'FCKeditor', 'Feedback', 'Files', 'Flash', 'Forms', 'Help', 'ICEcore', 'IO', 'Image', 'JPG', 'getold', 'JSP', 'KFSI', 'Laguna', 'Login', 'Motors', 'MultiSites', 'NR', 'OCodger', 'RSS', 'Safety', 'Smarty', 'Software', 'Static', 'Stress', 'getfull', 'Sugarcrm', 'Travel', 'UPLOAD', 'Urussanga', 'UserFiles', '__tpl', '_fckeditor', '_info', '_machine', '_plugins', '_sample', '_samples', 'postmost', '_source', '_testcases', 'aaa', 'abelardoluz', 'aberlardoluz', 'aborto', 'about', 'aboutus', 'abuse', 'abusers', 'ac_drives', 'acabamentos', 'mail', 'academias', 'acao', 'acartpro', 'acatalog', 'acc', 'acc_auto_del', 'acc_beep_ken', 'acc_beep_time', 'acc_ch_mail', 'acc_fc_prsc', 'accounts', 'validar', 'acc_html_mark', 'acc_html_rand', 'acc_lan_page', 'acc_pic_html', 'acc_profol', 'acc_soft_link', 'acc_ssd_page', 'acc_syun_ei', 'german', 'intranet', 'old', 'acc_time_go', 'acc_wbcreator', 'accept', 'accepted', 'acceso', 'access', 'accessibility', 'accessories', 'acciones', 'acclg', 'account', 'paste', 'paste22', 'acessorios', 'acontece', 'acougueiro', 'acoustic', 'act', 'action', 'activate', 'active', 'activeden', 'activism', 'actualit', 'actuators', 'ad', 'informatica', 'ad_division', 'ad_rate', 'adapter', 'adapters', 'adaptive', 'adaptivei', 'adatmentes', 'adbanner', 'adblock', 'adboard', 'adclick', 'add-ons', 'add', 'delete', 'added', 'addon', 'address', 'adduser', 'adfree', 'adhoc', 'adinfo', 'adios_papa', 'adlink', 'adlinks', 'acc_folder_vw', 'acc_syun_su']
    locais = ['ac', 'ad', 'ae', 'af', 'ag', 'al', 'am', 'an', 'ao', 'aq', 'ar', 'as', 'at', 'au', 'aw', 'az', 'ba', 'bb', 'bd', 'be', 'bf', 'bg', 'bh', 'bi', 'bj', 'bm', 'bn', 'bw', 'by', 'bz', 'ca', 'cc', 'cd', 'cf', 'cg', 'ch', 'ci', 'ck', 'cl', 'cm', 'cn', 'co', 'cr', 'cu', 'cv', 'cx', 'cy', 'cz', 'de', 'dj', 'dk', 'dm', 'do', 'dz', 'bo', 'br', 'ec', 'ee', 'eg', 'er', 'es', 'et', 'eu', 'fi', 'fj', 'fk', 'fm', 'fo', 'fr', 'ga', 'gb', 'gd', 'ge', 'gf', 'gg', 'gh', 'gi', 'gl', 'gm', 'gn', 'gp', 'gq', 'gr', 'bs', 'bt', 'gs', 'gt', 'gu', 'gw', 'gy', 'hk', 'hm', 'hn', 'hr', 'ht', 'hu', 'id', 'ie', 'il', 'im', 'in', 'io', 'iq', 'ir', 'is', 'it', 'je', 'jm', 'jo', 'jp', 'ke', 'kg', 'bv', 'kh', 'ki', 'km', 'kn', 'kr', 'kw', 'ky', 'kz', 'la', 'lb', 'lc', 'li', 'lk', 'lr', 'ls', 'lt', 'lu', 'lv', 'ly', 'ma', 'mc', 'md', 'me', 'mg', 'mh', 'mk', 'ml', 'mm', 'mn', 'mo', 'mp', 'mq', 'mr', 'ms', 'mt', 'mu', 'mv', 'mw', 'mx', 'my', 'mz', 'nb', 'nc', 'ne', 'nf', 'ng', 'ni', 'nl', 'no', 'np', 'nr', 'nu', 'nz', 'om', 'pa', 'pe', 'pf', 'pg', 'ph', 'pk', 'pl', 'pm', 'pn', 'pr', 'ps', 'pt', 'pw', 'py', 'qa', 're', 'ro', 'ru', 'rw', 'sa', 'sb', 'sc', 'sd', 'se', 'sg', 'sh', 'si', 'sj', 'sk', 'sl', 'sm', 'sn', 'so', 'sr', 'ss', 'st', 'su', 'sv', 'sy', 'sz', 'tc', 'td', 'tf', 'tg', 'th', 'tj', 'tk', 'tl', 'tm', 'tn', 'to', 'tr', 'tt', 'tv', 'tw', 'tz', 'ua', 'ug', 'uk', 'um', 'us', 'uy', 'uz', 'va', 'vc', 've', 'vg', 'vi', 'vn', 'vu', 'wf', 'ws', 'ye', 'yt', 'yu', 'za', 'zm', 'zw', 'ai']
    return "http://www." + random.choice(dominio).lower() + "." + random.choice(gTLD) + "." + random.choice(locais) + "/" + random.choice(pasta) + "/" + random.choice(arquivo) + "." + random.choice(ext)

# 生成随机useragent
def random_useragent():
    agentBrowser = ['Firefox', 'Safari', 'Opera', 'Flock', 'Internet Explorer', 'Seamonkey', 'Tor Browser', 'GNU IceCat', 'CriOS', 'TenFourFox', 'SeaMonkey', 'B-l-i-t-z-B-O-T', 'Konqueror', 'Mobile', 'Konqueror', 'Netscape', 'Chrome', 'Dragon', 'SeaMonkey', 'Maxthon', 'IBrowse', 'K-Meleon', 'GoogleBot', 'Konqueror', 'Minimo', 'Googlebot', 'WeltweitimnetzBrowser', 'SuperBot', 'TerrawizBot', 'YodaoBot', 'Wyzo', 'Grail', 'PycURL', 'Galaxy', 'EnigmaFox', '008', 'ABACHOBot', 'Bimbot', 'Covario IDS', 'iCab', 'KKman', 'Oregano', 'WorldWideWeb', 'Wyzo', 'GNU IceCat', 'Vimprobable', 'uzbl', 'Slim Browser', 'Flock', 'OmniWeb', 'Rockmelt', 'Shiira', 'Swift', 'Pale Moon', 'Camino', 'Flock', 'Galeon', 'Sylera']
    agentSistema = ['Windows 3.1', 'Windows 95', 'Windows 98', 'Windows 2000', 'Windows NT', 'Linux 2.4.22-10mdk', 'FreeBSD', 'Windows XP', 'Windows Vista', 'Redhat Linux', 'Ubuntu', 'Fedora', 'AmigaOS', 'BackTrack Linux', 'iPad', 'BlackBerry', 'Unix', 'CentOS Linux', 'Debian Linux', 'Macintosh', 'Android', 'iPhone', 'Windows NT 6.1', 'BeOS', 'OS 10.5', 'Nokia', 'Arch Linux', 'Ark Linux', 'BitLinux', 'Conectiva (Mandriva)', 'CRUX Linux', 'Damn Small Linux', 'DeLi Linux', 'Ubuntu', 'BigLinux', 'Edubuntu', 'Fluxbuntu', 'Freespire', 'GNewSense', 'Gobuntu', 'gOS', 'Mint Linux', 'Kubuntu', 'Xubuntu', 'ZeVenOS', 'Zebuntu', 'DemoLinux', 'Dreamlinux', 'DualOS', 'eLearnix', 'Feather Linux', 'Famelix', 'FeniX', 'Gentoo', 'GoboLinux', 'GNUstep', 'Insigne Linux', 'Kalango', 'KateOS', 'Knoppix', 'Kurumin', 'Dizinha', 'TupiServer', 'Linspire', 'Litrix', 'Mandrake', 'Mandriva', 'MEPIS', 'Musix GNU Linux', 'Musix-BR', 'OneBase Go', 'openSuSE', 'pQui Linux', 'PCLinuxOS', 'Plaszma OS', 'Puppy Linux', 'QiLinux', 'Red Hat Linux', 'Red Hat Enterprise Linux', 'CentOS', 'Fedora', 'Resulinux', 'Rxart', 'Sabayon Linux', 'SAM Desktop', 'Satux', 'Slackware', 'GoblinX', 'Slax', 'Zenwalk', 'SuSE', 'Caixa Mágica', 'HP-UX', 'IRIX', 'OSF/1', 'OS-9', 'POSYS', 'QNX', 'Solaris', 'OpenSolaris', 'SunOS', 'SCO UNIX', 'Tropix', 'EROS', 'Tru64', 'Digital UNIX', 'Ultrix', 'UniCOS', 'UNIflex', 'Microsoft Xenix', 'z/OS', 'Xinu', 'Research Unix', 'InfernoOS']
    locais = ['cs-CZ', 'en-US', 'sk-SK', 'pt-BR', 'sq_AL', 'sq', 'ar_DZ', 'ar_BH', 'ar_EG', 'ar_IQ', 'ar_JO', 'ar_KW', 'ar_LB', 'ar_LY', 'ar_MA', 'ar_OM', 'ar_QA', 'ar_SA', 'ar_SD', 'ar_SY', 'ar_TN', 'ar_AE', 'ar_YE', 'ar', 'be_BY', 'be', 'bg_BG', 'bg', 'ca_ES', 'ca', 'zh_CN', 'zh_HK', 'zh_SG', 'zh_TW', 'zh', 'hr_HR', 'hr', 'cs_CZ', 'cs', 'da_DK', 'da', 'nl_BE', 'nl_NL', 'nl', 'en_AU', 'en_CA', 'en_IN', 'en_IE', 'en_MT', 'en_NZ', 'en_PH', 'en_SG', 'en_ZA', 'en_GB', 'en_US', 'en', 'et_EE', 'et', 'fi_FI', 'fi', 'fr_BE', 'fr_CA', 'fr_FR', 'fr_LU', 'fr_CH', 'fr', 'de_AT', 'de_DE', 'de_LU', 'de_CH', 'de', 'el_CY', 'el_GR', 'el', 'iw_IL', 'iw', 'hi_IN', 'hu_HU', 'hu', 'is_IS', 'is', 'in_ID', 'in', 'ga_IE', 'ga', 'it_IT', 'it_CH', 'it', 'ja_JP', 'ja_JP_JP', 'ja', 'ko_KR', 'ko', 'lv_LV', 'lv', 'lt_LT', 'lt', 'mk_MK', 'mk', 'ms_MY', 'ms', 'mt_MT', 'mt', 'no_NO', 'no_NO_NY', 'no', 'pl_PL', 'pl', 'pt_PT', 'pt', 'ro_RO', 'ro', 'ru_RU', 'ru', 'sr_BA', 'sr_ME', 'sr_CS', 'sr_RS', 'sr', 'sk_SK', 'sk', 'sl_SI', 'sl', 'es_AR', 'es_BO', 'es_CL', 'es_CO', 'es_CR', 'es_DO', 'es_EC', 'es_SV', 'es_GT', 'es_HN', 'es_MX', 'es_NI', 'es_PA', 'es_PY', 'es_PE', 'es_PR', 'es_ES', 'es_US', 'es_UY', 'es_VE', 'es', 'sv_SE', 'sv', 'th_TH', 'th_TH_TH', 'th', 'tr_TR', 'tr', 'uk_UA', 'uk', 'vi_VN', 'vi'] 
    
    headers = []
    for _ in range(3):
        header = random.choice(agentBrowser) + "/" + str(random.randint(1, 20)) + "." + str(random.randint(1, 20)) + " (" + random.choice(agentSistema) + " " + str(random.randint(1, 7)) + "." + str(random.randint(0, 9)) + "; " + random.choice(locais) + ")"
        headers.append(header) 
    return " ".join(headers)

def generate_accept():
    return "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"

def generate_accept_language():
    languages = ["en-US,en;q=0.9", "en-GB,en;q=0.8", "fr-FR,fr;q=0.9", "de-DE,de;q=0.8", "es-ES,es;q=0.8"]
    return random.choice(languages)

# 生成随机的X-Forwarded-For、X-Originating-Ip、X-Remote-Addr、X-Remote-Ip
def generate_random_headers_X():
    # 生成随机IP地址
    def generate_random_ip():
        ip = []
        for _ in range(4):
            ip.append(str(random.randint(0, 255)))
        return '.'.join(ip)
    
    headers = {
        'X-Forwarded-For': generate_random_ip(),
        'X-Originating-Ip': generate_random_ip(),
        'X-Remote-Addr': generate_random_ip(),
        'X-Remote-Ip': generate_random_ip()
    }
    return headers

# 合并上述函数生成随机headers
def requests_headers():
    headers = {
        'User-Agent':random_useragent(),
        "Referer": random_referer(),
        'Upgrade-Insecure-Requests':'1',
        'Connection':'keep-alive',
        'Cache-Control':'max-age=0',
        'Accept': generate_accept(),
        'Accept-Encoding':'gzip, deflate, sdch',
        'Accept-Language': generate_accept_language(),
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'close',
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
    }
    random_headers = generate_random_headers_X()
    headers = headers.copy()  # 复制现有的请求头
    headers.update(random_headers)  # 将随机生成的请求头追加到现有的请求头

    return headers