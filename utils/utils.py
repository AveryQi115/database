from django.contrib.auth.models import User
import requests
from lxml import etree

DEPARTMENTS = (
        ('A','Anaesthesiology and Adult Intensive Care Department'),
        ('C','Child Surgical Department'),
        ('G','General and Vascular Surgical Department'),
        ('D','Dermatology'),
        ('O','Obstetric and Maternity Ward'),
        ('I','Internal Department'),
        ('L','Laryngology'),
        ('N','Neurology'),
        ('F','First-Aid Department'),
    )

GENDERS = (
        ('F', 'Female'),
        ('M', 'Male'),
    )

TITLES = (
        ('RN','RN'),
        ('CN','CNP'),
        ('PA','PA'),
        ('PH','Physician'),
    )

def getDepartment(s):
    if not s:
        return ''

    for i in DEPARTMENTS:
        if i[0]==s:
            return i[1]

def getGender(s):
    if not s:
        return ''

    for i in GENDERS:
        if i[0]==s:
            return i[1]

def getTitle(s):
    if not s:
        return ''

    for i in TITLES:
        if i[0]==s:
            return i[1]

def getDoctorName(d):
    if not d:
        return ''
    return d.name

def getUserGroup(id):
    group = 'patient'
    try:
        myuser = User.objects.get(id=id)
        for g in myuser.groups.all():
            group = g.__str__()
    except Exception as e:
        print(e)

    return group

def scraper():
    url = "https://go.drugbank.com/drugs"
    headers = {
        'cookie': 'cf_chl_prog=a12; cf_clearance=495fbda43b872054e89a03e4b13087fe56744c76-1623842881-0-250; _ga=GA1.2.1787877697.1623842882; _gid=GA1.2.1277953112.1623842882; _gat=1; _clck=15hrmls; __hstc=49600953.a974b156c74b89db73e6dc0a47ce7006.1623842883110.1623842883110.1623842883110.1; hubspotutk=a974b156c74b89db73e6dc0a47ce7006; __hssrc=1; __hssc=49600953.1.1623842883110; messagesUtk=6bf47eca0b79432d9e6b39b092dba92c; _clsk=4mxj2t|1623842885566|1|1|vmss-eus2/collect; _omx_drug_bank_session=K01QdWNKRGNIWnk0cDBPMUFDbzJIV2ZtcFJ3dGxuMnl1THZhTkduN0VLUlVvbnNHSEFXVE93azhZMFpGai96L1VZYkswVlZBdXpaQlBFWWdoNjhSSy9FM1hGMGxnRnNvamhoRjZvQ01xYmVzclFBamRPSmQyRUxULzVBK3ErZ3MzdDVEa1VhYnRsMnpTUTFvS0JDZzBnPT0tLVB3WVBtdzFkMi81VzUvZk04KzQzU0E9PQ%3D%3D--aed4d4b549776ec6d7d1e96fea3456ed4b5efc7b',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'
    }
    resp = requests.get(url = url, headers=headers)
    print(resp.status_code)
    print(resp.text)
    drugs = {"names":[],"costs":[]}
    if (resp.status_code==200):
        res = etree.HTML(resp.text)
        names = res.xpath('//td[contains(@class,"drug-name")]//a')
        for name in names:
            drug_name = name.xpath('./text()')[0]
            drugs["names"].append(drug_name)
        
        weights = res.xpath('//td[contains(@class,"weight-value")]/br/preceding-sibling::text()')
        for weight in weights:
            drugs["costs"].append(weight)
        return drugs

    return drugs


