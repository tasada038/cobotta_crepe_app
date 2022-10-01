from flask import render_template,  request, url_for, session , redirect, make_response
from werkzeug.exceptions import HTTPException

from web_app.robot.multi_cobotta import MultiMotion
from web_app.robot.bake_motion import BakeMotion
from web_app.robot.topping_motion import ToppingMotion

from web_app.robot.bake_clear_error import BakeClearError
from web_app.robot.topping_clear_error import ToppingClearError
from web_app.robot.bake_auto_calset import BakeAutoCalset
from web_app.robot.topping_auto_calset import ToppingAutoCalset

from web_app.robot.bake_each_process import *
from web_app.robot.topping_each_process import *

from web_app import app
from web_app import db
from web_app.models.customer import Customer

import paypayopa
import random
import time
import datetime

API_KEY = "xxxxxxxxxx" #"YOUR_API_KEY"
API_SECRET = "xxxxxxxxxx" #"YOUR_API_SECRET"
MERCHANT_ID = "xxxxxxxxxx" #"YOUR_SHOP_ID"

# Create Client
client = paypayopa.Client(auth=(API_KEY, API_SECRET), production_mode=False)
client.set_assume_merchant(MERCHANT_ID)

# global variable
order_all_cnt = 0
whip_strawberry_choco_cnt = 0
whip_caramel_flake_cnt = 0
whip_choco_almond_cnt = 0
order_menu_cnt = 0
cost_rate = 0
food_cost = 0
gross_profit = 0
amount_of_sales = 0

dough_cnt = 0
flake_cnt, chocotip_cnt, biscuit_cnt, almond_cnt, banana_cnt, fruit_cnt = 0, 0, 0, 0, 0, 0
choco_source_cnt, caramel_source_cnt, straw_source_cnt, blue_source_cnt = 0, 0, 0, 0
whip_cnt, custard_cnt = 0, 0
chocospray_cnt = 0

tonnbo_z, tonnbo_rx, tonnbo_ry, hera_y = 0, 0, 0, 0
straw_j6, caramel_j6, blue_j6 = 0, 0, 0

gender_list = ["男", "女"]
menu_list = [
    "チョコストロベリーホイップ", \
    "キャラメルフレークホイップ", \
    "アーモンドチョコホイップ", \
    "オーダーメニュー"
]


def create_qr_code(url :str):
    import uuid
    request = {
        "merchantPaymentId": uuid.uuid4().hex,
        "codeType": "ORDER_QR",
        "redirectUrl": "http://localhost:5073/" + url,
        "redirectType":"WEB_LINK",
        "orderDescription":"COBOTTA Crepe Cooking",
        "orderItems": [{
            "name": "Crepe",
            "category": "pasteries",
            "quantity": 1,
            "productId": "67678",
            "unitPrice": {
                "amount": 1,
                "currency": "JPY"
            }
        }],
        "amount": {
            "amount": 520,
            "currency": "JPY"
        },
    }

    response = client.Code.create_qr_code(request)
    qr_url = response['data']['url']

    print("ステータス→"+response['resultInfo']['code'])
    print("決済するURL→ "+ qr_url)
    
    return qr_url

# login page access
@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html', \
        title='Login', \
        err=False, \
        message='IDとパスワードを入力:', \
        id='' )

# login form sended.
@app.route('/login', methods=['POST'])
def login_post():    # Login and ID
    initial_id = ""
    initial_pswd = ""

    # get sended id and pswd value 
    id = request.form.get('id')
    pswd = request.form.get('pass')

    if id == initial_id:
        if pswd == initial_pswd:  
            session['login'] = True  
        else:   
            session['login'] = False   
    else:   
        return render_template('login.html', \
            title = 'Login', \
            err = True, \
            message='IDが違います', \
            id = id)

    session['id'] = id

    if session['login']:    # True Then, move to "home" page
        return redirect('/')
    else:    # False Then, Change Message Value
        return render_template('login.html', \
            title = 'Login', \
            err = True, \
            message='パスワードが違います', \
            id = id)

@app.route('/', methods = ['GET'])
def home():    # GET Access
    if 'login' in session and session['login']:

        try:
            online_status = "オンライン"
            choco_strawberry_url = create_qr_code("whip_strawberry_choco")
            charamel_flake_url = create_qr_code("whip_caramel_flake")
            almond_choco_url = create_qr_code("whip_choco_almond")
            order_url = create_qr_code("multicontrol")
        except:
            online_status = "オフライン"
            choco_strawberry_url = "http://localhost:5073/whip_strawberry_choco"
            charamel_flake_url = "http://localhost:5073/whip_caramel_flake"
            almond_choco_url = "http://localhost:5073/whip_choco_almond"
            order_url = "http://localhost:5073/multicontrol"

        return render_template('home.html', \
        title = "COBOTTA Crepe Cooking", \
        message = "COBOTTA Crepe Cooking",\
        choco_strawberry_url = choco_strawberry_url,\
        charamel_flake_url = charamel_flake_url,\
        almond_choco_url = almond_choco_url,\
        order_url = order_url,\
        online_status = online_status)
    else:
        return redirect('/login')

@app.route('/', methods = ['POST'])
def home_main():    # GET Access

    try:
        online_status = "オンライン"
        choco_strawberry_url = create_qr_code("whip_strawberry_choco")
        charamel_flake_url = create_qr_code("whip_caramel_flake")
        almond_choco_url = create_qr_code("whip_choco_almond")
        order_url = create_qr_code("multicontrol")
    except:
        online_status = "オフライン"
        choco_strawberry_url = "http://localhost:5073/whip_strawberry_choco"
        charamel_flake_url = "http://localhost:5073/whip_caramel_flake"
        almond_choco_url = "http://localhost:5073/whip_choco_almond"
        order_url = "http://localhost:5073/multicontrol"


    return render_template('home.html', \
        title = "COBOTTA Crepe Cooking", \
        message = "COBOTTA Crepe Cooking",\
        choco_strawberry_url = choco_strawberry_url,\
        charamel_flake_url = charamel_flake_url,\
        almond_choco_url = almond_choco_url,\
        order_url = order_url,\
        online_status = online_status)


@app.route('/bake_cobotta') # DropDown Bake Cobotta
def bake_cobotta():
    bake = BakeEachProcess()
    global tonnbo_z, tonnbo_rx, tonnbo_ry, hera_y
    """
    tonnbo_z = bake.read_d_param(0)
    tonnbo_rx = bake.read_d_param(1)
    tonnbo_ry = bake.read_d_param(2)
    hera_y = bake.read_d_param(3)
    """
    return render_template('bake.html', \
        title='Baking COBOTTA', \
        message='vertion 2.7.1 : you use ver 2.8.x and above, edit auto_calset.py',\
        message2='初期ポジション @P[2056]',\
        message3='起動権 : TP/Ethernet',\
        message4='IPアドレス : 192.168.0.1',\
        tonnbo_z_data=round(tonnbo_z,3), \
        tonnbo_rx_data = round(tonnbo_rx,3),\
        tonnbo_ry_data = round(tonnbo_ry,3),\
        hera_y_data = round(hera_y,3))

@app.route('/topping_cobotta') # DropDown Topping COBOTTA
def topping_cobotta():
    topping = ToppingEachProcess()
    global straw_j6, caramel_j6, blue_j6
    """
    straw_j6 = topping.read_i_param(1)
    caramel_j6 = topping.read_i_param(2)
    blue_j6 = topping.read_i_param(3)
    """
    return render_template('topping.html', \
        title='Topping COBOTTA', \
        message='vertion 2.7.2 : you use ver 2.8.x and above, edit auto_calset.py',\
        message2='初期ポジション @P[450]',\
        message3='起動権 : TP/Ethernet',\
        message4='IPアドレス : 192.168.0.2', \
        straw_j6_data = straw_j6,\
        caramel_j6_data = caramel_j6,\
        blue_j6_data = blue_j6)

@app.route('/sales') # DropDown Sales
def sales_crepe():

    return render_template('sales.html', \
        title='Sales', \
        message="現在の注文総数：" + str(order_all_cnt), \
        menu_01 ='チョコ ストロベリー ホイップ：'+str(whip_strawberry_choco_cnt), \
        menu_02 ='キャラメル フレーク ホイップ：'+str(whip_caramel_flake_cnt), \
        menu_03 ='アーモンド チョコ ホイップ：'+str(whip_choco_almond_cnt), \
        original_menu = 'オーダーメニュー：'+str(order_menu_cnt), \
        cost_rate_view = float(cost_rate), \
        total_food_cost = float(food_cost), \
        gross_profit_view = float(gross_profit), \
        sales = float(amount_of_sales),\
        whip_cnt = whip_cnt,\
        custard_cnt = custard_cnt,\
        choco_source_cnt = choco_source_cnt,\
        caramel_source_cnt = caramel_source_cnt,\
        straw_source_cnt = straw_source_cnt,\
        blue_source_cnt = blue_source_cnt,\
        flake_cnt = flake_cnt,\
        almond_cnt = almond_cnt,\
        chocotip_cnt = chocotip_cnt,\
        biscuit_cnt = biscuit_cnt)

def read_sales_value():
    topping = ToppingEachProcess()
    global cost_rate, order_all_cnt, \
           whip_strawberry_choco_cnt, whip_caramel_flake_cnt, whip_choco_almond_cnt, \
           order_menu_cnt, food_cost, gross_profit, amount_of_sales, \
           dough_cnt, flake_cnt, chocotip_cnt, biscuit_cnt, almond_cnt, banana_cnt, fruit_cnt, \
           choco_source_cnt, caramel_source_cnt, straw_source_cnt, blue_source_cnt, \
           whip_cnt, custard_cnt, chocospray_cnt

    f_data = topping.get_f_data()
    i_data = topping.get_i_data()

    cost_rate = round(f_data[0],2)
    order_all_cnt = round(i_data[2],2)
    whip_strawberry_choco_cnt = round(i_data[4],2)
    whip_caramel_flake_cnt = round(i_data[5],2)
    whip_choco_almond_cnt = round(i_data[6],2)
    order_menu_cnt = round(i_data[7],2)
    food_cost = round(i_data[8],2)
    gross_profit = round(i_data[9],2)
    amount_of_sales = round(i_data[3],2)

    dough_cnt = round(f_data[26],2)
    flake_cnt = round(f_data[27],2)
    chocotip_cnt = round(f_data[28],2)
    biscuit_cnt = round(f_data[29],2)
    almond_cnt = round(f_data[30],2)
    banana_cnt = round(f_data[31],2)
    fruit_cnt = round(f_data[32],2)
    choco_source_cnt = round(f_data[33],2)
    caramel_source_cnt = round(f_data[34],2)
    straw_source_cnt = round(f_data[35],2)
    blue_source_cnt = round(f_data[36],2)
    whip_cnt = round(f_data[37],2)
    custard_cnt = round(f_data[38],2)
    chocospray_cnt = round(f_data[39],2)

@app.route('/topping_sales_update')
def topping_sales_update():
    read_sales_value()

    return redirect('/sales')


@app.route('/privacy_policy') # DropDown Topping COBOTTA
def privacy_policy_app():
    return render_template('privacy_policy.html', \
        title='Application Privacy Policy', \
        message = 'Application Privacy Policy')

@app.before_first_request
def init():
    db.create_all()

@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':

        form_gender = request.form.get('gender')
        form_year = request.form.get('year', default=20, type=int)
        form_menu = request.form.get('menu')
        form_count = request.form.get('count')
        form_order_time = request.form.get('order_time')

        # debag
        #print("顧客名:{}".format(form_name))

        customer = Customer(
            gender=form_gender,
            year=form_year,
            menu=form_menu,
            count = form_count,
            order_time = form_order_time
        )
        db.session.add(customer)
        db.session.commit()

    customers = Customer.query.all()
    return render_template('add_customer.html', \
        title = "Customer Information", \
        message = "Customer Information", \
        customers=customers)



@app.route('/<int:id>', methods=['POST'])
def customer_detail(id):
    customer = Customer.query.get(id)
    # customer = Customer.query.get_or_404(id)
    # customer = Customer.query.filter(Customer.id == id).one()
    return render_template('customer_detail.html', \
        title = "Customer Information", \
        message = "Customer Information", \
        customer=customer)


@app.route('/<int:id>', methods=['GET'])
def customer_edit(id):
    # 編集ページ表示用
    customer = Customer.query.get(id)
    return render_template('customer_edit.html', \
        title = "Customer Information", \
        message = "Customer Information", \
        customer=customer)


@app.route('/<int:id>/update', methods=['POST'])
def customer_update(id):
    customer = Customer.query.get(id)
    customer.gender = request.form.get('gender')
    customer.year = request.form.get('year', default=20, type=int)
    customer.menu = request.form.get('menu')
    customer.count = request.form.get('count')
    customer.order_time = request.form.get('order_time')

    db.session.merge(customer)
    db.session.commit()
    return redirect('/add_customer')


@app.route('/<int:id>/delete', methods=['POST']) 
def customer_delete(id):  
    customer = Customer.query.get(id)   
    db.session.delete(customer)  
    db.session.commit()
    return redirect('/add_customer')

@app.route('/db_all_delete')
def customer_all_delete():
    Customer.query.delete()
    db.session.commit()
    return redirect('/add_customer')

def create_random_db(menu, cnt):
    dt =  datetime.datetime.today()

    form_gender = random.choice(gender_list)
    form_year = random.randrange(20,70,10)
    form_menu = menu
    form_count = cnt
    form_order_time = "{}:{}:{}".format(dt.hour, dt.minute, dt.second)

    customer = Customer(
        gender=form_gender,
        year=form_year,
        menu = form_menu,
        count = form_count,
        order_time = form_order_time
    )
    db.session.add(customer)
    db.session.commit()

    return customer

def gender_convert(db_gender):
    cobotta_global = ""
    if str(db_gender) == '男':
        cobotta_global = "man"
    else:
        cobotta_global = "woman"
    
    return cobotta_global

# Multi COBOTTA Control
@app.route('/multicontrol', methods=['GET', 'POST'])
def multi_control_form():
    multi = MultiMotion()
    topping = ToppingEachProcess()

    read_sales_value()
    order_all_cnt = topping.write_i_param(10,1)
    order_menu_cnt = topping.write_i_param(15,1)

    menu_data = []
    menu_data = request.form.getlist('menu')
    print("MENU DATA:{}".format(menu_data))

    db_data = create_random_db(menu_list[3], 1)
    gender = gender_convert(db_data.gender)
    menu = str(menu_data)

    return redirect('/'), multi.multi_process(menu_data, order_all_cnt, gender, db_data.year, menu, db_data.count, db_data.order_time)

# Select menu
@app.route('/whip_strawberry_choco')
def topping_whip_strawberry_choco():
    multi = MultiMotion()
    topping = ToppingEachProcess()

    read_sales_value()
    order_all_cnt = topping.write_i_param(10,1)
    whip_strawberry_choco_cnt = topping.write_i_param(12,1)

    db_data = create_random_db(menu_list[0], 1)
    gender = gender_convert(db_data.gender)
    menu = "whip_strawberry_choco"

    return redirect('/'), multi.multi_whip_strawberry_choco(order_all_cnt, gender, db_data.year, menu, db_data.count, db_data.order_time)

@app.route('/whip_caramel_flake')
def topping_whip_caramel_flake():
    multi = MultiMotion()
    topping = ToppingEachProcess()

    read_sales_value()
    order_all_cnt = topping.write_i_param(10,1)
    whip_caramel_flake_cnt = topping.write_i_param(13,1)

    db_data = create_random_db(menu_list[1], 1)
    gender = gender_convert(db_data.gender)
    menu = "whip_caramel_flake"

    return redirect('/'), multi.multi_whip_caramel_flake(order_all_cnt, gender, db_data.year, menu, db_data.count, db_data.order_time)
 
@app.route('/whip_choco_almond')
def topping_whip_choco_almond():
    multi = MultiMotion()
    topping = ToppingEachProcess()

    read_sales_value()
    order_all_cnt = topping.write_i_param(10,1)
    whip_choco_almond_cnt = topping.write_i_param(14,1)

    db_data = create_random_db(menu_list[2], 1)
    gender = gender_convert(db_data.gender)
    menu = "whip_choco_almond"

    return redirect('/'), multi.multi_whip_choco_almond(order_all_cnt, gender, db_data.year, menu, db_data.count, db_data.order_time)

@app.route('/whip_choco_banana')
def topping_whip_choco_banana():
    multi = MultiMotion()
    topping = ToppingEachProcess()

    read_sales_value()
    order_all_cnt = topping.write_i_param(10,1)
    
    return redirect('/'), multi.multi_whip_choco_banana()

@app.route('/custard_strawberry_biscuits')
def topping_custard_strawberry_biscuits():
    multi = MultiMotion()
    topping = ToppingEachProcess()

    read_sales_value()
    order_all_cnt = topping.write_i_param(10,1)

    return redirect('/'), multi.multi_custard_strawberry_biscuits()

# Baking COBOTTA
@app.route('/bakeinitial')
def bake_control():
    bake = BakeEachProcess()
    return redirect('/bake_cobotta'), bake.bake_initial()

@app.route('/bakemotion')
def bake_motion_only():
    bake = BakeMotion()
    return redirect('/bake_cobotta'), bake.bake_crepe()

@app.route('/bake_handopen')
def bake_hand_open():
    bake = BakeEachProcess()
    return redirect('/bake_cobotta'), bake.bake_hand_open()

@app.route('/bake_clear_error')
def bake_clear_error():
    bake = BakeClearError()
    return redirect('/bake_cobotta'), bake.bake_clear_error()

@app.route('/bake_autocal')
def bake_autocal():
    bake = BakeAutoCalset()
    return redirect('/bake_cobotta'), bake.bake_calset()

@app.route('/bake_packing')
def bake_packing():
    bake = BakeEachProcess()
    return redirect('/bake_cobotta'), bake.bake_packing()

# Bake Each Process
@app.route('/bake_oiling')
def bake_oiling():
    bake = BakeEachProcess()
    return redirect('/bake_cobotta'), bake.bake_oiling()

@app.route('/bake_redol')
def bake_redol():
    bake = BakeEachProcess()
    return redirect('/bake_cobotta'), bake.bake_redol()

@app.route('/bake_tonnbo')
def bake_tonnbo():
    bake = BakeEachProcess()
    return redirect('/bake_cobotta'), bake.bake_tonnbo()

@app.route('/bake_hera')
def bake_hera():
    bake = BakeEachProcess()
    return redirect('/bake_cobotta'), bake.bake_hera()

@app.route('/tonnbo_z_update', methods=['POST'])
def bake_tonnbo_z_update():
    bake = BakeEachProcess()
    global tonnbo_z, tonnbo_rx, tonnbo_ry, hera_y

    ajust_data = request.form.get('tonnbo_z')

    tonnbo_z = bake.write_d_param(0, ajust_data)
    print("new tonnbo z:{}".format(tonnbo_z))

    return render_template('bake.html', \
        title='Baking COBOTTA', \
        message='vertion 2.7.1 : you use ver 2.8.x and above, edit auto_calset.py',\
        message2='初期ポジション @P[2056]',\
        message3='起動権 : TP/Ethernet',\
        message4='IPアドレス : 192.168.0.1',\
        tonnbo_z_data=tonnbo_z, \
        tonnbo_rx_data = tonnbo_rx,\
        tonnbo_ry_data = tonnbo_ry,\
        hera_y_data = hera_y)

@app.route('/tonnbo_rx_update', methods=['POST'])
def bake_tonnbo_rx_update():
    bake = BakeEachProcess()
    global tonnbo_z, tonnbo_rx, tonnbo_ry, hera_y

    ajust_data = request.form.get('tonnbo_rx')

    tonnbo_rx = bake.write_d_param(1, ajust_data)
    print("new tonnbo rx:{}".format(tonnbo_rx))

    return render_template('bake.html', \
        title='Baking COBOTTA', \
        message='vertion 2.7.1 : you use ver 2.8.x and above, edit auto_calset.py',\
        message2='初期ポジション @P[2056]',\
        message3='起動権 : TP/Ethernet',\
        message4='IPアドレス : 192.168.0.1',\
        tonnbo_z_data=tonnbo_z, \
        tonnbo_rx_data = tonnbo_rx,\
        tonnbo_ry_data = tonnbo_ry,\
        hera_y_data = hera_y)

@app.route('/tonnbo_ry_update', methods=['POST'])
def bake_tonnbo_ry_update():
    bake = BakeEachProcess()
    global tonnbo_z, tonnbo_rx, tonnbo_ry, hera_y

    ajust_data = request.form.get('tonnbo_ry')

    tonnbo_ry = bake.write_d_param(2, ajust_data)
    print("new tonnbo ry:{}".format(tonnbo_ry))

    return render_template('bake.html', \
        title='Baking COBOTTA', \
        message='vertion 2.7.1 : you use ver 2.8.x and above, edit auto_calset.py',\
        message2='初期ポジション @P[2056]',\
        message3='起動権 : TP/Ethernet',\
        message4='IPアドレス : 192.168.0.1',\
        tonnbo_z_data=tonnbo_z, \
        tonnbo_rx_data = tonnbo_rx,\
        tonnbo_ry_data = tonnbo_ry,\
        hera_y_data = hera_y)

@app.route('/hera_y_update', methods=['POST'])
def bake_hera_y_update():
    bake = BakeEachProcess()
    global tonnbo_z, tonnbo_rx, tonnbo_ry, hera_y

    ajust_data = request.form.get('hera_y')

    hera_y = bake.write_d_param(3, ajust_data)
    print("new hera y:{}".format(hera_y))

    return render_template('bake.html', \
        title='Baking COBOTTA', \
        message='vertion 2.7.1 : you use ver 2.8.x and above, edit auto_calset.py',\
        message2='初期ポジション @P[2056]',\
        message3='起動権 : TP/Ethernet',\
        message4='IPアドレス : 192.168.0.1',\
        tonnbo_z_data=tonnbo_z, \
        tonnbo_rx_data = tonnbo_rx,\
        tonnbo_ry_data = tonnbo_ry,\
        hera_y_data = hera_y)

# Bake Rec XYZ Jnt
@app.route('/bake_rec_subx')
def bake_subx():
    bake = BakeEachProcess()
    return redirect('/bake_cobotta'), bake.bake_recovery_subx()

@app.route('/bake_rec_suby')
def bake_suby():
    bake = BakeEachProcess()
    return redirect('/bake_cobotta'), bake.bake_recovery_suby()

@app.route('/bake_rec_subz')
def bake_subz():
    bake = BakeEachProcess()
    return redirect('/bake_cobotta'), bake.bake_recovery_subz()

@app.route('/bake_rec_addx')
def bake_addx():
    bake = BakeEachProcess()
    return redirect('/bake_cobotta'), bake.bake_recovery_addx()

@app.route('/bake_rec_addy')
def bake_addy():
    bake = BakeEachProcess()
    return redirect('/bake_cobotta'), bake.bake_recovery_addy()

@app.route('/bake_rec_addz')
def bake_addz():
    bake = BakeEachProcess()
    return redirect('/bake_cobotta'), bake.bake_recovery_addz()

@app.route('/bake_rec_subj1')
def bake_subj1():
    bake = BakeEachProcess()
    return redirect('/bake_cobotta'), bake.bake_recovery_subj1()

@app.route('/bake_rec_subj2')
def bake_subj2():
    bake = BakeEachProcess()
    return redirect('/bake_cobotta'), bake.bake_recovery_subj2()

@app.route('/bake_rec_addj1')
def bake_addj1():
    bake = BakeEachProcess()
    return redirect('/bake_cobotta'), bake.bake_recovery_addj1()

@app.route('/bake_rec_addj2')
def bake_addj2():
    bake = BakeEachProcess()
    return redirect('/bake_cobotta'), bake.bake_recovery_addj2()

# Topping COBOTTA
@app.route('/toppinginitial')
def topping_control():
    topping = ToppingEachProcess()
    return redirect('/topping_cobotta'), topping.topping_initial()

@app.route('/toppingmotion')
def topping_motion_only():
    topping = ToppingMotion()
    return redirect('/topping_cobotta'), topping.topping_crepe()

@app.route('/topping_handopen')
def topping_hand_open():
    topping = ToppingEachProcess()
    return redirect('/topping_cobotta'), topping.topping_hand_open()

@app.route('/topping_clear_error')
def topping_clear_error():
    topping = ToppingClearError()
    return redirect('/topping_cobotta'), topping.topping_clear_error()

@app.route('/topping_autocal')
def topping_autocal():
    topping = ToppingAutoCalset()
    return redirect('/topping_cobotta'), topping.topping_calset()

@app.route('/topping_packing')
def topping_packing():
    topping = ToppingEachProcess()
    return redirect('/topping_cobotta'), topping.topping_packing()

# Topping Each Process
@app.route('/topping_whip')
def topping_whip_cream():
    topping = ToppingEachProcess()
    return redirect('/topping_cobotta'), topping.topping_whip()

@app.route('/topping_custard')
def topping_custard_cream():
    topping = ToppingEachProcess()
    return redirect('/topping_cobotta'), topping.topping_custard()

@app.route('/topping_flake')
def topping_flake_serve():
    topping = ToppingEachProcess()
    return redirect('/topping_cobotta'), topping.topping_flake()

@app.route('/topping_almond')
def topping_almond_serve():
    topping = ToppingEachProcess()
    return redirect('/topping_cobotta'), topping.topping_almond()

@app.route('/topping_choco')
def topping_choco_serve():
    topping = ToppingEachProcess()
    return redirect('/topping_cobotta'), topping.topping_choco()

@app.route('/topping_biscuits')
def topping_biscuits_serve():
    topping = ToppingEachProcess()
    return redirect('/topping_cobotta'), topping.topping_biscuits()

# Sources
@app.route('/topping_blueberry_jam')
def topping_blueberry_jam():
    topping = ToppingEachProcess()
    return redirect('/topping_cobotta'), topping.topping_blueberry_jam()

@app.route('/topping_strawberry_jam')
def topping_strawberry_jam():
    topping = ToppingEachProcess()
    return redirect('/topping_cobotta'), topping.topping_strawberry_jam()

@app.route('/topping_caramel_source')
def topping_caramel_source():
    topping = ToppingEachProcess()
    return redirect('/topping_cobotta'), topping.topping_caramel_source()

@app.route('/topping_chocolate_source')
def topping_chocolate_source():
    topping = ToppingEachProcess()
    return redirect('/topping_cobotta'), topping.topping_chocolate_source()

@app.route('/topping_honey')
def topping_honey():
    topping = ToppingEachProcess()
    return redirect('/topping_cobotta'), topping.topping_honey()

@app.route('/topping_matcha_source')
def topping_matcha_source():
    topping = ToppingEachProcess()
    return redirect('/topping_cobotta'), topping.topping_matcha_source()

@app.route('/straw_j6_update', methods=['POST'])
def strawberry_jam_update():
    topping = ToppingEachProcess()
    global straw_j6, caramel_j6, blue_j6

    ajust_data = request.form.get('straw_j6')

    straw_j6 = topping.write_i_param(1, ajust_data)
    print("new straw j6:{}".format(straw_j6))

    return render_template('topping.html', \
        title='Topping COBOTTA', \
        message='vertion 2.7.2 : you use ver 2.8.x and above, edit auto_calset.py',\
        message2='初期ポジション @P[450]',\
        message3='起動権 : TP/Ethernet',\
        message4='IPアドレス : 192.168.0.2', \
        straw_j6_data = straw_j6,\
        caramel_j6_data = caramel_j6,\
        blue_j6_data = blue_j6)

@app.route('/caramel_j6_update', methods=['POST'])
def caramel_source_update():
    topping = ToppingEachProcess()
    global straw_j6, caramel_j6, blue_j6

    ajust_data = request.form.get('caramel_j6')

    caramel_j6 = topping.write_i_param(2, ajust_data)
    print("new caramel j6:{}".format(caramel_j6))

    return render_template('topping.html', \
        title='Topping COBOTTA', \
        message='vertion 2.7.2 : you use ver 2.8.x and above, edit auto_calset.py',\
        message2='初期ポジション @P[450]',\
        message3='起動権 : TP/Ethernet',\
        message4='IPアドレス : 192.168.0.2', \
        straw_j6_data = straw_j6,\
        caramel_j6_data = caramel_j6,\
        blue_j6_data = blue_j6)

@app.route('/blue_j6_update', methods=['POST'])
def blueberry_jam_update():
    topping = ToppingEachProcess()
    global straw_j6, caramel_j6, blue_j6

    ajust_data = request.form.get('blue_j6')

    blue_j6 = topping.write_i_param(3, ajust_data)
    print("new blue j6:{}".format(blue_j6))

    return render_template('topping.html', \
        title='Topping COBOTTA', \
        message='vertion 2.7.2 : you use ver 2.8.x and above, edit auto_calset.py',\
        message2='初期ポジション @P[450]',\
        message3='起動権 : TP/Ethernet',\
        message4='IPアドレス : 192.168.0.2', \
        straw_j6_data = straw_j6,\
        caramel_j6_data = caramel_j6,\
        blue_j6_data = blue_j6)

# Fold Crepe
@app.route('/topping_fold')
def topping_fold_crepe():
    topping = ToppingEachProcess()
    return redirect('/topping_cobotta'), topping.topping_fold()

# Serve Each Task
@app.route('/topping_serve_right')
def topping_serve_right():
    topping = ToppingEachProcess()
    return redirect('/topping_cobotta'), topping.topping_serve_right()

@app.route('/topping_serve_left')
def topping_seve_left():
    topping = ToppingEachProcess()
    return redirect('/topping_cobotta'), topping.topping_serve_left()

@app.route('/topping_serve_cream')
def topping_seve_cream():
    topping = ToppingEachProcess()
    return redirect('/topping_cobotta'), topping.topping_serve_cream()

@app.route('/topping_serve_spray')
def topping_seve_spray():
    topping = ToppingEachProcess()
    return redirect('/topping_cobotta'), topping.topping_serve_spray()


# Topping Rec XYZ Jnt
@app.route('/topping_rec_subx')
def topping_subx():
    topping = ToppingEachProcess()
    return redirect('/topping_cobotta'), topping.topping_recovery_subx()

@app.route('/topping_rec_suby')
def topping_suby():
    topping = ToppingEachProcess()
    return redirect('/topping_cobotta'), topping.topping_recovery_suby()

@app.route('/topping_rec_subz')
def topping_subz():
    topping = ToppingEachProcess()
    return redirect('/topping_cobotta'), topping.topping_recovery_subz()

@app.route('/topping_rec_addx')
def topping_addx():
    topping = ToppingEachProcess()
    return redirect('/topping_cobotta'), topping.topping_recovery_addx()

@app.route('/topping_rec_addy')
def topping_addy():
    topping = ToppingEachProcess()
    return redirect('/topping_cobotta'), topping.topping_recovery_addy()

@app.route('/topping_rec_addz')
def topping_addz():
    topping = ToppingEachProcess()
    return redirect('/topping_cobotta'), topping.topping_recovery_addz()

@app.route('/topping_rec_subj1')
def topping_subj1():
    topping = ToppingEachProcess()
    return redirect('/topping_cobotta'), topping.topping_recovery_subj1()

@app.route('/topping_rec_subj2')
def topping_subj2():
    topping = ToppingEachProcess()
    return redirect('/topping_cobotta'), topping.topping_recovery_subj2()

@app.route('/topping_rec_addj1')
def topping_addj1():
    topping = ToppingEachProcess()
    return redirect('/topping_cobotta'), topping.topping_recovery_addj1()

@app.route('/topping_rec_addj2')
def topping_addj2():
    topping = ToppingEachProcess()
    return redirect('/topping_cobotta'), topping.topping_recovery_addj2()

# LogOut
@app.route('/logout', methods=['GET'])
def logout():
    session.pop('id', None)
    session.pop('login')
    return redirect('/login')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('not_found.html', \
        title='The requested URL was Not found', \
        message='アクセスしていただいたURLが見つかりません。'),404

@app.errorhandler(Exception)
def handle_exception(e):
    # pass through HTTP errors
    if isinstance(e, HTTPException):
        return e

    # now you're handling non-HTTP exceptions only
    return render_template('exception.html', \
        title='Exception Error has occurred', \
        message1='プログラムの実行中に割込み処理が発生しました',\
        message2='"Clear Error"よりエラー解除を行ってください'),500