# -*- coding: utf-8 -*-
"""
Created on Tue Jun 14 14:10:08 2022

@author: man Yip
"""
import pandas as pd
from DagLpDp import DAGLP
import numpy as np

def value_counts_weight(data,weight=None):
    if not isinstance(data,pd.core.series.Series):
        data = pd.Series(data)
    data.name = 'data'
        
    if weight is None:
        weight=pd.Series(np.ones_like(data),index=data.index)
    elif not isinstance(weight,pd.core.series.Series):
        weight = pd.Series(weight)
    weight = weight.loc[data.index]
    weight.name = 'weight'
    
    df = pd.concat([data,weight],axis=1)
    distr = df.groupby('data',dropna=False)['weight'].sum()
    distr = distr / distr.sum()
    return distr

def trancate_by_distr(distr,min_distr):
    tmp = distr.loc[distr.index.notna()]
    curr=0
    rm_points = []
    for k,v in tmp.items():
        curr+=v
        if curr < min_distr:
            rm_points.append(k)
        else:
            rm_points.append(k) #由于是右开区间，所以需要游标多走一位
            break
    
    tmp2 = tmp.iloc[::-1]
    curr=0
    for k,v in tmp2.items():
        curr+=v
        if curr < min_distr:
            rm_points.append(k)
        else:
            break        
    return list(tmp.loc[~tmp.index.isin(rm_points)].index.values)

def gen_connect_table(legal_points,distr,threshold_distr,min_distr):
    distr_notna = distr.loc[distr.index.notna()]
    ma = distr_notna.keys().max() 
    distr_notna[ma + 0.001] = 0   
    legal_points = legal_points+[ma + 0.001]     
    tables={}
    curr_from = distr_notna.keys().min()
    cursor = 0
    while(cursor < len(legal_points)):
        for end in legal_points[cursor:]:
            v = distr_notna.loc[curr_from:end].sum() - distr_notna.loc[end]
            if v >= min_distr:
                tables[(curr_from,end)] = -1 * (v-threshold_distr)**2
                # tables[(curr_from,end)] = 1 / (v-threshold_distr)**2
        curr_from = legal_points[cursor]  
        cursor+=1
    return tables

def freq_cut(data,threshold_distr,min_distr,weight=None):
    if threshold_distr > 1:
        threshold_distr = 1/threshold_distr
    distr = value_counts_weight(data,weight)
    legal_points = trancate_by_distr(distr,min_distr)
    tables = gen_connect_table(legal_points,distr,threshold_distr,min_distr)
    dlp = DAGLP(tables)
    fc = [v for k,v in dlp.nodePV.items() if k in dlp.ends]
    if len(fc) == 0:
        return ['[%s,%s]'%(distr.keys().min(),distr.keys().max())]
    fc = fc[0][0]
    bins = []
    for i,v in enumerate(fc):
        if i < len(fc)-2:
            tmp = '[%s,%s)'%(v,fc[i+1])
            bins.append(tmp)
        elif i == len(fc)-2:
            tmp = '[%s,%s]'%(v,distr.keys().max())
            bins.append(tmp)  
    def _sort(s):
        v1 = s[s.index('[')+1 : s.index(',')]
        return float(v1) 
    return sorted(bins,key = _sort) 


def cut_by_bins(data,bins):
    data_bin = pd.Series(data)
    mi = data_bin.min()
    ma = data_bin.max()
    label = data_bin.copy()
    label = label.apply(str)
    for i,b in enumerate(bins):
        coma = b.index(',')
        v1 = float(b[1:coma])
        if i == 0 and mi < v1:
            v1 = mi
            b = '%s%s%s'%(b[0],v1,b[coma:])
            coma = b.index(',')
            
        if b[0] =='[':
            cond1 = data_bin>=v1
        elif b[0]=='(':
            cond1 = data_bin>v1
        
        v2 = float(b[coma+1:-1])
        if i == len(bins)-1 and ma > v2:
            v2 = ma
            b = '%s%s%s'%(b[:coma+1],v2,b[-1])
            
        if b[-1] ==']':
            cond2 = data_bin <= v2
        elif b[-1]==')':
            cond2 = data_bin < v2
        label.loc[cond1 & cond2] = b
    label.loc[label=='nan']=None
    return label

def freq_cut_array(datas,threshold_distr,min_distr,cutby=0,weight=None):
    data = datas[cutby]
    bins = freq_cut(data,threshold_distr,min_distr,weight)
    gmin = pd.Series(data).min()
    gmax = pd.Series(data).max()
    
    for i in datas:
        i = pd.Series(i)
        imin = i.min()
        imax = i.max()
        if imin < gmin:
            gmin = imin
        if imax > gmax:
            gmax = imax
    bins[0] = '[%s%s'%(gmin,bins[0][bins[0].index(','):])
    bins[-1] = '%s,%s]'%(bins[-1][:bins[-1].index(',')],gmax)  
    
    label_arr = []
    for i in datas:
       tmp =  cut_by_bins(i,bins)
       label_arr.append(tmp)
    
    return label_arr  