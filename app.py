from flask import Flask, request, url_for, render_template, session, send_file
from werkzeug.utils import redirect
import hashlib
import socket
import pandas as pd
from datetime import datetime
import pdfkit
import code128

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
app = Flask(__name__)
app.secret_key = "security"
whiteList=['103.25.44.70','192.168.1.35']
loginTime=0
def verifyIP():
    print(IPAddr)
    if IPAddr in whiteList:
        return True
    else:
        return False

def verifyLogIn():
    r=(datetime.now()-loginTime).total_seconds()/60
    if 'loggedin' in session:
        if r<30:
            return 1
        else:
            session.pop('loggedin',None)
            return 0
    else:
        return 0

@app.route('/')
def hello_world():
    if verifyIP()==True:
        return redirect(url_for('login'))
    else:
        return render_template('404error.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        allowed_users = {'srhr1999@gmail.com':'7d4e632ba9ffbffcb7e5d76a364cd91b083db2a48cf2c2ae2a8c1dc4935a68cb'}
        username = request.form['email']
        password = request.form['password']
        to_hash=str(username+password)

        hex_dig = hashlib.sha256(to_hash.encode()).hexdigest()
        print(hex_dig)
        if username in list(allowed_users.keys()):
            if hex_dig==allowed_users[username]:
                print(0)
                print(hex_dig)
                global loginTime
                loginTime=datetime.now()
                print(loginTime)
                session['loggedin']=1
                return render_template('dashboard.html')
            else:
                print(-1)
                return 'Username and Password does not match'
        else:
            print(-2)
            return 'User does not exist in records'

    else:
        return render_template('index.html')

@app.route('/add_employee', methods=['POST', 'GET'])
def add_employee():
    if verifyLogIn():
        if request.method == 'POST':
            structure={'EmployeeID':['#Dummy'],'Name':['#Dummy'],'Father Name':['#Dummy'],'E-Mail':['#Dummy'],'Address':['#Dummy'],'Phone Number':['#Dummy'],'Emergency Phone Number':['#Dummy'],'Educational Qualification':['#Dummy'],'Experience':['#Dummy'],'DOB':['#Dummy'],'DOJ':'DOJ','Salary':['#Dummy'],'Aadhar Number':['#Dummy']}
            name = request.form['name']
            fathername = request.form['fathername']
            email = request.form['email']
            phonenumber = request.form['phonenumber']
            emergencyphonenumber = request.form['emergencyphonenumber']
            address = request.form['address']
            education = request.form['education']
            experience = request.form['experience']
            dob = request.form['dob']
            doj=request.form['doj']
            salary = request.form['salary']
            job = request.form['job']
            aadharnumber= request.form['aadharnumber']
            df=pd.read_csv('employee_details.csv')
            structure['EmployeeID'] = "SRSS_"+str(int(df.shape[0])+1)
            structure['Name']=name
            structure['Father Name']=fathername
            structure['E-Mail']=email
            structure['Phone Number']=phonenumber
            structure['Emergency Phone Number']=emergencyphonenumber
            structure['Address']=address
            structure['Educational Qualification']=education
            structure['Experience']=experience
            structure['DOB']=dob
            structure['DOJ']=doj
            structure['Salary']=salary
            structure['Aadhar Number']=aadharnumber
            structure['Role']=job
            df = df.append(structure, ignore_index=True)
            print(df.shape)
            df.to_csv('employee_details.csv',index=False)
            return render_template('success.html')

        else:

            return render_template('add_employee.html')
    else:
        return render_template('logout.html')

@app.route('/add_company', methods=['POST', 'GET'])
def add_company():
    if verifyLogIn():
        if request.method == 'POST':
            structure={'CompanyID':['#Dummy'],'Name':['#Dummy'],'E-Mail':['#Dummy'],'Address':['#Dummy'],'Phone Number':['#Dummy'],'Quotation':['#Dummy'],'DOJ':['#Dummy'],'GST Number':['#Dummy']}
            name = request.form['name']
            email = request.form['email']
            phonenumber = request.form['phonenumber']
            address = request.form['address']
            quotation = request.form['quotation']
            doj=request.form['doj']
            gstnumber= request.form['gstnumber']
            df=pd.read_csv('company_details.csv')
            # df=pd.DataFrame(structure)
            # df.drop(index=0,axis=0,inplace=True)
            structure['CompanyID'] = "CMP_"+str(int(df.shape[0])+1)
            structure['Name']=name
            structure['E-Mail']=email
            structure['Phone Number']=phonenumber
            structure['Address']=address
            structure['Quotation']=quotation
            structure['DOJ']=doj
            structure['GST Number']=gstnumber
            df = df.append(structure, ignore_index=True)
            print(df.shape)
            df.to_csv('company_details.csv',index=False)
            return render_template('success.html')

        else:

            return render_template('add_company.html')
    else:
        return render_template('logout.html')


@app.route('/view_employee')
def view_employee():
    if verifyLogIn():
        df=pd.read_csv('employee_details.csv')
        return render_template('view_employee.html',df=df,columns=df.columns)
    else:
        return render_template('logout.html')

@app.route('/view_company')
def view_company():
    if verifyLogIn():
        df=pd.read_csv('company_details.csv')
        return render_template('view_company.html',df=df,columns=df.columns)
    else:
        return render_template('logout.html')

@app.route('/employee_attendance', methods=['POST', 'GET'])
def employee_attendance():
    if verifyLogIn():
        if request.method == 'POST':
            structure={'EmployeeID':['#Dummy'],'CompanyID':['#Dummy'],'Date':['#Dummy'],'Money Given':['#Dummy']}
            empid = request.form['empid']
            cmpid = request.form['cmpid']
            money = request.form['money']

            df=pd.read_csv('attendance_details.csv')
            # df=pd.DataFrame(structure)
            # df.drop(index=0,axis=0,inplace=True)
            structure['EmployeeID'] = empid
            structure['CompanyID'] = cmpid
            structure['Date'] = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
            structure['Money Given']="-"+str(money)

            df = df.append(structure, ignore_index=True)
            print(df.shape)
            df.to_csv('attendance_details.csv',index=False)
            return render_template('success.html')

        else:
            df=pd.read_csv('employee_details.csv')
            df1 = pd.read_csv('company_details.csv')
            emp_id=list(df['EmployeeID'])
            emp_name=list(df['Name'])
            cmp_id=list(df1['CompanyID'])
            cmp_name=list(df1['Name'])
            return render_template('employee_attendance.html',emp_id=emp_id,emp_name=emp_name,cmp_id=cmp_id,cmp_name=cmp_name)
    else:
        return render_template('logout.html')

@app.route('/payroll', methods=['POST', 'GET'])
def payroll():
    if verifyLogIn():
        df = pd.read_csv('employee_details.csv')
        emp_id = list(df['EmployeeID'])
        emp_name = list(df['Name'])
        if request.method == 'POST':
            structure={'EmployeeID':['#Dummy'],'Date Paid':['#Dummy'],'Amount Paid':['#Dummy'],'Start Date':['#Dummy'],'End Date':['#Dummy']}
            empid = request.form['empid']
            startdate = request.form['startdate']
            enddate = request.form['enddate']
            df2=pd.read_csv('attendance_details.csv')
            Salary=int(df[df['EmployeeID']==str(empid)]['Salary'])
            print(Salary)
            k = df2[(df2['Date'] >= startdate) & (df2['Date'] <= enddate)].groupby('EmployeeID').sum()
            if (str(empid) in list(k.index)):
                k.reset_index(inplace=True)
                amtGiven=int(k[k['EmployeeID'] == str(empid)]['Money Given'])
                print(amtGiven)
            else:
                amtGiven=0
            money=int(Salary)+int(amtGiven)
            df1=pd.read_csv('payroll_details.csv')
            # df1=pd.DataFrame(structure)
            # df1.drop(index=0,axis=0,inplace=True)
            structure['EmployeeID'] = empid
            structure['Start Date'] = startdate
            structure['End Date'] = enddate
            structure['Date Paid'] = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
            structure['Amount Paid']=str(money)

            df1 = df1.append(structure, ignore_index=True)
            print(df1.shape)
            df1.to_csv('payroll_details.csv',index=False)
            return render_template('payroll.html',emp_id=emp_id,emp_name=emp_name,salary=money,basesalary=Salary,amtGiven=amtGiven)

        else:
            return render_template('payroll.html',emp_id=emp_id,emp_name=emp_name)
    else:
        return render_template('404error.html')

@app.route('/dashboard')
def dashboard():
    if verifyLogIn():
        return render_template('dashboard.html')
    else:
        return render_template('logout.html')

@app.route('/downloadEmployeeData')
def downloadEmployeeData ():
    path = "D:/Security/employee_details.csv"
    return send_file(path, as_attachment=True)

@app.route('/downloadCompanyData')
def downloadCompanyData ():
    path = "D:/Security/company_details.csv"
    return send_file(path, as_attachment=True)

@app.route('/logout')
def logout():
    if verifyLogIn():
        session.pop('loggedin', None)
        return render_template('logout.html')
    else:
        return render_template('404error.html')

# main driver function
if __name__ == '__main__':
    app.run()
