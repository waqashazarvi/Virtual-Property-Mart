from flask import Flask,render_template,request,session
from DB import DB
import base64
from io import BytesIO


app = Flask(__name__)

app.secret_key="bsjvhusdhg5565645"
app.config["SESSION_TYPE"]="filesystem"
app.config["SESSION_PERMANENT"]=False

# the working of places functionlity starts from here
####
####
@app.route('/')
def IndexPage():
    return  render_template("Index.html")

@app.route('/Home')
def Home():
    return render_template("Home.html")

@app.route('/signIn')
def sIn():
    return  render_template("SignIn.html")

@app.route('/submitSignInForm', methods=["POST"])
def submitSignInForm():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user=[email,password]
        db=DB("localhost","root","mian2468","ecommerce")
        found,email=db.login(user)
        if found:
            session['email']=email
            return render_template("Home.html")
        else:
            return  render_template("SignIn.html" , message="Email or Password is Incorrect")

@app.route('/signUp')
def sUp():
    return  render_template("SignUp.html")

@app.route('/submitSignUpForm', methods=["POST"])
def submitSignUpForm():
    if request.method == "POST":
        name=request.form["FName"]
        email = request.form["email"]
        password = request.form["password"]
        conPassword=request.form["conPassword"]
        user=[name, email,password]
        if len(password) >=8 and len(conPassword) >=8 :
            if password ==  conPassword:
                db=DB("localhost","root","mian2468","ecommerce")
                inserted=db.signUp(user)
                if inserted:
                    session['email']=email
                    return render_template("signupdashboard.html")
                else:
                    return  render_template("SignIn.html" , message="Email Already Exist")
            else:
                return  render_template("SignIn.html" , message="Password not Match")
        else:
            return  render_template("SignIn.html" , message="Password must be at least 8 characters long")
        
@app.route('/contactus')
def contactus():
    return render_template("contact.html")
@app.route('/goToContactPage', methods=["POST","GET"])
def contactPage():
    email=session.get("email")
    
    if email !=None:
        fname = request.args.get("name")
        lname = request.args.get("surname")
        email = request.args.get("email")
        text = request.args.get("message")
        print(fname, lname, email, text)
        name = fname + " " + lname
        db=DB("localhost","root","mian2468","ecommerce")
        inserted = db.contactUs(name,text,email)
        if inserted:
            return  render_template("Home.html")
        else:
            return  render_template("contact.html")
    else:
        return  render_template("SignIn.html",message1="First Fill this Form !!!")

@app.route('/goToAboutUsPage')
def categoryPage():
    email=session.get("email")
    if email !=None:
        return  render_template("aboutus.html")
    else:
        return  render_template("SignIn.html",message1="First Fill this Form !!!")


@app.route('/goToVisitPlaces')
def visitPlace():
    email = session.get("email")
    if email is not None:
        db = DB("localhost", "root", "mian2468", "ecommerce")
        found, data = db.showPlaces()
        if found:
            apartments = []
            for apartment in data:
                binary_data = apartment[7]
                image_data = base64.b64decode(binary_data)
                base64_image = base64.b64encode(image_data).decode('utf-8')
                apartments.append({
                    'id': apartment[0],
                    'area':apartment[2],
                    'location':apartment[3],
                    'price': apartment[4],
                    'owner': apartment[5],
                    'description': apartment[6],
                    'image': f"data:image/jpeg;base64,{base64_image}"
                })
            return render_template("visit places.html", apartments=apartments)
        else :
            return render_template("visit places.html", message="No apartments found")
            
    # else:
    #     return render_template("SignIn.html", message="First fill this form")


@app.route('/goToSpecificPlace')
def showFormPage():
    email=session.get("email")
    if email !=None:
        return  render_template("Search Specific Place Form.html")
    else:
        return  render_template("SignIn.html",message1="First Fill this Form !!!")

@app.route('/goToSpecifiedPlaces', methods=["POST"])
def visitSpecificPlace():
    email = session.get("email")
    if email is not None:
        loc=request.form["location"]
        sRange = request.form["start-range"]
        eRange = request.form["end-range"]
        sarea=request.form["start area range"]
        earea=request.form["end area range"]
        data=[loc,sRange,eRange,sarea,earea]

        db = DB("localhost", "root", "mian2468", "ecommerce")
        found, data = db.searchSpecificProperty(data)
        if found:
            apartments = []
            for apartment in data:
                binary_data = apartment[7]
                image_data = base64.b64decode(binary_data)
                base64_image = base64.b64encode(image_data).decode('utf-8')
                apartments.append({
                    'id': apartment[0],
                    'area':apartment[2],
                    'location':apartment[3],
                    'price': apartment[4],
                    'owner': apartment[5],
                    'description': apartment[6],
                    'image': f"data:image/jpeg;base64,{base64_image}"
                })
            return render_template("visit specific places.html", apartments=apartments)
        else :
            return render_template("visit specific places.html", message="No apartments found")
            
    else:
        return render_template("SignIn.html", message="First fill this form")
    


@app.route("/buyPlace/<int:apartment_id>")
def renderBuyPlace(apartment_id):
    email=session.get("email")
    session['apartId']=apartment_id
    if email !=None:
        return  render_template("buyPlaceForm.html")
    else:
        return  render_template("SignIn.html",message1="First Fill this Form !!!")
    

@app.route("/buyProperty",methods=["POST"])
def buyPlace():
    if request.method=="POST":
        number=session.get("apartId")
        email=session.get("email")
        print(number)
        bid=request.form["bid"]
        num=request.form["num"]
        name=request.form["name"]
        for char in name:
            if char.isdigit():
                return render_template("buyPlaceForm.html",message="Name must be in alphabets")
        db=DB("localhost","root","mian2468","ecommerce")
        data=[number,bid,num,name,email]
        inserted=db.buyProperty(data)
        if inserted:
            return render_template("Dashboard.html",message="Property")
        else:
            return  render_template("buyPlaceForm.html" , message="Your Bid is not sufficient for this property")


@app.route('/addPlace')
def addPlace():
    email=session.get("email")
    if email !=None:
        return render_template("AddPlace.html")
    else:
        return  render_template("SignIn.html",message1="First Fill this Form !!!")


#   helper function for converting an image into a suitable form

def convert_image_to_binary(file):
    with open(file, 'rb') as image_file:
        binary_data = image_file.read()
        base64_data = base64.b64encode(binary_data)
    return base64_data


@app.route('/submitProperty', methods=["POST"])
def submitAddPlaceForm():
    if request.method == "POST":
        area = request.form["area"]
        loc = request.form["location"]
        price = request.form["price"]
        owner = request.form["owner"]
        description = request.form["description"]
        image = request.files['image']
        acceptAm=request.form['accprice']

        file_path = 'D:\\6th Semester\\Web\\Project\\Final\\sem proj updated\\static\\images\\' + image.filename
        image.save(file_path)

        # Convert the image to binary data
        binary_data = convert_image_to_binary(file_path)
        email=session.get("email")
        data=[email,area,loc,price,owner,description,binary_data,acceptAm]
        db=DB("localhost","root","mian2468","ecommerce")
        inserted=db.addPlaces(data)
        print(inserted)
        if inserted ==True:
            # return render_template("index.html")
            found, data = db.showPlaces()
            if found:
                apartments = []
                for apartment in data:
                    binary_data = apartment[7]
                    image_data = base64.b64decode(binary_data)
                    base64_image = base64.b64encode(image_data).decode('utf-8')
                    apartments.append({
                        'id': apartment[0],
                        'area':apartment[2],
                        'location':apartment[3],
                        'price': apartment[4],
                        'owner': apartment[5],
                        'description': apartment[6],
                        'image': f"data:image/jpeg;base64,{base64_image}"
                    })
                return render_template("visit places.html", apartments=apartments)
        elif inserted == False:
            return  render_template("AddPlace.html" , message="Some error with your information")
        else:
            return  render_template("AddPlace.html" , message=inserted)
 


# the working of places functionlity ends from here
####
########

# the working of Cars functionality starts from here

@app.route('/goToVisitCars')
def visitCars():
    email = session.get("email")
    if email is not None:
        db = DB("localhost", "root", "mian2468", "ecommerce")
        found, data = db.showCars()
        if found:
            cars = []
            for car in data:
                binary_data = car[6]
                image_data = base64.b64decode(binary_data)
                base64_image = base64.b64encode(image_data).decode('utf-8')
                cars.append({
                    'id': car[0],
                    'seatingCap':car[2],
                    'price':car[3],
                    'owner': car[4],
                    'description': car[5],
                    'image': f"data:image/jpeg;base64,{base64_image}",
                    'name':car[8]
                })
            return render_template("visit Cars.html", cars=cars)
        else :
            return render_template("visit Cars.html", message="No car found")
            
    else:
        return render_template("SignIn.html", message="First fill this form")


@app.route('/addCar')
def addCar():
    email=session.get("email")
    if email !=None:
        return render_template("AddCar.html")
    else:
        return  render_template("SignIn.html",message1="First Fill this Form !!!")

#   helper function for converting an image into a suitable form

def convert_image1_to_binary(file):
    with open(file, 'rb') as image_file:
        binary_data = image_file.read()
        base64_data = base64.b64encode(binary_data)
    return base64_data


@app.route('/submitCar', methods=["POST"])
def submitCarForm():
    if request.method == "POST":
        name = request.form["name"]
        cap = request.form["seatingCap"]
        price = request.form["price"]
        owner = request.form["owner"]
        description = request.form["description"]
        image = request.files['image']
        acceptAm=request.form['accprice']

        file_path = 'D:\\6th Semester\\Web\\Project\\Final\\sem proj updated\\static\\images\\' + image.filename
        image.save(file_path)

        # Convert the image to binary data
        binary_data = convert_image1_to_binary(file_path)
        email=session.get("email")
        data=[email,cap,price,owner,description,binary_data,acceptAm,name]
        db=DB("localhost","root","mian2468","ecommerce")
        inserted=db.addCar(data)
        print(inserted)
        if inserted ==True:
            found, data = db.showCars()
            if found:
                cars = []
                for car in data:
                    binary_data = car[6]
                    image_data = base64.b64decode(binary_data)
                    base64_image = base64.b64encode(image_data).decode('utf-8')
                    cars.append({
                        'id': car[0],
                        'seatingCap':car[2],
                        'price':car[3],
                        'owner': car[4],
                        'description': car[5],
                        'image': f"data:image/jpeg;base64,{base64_image}",
                        'name':car[8]
                    })
                return render_template("visit Cars.html", cars=cars)
        elif inserted == False:
            return  render_template("AddPlace.html" , message="Some error with your information")
        else:
            return  render_template("AddPlace.html" , message=inserted)


@app.route("/buyCars/<int:car_id>")
def renderBuyCar(car_id):
    email=session.get("email")
    session['carId']=car_id
    print(car_id)
    if email !=None:
        return  render_template("buyCarForm.html")
    else:
        return  render_template("SignIn.html",message1="First Fill this Form !!!")

@app.route("/buyCar",methods=["POST"])
def buyCar():
    if request.method=="POST":
        number=session.get("carId")
        email=session.get("email")
        bid=request.form["bid"]
        num=request.form["num"]
        name=request.form["name"]
        for char in name:
            if char.isdigit():
                return render_template("buyPlaceForm.html",message="Name must be in alphabets")
        db=DB("localhost","root","mian2468","ecommerce")
        data=[number,bid,num,name,email]
        inserted=db.buyCar(data)
        if inserted:
            return render_template("Dashboard.html" , message="Car")
        else:
            return  render_template("buyPlaceForm.html" , message="Your Bid is not sufficient for this property")

@app.route('/goToSpecificCar')
def showCarFormPage():
    email=session.get("email")
    if email !=None:
        return  render_template("Search Specific Car Form.html")
    else:
        return  render_template("SignIn.html",message1="First Fill this Form !!!")



@app.route('/goToSpecifiedCars', methods=["POST"])
def visitSpecificCars():
    email = session.get("email")
    if email is not None:
        model=request.form["model"]
        sRange = request.form["start-range"]
        eRange = request.form["end-range"]
        data=[model,sRange,eRange]

        db = DB("localhost", "root", "mian2468", "ecommerce")
        found, data = db.searchSpecificCar(data)
        if found:
            cars = []
            for car in data:
                binary_data = car[6]
                image_data = base64.b64decode(binary_data)
                base64_image = base64.b64encode(image_data).decode('utf-8')
                cars.append({
                    'id': car[0],
                    'seatingCap':car[2],
                    'price':car[3],
                    'owner': car[4],
                    'description': car[5],
                    'image': f"data:image/jpeg;base64,{base64_image}",
                    'name':car[8]
                })
            return render_template("visit Cars.html", cars=cars)
        else :
            return render_template("visit Cars.html", message="No car found")      
    else:
        return render_template("SignIn.html", message="First fill this form")




@app.route('/logout')
def logOutContact():
    if session.get("email"):
        session.clear()
        return render_template("index.html")


    


if __name__ == '__main__':
    app.run(debug=True, port=8001)



