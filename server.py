from flask import Flask,jsonify,request,abort,session,render_template,json
import requests
import math
from flask_cors import cross_origin
import sqlite3

app=Flask(__name__)
app.secret_key = "abc"


conn = sqlite3.connect('database.db',check_same_thread=False)
if(not conn):
	abort(500)

conn.execute("PRAGMA foreign_keys=ON")


#user table
conn.execute('''CREATE TABLE IF NOT EXISTS Users(
            username TEXT PRIMARY KEY,
            email TEXT NOT NULL,
            mobile BIGINT NOT NULL,
            password TEXT NOT NULL
            );''')


#items table
conn.execute('''CREATE TABLE IF NOT EXISTS Items(
            itemId TEXT PRIMARY KEY,
            itemName TEXT NOT NULL,
            price INTEGER NOT NULL,
            specs TEXT NOT NULL,
            quantity INTEGER NOT NULL
            );''')


#shopping cart
conn.execute('''CREATE TABLE IF NOT EXISTS Cart(
            username TEXT,
            item TEXT NOT NULL,
            price INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            CONSTRAINT "userid" FOREIGN KEY (username) REFERENCES Users(username) ON DELETE CASCADE
            );''')


#Orders / Bought items history
conn.execute('''CREATE TABLE IF NOT EXISTS Orders(
            username TEXT,
            item TEXT NOT NULL,
            price INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            review INTEGER,
            CONSTRAINT "userid" FOREIGN KEY (username) REFERENCES Users(username) ON DELETE CASCADE
            );''')


# add products to database
'''conn = sqlite3.connect('database.db',check_same_thread=False)

fd = open("products/tvs_and_appliances/washing_machine/data.txt","r")
# "products/electronics/laptops/data.txt"
# "products/electronics/mobiles/data.txt"
# "products/tvs_and_appliances/tvs/data.txt"
content = fd.read()
item = content.split("\n")
for i in item:
    if(i):
        data = i.split(";")
        data = ",".join("'{}'".format(i) for i in data)
        print(data)
        print()

        #insert user data into database
        query="INSERT INTO Items ( itemId,itemName,price,specs,quantity ) VALUES ( " + data + " );"
        conn.execute(query)
        conn.commit()

conn.close() '''


@app.route('/api/login',methods=["POST","OPTIONS"])
@cross_origin(origin="*")
def login():

    #extract data
    d=request.get_json()
    
    username="'{}'".format(d["username"])
    password = d["pwd"]
    
    #connect to database
    conn = sqlite3.connect('database.db',check_same_thread=False)

    #check if user exists or not and if exists check password
    query="SELECT username,password FROM Users WHERE ( username =" + username + " );"

    try:
        db_data = conn.execute(query)

        for data in db_data:
            user,pwd = data
            
            if(pwd == password):
                #create a session for user
                session['username'] = d['username']

                return "Login successful"
                # return render_template('signup.html')

            elif(pwd != password):
                return "Incorrect Password"

        return "Incorrect Username"

    except Error as e:
        return "error" 




    #check if user is logged in
    if(session['username']):
        username = session['username']
        session.pop('username',None)
        return username + " logged out"

    else:
        return "you are not logged in"
    

@app.route('/api/signup',methods=["POST","OPTIONS"])
@cross_origin(origin="*")
def signup():

    #extract data
    d=request.get_json()
    
    data = [d["username"],d["email"],d["mobile"],d["pwd"]]
    data = ",".join("'{}'".format(i) for i in data)
    username="'{}'".format(d["username"])
    
    #connect to database
    conn = sqlite3.connect('database.db',check_same_thread=False)

    #check if user already exists
    query="SELECT username FROM Users WHERE ( username =" + username + " );"
    db_data = conn.execute(query)
    
    for data in db_data:
        for user in data:
                return "User already exists!"

    #insert user data into database
    query="INSERT INTO Users ( username,email,mobile,password ) VALUES ( " + data + " );"
    conn.execute(query)
    conn.commit()
    conn.close()

    return "successfully Registered!"


@app.route('/api/addtocart',methods=["POST","OPTIONS"])
@cross_origin(origin="*")
def addToCart():

    #extract data
    d=request.get_json()
    
    #get logged in user's name 
    # if(session['username']):
    #     username = session['username']
    # else:
    #     return "Login to shop"
    if(d["username"]=="none"):
        return "Login to continue"

    
    #check if quantity is correct
    path = "http://127.0.0.1:5000/api/getitemdata/" + d["itemId"]
    dat = requests.get(url=path)
    # x= dat.json()
    dat = dat.json()
    if(dat):
        for i in dat:
            if(int(i[4])< int(d['quantity'])):
                return "We have " + str(i[4]) + " items left!"
        

    data = [d["username"],d["itemId"],d["price"],d["quantity"]]
    data = ",".join("'{}'".format(i) for i in data)
    
    #connect to database
    conn = sqlite3.connect('database.db',check_same_thread=False)

    #insert user data into database
    query="INSERT INTO Cart ( username,item,price,quantity ) VALUES ( " + data + " );"
    conn.execute(query)
    conn.commit()
    conn.close()

    return "Item added to Cart!"


@app.route('/api/orders/<username>',methods=["GET","OPTIONS"])
@cross_origin(origin="*")
def orders(username):

    #extract data
    # d=request.get_json()
    
    # columns = ["username","item","price","quantity","review"]

    # username="'{}'".format(d["username"])

    #get logged in user's name 
    # print("hi")
    # print(session.get('username',None))
    # if 'username' in session:
    #     print("k")
    #     username = session['username']
    #     print(username)
    # else:
    #     return "Login to see your orders"
    # username = "'chetank'"
    #connect to database
    if(username=="none"):
        return "Login to continue"
    username="'{}'".format(username)
    conn = sqlite3.connect('database.db',check_same_thread=False)

    #Get the items the current user has bought
    query="SELECT username,item,price,quantity,review FROM Orders WHERE ( username =" + username + " );"

    try:
        db_data = conn.execute(query)

        b = []
        for _list in db_data:
            a = []
            for item in range(5):
                a.append(_list[item])
            b.append(a)
        
        return jsonify(b)

    except Error as e:
        return "error"


@app.route('/api/mycart/<username>',methods=["GET","OPTIONS"])
@cross_origin(origin="*")
def showMyCart(username):

    #extract data
    # d=request.get_json()
    
    # columns = ["username","item","price","quantity"]

    # username="'{}'".format(d["username"])

    #get logged in user's name 
    # if(session['username']):
    #     username = session['username']
    # else:
    #     return "Login to see your cart items"
    if(username=="none"):
        return "Login to continue"

    username="'{}'".format(username)
    #connect to database
    conn = sqlite3.connect('database.db',check_same_thread=False)

    #Get the items the current user has added to cart
    query="SELECT username,item,price,quantity FROM Cart WHERE ( username =" + username + " );"

    try:
        db_data = conn.execute(query)

        b = []
        for _list in db_data:
            a = []
            for item in range(4):
                a.append(_list[item])
            b.append(a)
        
        return jsonify(b)

    except Error as e:
        return "error"


@app.route('/api/buy',methods=["POST","OPTIONS"])
@cross_origin(origin="*")
def buy():

    #extract data
    d=request.get_json()

    if(d["username"]=="none"):
        return "Login to continue"
    # uname = d[0][0]

    # #get logged in user's name 
    # if(session['username']):
    #     username = session['username']
    # else:
    #     return "You are not logged in"
    
    # #check for correct user
    # if(uname != username):
    #     return "Error"


    #check if quantity is correct
    path = "http://127.0.0.1:5000/api/getitemdata/" + d["itemId"]
    dat = requests.get(url=path)
    # x= dat.json()
    dat = dat.json()
    if(dat):
        for i in dat:
            if(int(i[4])< int(d['quantity'])):
                return "We have " + str(i[4]) + " items left!"

    #connect to database
    conn = sqlite3.connect('database.db',check_same_thread=False)

    #insert user-item data into database
    # for item in d:
    data = [d["username"],d['itemId'],d["price"],d["quantity"],d["rating"]]
    quan = "'{}'".format(d["quantity"])
    itemid = "'{}'".format(d["itemId"])
    data = ",".join("'{}'".format(i) for i in data)
    print(data)
    query="INSERT INTO Orders ( username,item,price,quantity,review ) VALUES ( " + data + " );"
    conn.execute(query)
    conn.commit()

    #update quantity of items
    query = "UPDATE Items SET quantity=quantity-" + quan + "WHERE itemId=" + itemid + ";"
    conn.execute(query)
    conn.commit()

    conn.close()

    return "Order placed!"


@app.route('/api/getitemdata/<term>',methods=["GET"])
@cross_origin(origin="*")
def getItemData(term):

    #extract data
    # d=request.get_json()
    
    # columns = ["username","item","price","quantity"]

    # username="'{}'".format(d["username"])
    term = "'{}'".format(term)
    #get logged in user's name 
    # if(session['username']):
    #     username = session['username']
    # else:
    #     return "Login to see your cart items"
    
    #connect to database
    conn = sqlite3.connect('database.db',check_same_thread=False)

    #Get the items the current user has added to cart
    query="SELECT itemId,itemName,price,specs,quantity FROM Items WHERE ( itemId =" + term + " );"

    try:
        db_data = conn.execute(query)

        b = []
        for _list in db_data:
            a = []
            for item in range(5):
                a.append(_list[item])
            b.append(a)
        
        return jsonify(b)

    except:
        return "error"


@app.route('/api/search/<term>',methods=["GET"])
@cross_origin(origin="*")
def searchbar(term):
    file = open('search.txt', 'r') 
    content = file.read()
    lines = content.splitlines()
    listItem = []
    if(term != ''):
        for line in lines:
            if(term.upper() in line.upper()):
                listItem.append(line)
    response = app.response_class(response=json.dumps(listItem),status=200,mimetype='application/json')
    return response


@app.route('/api/recommend/<itemId>',methods=["GET"])
@cross_origin(origin="*")
def recommend(itemId):
    #get the data from database.
    #dict = {"username":[["item1","rating"],["item1","rating"]]  ,  .....}

    #get users
    conn = sqlite3.connect('database.db',check_same_thread=False)

    query="SELECT username FROM Users;"

    try:
        db_data = conn.execute(query)
        b = []
        for _list in db_data:
            a = []
            for item in range(1):
                a.append(_list[item])
            b.append(a)

    except:
        return "errowr"

    #b=[[user1],[user2]...]
    # print(b)

    ratings = {}
    for user in b:

        user1 = "'{}'".format(user[0])
        query = "SELECT item,review FROM Orders WHERE ( username=" + user1 + " );"
        try:
            db_data = conn.execute(query)
            c = []
            for _list in db_data:
                a = []
                for item in range(2):
                    a.append(_list[item])
                c.append(a)
            ratings[user[0]]=c

        except:
            return "error"
    
    # create item vs. user matrix
    items = ["EM1","EM2","EM3","EM4","EM5","EL1","EL2","EL3","EL4","EL5","TT1","TT2","TT3","TT4","TT5","TW1","TW2","TW3","TW4","TW5"]
    matrix = []
    for itemid in range(len(items)):
        matrix.append([])
        for rat in ratings:
            flag=0
            for i in ratings[rat]:
                if i[0] == items[itemid]:
                    matrix[itemid].append(i[1])
                    flag=1
            if(flag==0):
                matrix[itemid].append(0)
        matrix[itemid].append(items[itemid])

    # print(matrix)


    #seperate the test data from this matrix
    testData = matrix.pop(items.index(itemId))
    # print(testData)


    #call Knn
    result = KNN(matrix,testData)

    #get full data of result
    fulldata = []
    for i in result:
        path = "http://127.0.0.1:5000/api/getitemdata/" + i
        dat = requests.get(url=path)
        # x= dat.json()
        dat = dat.json()
        if(dat):
            for i in dat:
                i[0] = "./images/" + i[0] + ".jpeg"
                fulldata.append(i)
    
    # print(len(fulldata))
    return jsonify(fulldata)



def calculateDistance(test,train):   
    sum = 0   
    for feature in range(len(test)-1):        
        sum += math.pow(int(test[feature])-int(train[feature]),2)
    return math.sqrt(sum),train[-1]

k = 3

def KNN(trainData,testData):
        
    distance = []
    for train in trainData:
        distance.append(calculateDistance(testData,train))
        
    distance = sorted(distance,key = lambda x: x[0])
    
    #related items
    result = []
    for i in range(k):
        result.append(distance[i][1])
    # print(result)
    return result
                



if(__name__=="__main__"):
    app.run(debug=True)