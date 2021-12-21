#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 21:11:51 2021

@author: xinyi
"""
import json
import matplotlib.pyplot as plt
import pandas as pd


def draw_piechart(record):
    labels = list()
    percentage = list()
    for key in record:
        labels.append(key)
        percentage.append(float(record[key][:-1]))
    fig, ax = plt.subplots()
    ax.pie(percentage, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    ax.axis('equal') 
    plt.style.use('ggplot')
    plt.show()
    return
    
def draw_barchart(record):
    percentage = {"positive":[], "negative":[], "neutral":[]}
    categ = []
    for key in record:
        categ.append(key)
        for sen in record[key]:
            percentage[sen].append(float(record[key][sen][:-1]))
    df = pd.DataFrame(percentage, index=categ)
    df.plot(kind="bar",stacked=True, color=['mediumseagreen', 'lightcoral', 'cornflowerblue'])
    plt.legend()
    plt.style.use('ggplot')
    plt.show()
    return 
    

def main():
    
    #with open("../data/more_analysis.json") as fin:
    #    record = json.load(fin)
        
    categ_percent = {
      "efficacy": "21.9%",
      "mandate": "22.4%",
      "political": "11.5%",
      "children": "5.4%",
      "side_effect": "11.3%",
      "information": "9.3%",
      "unvax": "13.0%",
      "spread": "5.1%"
    }
    draw_piechart(categ_percent)
    
    senti_percent = {"positive": "41.2%", "negative": "38.0%", "neutral": "20.8%"}
    draw_piechart(senti_percent)
    
    with open("../data/sen_per_categ.json") as fin:
        record = json.load(fin)
    draw_barchart(record)


    return


if __name__ == "__main__":
    main()