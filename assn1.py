from flask import Flask
from flask import jsonify
from flask import request
from flask_restful import reqparse
app = Flask(__name__)
database = []
pay_database=[]
coffee_type ={"espresso": 8,
              "macchiato": 9,
              "latte":10,
              "flatwhite":11,
              "cappuccino":12,
              "mocha":13,
              "doppio":14,
              "longblack":15}
def get_creat_id(database):
    return len(database)+1
class Orders:
    def __init__(self,id,coffee,status,executing,addition):
        self.id = id
        self.coffee = coffee
        self.status = status
        self.addition =  addition
        self.executing = executing
class Payment:
    def __init__(self,id,type,amount,details):
        self.id = id
        self.type = type
        self.amount = amount
        self.details = details
#Create an order by Cashier
@app.route("/Cashier/orders", methods=['POST'])
def add_order():
    parser = reqparse.RequestParser()
    parser.add_argument('coffee', type=str)
    parser.add_argument('addition', type=str, action='append')
    args = parser.parse_args()
    check_len = len(request.args.to_dict())
    if check_len != 2:
        return jsonify("Parameter input is invalid (only coffee and addition is acceptable) "), 400
    else:
        status = False
        execution = False
        coffee = args.get("coffee")
        addition = args.get("addition")
        if 'coffee' not in request.args.to_dict():
            return ("Can not extract coffee plesse check the spell"),400
        elif 'addition' not in request.args.to_dict():
            return ("Can not extract addition please check the spell"),400
####### 条件判断 #### 只有list上的才可以下单。否则返回没有下单#######################
        if coffee in coffee_type:
            id = get_creat_id(database)
            database.append(Orders(id,coffee,status,execution,addition))
            return jsonify([st.__dict__ for st in database]),201
        else:
            return jsonify("Only the type in product list can be offered (eg.longblack) or see URL /Product to get the coffee type" ),400

#GET operation:
@app.route("/Cashier/orders", methods=['GET'])
def Cash_get_order():
    check_len = len(request.args.to_dict())
    if check_len != 0:
        return jsonify("Parameter input is invalid  "), 400
    else:
        response = jsonify([st.__dict__ for st in database])
        # response.headers._list.append(('Access-Control-Allow-Origin', '*'))
        return response
@app.route("/Cashier/orders/<id>", methods=['GET'])
def get_order_details(id):
    check_len = len(request.args.to_dict())
    if check_len != 0:
        return jsonify("Parameter input is invalid "), 400
    else:
        for st in database:
            if st.id == int(id):
                return jsonify(st.__dict__)
        return jsonify("can not find the true id"), 404
@app.route("/Products", methods=['GET'])
def get_coffee_type():
    check_len = len(request.args.to_dict())
    if check_len != 0:
        return jsonify("Parameter input is invalid "), 400
    else:
        response = jsonify([st for st in coffee_type])
     # response.headers._list.append(('Access-Control-Allow-Origin', '*'))
        return response

#amend the details
#cashier only can ammend the order
@app.route("/Cashier/amend/add/<id>", methods = ['PATCH'])
def add_the_addition(id):
    amend_praser =reqparse.RequestParser()
    amend_praser.add_argument("addition",type = str,action = 'apend')
    amend_args = amend_praser.parse_args()
    amend_addition = amend_args.get("addition")
    if 'addition' not in request.args.to_dict():
        return jsonify("invalid parameters. check the spell addition!"),400
    else:
        for st in database:
            if st.status == True or st.executing == True:
                return jsonify("the order has been paid or executed, can't amend"),401
            else:
                if st.id == int(id):
                    if amend_addition is not None:
                        for addi in amend_addition:
                            st.addition.append(addi)
                    return jsonify(ChangedAddition = st.addition ),200
        return jsonify("this id is not in the database. invalid id order"),404
@app.route("/Cashier/amend/delete/<id>",methods = ['PATCH'])
def delete_the_addition(id):
    amend_praser = reqparse.RequestParser()
    amend_praser.add_argument("addition", type=str, action = 'apend')
    amend_args = amend_praser.parse_args()
    amend_addition = amend_args.get("addition")
    check_num = 0
    if 'addition' not in request.args.to_dict():
        return jsonify("invalid parameters. check the spell addition!"),400
    else:
        for st in database:
            if st.status == True or st.executing == True:
                return jsonify("the order has been paid or executed, can't amend"),401
            else:
                if st.id == int(id):
                    if (len(request.args.to_dict()) == 1):
                        if amend_addition not in st.addition:
                            return jsonify("the argument are not in addition list "), 400
                        else:
                            st.addition.remove(amend_addition)
                            return jsonify(DeletedAddition=st.addition), 204
                    else:
                        for st1 in amend_addition:
                            if st1 not in st.addition:
                                check_num += 1
                        if check_num >=1:
                            check_num =0
                            return jsonify("the argument are not in addition list "), 404
                        else:
                            for st2 in amend_addition:
                                if st2 in st.addition:
                                    st.addition.remove(st2)
                            check_num=0
                            return jsonify(orderaddition=st.addition), 204
            return jsonify("error operation,the id is not valid"),400

@app.route("/Cashier/delete/<id>",methods = ['DELETE'])
def delete_the_order(id):
    check_flag = False
    if len(request.args.to_dict()) != 0:
        return jsonify("the arguments number is wrong !"), 400
    else:
        for st in database:
            if st.status == False and st.executing == False:
                if int(st.id) == int(id):
                    database.remove(st)
                    check_flag = True
            else:
                return jsonify("the order has been paid or executed, can't cancel"), 401
        if check_flag == False:
            return jsonify("No such id"), 404
        else:
            for st in database:
                if int(st.id) > int(id):
                    st.id -= 1
            for st1 in pay_database:
                if int(st1.id) > int(id):
                    st1.id -= 1
            return jsonify([st.__dict__ for st in database]), 204
#Cashier create the payment:
@app.route("/Cashier/payment/<id>",methods = ['POST'])
def create_payment(id):
    parser = reqparse.RequestParser()
    parser.add_argument('type', type=str)
    parser.add_argument('amount', type=int)
    parser.add_argument('details', type=str)
    args = parser.parse_args()
    check_len = len(request.args.to_dict())
    check_flag = False
    if check_len != 3:
        return jsonify("Parameter input is invalid (only coffee and addition is acceptable) "), 400
    else:
        for st1 in pay_database:
            if st1.id == int(id):
                return jsonify("Already Paid ,can not create the payment"), 400
        for st in database:
             if st.id == int(id):
                payment_type = args.get("type")
                payment_amount= args.get("amount")
                payment_details = args.get("details")
                pay_database.append(Payment(int(id), payment_type, payment_amount, payment_details))
                st.status = True
                check_flag = True
        if check_flag == True:
            return jsonify([st.__dict__ for st in pay_database]), 201
        else:
            return jsonify("There is not an order which id is 1 "), 404

#Barista get_the_open_orders:
@app.route("/Barista/orders", methods=['GET'])
def Bar_get_orders():
    check_len = len(request.args.to_dict())
    if check_len != 0:
        return jsonify("Parameter input is invalid "), 400
    else:
        response = jsonify([st.__dict__ for st in database])
    # response.headers._list.append(('Access-Control-Allow-Origin', '*'))
        return response
@app.route("/Barista/orders/<id>", methods=['GET'])
def Bar_order_details(id):
    check_len = len(request.args.to_dict())
    if check_len != 0:
        return jsonify("Parameter input is invalid "), 400
    else:
        for st in database:
            if st.id == int(id):
                return jsonify(st.__dict__)
        return jsonify("can not find the true id"), 404

#Barista_change_the_status
@app.route("/Barista/amend/<id>",methods = ['PATCH'])
def bar_amend_status(id):
    if len(request.args.to_dict()) != 0:
        return  jsonify("the arguments number is wrong !"),400
    else:
        check_flag = False
        for st in database:
            if st.id == int(id):
                st.executing = True
                check_flag = True
        if check_flag == True:
            return jsonify(AmendExecutingStatus=st.executing), 200
        else:
            return jsonify("There is no such id order"),404

#get payment id
@app.route("/Cashier/payment/<id>", methods=['GET'])
def Payment_details(id):
    check_len = len(request.args.to_dict())
    if check_len != 0:
        return jsonify("Parameter input is invalid "), 400
    else:
        for st in pay_database:
            if int(st.id) == int(id):
                return jsonify(st.__dict__)
        return jsonify("can not find the true id"), 404
@app.route("/payment", methods=['GET'])
def Payments():
    check_len = len(request.args.to_dict())
    if check_len != 0:
        return jsonify("Parameter input is invalid "), 400
    else:
        response = jsonify([st.__dict__ for st in pay_database])
    # response.headers._list.append(('Access-Control-Allow-Origin', '*'))
        return response
@app.route("/Barista/release/<id>", methods=['DELETE'])
def release_order(id):
    check_flag = False
    if len(request.args.to_dict()) != 0:
        return  jsonify("the arguments number is wrong !"),400
    else:
        for st in database:
            if st.status == True and st.executing == True:
                if int(st.id) == int(id):
                    database.remove(st)
                    check_flag = True
            else:
                return jsonify("the order has been paid or executed, can't release"), 401
        if check_flag == False:
            return jsonify("No such id"), 404
        else:
            for st in database:
                if int(st.id) > int(id):
                    st.id -=1
            for st1 in pay_database:
                if  int(st1.id) == int(st.id):
                    pay_database.remove(st1)
            for st1 in pay_database:
                if int(st1.id) > int(id):
                    st1.id  -=1
            return jsonify([st.__dict__ for st in database]), 204

@app.route("/Barista/check/<id>", methods=['GET'])
def check_status(id):
    check_len = len(request.args.to_dict())
    if check_len != 0:
        return jsonify("Parameter input is invalid "), 400
    else:
        for st in database:
            if int(st.id) == int(id):
                return jsonify(st.status),200
        return jsonify("can not find the true id"), 404
if __name__ == "__main__":
    app.run()

