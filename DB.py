import pymysql

class DB:
    def __init__(self,host,user,password,database):
        self.host=host
        self.user = user
        self.password=password
        self.database=database

    def signUp(self,data):
        mydb = None
        mydbCursor=None
        inserted = False
        try:
            # Get DB Connection
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            # Get cursor object
            mydbCursor = mydb.cursor()
            sql1="select * from user where email=%s"
            args1=(data[1])
            mydbCursor.execute(sql1, args1)
            results = mydbCursor.fetchone()
            if results ==None:
                sql1="insert into user (name,email,password) values (%s,%s,%s)"
                args1=(data[0],data[1],data[2])
                mydbCursor.execute(sql1, args1)
                mydb.commit()
                inserted=True
        except Exception as e:
            print(e)
        finally:
            if mydbCursor != None:
                mydbCursor.close()

            if mydb != None:
                mydb.close()
    
            return  inserted
        
    def login(self,data):
        mydb = None
        mydbCursor=None
        found = False
        results=""
        try:
            # Get DB Connection
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            # Get cursor object
            mydbCursor = mydb.cursor()
            sql1="select * from user where email=%s and password=%s"
            args1=(data[0],data[1])
            mydbCursor.execute(sql1, args1)
            results = mydbCursor.fetchone()
            if results !=None:
                found=True
                print(results[2])
        except Exception as e:
            print(e)
        finally:
            if mydbCursor != None:
                mydbCursor.close()

            if mydb != None:
                mydb.close()

            return  found,results[2]
        
    def addPlaces(self,data):
        mydb = None
        mydbCursor=None
        inserted = False
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            # Get cursor object
            mydbCursor = mydb.cursor()
            if  int(data [7]) <= int(data[3]):
                # Get DB Connection
                sql1 = "INSERT INTO places (emailid, area, loc, price, owner, description, image, `acceptable amount`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                args1 = (data[0], data[1], data[2], int(data[3]), data[4], data[5], data[6], int(data[7]))
                mydbCursor.execute(sql1, args1)
                mydb.commit()
                inserted=True
            else:
                inserted="Your Acceptable Amount must be less or equal to the price of the property !!"
        except Exception as e:
            print(e)
        finally:
            if mydbCursor != None:
                mydbCursor.close()

            if mydb != None:
                mydb.close()
            
        return  inserted

    def showPlaces(self):
        mydb = None
        mydbCursor=None
        found = False
        results=""
        try:
            # Get DB Connection
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            # Get cursor object
            mydbCursor = mydb.cursor()
            sql1="select * from places"
            mydbCursor.execute(sql1)
            results=mydbCursor.fetchall()
            if results:
                found=True
        except Exception as e:
            print(e)
        finally:
            if mydbCursor != None:
                mydbCursor.close()

            if mydb != None:
                mydb.close()

            return  found,results
        
    def buyProperty(self,data):
        mydb = None
        mydbCursor=None
        done = False
        results=""
        try:
            # Get DB Connection
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            # Get cursor object
            mydbCursor = mydb.cursor()
            sql1="select * from places where id=%s"
            args1=(data[0])
            mydbCursor.execute(sql1,args1)
            results=mydbCursor.fetchone()
            if results !=None:
                if float(data[1])>=float(results[8]):
                    sql1="delete from places where id=%s"
                    args1=(data[0])
                    mydbCursor.execute(sql1, args1)
                    mydb.commit()
                    done=True
                    if done:
                        sql= "insert into placehistory (emailidp,name, phone, bid) values(%s,%s,%s,%s)"
                        args = (data[4],data[3],data[2],data[1])
                        mydbCursor.execute(sql,args)
                        mydb.commit()

        except Exception as e:
            print(e)
        finally:
            if mydbCursor != None:
                mydbCursor.close()

            if mydb != None:
                mydb.close()

            return  done
    
    def searchSpecificProperty(self, data):
        mydb = None
        mydbCursor = None
        found = False
        results = ""

        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            # Get cursor object
            mydbCursor = mydb.cursor()
            whereClause = []
            args = []
            sql = "SELECT * FROM places"
            if data[0] !="":
                whereClause.append("loc LIKE %s")
                args.append("%" + data[0] + "%")

            if data[1] !="":
                whereClause.append("price >= %s")
                args.append(data[1])

            if data[2] !="":
                whereClause.append("price <= %s")
                args.append(data[2])

            if data[3] !="":
                whereClause.append("area >= %s")
                args.append(data[3])

            if data[4] !="":
                whereClause.append("area <= %s")
                args.append(data[4] )

            # print(whereClause)
            # print(args)

            if whereClause:
                sql += " WHERE " + " AND ".join(whereClause)

            mydbCursor.execute(sql, tuple(args))
            results = mydbCursor.fetchall()
            found = True

        except Exception as e:
            print(e)

        finally:
            if mydbCursor is not None:
                mydbCursor.close()

            if mydb is not None:
                mydb.close()

        return found, results



## functionality of cars
##
##

    def showCars(self):
        mydb = None
        mydbCursor=None
        found = False
        results=""
        try:
            # Get DB Connection
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            # Get cursor object
            mydbCursor = mydb.cursor()
            sql1="select * from cars"
            mydbCursor.execute(sql1)
            results=mydbCursor.fetchall()
            print(results)
            if results :
                found=True
        except Exception as e:
            print(e)
        finally:
            if mydbCursor != None:
                mydbCursor.close()

            if mydb != None:
                mydb.close()

            return  found,results   
    def addCar(self,data):
        mydb = None
        mydbCursor=None
        inserted = False
        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            # Get cursor object
            mydbCursor = mydb.cursor()
            if  int(data [6]) <= int(data[2]):
                # Get DB Connection
                sql1 = "INSERT INTO cars (email, `seating capacity`,price, owner, description, image, `acceptable amount`,model) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                args1 = (data[0], data[1], int(data[2]), data[3], data[4], data[5], int(data[6]), data[7])
                mydbCursor.execute(sql1, args1)
                mydb.commit()
                inserted=True
            else:
                inserted="Your Acceptable Amount must be less or equal to the price of the Car !!"
        except Exception as e:
            print(e)
        finally:
            if mydbCursor != None:
                mydbCursor.close()

            if mydb != None:
                mydb.close()
            
        return  inserted
    def buyCar(self,data):
        mydb = None
        mydbCursor=None
        done = False
        results=""
        try:
            # Get DB Connection
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            # Get cursor object
            mydbCursor = mydb.cursor()
            sql1="select * from cars where id=%s"
            args1=(data[0])
            mydbCursor.execute(sql1,args1)
            results=mydbCursor.fetchone()
            if results !=None:
                if int(data[1]) >= int(results[7]):
                    sql1="delete from cars where id=%s"
                    args1=(data[0])
                    mydbCursor.execute(sql1, args1)
                    mydb.commit()
                    done=True
                    if done:
                        sql= "insert into carshistory (emailidc,name, phone, bid) values(%s,%s,%s,%s)"
                        args = (data[4],data[3],data[2],data[1])
                        mydbCursor.execute(sql,args)
                        mydb.commit()

        except Exception as e:
            print(e)
        finally:
            if mydbCursor != None:
                mydbCursor.close()

            if mydb != None:
                mydb.close()

            return  done

    def searchSpecificCar(self, data):
        mydb = None
        mydbCursor = None
        found = False
        results = ""

        try:
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            # Get cursor object
            mydbCursor = mydb.cursor()
            whereClause = []
            args = []
            sql = "SELECT * FROM cars"
            if data[0] !="":
                whereClause.append("model LIKE %s")
                args.append(data[0])

            if data[1] !="":
                whereClause.append("price >= %s")
                args.append(data[1])

            if data[2] !="":
                whereClause.append("price <= %s")
                args.append(data[2])

            print(whereClause)
            print(args)

            if whereClause:
                sql += " WHERE " + " AND ".join(whereClause)

            mydbCursor.execute(sql, tuple(args))
            results = mydbCursor.fetchall()
            found = True

        except Exception as e:
            print(e)

        finally:
            if mydbCursor is not None:
                mydbCursor.close()

            if mydb is not None:
                mydb.close()

        return found, results
    
    def contactUs(self,name,message,email):
        mydb = None
        mydbCursor=None
        inserted = False
        try:
            # Get DB Connection
            mydb = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
            # Get cursor object
            print(name,message,email)
            mydbCursor = mydb.cursor()
            sql1="insert into contactus (name,message,contactemail) values (%s,%s,%s)"
            args1=(name,message,email)
            mydbCursor.execute(sql1, args1)
            mydb.commit()
            inserted=True
        except Exception as e:
            print(e)
        finally:
            if mydbCursor != None:
                mydbCursor.close()

            if mydb != None:
                mydb.close()
    
            return  inserted