from flask import Flask, render_template
app  = Flask(__name__)

@app.route("/")
def home():
   return render_template('index.html')

@app.route("/pos")
def pos():
    return "Hello World from Flask!"

# def isValid(email):
#     regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
#     if re.fullmatch(regex, email):
#       return True
#     else:
#       return False

@app.route("/request", methods=['POST'])
def postRequest():
   return "Create Method .!!" 

@app.route('/request', methods=['GET'])
def getRequest():
   return "Get Method.!!"

@app.route('/request/<id>', methods=['GET'])
def getRequestId(id):
    req_args = request.view_args  
    print('req_args: ', req_args)
    print('req_args id: ', req_args[id])
    return req_args[id]

@app.route("/request", methods=['PUT'])
def putRequest():
   return "Put method called"

@app.route('/request/<id>', methods=['DELETE'])
def deleteRequest(id):
   req_args = request.view_args
   print(req_args[id])
   return "Delete Method called"

