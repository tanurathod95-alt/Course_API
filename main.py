from sqlmodel import SQLModel,Session,select
from sqlalchemy.exc import OperationalError
from database import engine,get_session
from fastapi import FastAPI,HTTPException,Depends
from pydantic import BaseModel
from model import Course

app=FastAPI()
@app.on_event("startup")
def on_startup():
    try:
        SQLModel.metadata.create_all(engine)
        print("database connected succesfully")
    except OperationalError as e:
        print("database connection faild",e)

@app.get("/")
def home():
    return {
        "message":"Hello World"
    }

#Create Course
@app.post("/course")
def create_course(course:Course,session:Session=Depends(get_session)):
    session.add(course)
    session.commit()
    session.refresh(course)
    return course

#get_all
@app.get("/course")
def get_all(session:Session=Depends(get_session)):

    return session.exec(select(Course)).all()

#filter with query parameter   
@app.get("/course/expensive")
def get_all(min_fees:int,session:Session=Depends(get_session)):
    course= session.exec(select(Course).where(Course.fees>=min_fees)).all()
    if not course:
        raise HTTPException(status_code=404,detail="not found")
    return course

#is_active add column
@app.get("/course/is_active")
def get_is_active(session:Session=Depends(get_session)):
    course= session.exec(select(Course).where(Course.is_active==True)).all()
    if not course:
        raise HTTPException(status_code=404,detail="not found")
    return course

#get specific one
@app.get("/course/{id}")
def get_single(id:int,session:Session=Depends(get_session)):
    course=session.get(Course,id)
    if not  course:
        raise HTTPException(status_code=404,detail="Course not found")
    return course

#update Course
@app.put("/course/{id}")
def update_course(id:int, updated:Course, session:Session=Depends(get_session)):
    course=session.get(Course,id)
    if not course:
        raise HTTPException(status_code=404,detail="Course not found")
    course.name=updated.name
    course.duration_week=updated.duration_week
    course.fees=updated.fees
    session.add(course)
    session.commit()
    session.refresh(course)
    return{
        "message":"upadated course successfully",
        "data": course
    }

#deleted course
@app.delete("/course/{id}")
def course_delete(id=int,session:Session=Depends(get_session)):
    course=session.get(Course,id)
    if not  course:
        raise HTTPException(status_code=404,detail="Course not found")
    session.delete(course)
    session.commit()
    return {
        "message":"Deleted course successfully"

    }
