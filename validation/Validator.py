import functools
from flask import jsonify,request,g
from config.Settings import Settings
import jwt

def login_required(func):   #func->insertUsers
    @functools.wraps(func)
    def checkLogin(*args, **kwargs):
        
        auth=True
        auth_header = request.headers.get('Authorization') #retrieve authorization bearer token
        
        print('auth_header: [{}]'.format(auth_header))
        #Token JWTValue
        if auth_header: 
            auth_token = auth_header.split(" ")[1]#retrieve the JWT value without the Bearer 
        else:
            auth_token = ''
            auth=False #Failed check

        if auth_token:
            try:
                payload = jwt.decode(auth_token,Settings.secret,algorithms=['HS256'])
                #decode may throw an error if the jwt signature is invalid

                g.role=payload['role']
                g.userid=payload['userid']

            except jwt.exceptions.InvalidSignatureError as err:
                print(err)
                auth=False #Failed check

        if(auth==False):
            message={"message":"Invalid or missing JWT!"}
            return jsonify(message),401
        else:
            value = func(*args, **kwargs)
        
            return value
    return checkLogin

#2 Create another new decorator require_admin that checks that the user is an admin (through the data in the JWT payload).
def require_admin(func):
    @functools.wraps(func)
    def checkAdmin(*args, **kwargs):
        
        print('g.role[{}]'.format(g.role))
        if g.role.upper()=='ADMIN':
            value = func(*args, **kwargs)
        else:
            message={"message":"Invalid role!"}
            return jsonify(message),401
        
        return value
    return checkAdmin

#3 Create a new decorator @require_isAdminOrSelf
def require_isAdminOrSelf(func):
    @functools.wraps(func)
    def isAdminOrSelf(*args, **kwargs):
        
        userid=''
        #print(kwargs)
        try:
            userid=kwargs['userid']
        except Exception as e:
            print(e)
        
        print('userid[{}]'.format(userid))
        print('g.role[{}]'.format(g.role))
        print('g.userid[{}]'.format(g.userid))
        if userid==g.userid or g.role.upper()=='ADMIN':
            value = func(*args, **kwargs)
        else:
            message={"message":"Unauthorized access!"}
            return jsonify(message),401
        
        return value
    return isAdminOrSelf



'''
import functools

def decoratorName(func):
    @functools.wraps(func)
    def wrapper_decoratorName(*args, **kwargs):
        # Do something before
        value = func(*args, **kwargs)
        # Do something after
        return value
    return wrapper_decorator
'''