from fastapi.staticfiles import StaticFiles
from typing import List, Annotated
from fastapi import File, UploadFile
from fastapi.param_functions import Form
import MySQLdb
from pydantic import BaseModel
db = MySQLdb.connect("localhost", "root", "", "db",port_no)
import mysql.connector
import json
import os
import base64
import random
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
import bcrypt
from fastapi.middleware.cors import CORSMiddleware
import logging
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from io import BytesIO
from PIL import Image


# Configure logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app=FastAPI()

conf = ConnectionConfig(
    MAIL_USERNAME="",
    MAIL_PASSWORD="",
    MAIL_FROM="",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_FROM_NAME="",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
SERVER = "http://localhost:5000/"

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Mount the static files directory
app.mount("/static", StaticFiles(directory="./static/"), name="static")
BASE_DIRECTORY = "./static/temp_images/"

#generating sql commands
def create_sql_comand(keys,value):
    str1="select leaf_division from leaf where "
    for index in range(0,len(keys)-1):
        str1=str1+f"{keys[index]}='{value[index]}' and "
    str1=str1+f"{keys[len(keys)-1]}='{value[len(keys)-1]}'"
    return str1

#getting images path from contained folder
def getFileNames(folderNames):
    IMAGES_PATH = './static/dataset/'
    answer = {}
    fileName = []
    for folder in folderNames:
        allfiles = os.listdir(IMAGES_PATH+folder)    
        for file in allfiles:
            fileName.append(SERVER + IMAGES_PATH + folder + "/" + file)
        answer[folder] = fileName
        fileName = []  
    return answer

def insert_sql_comand(keys,value, plantName, startIndex, lastIndex, user):
    str1="insert into temp ("
    str1=str1+"leaf_division , "
    for index in range(0,len(keys)-1):
        str1=str1+f"{keys[index]} , "
    str1=str1+f"{keys[len(keys)-1]},"
    str1=str1+"start_index, last_index, user_id)values("    
    str1=str1+f"'{plantName}' , "
    for index in range(0,len(keys)-1):
        str1=str1+f"'{value[index]}' , "
    str1=str1+f"'{value[len(keys)-1]}', "
    str1=str1+f"{startIndex},{lastIndex},'{user}')"    
    return str1


def imagelist(selected_id):
    mycursor=db.cursor()
    command="select img_index from temp_images where folder_id=%s"
    try:
        images={}
        for i in range(0,len(selected_id)):
            mycursor.execute(command,(selected_id[i],))
            result=mycursor.fetchall()
            arr=[]
            for it in result:
                arr.append(it[0])
            #print(arr)
            images[selected_id[i]]=arr
               
        return images    
    except:    
           print( "Error: unable to fetch")
           return images    


def getUpvotes(selected_id):
    command1="select upvote from temp where folder_id=%s"
    command2="select img_index, upvote from temp_images where folder_id=%s"
    command3="select characteristics, suggestion, upvote from corrections where folder_id=%s"
    mycursor=db.cursor()
    try:
        return_result1={}
        for i in range(0,len(selected_id)):
            mycursor.execute(command1,(selected_id[i],))
            result1=mycursor.fetchone()
            return_result1[selected_id[i]]=[result1[0]]
        print(return_result1)
        return_result2={}
        for i in range(0,len(selected_id)):
            mycursor.execute(command2,(selected_id[i],))
            result2=mycursor.fetchall()
            for item in result2:
                return_result2[str(selected_id[i])+"_"+str(item[0])]=[item[1]]
        print(return_result2)
        return_result3={}
        for i in range(0,len(selected_id)):
            mycursor.execute(command3,(selected_id[i],))
            result3=mycursor.fetchall()
            for item in result3:
                return_result3[str(selected_id[i])+"_"+item[0]+"_"+item[1]]=[item[2]]
        print(return_result3)    
        return [return_result1, return_result2, return_result3]
    except:
        print( "Error: unable to get upvotes")
        return []


def folderReviews(selected_id, user):
    if user!="":
        command="select vote, report from folder_reviewers where folder_id=%s and user_id="+f"'{user}'"
        mycursor=db.cursor()
        try:
            return_result={}
            for i in range(0,len(selected_id)):
                mycursor.execute(command,(selected_id[i],))
                result=mycursor.fetchone()
                if result is not None:
                    return_result[selected_id[i]]=[result[0],result[1]]
            print(return_result)
            return return_result
        except:
            print( "Error: unable to change")
            return {}
    else:
        print("Not logged in")
        return {}  

def ImgReviews(selected_id, user):
    if user!="":
        command="select img_index, vote, report from image_reviewers where folder_id=%s and user_id="+f"'{user}'"
        mycursor=db.cursor()
        try:
            return_result={}
            for i in range(0,len(selected_id)):
                mycursor.execute(command,(selected_id[i],))
                result=mycursor.fetchall()
                for item in result:
                    return_result[str(selected_id[i])+"_"+str(item[0])]=[item[1],item[2]]
            print(return_result)    
            return return_result
        except:
            print( "Error: unable to change")
            return {}
    else:
        print("Not logged in")
        return {}

def get_corrections(selected_id):
    mycursor=db.cursor()
    try:
        return_result={}
        command="select characteristics, suggestion from corrections where folder_id=%s"
        for i in range(0,len(selected_id)):
            mycursor.execute(command,(selected_id[i],))
            result=mycursor.fetchall()
            for item in result:
                key=str(selected_id[i])+"_"+item[0]
                if key in return_result:
                    return_result[key].append(item[1])
                else:
                    return_result[key]=[item[1]]
        print(return_result)            
        return return_result
    except:
        print( "Error: unable to fetch")
        return {}


def correctionReviews(selected_id, user):
    if user!="":
        command="select characteristics, suggestion, vote from correction_reviewers where folder_id=%s and user_id="+f"'{user}'"
        mycursor=db.cursor()
        try:
            return_result={}
            for i in range(0,len(selected_id)):
                mycursor.execute(command,(selected_id[i],))
                result=mycursor.fetchall()
                for item in result:
                    return_result[str(selected_id[i])+"_"+item[0]+"_"+item[1]]=item[2]
            print(return_result)    
            return return_result
        except:
            print( "Error: unable to change")
            return {}
    else:
        print("Not logged in")
        return {}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
# dependency function to extract and verify the access token
def get_current_user(token: str = Depends(oauth2_scheme)):
    # print("entered in get_current_user")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        print("entered in get_current_user 1 "+ user_id )
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")



#recive client server call

@app.post('/predict')
def calc(data: dict = None):
    # data = request.get_json()
    keys=[]
    value=[]
    for arr in data:
         keys.append(arr)
         value.append(data[arr])
   
    command = create_sql_comand(keys,value)
    print(command)
    curs = db.cursor()  #create a curser to database for  data extraction
    try:
        curs.execute(command)
        folder=curs.fetchall() #insert extracted data to folder variable
        intersection_folder=[]
        print(folder)
        for foll in folder:
            intersection_folder.append(foll[0])
        filenames=getFileNames(intersection_folder)
        # print(filenames)
        # return json.dumps(filenames) #dump data from server to client
        return filenames
    except:
        print( "Error: unable to fetch items")
        return json.dumps({})   #dump data from server to client

       
# @app.route("/adddata", methods=["GET", "POST"])
def send(plantName, data, startIndex, lastIndex, user):
   print(data)
   print(type(data))
   keys1=[]
   value1=[]
   
   for arr in data:
        keys1.append(arr)
        value1.append(data[arr])
   
   command = insert_sql_comand(keys1,value1, plantName, startIndex, lastIndex, user)
   mycursor = db.cursor()  #create a curser to database for  data extraction
   print(command)
   try:
        mycursor.execute(command)
        db.commit()
        mycursor.execute("select max(folder_id) from temp where user_id="+f"'{user}'")
        result=mycursor.fetchone()
        print(result)
        query="insert into temp_images(folder_id,img_index) values(%s,%s)"
        for i in range(startIndex, lastIndex+1):
            print(i)
            tuple=(result[0],i)
            mycursor.execute(query,tuple)
        # print("done")    
        db.commit()    
        return 
   except:    
           print( "Error: unable to fetch items")
           return 


@app.route("/imagedata", methods=["GET", "POST"])
def image(plantName, images, startIndex):
    cnt=startIndex
    for base64_string in images:
        try:
        # Remove the data:image/jpeg;base64, header
            if base64_string.startswith("data:image/jpeg;base64,"):
                base64_string = base64_string.replace("data:image/jpeg;base64,", "")
            elif base64_string.startswith("data:image/png;base64,"):
                base64_string = base64_string.replace("data:image/png;base64,", "")
            elif base64_string.startswith("data:image/jpg;base64,"):
                base64_string = base64_string.replace("data:image/jpg;base64,", "")
            # Decode the Base64 string into bytes
            image_bytes = base64.b64decode(base64_string)
            # Create a BytesIO object to treat the bytes as an image file
            image_buffer = BytesIO(image_bytes)
            # Open the image using PIL (Python Imaging Library)
            image = Image.open(image_buffer)
            image.save(BASE_DIRECTORY + plantName + "/img_"+ str(cnt) +".png")
            cnt=cnt+1
        except Exception as e:
            print("Error decoding Base64 to image:", str(e))
            return None
    return         

def imagename(plantName):
   cnt=0
   command="select last_index from temp where folder_id=(select max(folder_id) from temp where leaf_division="+f"'{plantName}')"
   print(command)
   mycursor=db.cursor()
   try:
        mycursor.execute(command)
        result=mycursor.fetchone()
        if result is None:
            os.mkdir(BASE_DIRECTORY + plantName)
        else:
            cnt=result[0]
        startIndex=cnt+1
        # lastIndex=cnt + length
        # print(str(startIndex)+" start")
        return startIndex
   except:    
        print()
        return ""   

class AddLeaf(BaseModel):
    plantName: str
    userModel: dict
    images: List[str]

@app.post('/addleaf')
async def addLeaf(data: AddLeaf, user: str = Depends(get_current_user)):
    print(user)
    print(data.plantName)
    length=len(data.images)
    startIndex=imagename(data.plantName)
    print(data.userModel)
    send(data.plantName, data.userModel, startIndex, startIndex+length-1, user)
    image(data.plantName, data.images, startIndex)
    return {'msg':"Thank you for your contribution."}
    # print(data.images)
    

# Create a FastMail instance
fastmail = FastMail(conf)
# Send an email
async def sendMail(otp, recipient_email):
    print(otp+" "+recipient_email)
    message = MessageSchema(
        subject="subject",
        recipients=[recipient_email],
        body="body",
        subtype="plain"
    )
    try:
        await fastmail.send_message(message)
        return 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

class VerifyEmail(BaseModel):
    email: str

async def generate_otp(user_email):
    otp=random.randint(1000,9999)
    print(otp)
    # sendMail(str(otp), user_email)
    await sendMail(str(otp), user_email)
    print("sentmail_1")
    return str(otp)

@app.post('/resend')
async def resend(data: VerifyEmail):
    otp=await generate_otp(data.email)
    return {"flag":True, "otp":otp}


@app.post('/register')
async def signup(data: VerifyEmail):
    print(data.email)
    command="select user_id from users where user_id="+f"'{data.email}'"
    mycursor = db.cursor()  
    try:
        mycursor.execute(command)
        res=mycursor.fetchone()
        if res is not None:
            return {"flag":False, "value":"You are an existing user, please login"}
        otp=await generate_otp(data.email)
        return {"flag":True, "otp":otp}
    except:    
           print( "Error: unable to check email")
           return json.dumps("")

class UserRegistration(BaseModel):
    username: str
    phone: str
    password: str

@app.post('/registration_otp')
def registration_otp(data: UserRegistration):
    command = "insert into users values("+f"'{data.username}' , '{data.phone}', hex(aes_encrypt('{data.password}','PLANT')),0)"
    mycursor = db.cursor()
    try:
        mycursor.execute(command)
        db.commit()
        return {"msg":"You are successfully registered"}
    except:
        print( "Error: unable to register")
        return json.dumps("")    


# Route for token refresh
@app.get("/refreshToken")
def refresh_token(current_token: str = Depends(oauth2_scheme)):
    try:
        # logger.info(f"Received token: {current_token}")
        # Verify the old token and get user claims
        payload = jwt.decode(current_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=400, detail="Invalid token")

        # Generate a new token with an extended expiration time
        new_token_expires = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        new_token_payload = {"user_id": user_id, "exp": new_token_expires}
        new_token = jwt.encode(new_token_payload, SECRET_KEY, algorithm=ALGORITHM)
        return {"access_token": new_token, "token_type": "bearer"}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")    

def create_access_token(user_id, expires_delta):
    to_encode = {"user_id": user_id, "exp": datetime.utcnow() + expires_delta}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

class UserLogin(BaseModel):
    email: str
    password: str

@app.post("/login")
def signin(user: UserLogin):
    command = "select cast(aes_decrypt(unhex(password), 'key') as char) from users where user_id='"+user.email+"'"
    mycursor = db.cursor()
    print(command)
    try:
        mycursor.execute(command)
        result = mycursor.fetchone()
        print(result)
        if result is None:
            return { "message": "Register Yourself", "success": False}
        elif result[0] == user.password:
            access_token = create_access_token(user.email, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
            return {
                "message": "You are successfully logged in.",
                "success": True,
                "access_token": access_token,
                "token_type": "bearer"
            }
        else:
            return { "message": "Bad Request", "success": False}
    except:
        return json.dumps("")



@app.get("/checklogin")
def protected_route(current_user: str = Depends(get_current_user)):
    # print(current_user)
    if current_user!="":
        return "true"
    return "false"  

 
@app.post('/checkemail')
async def checkemail(data: VerifyEmail):
    print(data.email)
    command="select user_id from users where user_id="+f"'{data.email}'"
    mycursor = db.cursor()  
    print(command)
    try:
        mycursor.execute(command)
        result=mycursor.fetchone()
        print(result)
        print(type(result))
        if len(result)>0:
            otp=await generate_otp(data.email)
            print("sentmail_2")
            return {"flag":True, "otp":otp}
        else:
            return {"flag":False}
    except:    
           print( "Error: unable to change")
           return json.dumps("")
           

@app.post('/chngpswd')
def chngpswd(user: UserLogin):
    command = "update users set `password`="+f"hex(aes_encrypt('{user.password}','key')) where user_id='{user.email}'"
    mycursor = db.cursor()  
    print(command)
    try:
        mycursor.execute(command)
        db.commit()
        return json.dumps("Password changed successfully.")
    except:    
           print( "Error: unable to change")
           return json.dumps("")


# @app.route("/folderlist", methods=["GET", "POST"])
@app.get('/folderlist')
def folderlist(user: str = Depends(get_current_user)):
    command1="select folder_id from temp"
    mycursor = db.cursor()  
    try:
        mycursor.execute(command1)
        id_list=mycursor.fetchall()
        if id_list is None:
            return json.dumps([])
        print(id_list)
        index=[]
        if len(id_list)>5:
            index=random.sample(range(0,len(id_list)),5)
        else:
            for i in range(0,len(id_list)):
                index.append(i)
        selected_id=[]
        return_folder=[]
        for i in range(0,len(index)):
            selected_id.append(id_list[index[i]][0])
        print(selected_id)    
        command2="select folder_id, leaf_division, leaf_apices, leaf_bases, leaf_margin from temp where folder_id=%s"
        for i in range(0,len(selected_id)):
            mycursor.execute(command2,(selected_id[i],))
            folders=mycursor.fetchone()
            f1=[]
            for f in folders:
                f1.append(f)
            return_folder.append(f1)
        print(return_folder)
        return_image=imagelist(selected_id)
        upvotesCount=getUpvotes(selected_id)
        reviewed_folders=folderReviews(selected_id, user)  
        reviewed_images=ImgReviews(selected_id, user)
        corrections=get_corrections(selected_id)  
        reviewed_corrections=correctionReviews(selected_id, user)      
        return [return_folder,return_image,upvotesCount[0],upvotesCount[1],upvotesCount[2],reviewed_folders,reviewed_images,corrections,reviewed_corrections]
    except:    
           print( "Error: unable to check")
           return json.dumps("")  

class FolderVote(BaseModel):
    id: int
    ch: str
    report_reason: str

# @app.route("/folder_vote", methods=["GET", "POST"])
@app.post('/folder_vote')
def folder_vote(data: FolderVote, user: str = Depends(get_current_user)):
    print(user)
    print(data)
    mycursor = db.cursor()
    command1="select vote, report from folder_reviewers where user_id="+f"'{user}'"+" and folder_id="+f"{data.id}"
    try:
        #print(1)
        mycursor.execute(command1)
        #print(2)
        result=mycursor.fetchone()
        db.commit()
        # print(result)
        # print(type(result))
        command2=""
        command3=""
        if result is None:        
            if(data.ch=='u'):
                command2="insert into folder_reviewers values("+f"'{user}',{data.id},1,0,DEFAULT)"
                command3="update temp set upvote=upvote+1 where folder_id="+f"{data.id}"
                print("result is None")
            elif(data.ch=='d'):
                command2="insert into folder_reviewers values("+f"'{user}',{data.id},-1,0,DEFAULT)"
                command3="update temp set downvote=downvote+1 where folder_id="+f"{data.id}"
            elif(data.ch=='r'):
                command2="insert into folder_reviewers values("+f"'{user}',{data.id},0,1,'{data.report_reason}')"
                command3="update temp set report=report+1 where folder_id="+f"{data.id}"    
        else:
            if result[1]==1 and data.ch=='r':
                if result[0]==0:
                    command2="delete from folder_reviewers where user_id="+f"'{user}' and folder_id={data.id}"
                    command3="update temp set report=report-1 where folder_id="+f"{data.id}"
                elif result[0]==-1:
                    command2="update folder_reviewers set report=0, report_reason=DEFAULT(report_reason) where user_id="+f"'{user}' and folder_id={data.id}"
                    command3="update temp set report=report-1 where folder_id="+f"{data.id}"    
            elif result[0]==1 and data.ch=='r':
                command2="update folder_reviewers set vote=0, report=1, report_reason="+f"'{data.report_reason}' where user_id='{user}' and folder_id={data.id}"
                command3="update temp set upvote=upvote-1, report=report+1 where folder_id="+f"{data.id}"
            elif result[0]==1 and data.ch=='u':
                command2="delete from folder_reviewers where user_id="+f"'{user}' and folder_id={data.id}"
                command3="update temp set upvote=upvote-1 where folder_id="+f"{data.id}"
            elif result[0]==-1 and data.ch=='u':
                if result[1]==0:
                    command2="update folder_reviewers set vote=1 where user_id="+f"'{user}' and folder_id={data.id}"
                    command3="update temp set upvote=upvote+1, downvote=downvote-1 where folder_id="+f"{data.id}"
            elif result[0]==-1 and data.ch=='d':
                if result[1]==0:
                    command2="delete from folder_reviewers where user_id="+f"'{user}' and folder_id={data.id}"
                    command3="update temp set downvote=downvote-1 where folder_id="+f"{data.id}"
                elif result[1]==1:
                    command2="update folder_reviewers set vote=0 where user_id="+f"'{user}' and folder_id={data.id}"
                    command3="update temp set downvote=downvote-1 where folder_id="+f"{data.id}"    
            elif result[0]==-1 and data.ch=='r':
                    command2="update folder_reviewers set report=1, report_reason="+f"'{data.report_reason}' where user_id='{user}' and folder_id={data.id}"
                    command3="update temp set report=report+1 where folder_id="+f"{data.id}"
            elif result[0]==1 and data.ch=='d':
                command2="update folder_reviewers set vote=-1 where user_id="+f"'{user}' and folder_id={data.id}"
                command3="update temp set upvote=upvote-1, downvote=downvote+1 where folder_id="+f"{data.id}"
        print(command2)
        print(command3)
        if command2!="" and command3!="":
            mycursor.execute(command2)
            mycursor.execute(command3)
            command4="select upvote from temp where folder_id="+f"{data.id}"
            command5="select vote, report from folder_reviewers where user_id="+f"'{user}' and folder_id={data.id}"
            mycursor.execute(command4)
            res1=mycursor.fetchone()
            print(res1)
            mycursor.execute(command5)
            res2=mycursor.fetchone()
            print(res2)
            db.commit()
            if res2!=None:
                return_res=[res1[0],res2[0],res2[1]]
            else:
                return_res=[res1[0],0,0]  
            mycursor.close()
            print("done")
           
        return return_res        
    except:
        print( "Error: unable to change")
        return json.dumps("")

class ImageVote(BaseModel):
    id: int
    ind: int
    ch: str
    report_reason: str


# @app.route("/image_vote", methods=["GET", "POST"])
# @cross_origin(supports_credentials=True)
@app.post('/image_vote')
def image_vote(data: ImageVote, user: str = Depends(get_current_user)):
    mycursor = db.cursor()
    command1="select vote, report from image_reviewers where user_id="+f"'{user}' and folder_id={data.id} and img_index={data.ind}"
    try:
        print(1)
        mycursor.execute(command1)
        print(2)
        result=mycursor.fetchone()
        #db.commit()
        print(result)
        print(type(result))
        command2=""
        command3=""
        if result is None:        
            if(data.ch=='u'):
                command2="insert into image_reviewers values("+f"'{user}',{data.id},{data.ind},1,0,DEFAULT)"
                command3="update temp_images set upvote=upvote+1 where folder_id="+f"{data.id} and img_index={data.ind}"
            elif(data.ch=='d'):
                command2="insert into image_reviewers values("+f"'{user}',{data.id},{data.ind},-1,0,DEFAULT)"
                command3="update temp_images set downvote=downvote+1 where folder_id="+f"{data.id} and img_index={data.ind}"
            elif(data.ch=='r'):
                command2="insert into image_reviewers values("+f"'{user}',{data.id},{data.ind},0,1,'{data.report_reason}')"
                command3="update temp_images set report=report+1 where folder_id="+f"{data.id} and img_index={data.ind}"    
        else:
            if result[1]==1 and data.ch=='r':
                if result[0]==0:
                    command2="delete from image_reviewers where user_id="+f"'{user}' and folder_id={data.id} and img_index={data.ind}"
                    command3="update temp_images set report=report-1 where folder_id="+f"{data.id} and img_index={data.ind}"
                elif result[0]==-1:
                    command2="update image_reviewers set report=0, report_reason=DEFAULT(report_reason)  where user_id="+f"'{user}' and folder_id={data.id} and img_index={data.ind}"
                    command3="update temp_images set report=report-1 where folder_id="+f"{data.id} and img_index="+f"{data.ind}"    
            elif result[0]==1 and data.ch=='r':
                command2="update image_reviewers set vote=0, report=1, report_reason="+f"'{data.report_reason}' where user_id='{user}' and folder_id={data.id} and img_index={data.ind}"
                command3="update temp_images set upvote=upvote-1, report=report+1 where folder_id="+f"{data.id} and img_index={data.ind}"
            elif result[0]==1 and data.ch=='u':
                command2="delete from image_reviewers where user_id="+f"'{user}' and folder_id={data.id} and img_index={data.ind}"
                command3="update temp_images set upvote=upvote-1 where folder_id="+f"{data.id} and img_index={data.ind}"
            elif result[0]==-1 and data.ch=='u':
                if result[1]==0:
                    command2="update image_reviewers set vote=1 where user_id="+f"'{user}' and folder_id={data.id} and img_index={data.ind}"
                    command3="update temp_images set upvote=upvote+1, downvote=downvote-1 where folder_id="+f"{data.id} and img_index={data.ind}"
            elif result[0]==-1 and data.ch=='d':
                if result[1]==0:
                    command2="delete from image_reviewers where user_id="+f"'{user}' and folder_id={data.id} and img_index={data.ind}"
                    command3="update temp_images set downvote=downvote-1 where folder_id="+f"{data.id} and img_index={data.ind}"
                elif result[1]==1:
                    command2="update image_reviewers set vote=0 where user_id="+f"'{user}' and folder_id={data.id} and img_index={data.ind}"
                    command3="update temp_images set downvote=downvote-1 where folder_id="+f"{data.id} and img_index={data.ind}"    
            elif result[0]==-1 and data.ch=='r':
                    command2="update image_reviewers set report=1, report_reason="+f"'{data.report_reason}' where user_id='{user}' and folder_id={data.id} and img_index={data.ind}"
                    command3="update temp_images set report=report+1 where folder_id="+f"{data.id} and img_index="+f"{data.ind}"
            elif result[0]==1 and data.ch=='d':
                command2="update image_reviewers set vote=-1 where user_id="+f"'{user}' and folder_id={data.id} and img_index={data.ind}"
                command3="update temp_images set upvote=upvote-1, downvote=downvote+1 where folder_id="+f"{data.id} and img_index={data.ind}"
        print(command2)
        print(command3)
        if command2!="" and command3!="":
            mycursor.execute(command2)
            mycursor.execute(command3)
            command4="select upvote from temp_images where folder_id="+f"{data.id} and img_index={data.ind}"
            command5="select vote, report from image_reviewers where user_id="+f"'{user}' and folder_id={data.id} and img_index={data.ind}"
            mycursor.execute(command4)
            res1=mycursor.fetchone()
            print(res1)
            mycursor.execute(command5)
            res2=mycursor.fetchone()
            print(res2)
            db.commit()
            if res2!=None:
                return_res=[res1[0],res2[0],res2[1]]
            else:
                return_res=[res1[0],0,0]  
            mycursor.close()  
        return return_res        
    except:
        print( "Error: unable to change")
        return json.dumps("")


class SaveComments(BaseModel):
    id: int
    msg: str

@app.post('/save_comment')
def save_comment(data: SaveComments, user: str = Depends(get_current_user)):
    command="insert into reviews values("+f"{data.id},'{user}','{data.msg}',now())"
    mycursor=db.cursor()
    try:
        mycursor.execute(command)
        db.commit()
        return json.dumps("")
    except:
        print( "Error: unable to change")
        return json.dumps("")


class GetComments(BaseModel):
    id: int
    
@app.post('/get_comments')
def fetch_comment(data: GetComments):
    command="select user_id, comment, date from reviews where folder_id="+str(data.id)
    mycursor=db.cursor()
    try:
        mycursor.execute(command)
        comments=mycursor.fetchall()
        print(comments)
        return_comments=[]
        for i in comments:
            temp=[]
            for j in i:
                temp.append(j)
            return_comments.append(temp)  
        print(return_comments)      
        return return_comments
    except:
        print( "Error: unable to fetch")
        return json.dumps("")          


class SaveCorrections(BaseModel):
    id: int
    characteristics: str
    suggestion: str

@app.post('/save_corrections')
def save_corrections(data: SaveCorrections, user: str = Depends(get_current_user)):
    mycursor=db.cursor()
    try:
        command1="select * from corrections where folder_id="+f"{data.id} and characteristics='{data.characteristics}' and suggestion='{data.suggestion}'"
        mycursor.execute(command1)
        print(1)
        result=mycursor.fetchone()
        print(result)
        if result is None:
            command2="insert into corrections(folder_id, characteristics, suggestion, user_id) values("+f"{data.id},'{data.characteristics}','{data.suggestion}','{user}')"
            print(2)
            mycursor.execute(command2)
            print(3)
            db.commit()
            return ["added successfully",data.suggestion,0]
        else:    
            return ["exists already, please upvote that","",0]
    except:
        print( "Error: unable to change")
        return json.dumps("")


class SaveCorrections(BaseModel):
    id: int
    characteristics: str
    suggestion: str
    ch: str

@app.post('/correction_vote')
def correctionVote(data: SaveCorrections, user: str = Depends(get_current_user)):
    fol_id=data.id
    feature=data.characteristics
    suggestion=data.suggestion
    ch=data.ch
    command1="select vote from correction_reviewers where user_id="+f"'{user}' and folder_id={fol_id} and characteristics='{feature}' and suggestion='{suggestion}'"
    command2=""
    command3=""
    try:
        mycursor=db.cursor()
        mycursor.execute(command1)
        result=mycursor.fetchone()
        if result is None:
            if ch=='u':
                command2="insert into correction_reviewers values("+f"'{user}',{fol_id},'{feature}','{suggestion}',1)"
                command3="update corrections set upvote=upvote+1 where "+f"folder_id={fol_id} and characteristics='{feature}' and suggestion='{suggestion}'"
            elif ch=='d':
                command2="insert into correction_reviewers values("+f"'{user}',{fol_id},'{feature}','{suggestion}',-1)"
                command3="update corrections set downvote=downvote+1 where "+f"folder_id={fol_id} and characteristics='{feature}' and suggestion='{suggestion}'"
        else:
            if  ch=='u':
                if result[0]==1:
                    command2="delete from correction_reviewers where "+f"folder_id={fol_id} and characteristics='{feature}' and suggestion='{suggestion}'"
                    command3="update corrections set upvote=upvote-1 where "+f"folder_id={fol_id} and characteristics='{feature}' and suggestion='{suggestion}'"
                elif result[0]==-1:
                    command2="update correction_reviewers set vote=1 where "+f"folder_id={fol_id} and characteristics='{feature}' and suggestion='{suggestion}'"
                    command3="update corrections set upvote=upvote+1, downvote=downvote-1 where "+f"folder_id={fol_id} and characteristics='{feature}' and suggestion='{suggestion}'"
            elif  ch=='d':
                if result[0]==-1:
                    command2="delete from correction_reviewers where "+f"folder_id={fol_id} and characteristics='{feature}' and suggestion='{suggestion}'"
                    command3="update corrections set downvote=downvote-1 where "+f"folder_id={fol_id} and characteristics='{feature}' and suggestion='{suggestion}'"
                elif result[0]==1:
                    command2="update correction_reviewers set vote=-1 where "+f"folder_id={fol_id} and characteristics='{feature}' and suggestion='{suggestion}'"
                    command3="update corrections set downvote=downvote+1, upvote=upvote-1 where "+f"folder_id={fol_id} and characteristics='{feature}' and suggestion='{suggestion}'"        
        if command2!="" and command3!="":
            mycursor.execute(command2)
            mycursor.execute(command3)
            command4="select upvote from corrections where "+f"folder_id={fol_id} and characteristics='{feature}' and suggestion='{suggestion}'"
            command5="select vote from correction_reviewers where user_id="+f"'{user}' and folder_id={fol_id} and characteristics='{feature}' and suggestion='{suggestion}'"
            mycursor.execute(command4)
            res1=mycursor.fetchone()
            print(res1)
            mycursor.execute(command5)
            res2=mycursor.fetchone()
            print(res2)
            db.commit()
            if res2!=None:
                return_res=[res1[0],res2[0]]
            else:
                return_res=[res1[0],0]  
            mycursor.close()  
        return return_res
    
    except:    
        print("unable to update")
        return json.dumps("")

import uvicorn

if __name__ == '__main__':
    uvicorn.run("app:app", host="127.0.0.1", port=5000, reload=True)
#    app.run(host='0.0.0.0',debug=True)








