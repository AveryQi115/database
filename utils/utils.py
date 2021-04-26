from django.contrib.auth.models import User


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
            if g.__str__()=='doctor':
                group = 'doctor'
    except Exception as e:
        print(e)

    return group

