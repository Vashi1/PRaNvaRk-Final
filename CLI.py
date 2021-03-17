def authorisation(a, b):
    # FixedTODO Fix the bug regarding non-admin users in authorisation
    # flag is for ADMIN and chkr is for password
    import mysql.connector as sql
    flag = 0
    chkr = 0
    data = 0
    myql = sql.connect(host="localhost", user="Rakshith", password="Rakshith1@", database="medical_store")
    cur = myql.cursor(buffered=True)
    cur.execute("select Password from payroll where Uid = {}".format(a))
    d = cur.fetchone()
    if d is None:
        print("login not authorised! Please try again")
    elif d is not None:
        for c in d:
            data = c
        if data == b:
            print("login authorised")
            chkr = 1
            cur.execute("select ADMIN from payroll where Uid = {}".format(a))
            admin = cur.fetchone()
            if admin[0].lower() == "no":
                flag = 1
        elif data != b:
            print("The Password is incorrect")
    return flag, chkr


def list_user():
    import mysql.connector as sql
    from tabulate import tabulate
    myql = sql.connect(host="localhost", user="Rakshith", password="Rakshith1@", database="medical_store")
    cur = myql.cursor()
    cur.execute("select Uid, Name, ADMIN, Password from payroll")
    data = cur.fetchall()
    headers = ["Uid", "Name", "ADMIN", "Password"]
    print(tabulate(data, headers, tablefmt="grid"))


def user_manage_main():
    while True:
        print("\t\t\t1.Add User")
        print("\t\t\t2.Edit User Information")
        print("\t\t\t3.Search User")
        print("\t\t\t4.Delete User")
        print("\t\t\t5.List All Users")
        print("\t\t\t6.Back to Main Menu")
        choi_usr = input("Enter your choice : ")
        if choi_usr == '1':
            add_usr()
        elif choi_usr == '2':
            editusr()
        elif choi_usr == '3':
            srch_usr()
        elif choi_usr == '4':
            del_usr()
        elif choi_usr == '6':
            break
        elif choi_usr == "5":
            list_user()
        else:
            print("Please input a valid input")


def add_usr():
    while True:
        import mysql.connector as sql
        myql = sql.connect(host='localhost', user='Rakshith', password='Rakshith1@', database="medical_store")
        print("Please input the following data!")
        f = open("uid.txt", "r+")
        data = int(f.read())
        name = input("Enter the name : ")
        d_o_j = input("Enter the Date of joining(yyyy-mm-dd) : ")
        salary = int(input("Enter the salary : "))
        address = input("Enter the address : ")
        mobile_no = int(input("Enter the mobile number : "))
        email = input("Enter the email address : ")
        adm_right = input("Do you want to grant user rights(yes/no) : ")
        pa_wd = input("Enter the password for the user : ")
        cur = myql.cursor()
        cur.execute(
            "insert into payroll values ({}, '{}', '{}', {}, '{}', {}, '{}','{}','{}')".format(data, name, d_o_j,
                                                                                               salary,
                                                                                               address, mobile_no,
                                                                                               email, adm_right, pa_wd))
        f.close()
        f = open("uid.txt", "w")
        f.write(str(data + 1))
        f.close()
        print(cur.rowcount, "User was added")
        myql.commit()
        cho1 = input("Do you want to continue(y/n)")
        if cho1 == "y":
            pass
        elif cho1 == "n":
            myql.close()
            break
        else:
            print("Please enter a valid input")


def editusr():
    while True:
        print("Uid\tName\tD_O_J\tSalary\tAddress\tMobile_number\tE_mail\tADMIN\tPassword")
        clmn = input("Enter the column name : ")
        vlue = input("Enter the new value : ")
        uid = int(input("Enter the UID for the user : "))
        if clmn in ["Salary", "Mobile_number"]:
            import mysql.connector as sql
            myql = sql.connect(host="localhost", user='Rakshith', password="Rakshith1@", database='medical_store')
            cur = myql.cursor()
            cur.execute("update payroll set {0} = {1} where Uid = {2}".format(clmn, vlue, uid))
            print(cur.rowcount, "column was modified")
            myql.commit()
            cho2 = input("Do you want to continue(y/n) : ")
            if cho2 == 'y':
                pass
            elif cho2 == "n":
                myql.close()
                break
        elif clmn in ["Name", "D_O_J", "Address", "E_mail", "ADMIN", "Password"]:
            import mysql.connector as sql
            myql = sql.connect(host="localhost", user='Rakshith', password="Rakshith1@", database='medical_store')
            cur = myql.cursor()
            cur.execute("update payroll set {0} = '{1}' where Uid = {2}".format(clmn, vlue, uid))
            print(cur.rowcount, "column was modified")
            myql.commit()
            cho2 = input("Do you want to continue(y/n) : ")
            if cho2 == 'y':
                pass
            elif cho2 == "n":
                myql.close()
                break
        elif clmn == "Uid":
            print("ERROR! Uid cannot be changed")
            break
        else:
            print("Please enter a valid input!")


def srch_usr():
    from tabulate import tabulate
    while True:
        print("\t\t\t1.Do you search by Uid")
        print("\t\t\t2.Search by Username")
        print("\t\t\t3.Back(User Management)")
        cho3 = int(input("\t\t\tEnter your input : "))
        if cho3 == 1:
            uid1 = int(input("Enter the userid you want to search : "))
            import mysql.connector as sql
            myql = sql.connect(host="localhost", user='Rakshith', password="Rakshith1@", database='medical_store')
            cur = myql.cursor()
            cur.execute(
                "select Uid, Name, D_O_J, Salary, Address, Mobile_number, E_mail, ADMIN from payroll where Uid = {0}".format(
                    uid1))
            data = cur.fetchall()
            if data is None or data == []:
                print("The user does not exists")
            elif data is not None:
                print("The user exists")
                # The admi will tell whether the logged in user has admin rights
                cho4 = input("Do you want to view further details(y/n) : ")
                if cho4 == "y":
                    headers = ["Uid", "Name", "D_O_J", "Salary", "Address", "Mobile_number", "E_mail", "ADMIN"]
                    print(tabulate(data, headers, tablefmt="grid"))
        elif cho3 == 3:
            break
        elif cho3 == 2:
            uid2 = input("Enter the Username : ")
            import mysql.connector as sql
            myql = sql.connect(host="localhost", user='Rakshith', password="Rakshith1@", database='medical_store')
            cur = myql.cursor()
            cur.execute(
                "select Uid, Name, D_O_J, Salary, Address, Mobile_number, E_mail, ADMIN from payroll where Name = '{0}'".format(
                    uid2))
            data = cur.fetchall()
            if data is None or data == []:
                print("The user does not exists")
            elif data is not None:
                print("The user exists")
                cho4 = input("Do you want to view further details(y/n) : ")
                if cho4 == "y":
                    headers = ["Uid", "Name", "D_O_J", "Salary", "Address", "Mobile_number", "E_mail", "ADMIN"]
                    print(tabulate(data, headers, tablefmt="grid"))


def del_usr():
    while True:
        uid = int(input("Enter the user_id to be deleted : "))
        import mysql.connector as sql
        myql = sql.connect(host="localhost", user='Rakshith', password="Rakshith1@", database='medical_store')
        cur = myql.cursor()
        cur.execute("delete from payroll where Uid = {}".format(uid))
        myql.commit()
        print(cur.rowcount, "user was deleted")
        print("""\n
                         \n
                         \n""")
        chi = input("Do you want to continue(y/n) : ")
        if chi == "y":
            pass
        elif chi == "n":
            myql.close()
            break


def add_order():
    a = open("Sales_id.txt", "r+")
    f = int(a.read())
    from datetime import date
    today = date.today()
    d1 = today.strftime("%Y-%m-%d")
    import mysql.connector as sql
    myql = sql.connect(host="localhost", user="Rakshith", password="Rakshith1@", database="medical_store")
    cur = myql.cursor()
    print("Enter the following data :-")
    sid = f + 1
    c_name = input("Enter the customer name : ")
    while True:
        tp = 0
        gtp = 0
        mid = input("Enter the Mid of the product : ")
        cur.execute("select Quantity from stocks where mid = {}".format(mid))
        daa = cur.fetchall()
        if daa == []:
            print("ERROR ! No such medicine exists! Breaking the loop")
            break
        else:
            cur.execute("select GST from stocks where mid = {}".format(mid))
            daaa = cur.fetchall()
            print(daa)
            gst = daaa[0][0]
            a = daa[0][0]
            cur.execute("select discount from stocks where Mid = {}".format(mid))
            daa1 = cur.fetchall()
            discount = daa1[0][0]
            print("Quantity available is ", a)
            quan = int(input("Enter the quantity : "))
            if quan <= a:
                cur.execute("update stocks set Quantity = Quantity - {} where Mid = {}".format(quan, mid))
                myql.commit()
                cur.execute("select Price from stocks where Mid = {}".format(mid))
                price = cur.fetchall()
                idprice = price[0][0] * quan
                # itemgst = idprice *
                tp = (idprice + ((gst * idprice) / 100))
                gtp = tp - ((discount * tp) / 100)
                ch = input("Do you want to continue(y/n)?")
                if ch == "y" or ch == "Y":
                    cur.execute(
                        "insert into bill_detail values({}, '{}', '{}', {}, {}, {}, {}, {})".format(sid, c_name, d1, mid,
                                                                                                    gst, discount, gtp,
                                                                                                    quan))
                    myql.commit()
                    pass
                elif ch == "n" or ch == "N":
                    # tp = tp - ((discount * tp) / 100)
                    cur.execute(
                        "insert into bill_detail values({}, '{}', '{}', {}, {}, {}, {}, {})".format(sid, c_name, d1, mid,
                                                                                                    gst, discount, gtp,
                                                                                                    quan))
                    myql.commit()
                    cur.execute("select sum(tp) from bill_detail where Bill_id = {} group by Bill_id".format(sid))
                    total_price = cur.fetchone()
                    print("total price", total_price[0])
                    cur.execute(
                    "insert into sales values({}, '{}', {}, '{}')".format(sid, c_name, total_price[0], d1))
                    myql.commit()
                    f = open("Sales_id.txt", "w")
                    f.write(str(sid))
                    f.close()
                    myql.commit()
                    break
            else:
                print("Please check the stocks again!")


def sales_manage_main():
    while True:
        print("1.Generate e-Bill")
        print("2.View all bills")
        print("3.Search bills")
        print("4.Back(Main Menu)")
        ch = input("Enter your choice : ")
        if ch == "1":
            add_order()
        elif ch == "2":
            view_order()
        elif ch == "3":
            search_order()
        elif ch == "4":
            break
        else:
            print("Please enter a valid input")


def view_order():
    from tabulate import tabulate
    import mysql.connector as sql
    myql = sql.connect(host="localhost", user="Rakshith", password="Rakshith1@", database="medical_store")
    cur = myql.cursor()
    cur.execute("Select * from sales")
    data = cur.fetchall()
    if data is None or data == []:
        print("No orders exist")
    elif data is not None:
        headers = ["Bill_id", "C_name", "Total Price", "Date_of_sale"]
        print(tabulate(data, headers, tablefmt="grid"))


def search_order():
    import mysql.connector as sql
    from tabulate import tabulate
    bid = int(input("Enter the bill_id : "))
    myql = sql.connect(host="localhost", user="Rakshith", password="Rakshith1@", database="medical_store")
    cur = myql.cursor()
    cur.execute("select * from sales where sale_id = {}".format(bid))
    data = cur.fetchall()
    if data is None or data == []:
        print("No such order exists")
    else:
        headers = ["sale_id", "C_name", "Total_Price", "D_O_S"]
        print(tabulate(data, headers, tablefmt="grid"))
        choice = input("Do you want to view further details?(yes/no) : ")
        if choice.lower() == "no":
            pass
        elif choice.lower() == "yes":
            cur.execute("select * from bill_detail where Bill_id = {}".format(bid))
            dat = cur.fetchall()
            headers = ["Bill_id", "Cust_name", "bill_date", "mid", "GST_val", "Dis", "tp", "Quantity"]
            print(tabulate(dat, headers, tablefmt="grid"))
        else:
            print("Please enter a valid input")


def add_sup_order():
        choice = input("Do you want to add an existing product(1) or a non existing product(0) : ")
        if choice == "1":
            while True:
                from datetime import date
                today = date.today()
                d1 = today.strftime("%Y-%m-%d")
                print("Enter the following data!")
                f = open("Supply.txt", "r+")
                data = int(f.read())
                f.close()
                a = open("order_sp.txt", "r")
                order_sp = int(a.read())
                a.close()
                supid = input("Enter the supplier id: ")
                mid = input("Enter the Mid : ")
                import mysql.connector as sql
                myql = sql.connect(host="localhost", user="Rakshith", password="Rakshith1@", database="medical_store")
                cur = myql.cursor()
                cur.execute("select * from stocks where Mid = {}".format(mid))
                data_db = cur.fetchall()
                if data_db == []:
                    print("Error ! No such medicine exists! ")
                    break
                else:
                # Existing
                    print("The data is shown below :-")
                    print("Mid", "Mname", 'Sname', "Bname", "Existing quantity", "price", "location", "EXP_data",
                          'date of manufacturing',
                          sep='\t\t')
                    for i in range(0, cur.rowcount):
                        mname = data_db[i][1]
                        sname = data_db[i][2]
                        bname = data_db[i][3]
                        quan = data_db[i][4]
                        price = data_db[i][5]
                        location = data_db[i][6]
                        expdata = data_db[i][7]
                        D_O_M = data_db[i][8]
                        gst = data_db[i][9]
                        discount = data_db[i][10]
                        stat = 1
                        # fixedTODO add the field name
                        print(
                            "------------------------------------------------------------------------------------------------------------------------------------------------------------------")
                        print(mid, mname, sname, bname, quan, price, location, expdata, D_O_M, sep="\t\t")
                    ch = int(input("Enter the quantity to be ordered : "))
                    dod = input("Enter the date of delivery(YYYY-MM-DD) : ")
                    cur.execute(
                        "insert into supplier_data(orderid, order_date, supplier_id, Mid, Quantity, Price, Delievery_date, "
                        "Mname, Saltname, Brandname, Location, GST, discount, status, order_sp) values({},'{}',{},{},{},{},"
                        "'{}','{}', '{}', '{}', '{}', {}, {}, {}, {})".format(
                        data, d1, supid, mid, ch, price, dod, mname, sname, bname, location, gst, discount,
                        stat, order_sp))
                    myql.commit()
                    print(cur.rowcount, "Order was added")
                    myql.commit()
                    f = open("Supply.txt", "w+")
                    data = data + 1
                    f.write(str(data))
                    f.close()

                    choi_con = input("Do you want to continue(y/n) : ")
                    if choi_con.lower() == "y" or choi_con == "yes":
                        pass
                    elif choi_con.lower() == "n" or choi_con == "no":
                        f = open("order_sp.txt", "w")
                        f.write(str(data))
                        f.close()
                        break
                    else:
                        break
        elif choice == "0":
            while True:
                from datetime import date
                # Non-existing
                today = date.today()
                supid = input("Enter the supplier id: ")
                d1 = today.strftime("%Y-%m-%d")
                f = open("Supply.txt", "r+")
                data = int(f.read())
                f.close()
                f = open("Mid.txt", 'r+')
                mid = int(f.read())
                f.close()
                mname = input("Enter the Mname : ")
                salt_nme = input("Enter the salt name : ")
                b_name = input("Enter the Brand name : ")
                quan = int(input("Enter the quantity : "))
                price = int(input("Enter the cost : "))
                location = "Not specified"
                dod = input("Enter the Date_of_Delivery(YYYY-MM-DD) : ")
                GST = 0
                stat = 0
                discount = 0
                a = open("order_sp.txt", "r+")
                order_sp = int(a.read())
                import mysql.connector as sql
                myql = sql.connect(host="localhost", user="Rakshith", password="Rakshith1@", database="medical_store")
                cur = myql.cursor()
                cur.execute(
                    "insert into supplier_data(orderid, order_date, supplier_id, Mid, Quantity, Price, Delievery_date, Mname, Saltname, Brandname, Location, GST, discount, status, order_sp) values({},'{}',{},{},{},{},'{}','{}', '{}', '{}', '{}', {}, {}, {}, {})".format(
                        data, d1, supid, mid, quan, price, dod, mname, salt_nme, b_name, location, GST, discount,
                        stat, order_sp))
                myql.commit()
                f = open("Supply.txt", "w+")
                data = data + 1
                f.write(str(data))
                f.close()
                f = open("Mid.txt", "w+")
                mid += 1
                f.write(str(mid))
                f.close()
                choi_con = input("Do you want to continue(y/n) : ")
                if choi_con.lower() == "y" or "yes":
                    pass
                elif choi_con.lower() == "n" or "no":
                    a = open("order_sp.txt", "w")
                    order_sp += 1
                    a.write(str(order_sp))
                    a.close()
                    break
                else:
                    break


def recieve_sup_order():
    oid0 = int(input("Enter the order_sp : "))
    import mysql.connector as sql
    myql = sql.connect(host="localhost", user="Rakshith", password="Rakshith1@", database="medical_store")
    cur = myql.cursor()
    cur.execute(
        "select orderid, order_date, supplier_id, Mid, Quantity, Price, Delievery_date from supplier_data where order_sp = {}".format(
            oid0))
    data = cur.fetchall()
    print(cur.rowcount)
    if data == None or data == []:
        print("The Table is empty")
    else:
        print("The data is shown below :-")
        print("order_sp", "order_date", 'supplier_id', "Quantity", "Price", "Delivery_date", sep='\t\t')
        for i in range(0, cur.rowcount):
            print(i)
            oid = data[i][0]
            odate = data[i][1]
            supid = data[i][2]
            mid = data[i][3]
            quan = data[i][4]
            price = data[i][5]
            Delievery_date = data[i][6]
            print(
                "------------------------------------------------------------------------------------------------------------------------------------------------------------------")
            print(oid0, odate, supid, quan, price, Delievery_date, sep="\t\t")
            ch = input("Do you want to continue(y/n) : ")
            if ch == "y":
                cur.execute("select status from supplier_data where orderid = {}".format(oid))
                dat = cur.fetchall()
                if dat[0][0] == 1:
                    cur.execute('select Mid, Quantity, Saltname from supplier_data where orderid = {}'.format(oid))
                    data_sup_data = cur.fetchall()
                    for i in range(0, cur.rowcount):
                        mid = data_sup_data[i][0]
                        print(mid)
                        quan = data_sup_data[i][1]
                        cur.execute("update stocks set Quantity = Quantity + {} where Mid = {}".format(quan, mid))
                        cur.execute("update supplier_data set status = 2 where orderid = {}".format(oid))
                        myql.commit()
                elif dat[0][0] == 0:
                    cur.execute(
                        "select Mid, Mname, Saltname, Brandname, Quantity, Price, Location, Exp_date, order_date, GST, discount from supplier_data where order_sp = {}".format(
                            oid0))
                    data_sup_data = cur.fetchall()
                    for i in range(0, cur.rowcount):
                        mname = data_sup_data[i][1]
                        s_nme = data_sup_data[i][2]
                        bname = data_sup_data[i][3]
                        quant = data_sup_data[i][4]
                        pric = data_sup_data[i][5]
                        loca = data_sup_data[i][6]
                        expdata = input("Enter the expiry date(YYYY-MM-DD) :")
                        order_da = data_sup_data[i][8]
                        gst = int(input("Enter the GST value : "))
                        disco = int(input("Enter the discount value : "))
                        cur.execute(
                            "insert into stocks values({}, '{}', '{}', '{}', {}, {}, '{}', '{}', '{}', {}, {})".format(mid,
                                                                                                                       mname,
                                                                                                                       s_nme,
                                                                                                                       bname,
                                                                                                                       quant,
                                                                                                                       pric,
                                                                                                                       loca,
                                                                                                                       expdata,
                                                                                                                       order_da,
                                                                                                                       gst,
                                                                                                                       disco))
                        myql.commit()
                        cur.execute("update supplier_data set status = 2 where order_sp = {}".format(oid0))
                        myql.commit()
                elif dat[0][0] == 2:
                    print("The order is already added")
            if ch == "n":
                pass


def list_product():
    import mysql.connector as sql
    from tabulate import tabulate
    myql = sql.connect(host="localhost", user='Rakshith', password="Rakshith1@", database="medical_store")
    cur = myql.cursor()
    cur.execute("select * from stocks")
    data = cur.fetchall()
    if data == ('None',):
        print("The Table is empty")
    else:
        print("The data is shown below :-")
        headers = ["Mid", "Mname", "Sname", "Bname", "quantity", "price", 'location', "EXP_date",
                   'date of manufacturing', "GST", "discount"]
        print(tabulate(data, headers, tablefmt="grid"))


def edit_product():
    while True:
        mid = input("Enter the Mid of the Product : ")
        print("Mid Mname Saltname Brandname Quantity Price Location Exp_date D_O_M GST discount")
        fname = input("Enter the field name : ")
        val = input("Enter the new value : ")
        char_fields = ['Saltname', 'Brandname', 'Location', "Exp_date", "D_O_M"]
        if fname in char_fields:
            import mysql.connector as sql
            myql = sql.connect(host="localhost", user="Rakshith", password="Rakshith1@", database="medical_store")
            cur = myql.cursor()
            cur.execute("update stocks set {0} = '{1}' where Mid = {2}".format(fname, val, mid))
            myql.commit()
            print(cur.rowcount, "user is modified.")

        elif fname == "Mname":
            import mysql.connector as sql
            myql = sql.connect(host="localhost", user="Rakshith", password="Rakshith1@", database="medical_store")
            cur = myql.cursor()
            cur.execute("update stocks set {0} = '{1}' where Mid = {2}".format(fname, val, mid))
            myql.commit()
            print(cur.rowcount, "user is modified.")
        elif fname == "Quantity":
            import mysql.connector as sql
            myql = sql.connect(host="localhost", user="Rakshith", password="Rakshith1@", database="medical_store")
            cur = myql.cursor(buffered=True)
            cur.execute("update stocks set Quantity={0} where Mid={1}".format(val, mid))
            myql.commit()

        elif fname not in char_fields:
            import mysql.connector as sql
            myql = sql.connect(host="localhost  ", user="Rakshith", password="Rakshith1@", database="medical_store")
            cur = myql.cursor()
            cur.execute("update stocks set {0} = {1} where Mid = {2}".format(fname, val, mid))
            myql.commit()
            print(cur.rowcount, "product is modified.")
        else:
            print("Please enter a valid input!")
        ch = input("Do you want to continue(y/n) : ")
        if ch == "y":
            pass
        elif ch == "n":
            break
        else:
            print("Please enter a valid input!")


def search_product():
    while True:
        print("\t\t\tDo you want to search by:-")
        print("\t\t\t1.Search by Mid")
        print("\t\t\t2.Search by Mname")
        print("\t\t\t3.Seach by Salt_name")
        print("\t\t\t4.Back(Main Menu)")
        ch = input("Enter your choice : ")
        if ch == "1":
            while True:
                from tabulate import tabulate
                inp = int(input("Enter the Mid :"))
                import mysql.connector as sql
                myql = sql.connect(host="localhost", user="Rakshith", password="Rakshith1@", database="medical_store")
                cur = myql.cursor()
                cur.execute("select * from stocks where Mid = {}".format(inp))
                data = cur.fetchone()
                # ad = 0
                # for i in data:
                #    ad = i
                if data == [] or data is None:
                    print("The product is not available in inventory")
                    break
                else:
                    print("The product is available in the inventory")
                    ch1 = input("Do you want to view more information(y/n) : ")
                    if ch1 == "y":
                        print("Mid", "Mname", "Saltname", "Brandname", "Quantity", "Price", "Location", "Exp_date",
                              "D_O_M", sep="\t\t\t")
                        print(
                            "-------------------------------------------------------------------------------------------------------------------------------------------")
                        mid = data[0]
                        mname = data[1]
                        saltname = data[2]
                        brandname = data[3]
                        quantity = data[4]
                        price = data[5]
                        location = data[6]
                        expdate = data[7]
                        dom = data[8]
                        print(mid, mname, saltname, brandname, quantity, price, location, expdate, dom, sep="\t\t\t")
                        break
                    if ch1 == "n":
                        break
                    else:
                        print("Please enter a valid input!")
        elif ch == '2':
            while True:
                mname = input("Enter the M_name : ")
                import mysql.connector as sql
                myql = sql.connect(host="localhost", user="Rakshith", password="Rakshith1@", database="medical_store")
                cur = myql.cursor()
                cur.execute("select * from stocks where Mname = '{}'".format(mname))
                data = cur.fetchall()
                if data is None or data == []:
                    print("The product is not available in inventory")
                    break
                elif data is not None:
                    print("The product is available in the inventory")
                    ch1 = input("Do you want to view more information(y/n) : ")
                    if ch1 == "y":
                        print("Mid", "Mname", "Saltname", "Brandname", "Quantity", "Price", "Location", "Exp_date",
                              "D_O_M", sep="\t\t\t")
                        print(
                            "-------------------------------------------------------------------------------------------------------------------------------------------")
                        """mid = data[0]
                        mname = data[1]
                        saltname = data[2]
                        brandname = data[3]
                        quantity = data[4]
                        price = data[5]
                        location = data[6]
                        expdate = data[7]
                        dom = data[8]
                        print(mid, mname, saltname, brandname, quantity, price, location, expdate, dom, sep="\t\t\t")"""
                        for i in data[0]:
                            print(i, end="\t\t\t")
                        break
                    if ch1 == "n":
                        break
                    else:
                        print("Please enter a valid input!")
        elif ch == "3":
            while True:
                msalt = input("Enter the salt name : ")
                import mysql.connector as sql
                myql = sql.connect(host="localhost", user="Rakshith", password="Rakshith1@", database="medical_store")
                cur = myql.cursor()
                cur.execute("select * from stocks where Saltname = '{}'".format(msalt))
                data = cur.fetchall()
                ad = 0
                for i in data:
                    ad = i
                if ad == 0:
                    print("The product is not available in inventory")
                    break
                elif ad != 0:
                    print("The product is available in the inventory")
                    ch1 = input("Do you want to view more information(y/n) : ")
                    if ch1 == "y":
                        print("Mid", "Mname", "Saltname", "Brandname", "Quantity", "Price", "Location", "Exp_date",
                              "D_O_M", sep="\t\t\t")
                        print(
                            '-------------------------------------------------------------------------------------------------------------------------------------------')
                        '''mid = data[0]
                        mname = data[1]
                        saltname = data[2]
                        brandname = data[3]
                        quantity = data[4]
                        price = data[5]
                        location = data[6]
                        expdate = data[7]
                        dom = data[8]
                        print(mid, mname, saltname, brandname, quantity, price, location, expdate, dom, sep="\t\t\t")'''
                        for i in data[0]:
                            print(i, end="\t\t\t")
                        break
                    if ch1 == "n":
                        break
                    else:
                        print("Please enter a valid input!")
        elif ch == "4":
            break
        else:
            print("Please enter a valid input!")


def del_product():
    print("\t\t\t1.Delete by Mname")
    print("\t\t\t2.Delete by Mid")
    ch = input("Enter your choice : ")
    import mysql.connector as sql
    myql = sql.connect(host="localhost", user="Rakshith", password="Rakshith1@", database="medical_store")
    cur = myql.cursor()
    if ch == "1":
        mname = input("Enter the Mname : ")
        cur.execute("delete from stocks where Mname = '{0}'".format(mname))
        print(cur.rowcount, "item was deleted")
        myql.commit()
    elif ch == "2":
        mid = input("Enter the Mid : ")
        cur.execute("delete from stocks where Mid  = '{0}'".format(mid))
        print(cur.rowcount, "item was deleted")
        myql.commit()


def exp_product():
    import mysql.connector as sql
    from tabulate import tabulate
    # fixedTODO add for blank
    myql = sql.connect(host="localhost", user="Rakshith", password="Rakshith1@", database="medical_store")
    cur = myql.cursor()
    cur.execute("select * from stocks where Exp_date < curdate()")
    data = cur.fetchall()
    if data is None or data == []:
        print("No expired product exists")
    else:
        print("The details of expired products if given below : ")
        headers = ["Mid", "Mname", "Saltname", "Brandname", "Quantity", "Price", "Location", "Exp_date", "D_O_M", "GST",
                   "discount"]
        print(tabulate(data, headers, tablefmt="grid"))


def disp_sup_order():
    import mysql.connector as sql
    from tabulate import tabulate
    myql = sql.connect(host='localhost', user="Rakshith", password="Rakshith1@", database="medical_store")
    cur = myql.cursor()
    cur.execute('select * from supplier_data')
    data = cur.fetchall()
    headers = ['orderid', 'order_date', 'supplier_id', 'Mid', "Quantity", "Price", "Delievery_date", "Mname",
               "Saltname", "Brandname", "Location", "Exp_date", "GST", "discount", "status", "order_sp"]
    print(tabulate(data, headers, tablefmt="grid"))


# TODO fix the whole stock management module
def stock_manage_main():
    while True:
        print("\t\t\t1.Add Supply Order")
        print("\t\t\t2.List Products")
        print("\t\t\t3.Modify Product")
        print("\t\t\t4.Search Product")
        print("\t\t\t5.Delete Product ")
        print("\t\t\t6.Show Expired Products")
        print("\t\t\t7.Receive Supply Order")
        print("\t\t\t8.Show all supplier orders")
        print("\t\t\t9.Back(Main Menu)")
        ch1 = input("\t\tEnter your choice : ")
        if ch1 == "1":
            add_sup_order()
        elif ch1 == "2":
            list_product()
        elif ch1 == "3":
            edit_product()
        elif ch1 == "4":
            search_product()
        elif ch1 == "5":
            del_product()
        elif ch1 == "6":
            exp_product()
        elif ch1 == "8":
            disp_sup_order()
        # Doesn't exist anymore
        elif ch1 == "7":
            recieve_sup_order()
        elif ch1 == "9":
            break
        else:
            print("Please enter a valid input!")


def list_table():
    from tabulate import tabulate
    import mysql.connector as sql
    myql = sql.connect(host="localhost", user="Rakshith", password="Rakshith1@", database="medical_store")
    cur = myql.cursor()
    cur.execute("show tables")
    data = cur.fetchall()
    headers = ["Tables"]
    print(tabulate(data, headers, tablefmt="grid"))


def database_manage_main():
    while True:
        print("\t\t\t1.List Tables")
        print("\t\t\t2.Back(Main Menu)")
        cho = input("Enter your choice : ")
        if cho == "1":
            list_table()
        elif cho == "2":
            break
        else:
            print("Please enter a valid input!")


def user_manage_mini():
    while True:
        print("\t\t\t1.Search User")
        print("\t\t\t2.Back To Main Menu")
        cho_usr = input("Enter your choice :")
        if cho_usr == "1":
            srch_usr()
        elif cho_usr == "2":
            break
        else:
            print("Please enter a valid input")


def add_supplier():
    while True:
        print("Enter the following data!")
        f = open("Supplier.txt", "r+")
        data = int(f.read())
        f.close()
        sup_nme = input("Enter the supplier name : ")
        p_no = int(input("Enter the phone number : "))
        address = input("Enter the address : ")
        gst = input("Enter the Supplier GST number : ")
        import mysql.connector as sql
        myql = sql.connect(host="localhost", user="Rakshith", password="Rakshith1@", database="medical_store")
        cur = myql.cursor()
        cur.execute(
            "insert into supplier values({}, '{}', '{}', '{}', '{}')".format(data, sup_nme, p_no, address, gst))
        myql.commit()
        f = open("Supplier.txt", "w")
        data = data + 1
        f.write(str(data))
        f.close()
        ch = input("Do you want to continue(y/n)? : ")
        if ch == "y":
            pass
        elif ch == "n":
            break


def delete_supplier():
    print("1.Delete by supplier_id")
    print("2.Delete by supplier_name")
    ch = int(input("Enter your choice : "))
    if ch == 1:
        sid = int(input("Enter the supplier_id : "))
        import mysql.connector as sql
        myql = sql.connect(host="localhost", user="Rakshith", password="Rakshith1@", database="medical_store")
        cur = myql.cursor()
        cur.execute("delete from supplier where supplier_id = {}".format(sid))
        myql.commit()
        print(cur.rowcount, "supplier was deleted")
    if ch == 2:
        supname = input("Enter the supplier_name : ")
        import mysql.connector as sql
        myql = sql.connect(host="localhost", user="Rakshith", password="Rakshith1@", database="medical_store")
        cur = myql.cursor()
        cur.execute("delete from supplier where supplier_name ='{}'".format(supname))
        myql.commit()
        print(cur.rowcount, "supplier was deleted")


def list_supplier():
    from tabulate import tabulate
    headers = ["supplier_id", "supplier_name", "phone_number", "address", "supplier_gst"]
    import mysql.connector as sql
    myql = sql.connect(host='localhost', user="Rakshith", password="Rakshith1@", database="medical_store")
    cur = myql.cursor()
    cur.execute("Select * from supplier")
    data = cur.fetchall()
    if data is None or data == []:
        print("No record exists")
    else:
        print(tabulate(data, headers, tablefmt="grid"))


def search_supplier():
    from tabulate import tabulate
    while True:
        print("1.Search by supplier_id")
        print("2.Search by supplier_name")
        print("3.Back(Main Menu)")
        ch = input("Enter your choice : ")
        if ch == "1":
            import mysql.connector as sql
            myql = sql.connect(host="localhost", user="Rakshith", password="Rakshith1@", database="medical_store")
            cur = myql.cursor()
            sup_id = int(input("Enter the supplier_id : "))
            cur.execute("select * from supplier where supplier_id = {}".format(sup_id))
            data = cur.fetchall()
            if data is None or data == []:
                print("No such supplier exists")
            elif data is not None or data != []:
                print("The supplier exists!")
                headers = ['supplier_id', 'supplier_name', 'phone_number', 'address', 'supplier_gst']
                print(tabulate(data, headers, tablefmt='grid'))
        elif ch == "2":
            sup_name = input("Enter the supplier_name : ")
            import mysql.connector as sql
            myql = sql.connect(host="localhost", user="Rakshith", password="Rakshith1@", database="medical_store")
            cur = myql.cursor()
            cur.execute("select * from supplier where supplier_name = '{}'".format(sup_name))
            data = cur.fetchall()
            if data is None or data == []:
                print("No such supplier exists")
            elif data is not None or data != []:
                headers = ['supplier_id', 'supplier_name', 'phone_number', 'address', 'supplier_gst']
                print(tabulate(data, headers, tablefmt='grid'))
        elif ch == '3':
            break
        else:
            print("Please enter a valid input")


def edit_supplier():
    while True:
        print('supplier_id supplier_name phone_number address supplier_gst')
        field = input("Enter the field_name : ")
        supid = input("Enter the Supplier_id : ")
        if field in ['phone_number']:
            value = input("Enter the new value : ")
            import mysql.connector as sql
            myql = sql.connect(host="localhost", user="Rakshith", password="Rakshith1@", database="medical_store")
            cur = myql.cursor()
            cur.execute("update supplier set {} = {} where supplier_id = {}".format(field, value, supid))
            myql.commit()
            print(cur.rowcount, "supplier was modified")
        elif field in ['supplier_id']:
            print("You cannot change the supplier_id")
        elif field in ['supplier_name', 'address', 'supplier_gst']:
            value = input("Enter the new value : ")
            import mysql.connector as sql
            myql = sql.connect(host="localhost", user="Rakshith", password="Rakshith1@", database="medical_store")
            cur = myql.cursor()
            cur.execute("update supplier set {} = '{}' where supplier_id = {}".format(field, value, supid))
            myql.commit()
            print(cur.rowcount, "supplier was modified")
        ch = input("Do you want to continue(y/n)")
        if ch == 'y':
            pass
        elif ch == "n":
            break
        else:
            print("Please enter a valid input")


def supplier_management():
    while True:
        print("\t\t\t1.Search Supplier")
        print("\t\t\t2.Add Supplier")
        print("\t\t\t3.List all Supplier")
        print("\t\t\t4.Modify Supplier")
        print("\t\t\t5.Remove Supplier")
        print("\t\t\t6.Back(Main Menu)")
        cho_sup = input("Enter your choice: ")
        if cho_sup == "1":
            search_supplier()
        elif cho_sup == "2":
            add_supplier()
        elif cho_sup == "3":
            list_supplier()
        elif cho_sup == "4":
            edit_supplier()
        elif cho_sup == "5":
            delete_supplier()
        elif cho_sup == "6":
            break
        else:
            print("Please enter a valid input")


def stock_manage_mini():
    while True:
        print("Main Menu")
        print("\t\t\t1.Search Product")
        print("\t\t\t2.View all expired products")
        print("\t\t\t3.List all products")
        print("\t\t\t4.Back(Main Menu)")
        cho_stk = input("Enter your choice: ")
        if cho_stk == "1":
            search_product()
        elif cho_stk == "2":
            exp_product()
        elif cho_stk == "3":
            list_product()
        elif cho_stk == "4":
            break
        else:
            print("Please enter a valid input")


import tkinter

root = tkinter.Tk()
root.overrideredirect(True)
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.geometry('%dx%d+%d+%d' % (width * 0.8, height * 0.8, width * 0.1, height * 0.1))
image_file = "splash.png"
image = tkinter.PhotoImage(file=image_file)
canvas = tkinter.Canvas(root, height=height * 1, width=width * 1, bg="brown")
canvas.create_image(width * 1 / 2, height * 1 / 2, image=image)
canvas.pack()
root.after(5000, root.destroy)
root.mainloop()

user = int(input("Enter the Userid : "))
pass_chk = input("Enter the password : ")
admi, chk = authorisation(user, pass_chk)
if admi == 0 and chk == 1:
    while True:
        print("Main Menu")
        print("\t\t\t1.User Management")
        print("\t\t\t2.Bill Creation")
        print("\t\t\t3.Stock Management")
        print("\t\t\t4.Database Management")
        print("\t\t\t5.Supplier Management")
        print("\t\t\t6.Quit")
        cho_ini = input("Enter your choice : ")
        if cho_ini == '1':
            user_manage_main()
        elif cho_ini == '2':
            sales_manage_main()
        elif cho_ini == '3':
            stock_manage_main()
        elif cho_ini == "4":
            database_manage_main()
        elif cho_ini == "5":
            supplier_management()
        elif cho_ini == "6":
            print("Good Bye!")
            break

elif admi == 1 and chk == 1:
    while True:
        print("Main Menu")
        print("\t\t\t1.User Management")
        print("\t\t\t2.Stock Management")
        print("\t\t\t3.Quit")
        cho_ini = input("Enter your choice: ")
        if cho_ini == '1':
            user_manage_mini()
        elif cho_ini == '2':
            stock_manage_mini()
        elif cho_ini == "3":
            print("Bye")
            break
