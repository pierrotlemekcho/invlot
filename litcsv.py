# coding: utf8
import csv
from lxml import etree

""" création du fichier xml qui met a jour le stock par numero de lot
    suite a inventaire physique transcrit sur fichier csv avec les colonnes:
    Article,Numero de lot,Quantité disponible,date d'expiration,Quantité relevé
    Fichier excel exporte depuis EXACTonline
     Stock>>Articles>>Numero de  lot>>Aperçu
     disponible = oui """

stock = {}  #  dict  article : liste  des lots diponible avec leurs valeurs
#    [num_lot,quant_info,date_exp,quant_reel]
stock_xml = []  #  idem avec total des quantité info et reel par article
stock_xml_neg = []  #  idem pour les articles dont le stock doit diminuer
stock_xml_pos = []  #  "                                       " augmenter


with open('invent.csv', newline='') as csvfile:
    lecteur = csv.reader(csvfile)
    for row in lecteur :
        code_article = row[0].split(' - ')  #  code_article article,libellé
        num_lot = row[1]
        quant_info = row[2]
        date_exp = row[3]
        quant_reel = row[4]
        if row[0] != 'Article' :
            if code_article[0] in stock.keys():
                stock[code_article[0]].append([num_lot,quant_info,date_exp,quant_reel])
            else :
                stock[code_article[0]] = [[num_lot,quant_info,date_exp,quant_reel]]
print(stock)
for article in stock :
    quant_info_tot = 0
# coding: utf8
import csv
from lxml import etree

""" création du fichier xml qui met a jour le stock par numero de lot
    suite a inventaire physique transcrit sur fichier csv avec les colonnes:
    Article,Numero de lot,Quantité disponible,date d'expiration,Quantité relevé
    Fichier excel exporte depuis EXACTonline
     Stock>>Articles>>Numero de  lot>>Aperçu
     disponible = oui """

stock = {}  #  dict  article : liste  des lots diponible avec leurs valeurs
#    [num_lot,quant_info,date_exp,quant_reel]
stock_xml = []  #  idem avec total des quantité info et reel par article
stock_xml_neg = []  #  idem pour les articles dont le stock doit diminuer
stock_xml_pos = []  #  "                                       " augmenter


with open('invent.csv', newline='') as csvfile:
    lecteur = csv.reader(csvfile)
    for row in lecteur :
        code_article = row[0].split(' - ')  #  code_article article,libellé
        num_lot = row[1]
        quant_info = row[2]
        date_exp = row[3]
        quant_reel = row[4]
        if row[0] != 'Article' :
            if code_article[0] in stock.keys():
                stock[code_article[0]].append([num_lot,quant_info,date_exp,quant_reel])
            else :
                stock[code_article[0]] = [[num_lot,quant_info,date_exp,quant_reel]]
print(stock)
for article in stock :
    quant_info_tot = 0
    quant_reel_tot = 0
    lots = []
    for lot in stock[article] :
        quant_info_tot += float(lot[1])
        quant_reel_tot += float(lot[3])
        lots.append(lot)
    stock_xml.append([article,quant_info_tot,quant_reel_tot,lots])
    if quant_info_tot > quant_reel_tot :
        stock_xml_neg.append([article,quant_info_tot,quant_reel_tot,lots])
    if quant_info_tot < quant_reel_tot :
        stock_xml_neg.append([article,quant_info_tot,quant_reel_tot,lots])
        #  que faire si =

print(stock_xml)

def faire_xml(list_stock,nom_fichier):
    eExact = etree.Element('eExact')
    StockCounts = etree.SubElement(eExact,'StockCounts')
    StockCount = etree.SubElement(StockCounts,'StockCount')
    Warehouse = etree.SubElement(StockCount,'Warehouse')
    Warehouse.set('code',"1")
    j =  1
    for line in list_stock:
        StockCountLine = etree.SubElement(StockCount,'StockCountLine')
        StockCountLine.set('LineNumber', str(j))
        Quantity = etree.SubElement(StockCountLine,'Quantity')
        Quantity.text = str(line[2] - line[1]) # normalement line[1] à comprendre]
        NewQuantity=etree.SubElement(StockCountLine,'NewQuantity')
        NewQuantity.text = str(line[2])
        Item = etree.SubElement(StockCountLine,'Item')
        Item.set('code',line[0])
        BatchNumbers = etree.SubElement(StockCountLine,'BatchNumbers')
        for lot in line[3] :
            print(lot)
            BatchNumberLine = etree.SubElement(BatchNumbers,'BatchNumberLine')
            BatchNumberLine.set('Quantity',str(lot[3]))
            BatchNumber = etree.SubElement(BatchNumberLine,'BatchNumber')
            BatchNumber.set('BatchNumber',str(lot[0]))
            #BatchNumber.set('ExpiryDate',str(lot[2]))
        j += 1

    with open(nom_fichier,'w') as fichier:
        fichier.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        fichier.write(etree.tostring(eExact,pretty_print=True,encoding='utf-8').decode('utf_8'))

faire_xml(stock_xml,'stock_xml')
faire_xml(stock_xml_neg,'stock_neg.xml')
faire_xml(stock_xml_pos,'stock_pos.xml')

    quant_reel_tot = 0
    lots = []
    for lot in stock[article] :
        quant_info_tot += float(lot[1])
        quant_reel_tot += float(lot[3])
        lots.append(lot)
    stock_xml.append([article,quant_info_tot,quant_reel_tot,lots])
    if quant_info_tot > quant_reel_tot :
        stock_xml_neg.append([article,quant_info_tot,quant_reel_tot,lots])
    if quant_info_tot < quant_reel_tot :
        stock_xml_neg.append([article,quant_info_tot,quant_reel_tot,lots])
        #  que faire si =

print(stock_xml)

def faire_xml(list_stock,nom_fichier):
    eExact = etree.Element('eExact')
    StockCounts = etree.SubElement(eExact,'StockCounts')
    StockCount = etree.SubElement(StockCounts,'StockCount')
    Warehouse = etree.SubElement(StockCount,'Warehouse')
    Warehouse.set('code',"1")
    j =  1
    for line in list_stock:
        StockCountLine = etree.SubElement(StockCount,'StockCountLine')
        StockCountLine.set('LineNumber', str(j))
        Quantity = etree.SubElement(StockCountLine,'Quantity')
        Quantity.text = str(line[2] - line[1]) # normalement line[1] à comprendre]
        NewQuantity=etree.SubElement(StockCountLine,'NewQuantity')
        NewQuantity.text = str(line[2])
        Item = etree.SubElement(StockCountLine,'Item')
        Item.set('code',line[0])
        BatchNumbers = etree.SubElement(StockCountLine,'BatchNumbers')
        for lot in line[3] :
            print(lot)
            BatchNumberLine = etree.SubElement(BatchNumbers,'BatchNumberLine')
            BatchNumberLine.set('Quantity',str(lot[3]))
            BatchNumber = etree.SubElement(BatchNumberLine,'BatchNumber')
            BatchNumber.set('BatchNumber',str(lot[0]))
            #BatchNumber.set('ExpiryDate',str(lot[2]))
        j += 1

    with open(nom_fichier,'w') as fichier:
        fichier.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        fichier.write(etree.tostring(eExact,pretty_print=True,encoding='utf-8').decode('utf_8'))

faire_xml(stock_xml,'stock_xml')
faire_xml(stock_xml_neg,'stock_neg.xml')
faire_xml(stock_xml_pos,'stock_pos.xml')

