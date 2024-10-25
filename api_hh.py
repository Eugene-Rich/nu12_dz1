# Анализ вакансий
import requests
import pprint
import json

def anvak(snippet, msna):   # Процедура анализа вакансий

    requirement = snippet['requirement']

    if requirement == None:
        return

    # print(requirement)

    if 'СКД' in requirement:
        msna.append('СКД')
    elif 'SQL' in requirement:
        msna.append('SQL')
    elif 'XDTO' in requirement:
        msna.append('XDTO')
    elif 'НТТР' in requirement:
        msna.append('НТТР-сервисы')
    elif 'WEB' in requirement:
        msna.append('WEB-сервисы')
    elif 'БСП' in requirement:
        msna.append('БСП')
    elif 'библиотеками стандартных подсистем' in requirement:
        msna.append('БСП')
    elif 'аличие сертификатов' in requirement:
        msna.append('Наличие сертификатов')
    elif 'апросы' in requirement:
        msna.append('Язык запросов')
    elif 'латформ' in requirement:
        msna.append('Знание платформы')
    elif 'Грамотное общение' in requirement:
        msna.append('Грамотное общение')
    elif 'типовы' in requirement:
        msna.append('Знание типовых конфигураций')
    elif 'нтеграц' in requirement:
        msna.append('Интеграция с другими программами')
    elif 'УТ 10.3' in requirement:
        msna.append('Знание УТ 10.3')
    elif 'УТ 11' in requirement:
        msna.append('Знание УТ 11')
    elif 'БП 3.0' in requirement:
        msna.append('Знание БП 3.0')
    elif 'ЗУП' in requirement:
        msna.append('Знание ЗУП')
    elif 'управля' in requirement:
        msna.append('Владение управляемыми формами')
    elif 'ринципов бухг' in requirement:
        msna.append('Знание основных принципов бухгалтерского учета')
    elif 'способность к обучению' in requirement:
        msna.append('Способность к обучению')
    elif 'Опыт обновления не типовых конфигураций' in requirement:
        msna.append('Опыт обновления не типовых конфигураций')
    elif 'бмен' in requirement:
        msna.append('Опыт работы с обменами')

url = 'https://api.hh.ru/vacancies'

sh_params = {
    'text': 'NAME:(Программист 1с) AND Иркутск'
}

params = sh_params
params['page'] = 1
result = requests.get(url, params=params).json()
#pprint.pprint(result)

msna = []

for itms in result['items']:
    sn = itms['snippet']
    anvak(sn, msna)

kolvos = result['pages']
vsegovak = result['per_page']

for iss in range(2, kolvos+1):

    params = sh_params
    params['page'] = iss

    result = requests.get(url, params=params).json()

    vsegovak = vsegovak + result['per_page']

    for itms in result['items']:
        sn = itms['snippet']
        anvak(sn, msna)

# Обработка накопленных требований по вакансиям

tre = []
kovt = []
proce = []

# Сначала подсчитаем количество требований по вакансии
for itm in msna:
    if itm in tre:
        indx = tre.index(itm)
        kovt[indx] = kovt[indx] + 1
    else:
        tre.append(itm)
        kovt.append(1)

# Подсчитаем проценты
for itm in range(0, len(tre)):
    rproc = round((kovt[itm] / len(tre)) * 100, 1)
    proce.append(rproc)

# Формирование и вывод JSON - файла

requ = []
for itm in range(0, len(tre)):
    nd = {'name': tre[itm],'count': kovt[itm],'persent': proce[itm]}
    requ.append(nd)

to_json = [{'keywords': 'Программист 1С', 'count': vsegovak, 'requirements': requ}]
#pprint.pprint((to_json))
#print()

with open('hh_requ.json', 'w') as f:
    json.dump(to_json, f)

with open('hh_requ.json') as f:
    pprint.pprint(json.loads(f.read()))

