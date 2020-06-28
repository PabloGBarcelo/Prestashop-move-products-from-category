#######################################################################################
#   name: Pablo Gutiérrez Barceló
#   description: Prestashop 1.7.* move all your products from one categorie to another
#   email: pablo@gutierrezbarcelo.com
#   Feel free to use and modify but do not sell it.
#######################################################################################

import requests
import mysql.connector
import datetime
import asyncio
import datetime
from mysql.connector import errorcode
from requests.auth import HTTPBasicAuth
import xml.etree.ElementTree as ET
import numpy as np
##### DATA PRODUCTION #####
protocol = 'https://'
config = {
    'host': '',  # INSERT HOST WiTHOUT HTTPS://
    'user': '',  # INSERT USER OF DATABASE
    'password': '',  # INSERT PASSWORD OF DATABASE
    'database': '',  # INSERT NAME OF DATABASE
    'raise_on_warnings': True,
    'autocommit': True
}

oldCategorie = "164"  # INSERT NUMBER OF OLD CATEGORIE
newCategorie = "112"  # INSERT NUMBER OF NEW CATEGORIE


def sendQuery(query, fetch=None, dictionaryMode=False):
    cursor = cnx.cursor(dictionary=dictionaryMode)
    cursor.execute(query)
    print(query)
    if fetch == 'all':
        result = cursor.fetchall()
        cursor.close()
        return result
    elif fetch == 'oneResult':
        result = cursor.fetchone()
        cursor.close()
        return result
    else:
        cursor.close()
        # For INSERT and DELETE
        return


try:
    go = input('Are you sure? You will move your products from category {0} => to => {1}? (sure/n): '.format(
        oldCategorie, newCategorie))
    if go.upper() == 'SURE':
        fromTime = datetime.datetime.now()

        # Create connection
        cnx = mysql.connector.connect(**config)
        results = sendQuery("SELECT id_product FROM ps_product WHERE id_category_default={0}".format(
            oldCategorie), "all", True)
        cursor = cnx.cursor(dictionary=True)
        print(results)
        # Get all product with default_category in oldCategorie

        for idorder in results:
            sendQuery("UPDATE ps_product SET id_category_default={0} WHERE id_product={1}".format(
                newCategorie, idorder['id_product']))

            sendQuery("UPDATE ps_product_shop SET id_category_default={0} WHERE id_product={1}".format(
                newCategorie, idorder['id_product']))

            # Remove that product in that categorie ps_category_product
            sendQuery("DELETE FROM ps_category_product WHERE id_product={0} AND id_category={1}".format(idorder['id_product'],
                                                                                                        oldCategorie))
            # Check if exist product in ps_category_product
            result = sendQuery("SELECT id_product FROM `ps_category_product` WHERE id_category = {0} ORDER BY position DESC LIMIT 1".format(
                newCategorie), 'oneResult')[0]
            print(result)
            if result == None:
                # Get last position in in ps_category_product on new categorie
                nextPosition = int(sendQuery("SELECT position FROM `ps_category_product` WHERE id_category = {0} ORDER BY position DESC LIMIT 1".format(
                    newCategorie), "oneResult")[0]) + 1

                # Add new position in new categorie ps_category_product
                sendQuery("INSERT INTO ps_category_product VALUES ({0},{1},{2})".format(
                    newCategorie, idorder['id_product'], nextPosition))

            else:
                print("Exist position, skip")
            print("Product moved! - " + str(idorder['id_product']))
            print("\n")
            print(
                "FINISHED DEFAULT CATEGORY, LOADING NON DEFAULT PRODUCTS CATEGORY! - Moved {0} products in {1} seconds".format(len(results), (datetime.datetime.now() - fromTime)))
            print(
                "{0} seconds / product".format((datetime.datetime.now() - fromTime) / len(results)))

        print("\n Checking without parent oldCategorie but with secondary categorie")
        # Now check products without default categorie but with secondary

        # Get all products with oldCategorie
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT id_product FROM ps_category_product WHERE id_category = {0}".format(
            oldCategorie)
        cursor.execute(query)
        results = cursor.fetchall()
        print("Products loaded: {0}".format(len(results)))
        cursor.close()
        for idorder in results:
            # Check if exist product in ps_category_product (new categorie):
            result = sendQuery("SELECT id_product FROM `ps_category_product` WHERE id_category = {0} AND id_product={1} ORDER BY position DESC LIMIT 1".format(
                newCategorie, idorder['id_product']), "oneResult")

            print("\nChecking if exist in new Categorie...")
            print(result)
            cursor.close()
            if result == None:
                # Get last position in ps_category_product on new categorie
                nextPosition = int(sendQuery("SELECT position FROM `ps_category_product` WHERE id_category = {0} ORDER BY position DESC LIMIT 1".format(
                    newCategorie), "oneResult")[0]) + 1

                # Add new position in new categorie ps_category_product
                sendQuery("INSERT INTO ps_category_product VALUES ({0},{1},{2})".format(
                    newCategorie, idorder['id_product'], nextPosition))

            else:
                print("Exist position, skip")
            # Remove that product in old categorie ps_category_product
            sendQuery("DELETE FROM ps_category_product WHERE id_product={0} AND id_category={1}".format(idorder['id_product'],
                                                                                                        oldCategorie))

        cnx.close()
    else:
        print("Cancel!")


except mysql.connector.Error as err:
    print("Something was wrong, check error:")
    print(err)
