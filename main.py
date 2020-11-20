import datetime
from flask import Flask, Response, request, render_template, redirect
import requests
import os

app = Flask(__name__)


def invalid_count_resp(err_msg) -> Response:
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="150" height="80" role="img" aria-label="Error: e"><title>Error: e</title><g clip-path="url(#r)"><rect x="50" width="80" height="50" fill="#e05d44"/><rect width="80" height="50" fill="#555"/></g><g fill="#fff" text-anchor="middle" font-family="Verdana,Geneva,DejaVu Sans,sans-serif" text-rendering="geometricPrecision" font-size="180"><text x="380" y="310" transform="scale(.1)" fill="#fff" textLength="420">Error</text><text x="1050" y="310" transform="scale(.1)" fill="#fff" textLength="70">{}</text></g></svg>'''.format(err_msg)

    expiry_time = datetime.datetime.utcnow() - datetime.timedelta(minutes=10)

    headers = {'Cache-Control': 'no-cache,max-age=0', 'Expires': expiry_time.strftime("%a, %d %b %Y %H:%M:%S GMT")}

    return Response(response=svg, content_type="image/svg+xml", headers=headers)

# happy & unhappy counter

def happy_counter(key):
    url = 'https://api.countapi.xyz/hit/abhi-happy/{0}'.format(key)
    try:
        resp = requests.get(url)
        if resp and resp.status_code == 200:
            return resp.json()['value']
        else:
            return None
    except Exception as e:
        return None

def unhappy_counter(key):
    url = 'https://api.countapi.xyz/hit/abhi-unhappy/{0}'.format(key)
    try:
        resp = requests.get(url)
        if resp and resp.status_code == 200:
            return resp.json()['value']
        else:
            return None
    except Exception as e:
        return None


# -----------INFO SECTION----------------------
def gethappyinfo(key):
    url = 'https://api.countapi.xyz/info/abhi-happy/{0}'.format(key)
    try:
        resp = requests.get(url)
        if resp and resp.status_code == 200:
            return resp.json()['value']
        else:
            return None
    except Exception as e:
        return None


def getunhappyinfo(key):
    url = 'https://api.countapi.xyz/info/abhi-unhappy/{0}'.format(key)
    try:
        resp = requests.get(url)
        if resp and resp.status_code == 200:
            return resp.json()['value']
        else:
            return None
    except Exception as e:
        return None



@app.route("/happy", methods = ['GET', 'POST'])
def happy() -> Response:
    
    if request.method == 'POST':
        ref = request.get_json()
        hash = ref['data']
        print(hash)
        req_source = hash
    else:
      req_source = identity_request_source()
      if not req_source:
          return invalid_count_resp('Missing required param: ref')

    hinfo = gethappyinfo(req_source)

    if not hinfo:
        hinfo = '0'

       # return invalid_count_resp("hAPPY API Failed")

    svg = '''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" height="80" width="150"><clipPath id="round"><rect fill="#fff" height="80" rx="3" width="150"/></clipPath><g clip-path="url(#round)"><rect height="60" width="70"/><rect fill="#88d8b0" height="60" width="50" x="70"/></g><g fill="#fff" font-family="DejaVu Sans,Verdana,Geneva,sans-serif" font-size="180" text-anchor="middle"><image height="50" width="60" x="5" xlink:href="data:image/svg+xml;charset=UTF-8,%3c?xml version='1.0' encoding='iso-8859-1'?%3e %3csvg fill='%2388d8b0' height='100px' version='1.1' id='Capa_1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink' x='0px' y='0px' viewBox='0 0 512 512' style='enable-background:new 0 0 512 512;' xml:space='preserve'%3e%3cg%3e%3cg%3e%3cpath d='M256,0C114.615,0,0,114.615,0,256s114.615,256,256,256s256-114.615,256-256S397.385,0,256,0z M256,480 C132.288,480,32,379.712,32,256S132.288,32,256,32s224,100.288,224,224S379.712,480,256,480z'/%3e%3c/g%3e%3c/g%3e%3cg%3e%3cg%3e%3ccircle cx='176' cy='176' r='32'/%3e%3c/g%3e%3c/g%3e%3cg%3e%3cg%3e%3ccircle cx='336' cy='176' r='32'/%3e%3c/g%3e%3c/g%3e%3cg%3e%3cg%3e%3cpath d='M368,256c0,61.856-50.144,112-112,112s-112-50.144-112-112h-32c0,79.529,64.471,144,144,144s144-64.471,144-144H368z'/%3e%3c/g%3e%3c/g%3e%3cg%3e%3c/g%3e%3cg%3e%3c/g%3e%3cg%3e%3c/g%3e%3cg%3e%3c/g%3e%3cg%3e%3c/g%3e%3cg%3e%3c/g%3e%3cg%3e%3c/g%3e%3cg%3e%3c/g%3e%3cg%3e%3c/g%3e%3cg%3e%3c/g%3e%3cg%3e%3c/g%3e%3cg%3e%3c/g%3e%3cg%3e%3c/g%3e%3cg%3e%3c/g%3e%3cg%3e%3c/g%3e%3c/svg%3e " y="3"/><text lengthAdjust="spacing" textLength="235" transform="scale(0.1)" x="950" y="340">{}</text></g></svg>'''.format(str(hinfo))


    expiry_time = datetime.datetime.utcnow() - datetime.timedelta(minutes=10)

    headers = {'Cache-Control': 'no-cache,max-age=0,no-store,s-maxage=0,proxy-revalidate',
               'Expires': expiry_time.strftime("%a, %d %b %Y %H:%M:%S GMT")}

    return Response(response=svg, content_type="image/svg+xml", headers=headers)


@app.route("/unhappy", methods=['GET', 'POST'])
def unhappy() -> Response:
  

    if request.method == 'POST':
        ref = request.get_json()
        hash = ref['data']
        print(hash)
        req_source = hash
    else:
      req_source = identity_request_source()
      if not req_source:
          return invalid_count_resp('Missing required param: ref')
 

       
    unhinfo = getunhappyinfo(req_source)

    if not unhinfo:
        unhinfo = '0'

        #return invalid_count_resp("Unhappy API Failed")

    print(unhinfo)
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" height="80" width="150"><clipPath id="round"><rect fill="#fff" height="80" rx="3" width="150"/></clipPath><g clip-path="url(#round)"><rect height="60" width="70"/><rect fill="#fe8a71" height="60" width="50" x="70"/></g><g fill="#fff" font-family="DejaVu Sans,Verdana,Geneva,sans-serif" font-size="180" text-anchor="middle"><image height="50" width="60" x="5" xlink:href="data:image/svg+xml;charset=UTF-8,%3c?xml version='1.0' encoding='iso-8859-1'?%3e %3csvg fill='%23fe8a71' version='1.1' id='Capa_1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink' x='0px' y='0px' viewBox='0 0 512 512' style='enable-background:new 0 0 512 512;' xml:space='preserve'%3e%3cg%3e%3cg%3e%3cpath d='M436.813,75.188C388.327,26.702,324.113,0,256,0S123.673,26.702,75.188,75.188C26.703,123.674,0,187.887,0,256 s26.702,132.327,75.188,180.812C123.674,485.297,187.887,512,256,512s132.327-26.702,180.813-75.188 C485.299,388.326,512,324.113,512,256S485.298,123.673,436.813,75.188z M256,482C131.383,482,30,380.617,30,256S131.383,30,256,30 s226,101.383,226,226S380.617,482,256,482z'/%3e%3c/g%3e%3c/g%3e%3cg%3e%3cg%3e%3cpath d='M346,151c-24.813,0-45,20.187-45,45s20.187,45,45,45s45-20.187,45-45S370.813,151,346,151z M346,211 c-8.271,0-15-6.729-15-15s6.729-15,15-15s15,6.729,15,15S354.271,211,346,211z'/%3e%3c/g%3e%3c/g%3e%3cg%3e%3cg%3e%3cpath d='M166,151c-24.813,0-45,20.187-45,45s20.187,45,45,45s45-20.187,45-45S190.813,151,166,151z M166,211 c-8.271,0-15-6.729-15-15s6.729-15,15-15s15,6.729,15,15S174.271,211,166,211z'/%3e%3c/g%3e%3c/g%3e%3cg%3e%3cg%3e%3cpath d='M256,269.329c-66.389,0-126.054,39.574-152.005,100.819l27.623,11.704c21.241-50.131,70.064-82.523,124.382-82.523 s103.141,32.392,124.382,82.523l27.623-11.704C382.054,308.903,322.389,269.329,256,269.329z'/%3e%3c/g%3e%3c/g%3e%3cg%3e%3c/g%3e%3cg%3e%3c/g%3e%3cg%3e%3c/g%3e%3cg%3e%3c/g%3e%3cg%3e%3c/g%3e%3cg%3e%3c/g%3e%3cg%3e%3c/g%3e%3cg%3e%3c/g%3e%3cg%3e%3c/g%3e%3cg%3e%3c/g%3e%3cg%3e%3c/g%3e%3cg%3e%3c/g%3e%3cg%3e%3c/g%3e%3cg%3e%3c/g%3e%3cg%3e%3c/g%3e%3c/svg%3e" y="3"/><text lengthAdjust="spacing" textLength="235" transform="scale(0.1)" x="950" y="340">{}</text></g></svg>'''.format(str(unhinfo))


    expiry_time = datetime.datetime.utcnow() - datetime.timedelta(minutes=10)

    headers = {'Cache-Control': 'no-cache,max-age=0,no-store,s-maxage=0,proxy-revalidate',
               'Expires': expiry_time.strftime("%a, %d %b %Y %H:%M:%S GMT")}

    return Response(response=svg, content_type="image/svg+xml", headers=headers)

@app.route("/happy/done")
def happy_done() -> Response:
    req_source = identity_request_source()

    if not req_source:
        return invalid_count_resp('Missing required param: ref')

    hcount = happy_counter(req_source)

    if not hcount:
        return invalid_count_resp("Assign API Failed")

   # svg = '''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" height="80" width="150"><clipPath id="round"><rect fill="#fff" height="80" rx="3" width="150"/></clipPath><g clip-path="url(#round)"><rect height="60" width="70"/><rect fill="#88d8b0" height="60" width="50" x="70"/></g><g fill="#fff" font-family="DejaVu Sans,Verdana,Geneva,sans-serif" font-size="180" text-anchor="middle"><image height="50" width="60" x="5" xlink:href="data:image/svg+xml;charset=UTF-8,%3c?xml version='1.0' encoding='iso-8859-1'?%3e %3csvg fill='%2388d8b0' height='100px' version='1.1' id='Capa_1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink' x='0px' y='0px' viewBox='0 0 512 512' style='enable-background:new 0 0 512 512;' xml:space='preserve'%3e%3cg%3e%3cg%3e%3cpath d='M256,0C114.615,0,0,114.615,0,256s114.615,256,256,256s256-114.615,256-256S397.385,0,256,0z M256,480 C132.288,480,32,379.712,32,256S132.288,32,256,32s224,100.288,224,224S379.712,480,256,480z'/%3e%3c/g%3e%3c/g%3e%3cg%3e%3cg%3e%3ccircle cx='176' cy='176' r='32'/%3e%3c/g%3e%3c/g%3e%3cg%3e%3cg%3e%3ccircle cx='336' cy='176' r='32'/%3e%3c/g%3e%3c/g%3e%3cg%3e%3cg%3e%3cpath d='M368,256c0,61.856-50.144,112-112,112s-112-50.144-112-112h-32c0,79.529,64.471,144,144,144s144-64.471,144-144H368z'/%3e%3c/g%3e%3c/g%3e%3cg%3e%3c/g%3e%3cg%3e%3c/g%3e%3cg%3e%3c/g%3e%3cg%3e%3c/g%3e%3cg%3e%3c/g%3e%3cg%3e%3c/g%3e%3cg%3e%3c/g%3e%3cg%3e%3c/g%3e%3cg%3e%3c/g%3e%3cg%3e%3c/g%3e%3cg%3e%3c/g%3e%3cg%3e%3c/g%3e%3cg%3e%3c/g%3e%3cg%3e%3c/g%3e%3cg%3e%3c/g%3e%3c/svg%3e " y="3"/><text lengthAdjust="spacing" textLength="235" transform="scale(0.1)" x="950" y="340">{}</text></g></svg>'''.format(str(hcount))


    expiry_time = datetime.datetime.utcnow() - datetime.timedelta(minutes=10)

    headers = {'Cache-Control': 'no-cache,max-age=0,no-store,s-maxage=0,proxy-revalidate',
               'Expires': expiry_time.strftime("%a, %d %b %Y %H:%M:%S GMT")}
# Response(response=svg, content_type="image/svg+xml", headers=headers)
    user = req_source.split('.')[0]
    repo = req_source.split('.')[1]
    res = "https://github.com/{}/{}".format(user,repo)
    return redirect(res, code=302)

@app.route("/unhappy/done")
def unhappy_done() -> Response:
    
    req_source = identity_request_source()

    if not req_source:
        return invalid_count_resp('Missing required param: ref')

    unhcount = unhappy_counter(req_source)

    if not unhcount:
        return invalid_count_resp("Assign API Failed")

   # svg = '''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" height="80" width="150"><clipPath id="round"><rect fill="#fff" height="80" rx="3" width="150"/></clipPath><g clip-path="url(#round)"><rect height="60" width="70"/><rect fill="#88d8b0" height="60" width="50" x="70"/></g><g fill="#fff" font-family="DejaVu Sans,Verdana,Geneva,sans-serif" font-size="180" text-anchor="middle"><image height="50" width="60" x="5" xlink:href="data:image/svg+xml;charset=UTF-8,%3c?xml version='1.0' encoding='iso-8859-1'?%3e %3csvg fill='%2388d8b0' height='100px' version='1.1' id='Capa_1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink' x='0px' y='0px' viewBox='0 0 512 512' style='enable-background:new 0 0 512 512;' xml:space='preserve'%3e%3cg%3e%3cg%3e%3cpath d='M256,0C114.615,0,0,114.615,0,256s114.615,256,256,256s256-114.615,256-256S397.385,0,256,0z M256,480 C132.288,480,32,379.712,32,256S132.288,32,256,32s224,100.288,224,224S379.712,480,256,480z'/%3e%3c/g%3e%3c/g%3e%3cg%3e%3cg%3e%3ccircle cx='176' cy='176' r='32'/%3e%3c/g%3e%3c/g%3e%3cg%3e%3cg%3e%3ccircle cx='336' cy='176' r='32'/%3e%3c/g%3e%3c/g%3e%3cg%3e%3cg%3e%3cpath d='M368,256c0,61.856-50.144,112-112,112s-112-50.144-112-112h-32c0,79.529,64.471,144,144,144s144-64.471,144-144H368z'/%3e%3c/g%3e%3c/g%3e%3cg%3e%3c/g%3e%3cg%3e%3c/g%3e%3cg%3e%3c/g%3e%3cg%3e%3c/g%3e%3cg%3e%3c/g%3e%3cg%3e%3c/g%3e%3cg%3e%3c/g%3e%3cg%3e%3c/g%3e%3cg%3e%3c/g%3e%3cg%3e%3c/g%3e%3cg%3e%3c/g%3e%3cg%3e%3c/g%3e%3cg%3e%3c/g%3e%3cg%3e%3c/g%3e%3cg%3e%3c/g%3e%3c/svg%3e " y="3"/><text lengthAdjust="spacing" textLength="235" transform="scale(0.1)" x="950" y="340">{}</text></g></svg>'''.format(str(unhinfo))

    expiry_time = datetime.datetime.utcnow() - datetime.timedelta(minutes=10)

    headers = {'Cache-Control': 'no-cache,max-age=0,no-store,s-maxage=0,proxy-revalidate',
               'Expires': expiry_time.strftime("%a, %d %b %Y %H:%M:%S GMT")}
# Response(response=svg, content_type="image/svg+xml", headers=headers)
    user = req_source.split('.')[0]
    repo = req_source.split('.')[1]
    res = "https://github.com/{}/{}".format(user,repo)
    return redirect(res, code=302)


@app.route("/index.html")
@app.route("/index")
@app.route("/")
def index() -> Response:
    return render_template('index.html')


def identity_request_source() -> str:
    ref = request.args.get('ref')
    print(ref)
    if ref is not None and len(ref):
        m = ref
        return m 
    return None


if __name__ == '__main__':
    app.run()