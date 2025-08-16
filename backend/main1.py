from fastapi import FastAPI, Depends, UploadFile, File, Form, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from auth import authenticate_user, create_access_token, get_current_user
from rag1 import ingest_file, get_answer
from fastapi import Body
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
from db import users_collection

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/register")
def register(data: dict = Body(...)):
    username = data["username"]
    password = pwd_context.hash(data["password"])
    
    if users_collection.find_one({"username": username}):
        raise HTTPException(status_code=400, detail="Username exists")
    
    new_user = {"username": username, "hashed_password": password}
    users_collection.insert_one(new_user)
    return {"msg": "registered"}

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/upload")
async def upload_doc(file: UploadFile = File(...), user=Depends(get_current_user)):
    print(f"Uploading file: {file.filename} for user: {user}")
    content = await file.read()
    filename = f"documents/{file.filename}"
    with open(filename, "wb") as f:
        f.write(content)
    ingest_file(filename, user_id=user["_id"])
    return {"status": "uploaded"}

@app.post("/query")
async def ask_question(query: str = Form(...), user=Depends(get_current_user)):
    answer = get_answer(query, user_id=user["_id"])
    return {"answer": answer}
