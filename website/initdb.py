import psycopg2

#CREATE TABLE##############

INIT_STATEMENTS = [
    
    #SELLER TABLE
    """CREATE TABLE IF NOT EXISTS SELLER
    (
    userid   SERIAL PRIMARY KEY,    
    username VARCHAR(20) NOT NULL,
    password VARCHAR(15) NOT NULL,
    name     VARCHAR(20),
    surname  VARCHAR(20),
    phone    VARCHAR(20),
    mail     VARCHAR(30),
    payment  INTEGER,
    is_admin INTEGER DEFAULT 0,
    UNIQUE (username)
    );
    insert into seller (username, password, name, surname, phone, mail, payment,is_admin) 
    values('admin', '1234567','Admin','Adminson','05393259898','admin@gmail.com',1,1)
    ON CONFLICT DO NOTHING;
    """,

    #PRODUCT TABLE
    """CREATE TABLE IF NOT EXISTS product
    (
    productid   SERIAL PRIMARY KEY,    
    name 		VARCHAR(20) NOT NULL,
    brand  		VARCHAR(20),
    category    VARCHAR(20),
    startbid  	INTEGER,
	sellerid	INTEGER,
    year	  	INTEGER,
	CONSTRAINT 	fk_customer
      FOREIGN KEY(sellerid) 
	  REFERENCES seller(userid)
		ON DELETE CASCADE
		ON UPDATE CASCADE
    );""",

    #SELLER CLASS TABLE
    """CREATE TABLE IF NOT EXISTS sellerclass
    (
    classid   	SERIAL PRIMARY KEY,    
    title 		VARCHAR(20) NOT NULL,
    minsell  	INTEGER,
	minrate		INTEGER,
    cargo	  	INTEGER,
	percent		INTEGER,
    PRIMARY KEY(classid)
    );""",
    
    #Sellerclasses are determined
    """
    INSERT INTO sellerclass values(0,'gold',0,0,0,0)
    ON CONFLICT DO NOTHING;
    INSERT INTO sellerclass VALUES(1,'rockstar',2,2,10,10)
    ON CONFLICT DO NOTHING;
    """,

    #BUYER TABLE
    """CREATE TABLE IF NOT EXISTS BUYER
    (
    userid		SERIAL PRIMARY KEY,
    username 	VARCHAR(20) NOT NULL,
    password    VARCHAR(20) NOT NULL,
    name     	VARCHAR(20),
    surname  	VARCHAR(20),
    phone    	VARCHAR(20),
    mail     	VARCHAR(30),
    date        VARCHAR(25),
    UNIQUE (username)
    );""",
    
    #SOLD PRODUCT TABLE
    """CREATE TABLE IF NOT EXISTS soldproduct
    (
    buyerid		INTEGER ,
    productid   INTEGER ,
    sellerid	INTEGER ,
    highestbid	INTEGER,
    buyeraddress VARCHAR(40) NOT NULL,
    cargonum	INTEGER,
    buyercity	VARCHAR(10) NOT NULL,
    postcode    INTEGER,
	CONSTRAINT 	fk_seller
      FOREIGN KEY(sellerid) 
	  REFERENCES seller(userid)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	CONSTRAINT 	fk_buyer
      FOREIGN KEY(buyerid) 
	  REFERENCES buyer(userid)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	CONSTRAINT 	fk_product
      FOREIGN KEY(productid) 
	  REFERENCES product(productid)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
    PRIMARY KEY (buyerid, productid, sellerid));
    """,
	
    #SELLER INFO TABLE
    """
    CREATE TABLE IF NOT EXISTS sellerinfo(	
	sellerid      INTEGER,
    numofproducts INTEGER, 		
    numofsells    INTEGER, 	 
    totalbids     INTEGER,  	  
    rating        FLOAT,
    sellerclassid INTEGER,
	CONSTRAINT 	fk_seller
      FOREIGN KEY(sellerid) 
	  REFERENCES seller(userid)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	CONSTRAINT 	fk_sellerclass
      FOREIGN KEY(sellerclassid) 
	  REFERENCES sellerclass(classid)
		ON DELETE CASCADE
		ON UPDATE CASCADE,
	PRIMARY KEY(sellerid)
	);
    """
]


def initialize(url):

    with psycopg2.connect(url) as con:
        cur = con.cursor()
        for db_statement in INIT_STATEMENTS:
            cur.execute(db_statement)
        con.commit()

