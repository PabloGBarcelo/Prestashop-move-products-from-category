# pip install -r requeriments.txt
# Fill lines 20-20 with database access
# Change line 28 and 29 with oldCategorie and newCategorie

# Prestashop-move-products-between-categories
This script allow to move all products from categorie (default and non-default) to another categorie removing only from last one.
I've made synchronous mode because is safest for universal purposes, you can make your own thread-semaphore function if your tables are locked while some insert is made.

Tested on Prestashop 1.7.6.5

Prestashop webservice is much slower managing this kind of tasks. With this script take about 0.5-0.8 secs by product. 
