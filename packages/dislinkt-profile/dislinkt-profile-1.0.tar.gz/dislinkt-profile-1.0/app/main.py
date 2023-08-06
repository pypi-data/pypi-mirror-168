from datetime import datetime, date
from typing import Union
import uvicorn
from sqlalchemy.ext.declarative import declarative_base
from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, HTTPException
from fastapi import Request

import models
from database import local_session, engine
from dto import UserDTO
from models import User, Profile, Education
from routers import auth

from users import UserCreate, ProfileCreate, ProfileEdit, EducationCreate
from userform import UserCreateForm


# def get_db():
#     try:
#         db = SessionLocal()
#         yield db
#     finally:
#         db.close()


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_methods="*",
    allow_headers="*",
)

app.include_router(auth.router)
# app.include_router(route_users.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


# @app.post("/register")
# async def register(request: Request):
#     req = await request.json()
#     print(req)
#     user = User()
#     user.username = req['username']
#     user.email = req['email']
#     user.password = req['password']
#     user.ime = req['ime']
#     user.prezime = req['prezime']
#     user.telefon = req['telefon']
#     # user.datumRodjenja = datetime.date(req['datumRodjenja'])
#     date_time_str = req['datumRodjenja']
#     date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d')
#     user.datumRodjenja = datetime.date(date_time_obj)
#     user.pol = req['pol']
#     user.role = "reg_user"
#     local_session.add(user)
#     local_session.commit()
#
#     return {
#         "code": "success",
#         "message": "registration successful"
#     }


@app.post("/register")
async def register(request: UserCreate):
    userDict = request.dict()
    print(userDict)
    hasErrors = False
    errorList = ""
    for db_user in local_session.query(User).all():
        if db_user.email == request.email:
            hasErrors = True
            errorList += "User with this email already exists. "
        if db_user.username == request.username:
            hasErrors = True
            errorList += "This username is not available. "

    if hasErrors:
        return {
            "code": "exception",
            "message": errorList
        }

    user = User()
    user.username = request.username
    user.email = request.email
    password = request.password
    hashedpassword = auth.get_password_hash(password)
    user.password = hashedpassword
    user.ime = request.ime
    user.prezime = request.prezime
    user.telefon = request.telefon
    # user.datumRodjenja = datetime.date(req['datumRodjenja'])
    date_time_str = request.datumRodjenja
    date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d')
    user.datumRodjenja = datetime.date(date_time_obj)
    user.pol = request.pol
    user.role = "reg_user"
    local_session.add(user)
    local_session.commit()
    user_id = user.id
    print(user_id)

    return {
        "user_id": user_id,
        "code": "success",
        "message": "registration successful"
    }


@app.post("/profile")
async def register(request: ProfileCreate):
    profileDict = request.dict()
    print(profileDict)
    profile = Profile()
    profile.user_id = request.user_id
    profile.private = request.private
    profile.picture = ""
    profile.description = ""
    local_session.add(profile)
    local_session.commit()
    profile_id = profile.id
    print(profile_id)

    return {
        "profile_id": profile_id,
        "code": "success",
        "message": "profile successfuly created"
    }

@app.get("/profile/{id}")
async def get_profile(id):
    profile = local_session.query(Profile).get(id);
    return profile


@app.put("/profile/edit/{profile_id}")
async def edit_profile(profile_id: str, request: ProfileEdit):
    profileDict = request.dict()
    print(profileDict)

    local_session.query(Profile).filter_by(id=profile_id).update({"description": request.description})
    local_session.query(Profile).filter_by(id=profile_id).update({"private": request.private})

    local_session.commit()

    return {
        "code": "success",
        "message": "profile successfuly updated"
    }


@app.post("/profile/addEducation")
async def add_Education(request: EducationCreate):
    eduDict = request.dict()
    print(eduDict)
    education = Education()
    education.profile_id = request.profile_id
    education.school = request.school
    education.degree = request.degree

    start_date_str = request.start
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    education.start = datetime.date(start_date)

    end_date_str = request.end
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    education.end = datetime.date(end_date)

    local_session.add(education)
    local_session.commit()
    education_id = education.id
    print(education_id)

    return {
        "education_id": education_id,
        "code": "success",
        "message": "profile successfuly updated"
    }


@app.get("/profile/{profile_id}/education")
async def get_education(profile_id):
    education_list = []
    for education in local_session.query(Education).filter(Education.profile_id == profile_id):
        education_list.append(education)

    print(education_list)
    return education_list


@app.delete("/profile/education/{education_id}")
async def delete_education(education_id):
    local_session.query(Education).filter(Education.id == education_id).delete(synchronize_session="fetch")
    local_session.commit()
    return {
        "code": "success",
        "message": "successfuly deleted education"
    }


@app.put("/users/{user_id}")
async def edit_user(user_id: int, request: UserCreate):
    userDict = request.dict()
    print(userDict)

    oldUser = local_session.query(User).get(user_id)
    print(oldUser)

    hasErrors = False
    errorList = ""
    for db_user in local_session.query(User).all():
        if db_user.email == request.email and db_user.email != oldUser.email:
            hasErrors = True
            errorList += "User with this email already exists. "
        if db_user.username == request.username and db_user.username != oldUser.username:
            hasErrors = True
            errorList += "This username is not available. "

    if hasErrors:
        return {
            "code": "exception",
            "message": errorList
        }

    local_session.query(User).filter_by(id=user_id).update({"email": request.email,
                                                            "username": request.username,
                                                            "ime": request.ime,
                                                            "prezime": request.prezime,
                                                            "telefon": request.telefon,
                                                            "pol": request.pol})
    # local_session.query(User).filter_by(id=user_id).update({"username": request.username})
    # local_session.query(User).filter_by(id=user_id).update({"ime": request.ime})
    # local_session.query(User).filter_by(id=user_id).update({"prezime": request.prezime})
    # local_session.query(User).filter_by(id=user_id).update({"telefon": request.telefon})
    # local_session.query(User).filter_by(id=user_id).update({"pol": request.pol})
    local_session.commit()

    return {
        "code": "success",
        "message": "update successful"
    }


# @app.post("/register/")
# async def register(request: Request): #, db: Session = Depends(get_db)):
#     form = UserCreateForm(request)
#     await form.load_data()
#     if await form.is_valid():
#         user = UserCreate(
#             username=form.username, email=form.email, password=form.password
#         )
#         # try:
#         #     user = create_new_user(user=user, db=db)
#         #     return responses.RedirectResponse(
#         #         "/?msg=Successfully-Registered", status_code=status.HTTP_302_FOUND
#         #     )  # default is post request, to use get request added status code 302
#         # except IntegrityError:
#         #     form.__dict__.get("errors").append("Duplicate username or email")
#         #     return templates.TemplateResponse("users/register.html", form.__dict__)
#     return {
#         "code": "success",
#         "message": "registration successful"
#     }


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    models.Base.metadata.create_all(engine)
    uvicorn.run(app, port=8001, host="0.0.0.0")

