#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt
import pdfplumber
from io import BytesIO
import unicodedata
import re
import os

def get_reportfn():
    url = 'https://www.udape.gob.bo/index.php?option=com_content&view=article&id=220:reporte-covid-19&catid=41'
    html = BeautifulSoup(requests.get(url).text, 'html.parser')
    fn = html.select('#table1 li a')[0]['href'].split('/')[-1]
    return fn

def reportfn2date(fn):
    match = re.findall('([0-9]*_[0-9]*_[0-9]*21)', reportfn)[0]
    dateformat = '%d_%m_%Y' if len(match.split('_')[-1]) == 4 else '%d_%m_%y'
    return dt.datetime.strptime(match, dateformat).date()

def get_last(fn):
    return pd.read_csv(fn, parse_dates=[0], index_col=0).index[-1].date()

def normie(text):
    return unicodedata.normalize(u'NFKD', ' '.join(text.lower().split())).encode('ascii', 'ignore').decode('utf8')

def is_diario(text):
    return len(re.findall('.*casos confirmados, fallecidos y recuperados por departamento por dia, del [0-9\/]*', text)) != 0

def is_acumulado(text):
    return len(re.findall('.*casos acumulados de confirmados, activos, fallecidos y recuperados por departamento, del [0-9\/]*', text)) != 0

def month_matcher(text):
    months = {'ago':8, 'oct':10, 'may':5, 'jul':7, 'sep':9, 'jun':6, 'nov':11, 'abr':4, 'dic':12, 'mar':3, 'ene':1, 'feb':2}
    return months[text]

def get_data_diarios(page):
    table = pd.DataFrame(page.extract_tables()[0]).T.drop(columns=[1])
    table.columns = table.iloc[0].apply(lambda _ : _.replace('(*)','').strip()).tolist()
    table = table[1:]
    for i, row in table.iterrows():
        if row['Departamento'] != None:
            fecha = row['Departamento']
            ii = 0
            confirmados_diarios.append([fecha] + row[columns].tolist())
        else:
            if ii == 0:
                decesos_diarios.append([fecha] + row[columns].tolist())
                ii += 1
            else:
                recuperados_diarios.append([fecha] + row[columns].tolist())

def get_data_acumulados(page):
    table = pd.DataFrame(page.extract_tables()[0]).T.drop(columns=[1])
    table.columns = table.iloc[0].apply(lambda _ : _.replace('(*)','').strip()).tolist()
    table = table[1:]
    for i, row in table.iterrows():
        if row['Departamento'] != None:
            fecha = row['Departamento']
            ii = 0
            confirmados_acumulados.append([fecha] + row[columns].tolist())
        else:
            if ii == 0:
                activos_acumulados.append([fecha] + row[columns].tolist())
                ii += 1
            elif ii == 1:
                decesos_acumulados.append([fecha] + row[columns].tolist())
                ii += 1
            else:
                recuperados_acumulados.append([fecha] + row[columns].tolist())
                
def format_date(text):
    global whatyear
    month = month_matcher(text.split('-')[1][:3])
    day = int(text.split('-')[0])
    if month == 1 and day == 1:
        whatyear += 1
    return dt.datetime(whatyear, month_matcher(text.split('-')[1][:3]), int(text.split('-')[0]))

def make_dataframe(data, filename):
    global whatyear
    whatyear = 2021
    df = pd.DataFrame(data, columns=['Fecha'] + columns)
    df = df.replace(to_replace='', value=0)
    df = df.replace(to_replace='\.', value='', regex=True)
    df.Fecha = df.Fecha.apply(lambda _: format_date(_))
    df[columns] = df[columns].astype(int)
    df = pd.concat([pd.read_csv(filename+'.csv', parse_dates=[0]).rename(columns={'Unnamed: 0': 'Fecha'}), df]).drop_duplicates(subset=['Fecha'], keep='last').set_index('Fecha')
    df[df.index <= report_day].sort_index().to_csv(filename+'.csv', index_label='')

# Nuevo reporte?
reportfn = get_reportfn()
last = get_last('confirmados_diarios.csv')
if last < reportfn2date(reportfn):

    report_day = reportfn2date(reportfn).strftime('%Y-%m-%d')
    report_url = 'https://www.udape.gob.bo/portales_html/ReporteCOVID/R_diario/' + reportfn
    columns = ['Chuquisaca', 'La Paz', 'Cochabamba', 'Oruro', 'Potosí', 'Tarija', 'Santa Cruz', 'Beni', 'Pando']
    empty = pd.DataFrame(index = pd.date_range('2020-03-10', report_day), columns=columns).fillna(0)
    whatyear = 2020

    # Cargo el reporte
    req = requests.get(report_url)
    if req.status_code != 200:
        raise SystemError("El enlace es incorrecto")
    try:
        pdf = pdfplumber.open(BytesIO(req.content))
    except Exception:
        raise SystemError("Error al cargar el pdf")

    # Donde acopio datos
    confirmados_diarios, decesos_diarios, recuperados_diarios = [],[],[]
    confirmados_acumulados, activos_acumulados, recuperados_acumulados, decesos_acumulados = [], [], [], []
    diario_pages, acumulado_pages = [], []

    # Una ojeada para encontrar las páginas que me interesan
    for i, page in enumerate(pdf.pages):
        pagetext = normie(page.extract_text())
        if is_diario(pagetext):
            diario_pages.append(page)
        if is_acumulado(pagetext):
            acumulado_pages.append(page)

    # procesar datos para casos diarios
    for page in reversed(diario_pages):
        get_data_diarios(page)

    make_dataframe(confirmados_diarios, 'confirmados_diarios')
    make_dataframe(decesos_diarios, 'decesos_diarios')
    make_dataframe(recuperados_diarios, 'recuperados_diarios')

    # procesar datos para casos acumulados
    for page in reversed(acumulado_pages):
        get_data_acumulados(page)
    
    make_dataframe(confirmados_acumulados, 'confirmados_acumulados')
    make_dataframe(activos_acumulados, 'activos_acumulados')
    make_dataframe(decesos_acumulados, 'decesos_acumulados')
    make_dataframe(recuperados_acumulados, 'recuperados_acumulados')

    print(report_day)
