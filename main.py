from flask import Flask, request, jsonify
from flask_cors import CORS
from search import Search
import html
import rich
import db
import general
import waitlist


def info(msg):
    rich.print("[bold][green]INFO[/bold]: " + msg + "[/green]")

info("Initiating..")

mod = True
info("MOD - TRUE")
shutdown = False
adwin = [{"ad":"min"}]
ads = db.AdDatabase()
waitlist = waitlist.Waitlist()
general = general.Banned()


Reports = {}


app = Flask(__name__)
info("Started!")
CORS(app)

def ban_ip(id,a):
    ip = waitlist.get_ad(id)["ip"]
    info(f"Banning IP - {ip} - ADMIN - {a}")
    general.add_banned_ip(ip)

def moderate(a):
    global mod
    info(f"Setting MOD On - ADMIN - {a}")
    mod = True
def moderate_of(a):
    global mod
    info(f"Setting MOD Off - ADMIN - {a}")
    mod =  False
def shutdown_(a):
    global shutdown
    info(f"Setting Shutdown On - ADMIN - {a}")
    shutdown = True
def shutdown_off(a):
    global shutdown
    info(f"Setting Shutdown Off - ADMIN - {a}")
    shutdown =  False
def approve_(id):
    inf = waitlist.get_ad(id)
    inf.pop('ip')
    ads.add_ad(inf)
    waitlist.remove_ad(id)
def ignore_fun(id):
    waitlist.remove_ad(id)



@app.route('/', methods=['GET','POST'])
def index():
    return "Welcome to the BACKEND API"

@app.route('/search', methods=['GET'])
def search():
    if shutdown:
        return "", 404


    query =  html.escape(request.headers.get('query'))
    page = int(request.headers.get('page', 1))

    if query.replace(" ","") == "":
        return {}

    if not query:
        return jsonify({"error": "query header is required"}), 400

    search_results = Search(query, page, ads.search_ad)

    return jsonify(search_results), 200

@app.route('/add')
def add():
    if shutdown:
        return "", 404
    data = { 'title':html.escape(request.headers.get('title')),
            'description': html.escape(request.headers.get('description')),
            'location':html.escape(request.headers.get('location')),
            'phonenum':html.escape(request.headers.get('phonenum')),
            'website':html.escape(request.headers.get('website')),
            'email':html.escape(request.headers.get('email')),
            'entry_type':html.escape(request.headers.get('entrytype'))
    }
    if 'X-Forwarded-For' in request.headers:
        ip = request.headers['X-Forwarded-For'].split(',')[0].strip()
    else:
        ip = request.remote_addr

    if data['title'] == '' or data['description'] == '' or data['location'] == "" or data['phonenum'] == '' or data['entry_type'] == '':
        return jsonify({"error": "link and name headers are required"}), 400
    if general.check_if_banned_ip(ip):
        return "Banned ip", 403

    if mod:
        data['ip'] = ip
        waitlist.create_ad(data)

    else:
        # Insert new document into the collection
        ads.add_ad(data)
    return jsonify({"message": "Link added successfully"})

@app.route('/verify',methods=['POST'])
def login():
    adminname =  html.escape(request.headers.get('adminname'))
    password =  html.escape(request.headers.get('password'))
    if {adminname:password} in adwin:
        return "success",200
    else:
        return "failed",400

@app.route('/results',methods=['GET','POST'])
def results():
    adminname =  html.escape(request.headers.get('adminname'))
    password =  html.escape(request.headers.get('password'))
    if {adminname:password} in adwin:
        return waitlist.load_from_pickle()
    else:
        return "...",400

@app.route('/banip',methods=['GET','POST'])
def banip():
    adminname =  html.escape(request.headers.get('adminname'))
    password =  html.escape(request.headers.get('password'))
    id =  html.escape(request.headers.get('id'))
    if {adminname:password} in adwin:
        ban_ip(id, adminname)
        return "success", 200
    else:
        return "...",400
@app.route('/approve',methods=['POST'])
def approve():
    adminname =  html.escape(request.headers.get('adminname'))
    password =  html.escape(request.headers.get('password'))
    id =  html.escape(request.headers.get('id'))
    if {adminname:password} in adwin:
        approve_(id)
        return "success", 200
    else:
        return "...",400
@app.route('/ignore',methods=['POST'])
def ignore():
    adminname =  html.escape(request.headers.get('adminname'))
    password =  html.escape(request.headers.get('password'))
    id =  html.escape(request.headers.get('id'))
    if {adminname:password} in adwin:
        ignore_fun(id)
        return "success", 200
    else:
        return "...",400

@app.route('/shutdown_on',methods=['POST'])
def shutdown_on():
    adminname =  html.escape(request.headers.get('adminname'))
    password =  html.escape(request.headers.get('password'))
    if {adminname:password} in adwin:
        shutdown_(adminname)
        return "success", 200
    else:
        return "...",400
@app.route('/shutdown_off',methods=['POST'])
def shutdown_of():
    adminname =  html.escape(request.headers.get('adminname'))
    password =  html.escape(request.headers.get('password'))
    if {adminname:password} in adwin:
        shutdown_off(adminname)
        return "success", 200
    else:
        return "...",400
@app.route('/moderate_on',methods=['POST'])
def moderate_on():
    adminname =  html.escape(request.headers.get('adminname'))
    password =  html.escape(request.headers.get('password'))
    if {adminname:password} in adwin:
        moderate(adminname)
        return "success", 200
    else:
        return "...",400
@app.route('/moderate_off',methods=['POST'])
def moderate_off():
    adminname =  html.escape(request.headers.get('adminname'))
    password =  html.escape(request.headers.get('password'))
    if {adminname:password} in adwin:
        moderate_of(adminname)
        return "success", 200
    else:
        return "...",400
@app.route('/report')
def report():
    if shutdown:
        return "", 404
    id =  html.escape(request.headers.get('id'))

    if not id:
        return "ERROR", 400

    if 'X-Forwarded-For' in request.headers:
        ip = request.headers['X-Forwarded-For'].split(',')[0].strip()
    else:
        ip = request.remote_addr
    try:
        z = Reports[id]
    except:
        Reports[id] = []
    if ip in Reports[id]:
        return "reportspam"
    else:
        Reports[id].append(ip)
    if len(Reports[id]) >= 9:
        ads.delete_ad(id)

    return "DONE"

#127.0.0.1
app.run(host='127.0.0.1', port=8080)

