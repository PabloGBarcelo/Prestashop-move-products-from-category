# Prestashop-move-products-from-category
This script allow to move all products from categorie (default and non-default) to another categorie removing only from last one.
I've made synchronous mode because is safety for universal purposes, you can make your own thread-semaphore function if your tables are locked while some insert is made.

Tested on Prestashop 1.7.6.5
Fill lines 20-23 with database access data (remember to allow in your server firewall access to database from your IP)
Change line 28 and 29 with oldCategorie and newCategorie

Did it!

P.D.: I tried with prestashop webservice but server load increase more than using access-database and is much slower. With this script take about 0.5-0.8 secs by products. 
