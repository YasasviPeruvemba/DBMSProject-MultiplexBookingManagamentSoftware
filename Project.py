from flask import Flask, render_template,request,redirect,url_for
import mysql.connector
from datetime import datetime
try:
    connection = mysql.connector.connect(user='root', password='qwertyuiop', host='localhost', database='project')
    cursor = connection.cursor()
    print("connected")
except:
    print("not connected")

app = Flask(__name__)

@app.route('/')
@app.route('/Login', methods=['GET', 'POST'])
def login():
    error=request.args.get('error')
    movie=None
    if request.method=='POST':
        username=request.form['user']
        password=request.form['pass']
        if request.form['cred']=='Login':    
            query=("SELECT PASSWORD FROM CUSTOMER WHERE USERNAME='"+username+"';")
            cursor.execute(query)
            print(query)
            result=cursor.fetchall()
            tot=len(result)
            print(password)
            if tot>0:
                    if password==result[0][0]:  
                        if username=="Admin":
                            return redirect(url_for("Admin"))
                        else :    
                            return redirect(url_for('Customer',username=username))
                    else:
                        error="Invalid Password"
            else :
                error="Invalid Username"
        else :
            query=("INSERT INTO LOGIN VALUES('"+password+"','"+username+"');")
            cursor.execute(query)
            connection.commit()
            return redirect(url_for('SignUp',username=username,password=password))
    return render_template("Login.html",error=error)

@app.route('/Admin', methods=['GET','POST'])
def Admin():
    if request.method=='POST':
        return redirect(url_for("login"))
    return render_template("Admin.html")

@app.route('/AddShowsSelect', methods=['GET','POST'])
def AddShowsSelect():
    query=("SELECT MULTIPLEX_NAME FROM MULTIPLEX;")
    cursor.execute(query)
    multiplex=cursor.fetchall()
    query=("SELECT MOV_NAME FROM MOVIES;")
    cursor.execute(query)
    movies=cursor.fetchall()
    if request.method=='POST' :
        if request.form['continue']=='Continue':
            multiplexname=request.form['multiplex']
            moviename=request.form['movie']
            query=("SELECT MULTIPLEX_ID FROM MULTIPLEX WHERE MULTIPLEX_NAME='"+multiplexname+"';")
            cursor.execute(query)
            multiplex=cursor.fetchall()
            multiplexid=multiplex[0][0]
            return redirect(url_for("AddShowsFinal",moviename=moviename,multiplexid=multiplexid))
        else :
            return redirect(url_for("Admin"))
    return render_template("AddShowsSelect.html",data=[multiplex,movies])

@app.route('/AddShowsFinal', methods=['GET','POST'])
def AddShowsFinal():
    moviename=request.args.get('moviename')
    multiplexid=request.args.get('multiplexid')
    date='DATE'
    query=("SELECT SHOW_ID,HALL_NO,"+date+",TIMING FROM SHOWS WHERE MOV_NAME='"+moviename+"' AND MULTIPLEX_ID="+multiplexid+";")
    print(query)
    cursor.execute(query)
    showinfo=cursor.fetchall()
    query=("SELECT HALL_NO FROM HALL WHERE MULTIPLEX_ID='"+multiplexid+"';")
    print(query)
    cursor.execute(query)
    hall=cursor.fetchall()
    if request.method=='POST' :
        if request.form['button']=="Add Show" :
            date=request.form['date']
            timing=request.form['time']
            hallno=request.form["hallno"]
            Date="DATE"
            query=("INSERT INTO SHOWS(MOV_NAME,MULTIPLEX_ID,HALL_NO,"+Date+",TIMING) VALUES('"+moviename+"','"+multiplexid+"','"+hallno+"','"+date+"','"+timing+"');")
            print(query)
            cursor.execute(query)
            connection.commit()
            return redirect(url_for("AddShowsSelect"))
        else :
            return redirect(url_for("AddShowsSelect"))     
    return render_template("AddShowsFinal.html",moviename=moviename,multiplexid=multiplexid,hall=hall,data=showinfo)

@app.route('/RemoveShowSelectMultiplex', methods=['GET','POST'])
def RemoveShowSelectMultiplex():
    query=("SELECT MULTIPLEX_NAME FROM MULTIPLEX;")
    print(query)
    cursor.execute(query)
    multiplexes=cursor.fetchall()
    if request.method=="POST" :
        if request.form['button']=="Remove Show": 
            multiplexname=request.form['multiplex']
            query=("SELECT MULTIPLEX_ID FROM MULTIPLEX WHERE MULTIPLEX_NAME='"+multiplexname+"';")
            print(query)
            cursor.execute(query)
            multiplexid=cursor.fetchall()
            query=("SELECT * FROM SHOWS WHERE MULTIPLEX_ID='"+str(multiplexid[0][0])+"';")
            print(query)
            cursor.execute(query)
            shows=cursor.fetchall()
            return render_template("RemoveShowFinal.html",shows=shows)
        else :
            return redirect(url_for("Admin"))    
    return render_template("RemoveShowSelectMultiplex.html",data=multiplexes)

@app.route('/RemoveShowFinal/<shows>', methods=['GET','POST'])
def RemoveShowFinal(shows):
    if request.method=='POST':
        if request.form['button']=="Remove":
            showid=request.form['showid']
            query=("DELETE FROM SHOWS WHERE SHOW_ID='"+showid+"';")
            print(query)
            cursor.execute(query)
            connection.commit()
            return redirect(url_for("RemoveShowSelectMultiplex"))
        else :
            return redirect(url_for("RemoveShowSelectMultiplex"))  
    return render_template("RemoveShowFinal.html",shows=shows)

@app.route('/FeedBack', methods=['GET','POST'])
def FeedBack():
    query=("SELECT * FROM FEEDBACK;")
    print(query)
    cursor.execute(query)
    feedback=cursor.fetchall()
    if request.method=="POST":
        return redirect(url_for("Admin"))
    return render_template("FeedBack.html",data=feedback)            

@app.route('/AddMovie', methods=['GET','POST'])
def AddMovie():
    if request.method=="POST":
        if request.form['button']=="Add Movie":
            moviename=request.form['moviename']
            genre=request.form['genre']
            rating=request.form['rating']
            cost=request.form['cost']
            query=("INSERT INTO MOVIES VALUES('"+moviename+"','"+genre+"',"+rating+","+cost+");")
            print(query)
            cursor.execute(query)
            connection.commit()
            return redirect(url_for("AddMovie"))
        else :
            return redirect(url_for("Admin"))    
    return render_template("AddMovie.html")

@app.route('/AddCoupon', methods=['GET','POST'])
def AddCoupon():
    if request.method=='POST':
        if request.form['button']=="Add Coupon":
            couponid=request.form['couponid']
            discount=request.form['discount']
            query=("INSERT INTO COUPON VALUES('"+couponid+"',"+str(discount)+","+str(0)+");")
            print(query)
            cursor.execute(query)
            connection.commit()
            return redirect(url_for("AddCoupon"))
        else :
            return redirect(url_for("Admin"))    
    return render_template("AddCoupon.html")

@app.route('/RemoveMovie', methods=['GET','POST'])
def RemoveMovie():
    query=("SELECT MOV_NAME FROM MOVIES;")
    print(query)
    cursor.execute(query)
    movies=cursor.fetchall()
    if request.method=="POST" :
        if request.form['button']=="Remove Movie":
            moviename=request.form['movie']
            query=("CALL DELETEMOVIE('"+moviename+"');")
            print(query)
            cursor.execute(query)
            connection.commit()
            return redirect(url_for("RemoveMovie"))
        else :
            return redirect(url_for("Admin"))   
    return render_template("RemoveMovie.html",data=movies)

@app.route('/ViewSalesSelect', methods=['GET','POST'])
def ViewSalesSelect():
    query=("SELECT MULTIPLEX_NAME FROM MULTIPLEX;")
    print(query)
    cursor.execute(query)
    multiplex=cursor.fetchall()
    if request.method=="POST" :
        if request.form['button']=="Show Details":
            reqdmultiplex=request.form['multiplex']
            if request.form['interval']=="Last Week":
                query=("SELECT * FROM BILLING WHERE MULTIPLEX_NAME='"+reqdmultiplex+"' AND DATE_OF_PURCHASE>(SELECT DATE_SUB(CURDATE(),INTERVAL 7 DAY));")
            else :
                query=("SELECT * FROM BILLING WHERE MULTIPLEX_NAME='"+reqdmultiplex+"' AND DATE_OF_PURCHASE>(SELECT DATE_SUB(CURDATE(),INTERVAL 31 DAY));")
            print(query)
            cursor.execute(query)
            billing=cursor.fetchall()        
            return render_template("ViewSales.html",billing=billing)
        else :
            return redirect(url_for("Admin"))    
    return render_template("ViewSalesSelect.html",data=multiplex)        

@app.route('/Customer/<username>', methods=['GET','POST'])
def Customer(username):
    query=("SELECT * FROM MOVIES ORDER BY RATING DESC;")
    print(query)
    cursor.execute(query)
    movie=cursor.fetchall()
    if request.method=='POST':
        if request.form['book']=="Contact Us":
            return redirect(url_for("ContactUs",username=username))
        elif request.form['book']=="Book Now":
            return redirect(url_for("BookNow",username=username))
        elif request.form['book']=='Logout':
            return redirect(url_for("login"))          
    return render_template("CustHomePage.html",username=username,data=movie)

@app.route('/ContactUs/<username>',methods=['GET','POST'])
def ContactUs(username):
    if request.method=='POST':
        message=request.form['message']
        query=("INSERT INTO FEEDBACK VALUES('"+message+"',NOW(),'"+username+"');")
        print(query)
        cursor.execute(query)
        connection.commit()
        return redirect(url_for("Customer",username=username))
    return render_template("ContactUs.html",username=username)

@app.route('/<username>/BookNow',methods=['GET','POST'])
def BookNow(username):
    query=("SELECT MOV_NAME FROM MOVIES;")
    print(query)
    cursor.execute(query)
    movies=cursor.fetchall()
    query=("SELECT MULTIPLEX_NAME FROM MULTIPLEX;")
    print(query)
    cursor.execute(query)
    multiplex=cursor.fetchall()
    no_multiplex=len(multiplex)
    if request.method=="POST":
        if request.form['button']=="ShortList Shows":
            moviename=request.form['movie']
            multiplexname=request.form['multiplex']
            date=request.form['date']
            return redirect(url_for("BookNowConfirm",username=username,moviename=moviename,multiplexname=multiplexname,date=date))
        else :
            return redirect(url_for("Customer",username=username))    
    return render_template("BookNow.html",username=username,data=[movies,multiplex,no_multiplex])    

@app.route('/<username>/BookNowConfirm',methods=['GET','POST'])
def BookNowConfirm(username):
    error=None
    moviename=request.args.get("moviename")
    multiplexname=request.args.get("multiplexname")
    date=request.args.get("date")
    query=("SELECT TIMING,SHOW_ID FROM SHOWS,MULTIPLEX WHERE SHOWS.MULTIPLEX_ID = MULTIPLEX.MULTIPLEX_ID AND MOV_NAME='"+moviename+"' AND MULTIPLEX_NAME='"+multiplexname+"' AND DATE='"+date+"';")
    print(query)
    cursor.execute(query)
    showtime=cursor.fetchall()
    query=("SELECT * FROM COUPON;")
    print(query)
    cursor.execute(query)
    coupon=cursor.fetchall()
    if request.method=='POST':
        if request.form['cont']=="Back" :
            return redirect(url_for("BookNow",username=username))
        showtime=str(request.form['showtime'])
        movie=request.form['movie']
        multiplex=request.form['multiplex']
        date=request.form['date']
        query=("SELECT COST FROM MOVIES WHERE MOV_NAME='"+movie+"';")
        print(query)
        cursor.execute(query)
        cost=cursor.fetchall()
        costticket=cost[0][0]
        query=("SELECT SHOW_ID FROM SHOWS INNER JOIN MULTIPLEX ON SHOWS.MULTIPLEX_ID=MULTIPLEX.MULTIPLEX_ID WHERE MOV_NAME='"+movie+"' AND MULTIPLEX_NAME='"+multiplex+"' AND DATE='"+date+"' AND TIMING='"+showtime+"';")
        print(query)
        cursor.execute(query)
        showID=cursor.fetchall()
        showIDint=showID[0][0]
        query=("SELECT SEAT_NO FROM TICKETS WHERE SHOW_ID='"+str(showID[0][0])+"';")
        print(query)
        cursor.execute(query)
        seats=cursor.fetchall()
        discount=0
        couponapplied=request.form['coupon']                                     
        if request.form['cont']=='APPLY COUPON & CONTINUE':
            for r in coupon:
                if r[0]==couponapplied and r[2]==0 :
                    query=("UPDATE COUPON SET STATUS=1 WHERE COUPON_ID='"+r[0]+"';")
                    print(query)
                    cursor.execute(query)
                    connection.commit()
                    discount=r[1]   
            return redirect(url_for("BookSeat",username=username,date=date,cost=costticket,discount=discount,showID=showIDint,movie=movie,multiplex=multiplex))
        else :
            return redirect(url_for("BookSeat",username=username,date=date,cost=costticket,discount=discount,showID=showIDint,movie=movie,multiplex=multiplex))
    return render_template("BookNowConfirm.html",username=username,moviename=moviename,multiplexname=multiplexname,date=date,data=showtime)

@app.route('/<username>/BookSeat',methods=['GET','POST'])
def BookSeat(username):
    date=request.args.get('date')
    cost=int(request.args.get('cost'))
    if request.args.get('discount'):
        discount=int(request.args.get('discount'))
    else :
        discount=0 
    showID=request.args.get('showID')
    query=("SELECT SEAT_NO FROM TICKETS WHERE SHOW_ID='"+showID+"';")
    cursor.execute(query)
    seats=cursor.fetchall()
    movie=request.args.get('movie')
    multiplex=request.args.get('multiplex')
    seatmatrix=[]
    for i in range(0,51):
        seatmatrix.append(1)    
    if seats:    
        for r in seats:
            t=int(r[0])
            print(t)
            seatmatrix[t]=0
    cost=int((cost*(100-discount))/100)
    if request.method=='POST':
        if request.form['button']=="Book Ticket" :
            seat=request.form['seat']
            query=("INSERT INTO TICKETS(SEAT_NO,USERNAME,SHOW_ID,COST) VALUES("+str(seat)+",'"+username+"',"+str(showID)+","+str(cost)+");")
            print(query)
            cursor.execute(query)
            connection.commit()
            return redirect(url_for("Ticket",username=username,date=date,movie=movie,multiplex=multiplex,seat=seat,showID=showID))  
    return render_template("BookSeat.html",username=username,cost=cost,date=date,data=seatmatrix,showID=showID,movie=movie,multiplex=multiplex)

@app.route('/<username>/Ticket', methods=["GET","POST"])
def Ticket(username):
    movie=request.args.get('movie')
    multiplex=request.args.get('multiplex')
    showID=request.args.get('showID')
    seat=request.args.get('seat')
    date=request.args.get('date')
    query=("SELECT TIMING FROM SHOWS WHERE SHOW_ID='"+showID+"';")
    print(query)
    cursor.execute(query)
    showtime=cursor.fetchall()
    print(query)
    if request.method=='POST':
        return redirect(url_for("Customer",username=username))
    query=("SELECT HALL_NO FROM SHOWS WHERE SHOW_ID='"+showID+"';")
    print(query)
    cursor.execute(query)
    hall=cursor.fetchall()
    return render_template("Ticket.html",showID=showID,username=username,date=date,showtime=showtime,movie=movie,multiplex=multiplex,seat=seat,data=hall)

@app.route('/SignUp/<username>', methods=["GET","POST"])
def SignUp(username):
    error=None
    password=request.args.get('password')
    if request.method=='POST':
        repass=request.form['pass']
        f_name=request.form['f_name']
        l_name=request.form['l_name']
        gender=request.form['gender']
        phone=request.form['phone']
        mail=request.form['mail']
        if repass==password:
            query=("INSERT INTO CUSTOMER VALUES('"+username+"','"+repass+"','"+f_name+"','"+l_name+"','"+gender+"','"+phone+"','"+mail+"');")
            print(query)
            cursor.execute(query)
            connection.commit()
            return redirect(url_for("login"))
        else:
            error="Passwords did not match"
            query=("DELETE FROM LOGIN WHERE USERNAME='"+username+"';")
            print(query)
            cursor.execute(query)
            connection.commit()
            return redirect(url_for("login",error=error)) 
                
    return render_template("SignUp.html",username=username,password=password)

if __name__ == '__main__':
    app.run(debug=True)
