import psycopg2
import os 
from datetime import date


class SELLER:
    is_active = True
    is_authenticated = True
    admin = False

    def __init__(self, userid, username, password, name, surname, phone, mail, payment, is_admin): 
        self.userid   = userid
        self.username = username
        self.password = password
        self.name     = name    
        self.surname  = surname 
        self.phone    = phone   
        self.mail     = mail    
        self.payment  = payment 
        self.is_admin = is_admin
        
    
    def get_id(self):
        return self.username

class SELLERCLASS:
   def __init__(self, classid, title, minsell, minrate, cargo, percent): 
    self.classid = classid 
    self.title 	 = title 	
    self.minsell = minsell 
    self.minrate = minrate	  
    self.cargo	 = cargo	
    self.percent = percent	  
 
class PRODUCT:
   def __init__(self, productid, name, brand, category, startbid, sellerid, year): 
    self.productid  = productid  
    self.name 	    = name 		
    self.brand  	= brand  	 
    self.category   = category  	  
    self.startbid   = startbid  
    self.sellerid   = sellerid	  
    self.year	    = year	  
    
class BUYER:
    is_active = True
    is_authenticated = True

    def __init__(self, buyerid, username, name, surname, phone, mail, password): 
        self.userid    = buyerid  
        self.username   = username
        self.name 	    = name 		
        self.surname  	= surname 
        self.password   = password
        self.phone      = phone  	  
        self.mail       = mail

    def get_id(self):
        return self.username
    
class SOLDPRODUCT:
   def __init__(self, buyerid, productid, sellerid, highestbid, buyeraddress, cargonum, buyercity, postcode): 
    self.buyerid      = buyerid 
    self.productid    = productid 
    self.sellerid     = sellerid
    self.highestbid   = highestbid 		
    self.buyeraddress = buyeraddress  	 
    self.cargonum     = cargonum  	  
    self.buyercity    = buyercity  
    self.postcode     = postcode
    
class SELLERINFO:
   def __init__(self, sellerid, numofproducts, numofsells, totalbids, rating, sellerclassid): 
    self.sellerid      = sellerid  
    self.numofproducts = numofproducts 		
    self.numofsells    = numofsells  	 
    self.totalbids     = totalbids  	  
    self.rating        = rating  
    self.sellerclassid = sellerclassid	     

class DB:
    def __init__(self):
        pass
    #SELLER CRUD##################################

    def add_seller(self, username, password, name, surname, phone, mail, payment):
        
        url = os.getenv("DATABASE_URL")
        con = psycopg2.connect(url)


        cur = con.cursor()
        db_statement = "INSERT INTO seller (username, password, name, surname, phone, mail, payment)  \
        VALUES(%s,%s,%s,%s,%s,%s,%s); \
        INSERT INTO sellerinfo values \
        ((SELECT userid FROM seller WHERE username = %s),0,0,0,0,\
		(SELECT classid FROM sellerclass WHERE classid= 0));"

        cur.execute(db_statement, (username, password, name, surname, phone, mail, payment, username))
        cur.execute("select * from seller ")
        rows = cur.fetchall()
        for i in rows:
            print(i)
        
        con.commit()
        con.close()  


    def get_seller_count(self):
        url = os.getenv("DATABASE_URL")
        con = psycopg2.connect(url)
        cur = con.cursor()
        db_statement = """SELECT COUNT(*) FROM seller"""
        cur.execute(db_statement)
        row = cur.fetchone()

        return row[0]

    def get_sellers_by_sold(self):
        url = os.getenv("DATABASE_URL")
        con = psycopg2.connect(url)
        cur = con.cursor()
        db_statement = """select username, title, numofproducts, numofsells, totalbids, rating \
        from (seller join sellerinfo \
        on seller.userid = sellerinfo.sellerid) join sellerclass \
        on sellerinfo.sellerclassid = sellerclass.classid order by numofsells desc;"""

        cur.execute(db_statement)
        rows = cur.fetchall()

        return rows

    def get_sellers_by_rating(self):
        url = os.getenv("DATABASE_URL")
        con = psycopg2.connect(url)
        cur = con.cursor() 
        db_statement = """select username, title, numofproducts, numofsells, totalbids, \
        rating from (seller join sellerinfo \
        on seller.userid = sellerinfo.sellerid) join sellerclass \
        on sellerinfo.sellerclassid = sellerclass.classid  order by rating desc;"""

        cur.execute(db_statement)
        rows = cur.fetchall()

        return rows    

    def get_seller_by_username(self, username):

        url = os.getenv("DATABASE_URL")
        con = psycopg2.connect(url)
        cur = con.cursor()
        db_statement = "select * from seller where username = '{}'".format(username)
        cur.execute(db_statement)

        row = cur.fetchone()
        seller_object = None

        if row is not None:
            seller_object = SELLER(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7], row[8]) 

        con.commit()
        con.close() 

        return seller_object

    def get_seller_by_email(self, email):

        url = os.getenv("DATABASE_URL")
        con = psycopg2.connect(url)
        cur = con.cursor()

        db_statement = "select * from seller where mail = '{}'".format(email)
        cur.execute(db_statement)

        row = cur.fetchone()
        seller_object = None

        if row is not None:
            seller_object = SELLER(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7], row[8]) 

        con.commit()
        con.close() 

        return seller_object

    def delete_seller(self, username):
        
        url = os.getenv("DATABASE_URL")
        con = psycopg2.connect(url)

        cur = con.cursor()

        db_statement = "delete from seller where username = '{}'".format(username)

        cur.execute(db_statement)
        con.commit()
        con.close()  

    def update_seller_password(self, password, username):
    
        url = os.getenv("DATABASE_URL")
        con = psycopg2.connect(url)
        cur = con.cursor()

        db_statement = """UPDATE seller SET PASSWORD = '{}' WHERE USERNAME = '{}'""".format(password, username)
        
        cur.execute(db_statement)
        con.commit()   
        con.close() 
    
    def update_seller(self, username, name, surname, phone):

        url = os.getenv("DATABASE_URL")
        con = psycopg2.connect(url)
        cur = con.cursor()

        db_statement = """UPDATE seller SET name = '{}', surname = '{}', \
        phone = '{}'    WHERE USERNAME = '{}'\
        """.format(name, surname, phone, username)
        
        cur.execute(db_statement)
        con.commit()   
        con.close() 

    #SELLERCLASS CRUD##################################

    def add_sellerclass(self, id, title, minsell, minrate, cargo, percent):

        url = os.getenv("DATABASE_URL")
        con = psycopg2.connect(url)

        cur = con.cursor()

        db_statement = "INSERT INTO sellerclass (classid, title, minsell, minrate, cargo, percent) \
        VALUES(%s,%s,%s,%s,%s,%s)"

        cur.execute(db_statement, (id, title, minsell, minrate, cargo, percent))
        con.commit()
        con.close()         

    def get_sellerclass(self, username):

        url = os.getenv("DATABASE_URL")
        con = psycopg2.connect(url)

        cur = con.cursor()
        
        db_statement = "select * from sellerclass where classid = (select sellerclassid from sellerinfo where sellerid = \
        (select userid from seller where username = '{}'))".format(username)

        cur.execute(db_statement)

        row = cur.fetchone()
        seller_object = None

        if row is not None:
            seller_object = SELLERCLASS(row[0],row[1],row[2],row[3],row[4],row[5]) 

        con.commit()
        con.close() 

        return seller_object


    def get_sellerclass_by_title(self, title):

        url = os.getenv("DATABASE_URL")
        con = psycopg2.connect(url)

        cur = con.cursor()
        
        db_statement = "select * from sellerclass where title = '{}'".format(title)

        cur.execute(db_statement)

        row = cur.fetchone()
        seller_object = None

        if row is not None:
            seller_object = SELLERCLASS(row[0],row[1],row[2],row[3],row[4],row[5]) 

        con.commit()
        con.close() 

        return seller_object

    def get_sellerclasses(self):

        url = os.getenv("DATABASE_URL")
        con = psycopg2.connect(url)
        cur = con.cursor()
        
        db_statement = "select * from sellerclass"

        cur.execute(db_statement)
        rows = cur.fetchall()
        con.commit()
        con.close() 

        return rows

    def delete_sellerclass(self, title):
        
        url = os.getenv("DATABASE_URL")
        con = psycopg2.connect(url)

        cur = con.cursor()
        db_statement = "delete from sellerclass where title = '{}'".format(title)
        cur.execute(db_statement)
   
        con.commit()
        con.close()  

    def update_sellerclass(self, classid, old_title, new_title, minsell, minrate, cargo, percent):
        
        url = os.getenv("DATABASE_URL")
        con = psycopg2.connect(url)

        cur = con.cursor()
        db_statement = """update sellerclass set classid = {},\
            title = '{}', minsell = {}, minrate = {}, cargo = {}, percent = {}
            where title = '{}' """.format(classid, new_title, minsell, minrate, cargo, percent, old_title)

        cur.execute(db_statement)
        con.commit()   
        con.close()  

    #PRODUCT CRUD##################################

    def add_product(self, name, brand, category, startbid, sellerid, year):
        
        url = os.getenv("DATABASE_URL")
        con = psycopg2.connect(url)

        cur = con.cursor()
        db_statement = "INSERT INTO product (name, brand, category, startbid, sellerid, year) \
        VALUES(%s,%s,%s,%s,%s,%s)"
        
        cur.execute(db_statement, (name, brand, category, startbid, sellerid, year))
        con.commit()
        con.close()         

    def get_product(self, title):

        url = os.getenv("DATABASE_URL")
        con = psycopg2.connect(url)

        cur = con.cursor()
        db_statement = "select * from product where name = '{}'".format(title)
        cur.execute(db_statement)

        row = cur.fetchone()
        seller_object = None

        if row is not None:
            seller_object = PRODUCT(row[0],row[1],row[2],row[3],row[4],row[5],row[6]) 

        con.commit()
        con.close() 

        return seller_object

    def get_product_count(self):
        url = os.getenv("DATABASE_URL")
        con = psycopg2.connect(url)
        cur = con.cursor()
        db_statement = """SELECT COUNT(*) FROM product"""
        cur.execute(db_statement)
        row = cur.fetchone()

        return row[0]

    def get_product_by_brand(self):
        url = os.getenv("DATABASE_URL")
        con = psycopg2.connect(url)
        cur = con.cursor() 
        db_statement = """select product.name, product.brand, product.category, product.year, product.startbid, \
        seller.username from (product join seller \
        on seller.userid = product.sellerid) join buyer \
        on buyer.buyerid = product.buyerid  order by product.brand desc;"""

        cur.execute(db_statement)
        rows = cur.fetchall()

        return rows 

    def get_product_by_category(self):
        url = os.getenv("DATABASE_URL")
        con = psycopg2.connect(url)
        cur = con.cursor() 
        db_statement = """select product.name, product.brand, product.category, product.year, product.startbid, \
        seller.username from (product join seller \
        on seller.userid = product.sellerid) join buyer \
        on buyer.buyerid = product.buyerid  order by product.category desc;"""

        cur.execute(db_statement)
        rows = cur.fetchall()

        return rows 

    def get_product_by_year(self):
        url = os.getenv("DATABASE_URL")
        con = psycopg2.connect(url)
        cur = con.cursor() 
        db_statement = """select product.name, product.brand, product.category, product.year, product.startbid, \
        seller.username from (product join seller \
        on seller.userid = product.sellerid) join buyer \
        on buyer.buyerid = product.buyerid  order by product.year desc;"""

        cur.execute(db_statement)
        rows = cur.fetchall()

        return rows 

    def delete_product(self, name):
        
        url = os.getenv("DATABASE_URL")
        con = psycopg2.connect(url)

        cur = con.cursor()
        db_statement = "delete from product where name = '{}'".format(name)

        cur.execute(db_statement)
        con.commit()
        con.close()  

    def update_product(self, name, brand, category, startbid, year):
        
        url = os.getenv("DATABASE_URL")
        con = psycopg2.connect(url)

        cur = con.cursor()
        db_statement = """update product set \
            brand = '{}', category = '{}', startbid = {}, year = {} \
        where name = '{}' """.format(brand, category, startbid, year, name)

        cur.execute(db_statement)
        con.commit()   
        con.close()  
        

    #SELLERINFO CRUD##################################

    def add_sellerinfo(self, numofproducts, numofsells, totalbids, rating, sellerclassid):

        url = os.getenv("DATABASE_URL")
        con = psycopg2.connect(url)
        cur = con.cursor()
        
        db_statement = "INSERT INTO sellerinfo (numofproducts, numofsells, totalbids, rating, sellerclassid) \
        VALUES(%s,%s,%s,%s,%s)"

        cur.execute(db_statement, (numofproducts, numofsells, totalbids, rating, sellerclassid))
        con.commit()
        con.close()      

    def get_sellerinfo(self, sellerid):

        url = os.getenv("DATABASE_URL")
        con = psycopg2.connect(url)

        cur = con.cursor()
        db_statement = "select * from sellerinfo where sellerid = {}".format(sellerid)
        cur.execute(db_statement)

        row = cur.fetchone()
        sellerinfo_object = None

        if row is not None:
            sellerinfo_object = SELLERINFO(row[0],row[1],row[2],row[3],row[4],row[5]) 

        con.commit()
        con.close() 

        return sellerinfo_object

    def delete_sellerinfo(self, sellerid):
        
        url = os.getenv("DATABASE_URL")
        con = psycopg2.connect(url)
        cur = con.cursor()

        db_statement = "delete from sellerinfo where sellerid = {}".format(sellerid)
        cur.execute(db_statement)
        con.commit()
        con.close()  

    def update_sellerinfo(self, numofproducts, numofsells, totalbids, rating, sellerclassid, sellerid):
        
        url = os.getenv("DATABASE_URL")
        con = psycopg2.connect(url)

        cur = con.cursor()
        db_statement = """update sellerinfo set \
            numofproducts = {}, numofsells = {}, totalbids = {}, rating = {}, sellerclassid = {}
            where sellerid = {} """.format(numofproducts, numofsells, totalbids, rating, sellerclassid, sellerid)

        cur.execute(db_statement)

        con.commit()   
        con.close()   

    def add_rating(self, rating, sellerid):
        url = os.getenv("DATABASE_URL")
        con = psycopg2.connect(url)

        cur = con.cursor()
        db_statement = """ select rating, numofproducts from sellerinfo where sellerid = {}""".format(sellerid)
        cur.execute(db_statement)
        
        row = cur.fetchone()

        old_rating = row[0]
        numofproducts = row[1] 
        new_rating = ((numofproducts-1)*old_rating + rating)/numofproducts

        db_statement = """update sellerinfo set \
            rating = {}
            where sellerid = {} """.format(new_rating, sellerid)

        cur.execute(db_statement)
        con.commit()   
        con.close()

    def sold_product(self, sellerid, rating):
        url = os.getenv("DATABASE_URL")
        con = psycopg2.connect(url)

        cur = con.cursor()
        db_statement = "select numofsells from sellerinfo where sellerid = {}".format(sellerid)
        cur.execute(db_statement)
        row = cur.fetchone()
        numofsells = row[0] + 1
        
        db_statement = """update sellerinfo set \
            numofsells = {}
            where sellerid = {} """.format(numofsells, sellerid)

        cur.execute(db_statement)
        con.commit()   
        con.close()   

        self.add_rating(rating, sellerid)

    def add_bid_to_sellerinfo(self, sellerid):
        url = os.getenv("DATABASE_URL")
        con = psycopg2.connect(url)

        cur = con.cursor()
        db_statement = "select numofbids from sellerinfo where sellerid = {}".format(sellerid)
        cur.execute(db_statement)
        row = cur.fetchone()
        numofbids = row[0] + 1
        
        db_statement = """update sellerinfo set \
            numofsells = {}
            where sellerid = {} """.format(numofbids, sellerid)

        cur.execute(db_statement)
        con.commit()   
        con.close()   

    def add_product_to_sellerinfo(self, sellerid):
        url = os.getenv("DATABASE_URL")
        con = psycopg2.connect(url)

        cur = con.cursor()
        db_statement = "select numofproducts from sellerinfo where sellerid = {}".format(sellerid)
        cur.execute(db_statement)
        row = cur.fetchone()
        numofproducts = row[0] + 1
        
        db_statement = """update sellerinfo set \
            numofproducts = {}
            where sellerid = {} """.format(numofproducts, sellerid)

        cur.execute(db_statement)
        con.commit()   
        con.close()

    #BUYER CRUD##################################
    
    def add_buyer(self, username, password, name, surname, phone, mail):

        url = os.getenv("DATABASE_URL")
        con = psycopg2.connect(url)
        cur = con.cursor()

        today = str(date.today())

        db_statement ="""INSERT INTO buyer (username, name, surname, phone, mail, password, date) \
            VALUES(%s,%s,%s,%s,%s,%s,%s)"""
        cur.execute(db_statement, (username, name, surname, phone, mail, password, today))
        con.commit()
        con.close() 
        
    def get_buyer(self, username):

        url = os.getenv("DATABASE_URL")
        con = psycopg2.connect(url)

        cur = con.cursor()
        db_statement = "select * from buyer where username = '{}'".format(username)
        cur.execute(db_statement)
        row = cur.fetchone()
        buyer_object = None

        if row is not None:
            buyer_object = BUYER(row[0],row[1],row[2],row[3],row[4],row[5],row[6]) 

        con.commit()
        con.close() 

        return buyer_object

    def get_buyer_count(self):
        url = os.getenv("DATABASE_URL")
        con = psycopg2.connect(url)
        cur = con.cursor()
        db_statement = """SELECT COUNT(*) FROM buyer"""
        cur.execute(db_statement)
        row = cur.fetchone()

        return row[0]

    def get_buyer_by_email(self, email):

        url = os.getenv("DATABASE_URL")
        con = psycopg2.connect(url)

        cur = con.cursor()
        db_statement = "select * from buyer where mail = '{}'".format(email)
        cur.execute(db_statement)
        row = cur.fetchone()
        buyer_object = None

        if row is not None:
            buyer_object = BUYER(row[0],row[1],row[2],row[3],row[4],row[5],row[6]) 

        con.commit()
        con.close() 

        return buyer_object

    def get_buyers(self):

        url = os.getenv("DATABASE_URL")
        con = psycopg2.connect(url)

        cur = con.cursor()
        db_statement = "select username, date from buyer order by date"
        cur.execute(db_statement)
        rows = cur.fetchall()

        con.commit()
        con.close() 

        return rows

    def update_buyer(self, username, name, surname, phone):

        url = os.getenv("DATABASE_URL")
        con = psycopg2.connect(url)
        cur = con.cursor()

        db_statement = """UPDATE buyer SET name = '{}', surname = '{}', \
        phone = '{}' WHERE USERNAME = '{}'""".format(name, surname, phone, username)
        
        print(db_statement)
        cur.execute(db_statement)
        con.commit()   
        con.close()     

    def delete_buyer(self, username):
        
        url = os.getenv("DATABASE_URL")
        con = psycopg2.connect(url)
        
        cur = con.cursor()
        db_statement = "delete from buyer where username = '{}'".format(username)
        cur.execute(db_statement)
        con.commit()
        con.close()  

    def update_buyer_password(self, password, username):
        
        url = os.getenv("DATABASE_URL")
        con = psycopg2.connect(url)
        cur = con.cursor()

        db_statement = """UPDATE buyer SET PASSWORD = '{}' WHERE USERNAME = '{}'""".format(password, username)

        cur.execute(db_statement)
        con.commit()   
        con.close()

        
    #SOLDPRODUCT CRUD##################################
    
    def add_soldproduct(self, highestbid, buyeraddress, cargonum, buyercity, postcode):
        
        url = os.getenv("DATABASE_URL")
        con = psycopg2.connect(url)
        
        cur = con.cursor()
        db_statement = "INSERT INTO soldproduct (highestbid, buyeraddress, cargonum, buyercity, postcode) VALUES(%s,%s,%s,%s,%s,%s,%s)"
        cur.execute(db_statement, (highestbid, buyeraddress, cargonum, buyercity, postcode))
        con.commit()
        con.close()
        
    def get_soldproduct(self, productid):

        url = os.getenv("DATABASE_URL")
        con = psycopg2.connect(url)

        cur = con.cursor()
        db_statement = "select * from soldproduct where productid = {}".format(productid)
        cur.execute(db_statement)

        row = cur.fetchall()[0]
        soldproduct_object = None

        if row is not None:
            soldproduct_object = SOLDPRODUCT(row[0],row[1],row[2],row[3],row[4],row[5]) 

        con.commit()
        con.close() 

        return soldproduct_object

    def delete_soldproduct(self, productid):
        
        url = os.getenv("DATABASE_URL")
        con = psycopg2.connect(url)

        cur = con.cursor()
        db_statement = "delete from soldproduct where productid = {}".format(productid)
        cur.execute(db_statement)
        con.commit()
        con.close()
    
    def update_soldproduct(self, highestbid, buyeraddress, cargonum, buyercity, postcode):
        
        url = os.getenv("DATABASE_URL")
        con = psycopg2.connect(url)

        cur = con.cursor()
        db_statement = """update soldproduct set \
            highestbid = {} , buyeraddress = '{}', \
            postcode = {}, buyercity = '{}' \
            where cargonum = {}""".format(highestbid, buyeraddress, postcode, buyercity, cargonum)

        cur.execute(db_statement)
        con.commit()   
        con.close()  
        
      
