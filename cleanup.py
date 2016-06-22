# -*- coding: utf-8 -*-
"""
Created on Thu May 05 17:23:38 2016

@author: Dario
"""

import pandas as pd
from unidecode import unidecode
import re

def normalize_puesto(pstr):
    pstr = unidecode(unicode(pstr,'windows-1252')).strip().lower()
    pstr = re.sub('\(.*?\)','', pstr)
    return pstr
def load_data(path='cs_DGII_Nomina_2016.csv',sep=';'):
    df = cleanup(pd.read_csv(path,sep))
    return df
def cleanup(df):
    df.columns = [x.strip().translate(None,',').lower() for x in df.columns.values]
    # parse salaries
    df.salario = df.salario.apply(lambda x: x.translate(None,',').strip())
    df.salario = df.salario.astype(float)
    # cleanup puesto
    df['puesto_clean'] = df.puesto.apply(normalize_puesto)
    df.drop(['puesto'],axis=1,inplace=True)
    df.rename(columns={'puesto_clean':'puesto'},inplace=True)
    #
    df['salariok'] = df.salario.div(1000).round(4)
    #
    return df
def split_by_month(df):
    ene = df[df.mes == 'ene-16']
    feb = df[df.mes == 'feb-16']
    return (ene, feb)

def prepare():
    df = load_data()
    ene, feb = split_by_month(df)
    return ene, feb

if __name__ == '__main__':
    ene, feb = prepare()
    ene.to_csv('dgii_ene_2016.csv',index=False)
    feb.to_csv('dgii_feb_2016.csv',index=False)
    df.to_csv('dgii_clean.csv',index=False)
