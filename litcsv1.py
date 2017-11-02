# coding: utf8
import csv
from lxml import etree

""" création du fichier xml qui met a jour le stock par numero de lot
    suite a inventaire physique transcrit sur fichier csv avec les colonnes:
    Article,Numero de lot,Quantité disponible,date d'expiration,Quantité relevé
    Fichier excel exporte depuis EXACTonline
     Stock>>Articles>>Numero de  lot>>Aperçu
     disponible = oui """


def trier_csv(fichier):
    """prend un fichier inventaire csv et retourne la liste
    des quantités qui augmentent inventaire_plus
     et la liste des quantités qui diminuent inventaire_moins"""
    inventaire_plus = []
    inventaire_moins = []
    for row in fichier:
        quant_info = row[2]
        quant_reel = row[4]
        if quant_info < quant_reel:
            inventaire_plus.append(row)
        else:
            inventaire_moins.append(row)
            # il faut faire si =
    return inventaire_plus, inventaire_moins


def faire_stock(inventaire):
    """ prend un inventaire (article lot quantité date) et
    retourne un dict stock avec tout les numero de lots  regroupés par
    articles """
    stock = {}
    for row in inventaire:
        code_article = row[0].split(' - ')  # code_article article,libellé
        num_lot = row[1]
        quant_info = row[2]
        date_exp = row[3]
        quant_reel = row[4]
        if row[0] != 'Article':
            if code_article[0] in stock.keys():
                stock[code_article[0]].append([num_lot, quant_info, date_exp,
                                               quant_reel])
            else:
                stock[code_article[0]] = [[num_lot, quant_info, date_exp,
                                  quant_reel]]
    return stock


def faire_stocktoted(stock):
    """ retourne une liste inventaire totalisé par aticle :
        [article, quantité totalinfo,quantité total stock,[lot,lot...]]
    et la liste de tout les lots de cet article """
    stocktoted = []
    for article in stock:
        quant_info_tot = 0
        quant_reel_tot = 0
        lots = []
        for lot in stock[article]:
            quant_info_tot += float(lot[1])
            quant_reel_tot += float(lot[3])
            lots.append(lot)
        stocktoted.append([article, quant_info_tot, quant_reel_tot, lots])
    print('===================')
    print(stocktoted)
    print('===================')
    return stocktoted


def maj_stockmoins(stocktotedplus, stocktotedmoins):
    for listplus in stocktotedplus:
        for listmoins in stocktotedmoins:
            if listmoins[0] == listplus[0]:
                listmoins[1] = listplus[2]
    print('--------------------')
    print(stocktotedmoins)
    print('--------------------')
    return stocktotedmoins


def faire_xml(stocktoted, nom_fichier):
    eExact = etree.Element('eExact')
    StockCounts = etree.SubElement(eExact, 'StockCounts')
    StockCount = etree.SubElement(StockCounts, 'StockCount')
    Warehouse = etree.SubElement(StockCount, 'Warehouse')
    Warehouse.set('code', "1")
    j = 1
    for line in stocktoted:
        StockCountLine = etree.SubElement(StockCount, 'StockCountLine')
        StockCountLine.set('LineNumber', str(j))
        Quantity = etree.SubElement(StockCountLine, 'Quantity')
        Quantity.text = str(line[2] - line[1])
        NewQuantity = etree.SubElement(StockCountLine, 'NewQuantity')
        NewQuantity.text = str(line[2])
        Item = etree.SubElement(StockCountLine, 'Item')
        Item.set('code', line[0])
        BatchNumbers = etree.SubElement(StockCountLine, 'BatchNumbers')
        for lot in line[3]:
            print(lot)
            BatchNumberLine = etree.SubElement(BatchNumbers, 'BatchNumberLine')
            BatchNumberLine.set('Quantity', str(lot[3]))
            BatchNumber = etree.SubElement(BatchNumberLine, 'BatchNumber')
            BatchNumber.set('BatchNumber', str(lot[0]))
#BatchNumber.set('ExpiryDate',str(lot[2]))
        j += 1

    with open(nom_fichier, 'w') as fichier:
        fichier.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        fichier.write(etree.tostring(eExact, pretty_print = True,
                                     encoding = 'utf-8').decode('utf_8'))

with open('invent.csv', newline='') as csvfile:
    lecteur = csv.reader(csvfile)
    inv_plus,inv_moins = trier_csv(lecteur)
print(inv_plus)
print(inv_moins)
stock_plus_toted = faire_stocktoted(faire_stock(inv_plus))
stock_moins_toted = faire_stocktoted(faire_stock(inv_moins))
stock_moins_toted_maj = maj_stockmoins(stock_plus_toted, stock_moins_toted)


faire_xml(stock_moins_toted_maj, 'stock_neg.xml')
faire_xml(stock_plus_toted, 'stock_pos.xml')
