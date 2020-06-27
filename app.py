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

try:
    go = input('Are you sure? You will move your products from category {0} => to => {1}? (sure/n): '.format(
        oldCategorie, newCategorie))
    if go.upper() == 'SURE':
        fromTime = datetime.datetime.now()

        # Create connection
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor(dictionary=True)

        # Get all product with default_category in oldCategorie
        query = "SELECT id_product FROM ps_product WHERE id_category_default={0}".format(
            oldCategorie)
        print(query)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        print(results)
        for idorder in results:
            cursor = cnx.cursor()
            query = "UPDATE ps_product SET id_category_default={0} WHERE id_product={1}".format(
                newCategorie, idorder['id_product'])
            print(query)
            cursor.execute(query)
            cursor.close()
            cursor = cnx.cursor()
            query = "UPDATE ps_product_shop SET id_category_default={0} WHERE id_product={1}".format(
                newCategorie, idorder['id_product'])
            print(query)
            cursor.execute(query)
            cursor.close()

            # Remove that product in that categorie ps_category_product
            cursor = cnx.cursor()
            query = "DELETE FROM ps_category_product WHERE id_product={0} AND id_category={1}".format(idorder['id_product'],
                                                                                                      oldCategorie)
            print(query)
            cursor.execute(query)
            cursor.close()

            # Check if exist product in ps_category_product
            cursor = cnx.cursor()
            query = "SELECT id_product FROM `ps_category_product` WHERE id_category = {0} ORDER BY position DESC LIMIT 1".format(
                newCategorie)
            cursor.execute(query)
            result = cursor.fetchone()[0]
            cursor.close()
            print(result)
            if not cursor.fetchone():

                # Get last position in in ps_category_product on new categorie
                cursor = cnx.cursor()
                query = "SELECT position FROM `ps_category_product` WHERE id_category = {0} ORDER BY position DESC LIMIT 1".format(
                    newCategorie)
                cursor.execute(query)
                nextPosition = int(cursor.fetchone()[0]) + 1
                cursor.close()

                # Add new position in new categorie ps_category_product
                cursor = cnx.cursor()
                query = "INSERT INTO ps_category_product VALUES ({0},{1},{2})".format(
                    newCategorie, idorder['id_product'], nextPosition)
                print(query)
                cursor.execute(query)
                cursor.close()
            else:
                print("Exist position, skip")
            print("Product moved! - " + str(idorder['id_product']))
            print("\n")
            print(
                "FINISHED! - Moved {0} products in {1} seconds".format(len(results), (datetime.datetime.now() - fromTime)))
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
            cursor = cnx.cursor()
            query = "SELECT id_product FROM `ps_category_product` WHERE id_category = {0} AND id_product={1} ORDER BY position DESC LIMIT 1".format(
                newCategorie, idorder['id_product'])
            cursor.execute(query)
            result = cursor.fetchone()
            print("\nChecking if exist in new Categorie...")
            print(result)
            cursor.close()
            if result == None:
                # Get last position in ps_category_product on new categorie
                cursor = cnx.cursor()
                query = "SELECT position FROM `ps_category_product` WHERE id_category = {0} ORDER BY position DESC LIMIT 1".format(
                    newCategorie)
                cursor.execute(query)
                nextPosition = int(cursor.fetchone()[0]) + 1
                cursor.close()

                # Add new position in new categorie ps_category_product
                cursor = cnx.cursor()
                query = "INSERT INTO ps_category_product VALUES ({0},{1},{2})".format(
                    newCategorie, idorder['id_product'], nextPosition)
                print(query)
                cursor.execute(query)
                cursor.close()
            else:
                print("Exist position, skip")
            # Remove that product in old categorie ps_category_product
            cursor = cnx.cursor()
            query = "DELETE FROM ps_category_product WHERE id_product={0} AND id_category={1}".format(idorder['id_product'],
                                                                                                      oldCategorie)
            print(query)
            cursor.execute(query)
            cursor.close()
        cnx.close()
    else:
        print("Cancel!")


except mysql.connector.Error as err:
    print("Something was wrong, check error:")
    print(err)
