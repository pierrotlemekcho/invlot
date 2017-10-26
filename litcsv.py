# coding: utf8
import csv
from lxml import etree

""" création du fichier xml qui met a jour le stock par numero de lot
    suite a inventaire physique transcrit sur fichier csv avec les colonnes:
    Article,Numero de lot,Quantité disponible,date d'expiration,Quantité relevé
    Fichier excel exporte depuis EXACTonline 
     Stock>>Articles>>Numero de  lot>>Aperçu 
     disponible = oui """

stock = {}
stock_xml = []

with open('invent.csv', newline='') as csvfile:
    lecteur = csv.reader(csvfile)
    for row in lecteur :
        code = row[0].split(' - ') # code article,libellé
        num_lot = row[1]
        quant_dispo = row[2]
        date_exp = row[3]
        quant_reel = row[4]
        if row[0] != 'Article' :
            if code[0] in stock.keys():
                stock[code[0]].append([num_lot,quant_dispo,date_exp,quant_reel])
            else :
                stock[code[0]] = [[num_lot,quant_dispo,date_exp,quant_reel]]

for key in stock :
    squant_dispo = 0
    squant_reel = 0
    lots = []
    for value in stock[key] :
        squant_dispo += float(value[1])
        squant_reel += float(value[3])
        lots.append(value)
    stock_xml.append([key,squant_dispo,squant_reel,lots])

eExact = etree.Element('eExact')
StockCounts = etree.SubElement(eExact,'StockCounts')
StockCount = etree.SubElement(StockCounts,'StockCount')
Warehouse = etree.SubElement(StockCount,'Warehouse')
Warehouse.set('code',"1")
j =  1
for line in stock_xml :
    StockCountLine = etree.SubElement(Warehouse,'StockCountLine')
    StockCountLine.set('LineNumber', str(j))
    Quantity = etree.SubElement(StockCountLine,'Quantity')
    Quantity.text = str(line[1])
    NewQuantity=etree.SubElement(StockCountLine,'NewQuantity')
    NewQuantity.text = str(line[2])
    Item = etree.SubElement(StockCountLine,'Item')
    Item.set('code',line[0])
    BatchNumbers = etree.SubElement(StockCountLine,'BatchNumbers')
    for lot in line[3] :
        BatchNumberLine = etree.SubElement(BatchNumbers,'BatchNumberLine')
        BatchNumberLine.set('Quantity',str(lot[3]))
        BatchNumber = etree.SubElement(BatchNumberLine,'BatchNumber')
        BatchNumber.set('BatchNumber',lot[0])
        BatchNumber.set('ExpiryDate',lot[2])
    j += 1

with open('stock.xml','w') as fichier:
    fichier.write('<?xml version="1.0" encoding="UTF_8"?>\n')
    fichier.write(etree.tostring(eExact,pretty_print=True).decode('utf_8'))

