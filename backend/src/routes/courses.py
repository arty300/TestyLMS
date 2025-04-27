from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from pymongo import MongoClient
from src.database import db
from src.models.course import Course, CourseCreate, HiddenSection
from src.routes.users import get_current_user, get_current_admin_user
from bson import ObjectId
from docx import Document
from gridfs import GridFS
from fastapi.responses import StreamingResponse
import io
import logging
import base64


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(),  # Вывод в консоль
        logging.FileHandler("fastapi.log")  # Сохранение в файл
    ]
)
logger = logging.getLogger(__name__)

router = APIRouter()
images_router = APIRouter()

async def get_db():
    return db

@router.post("", response_model=Course)
async def create_course(course: CourseCreate, db=Depends(get_db), current_user=Depends(get_current_admin_user)):
    course_dict = course.dict()
    result = db.courses.insert_one(course_dict)
    return {**course_dict, "id": str(result.inserted_id)}

@router.get("", response_model=list[Course])
async def get_courses(db=Depends(get_db), current_user=Depends(get_current_user), group: str = None):
    if current_user["role"] == "admin":
        query = {"allowedGroups": group} if group else {}
        courses = list(db.courses.find(query))
    else:
        user_groups = current_user.get("groups", [])
        query = {
            "$or": [
                {"allowedGroups": {"$in": user_groups}},
                {"allowedGroups": {"$size": 0}},
            ]
        }
        if group:
            query["$or"].append({"allowedGroups": group})
        courses = list(db.courses.find(query))
    return [{**course, "id": str(course["_id"])} for course in courses]

@router.get("/{course_id}", response_model=Course)
async def get_course(course_id: str, db=Depends(get_db), current_user=Depends(get_current_user)):
    try:
        course = db.courses.find_one({"_id": ObjectId(course_id)})
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        if current_user["role"] != "admin":
            user_groups = current_user.get("groups", [])
            if course.get("allowedGroups") and not any(g in user_groups for g in course["allowedGroups"]):
                raise HTTPException(status_code=403, detail="Access denied")
        
        # Проверяем, какие скрытые разделы разблокированы для пользователя
        unlocked_sections = current_user.get("unlockedSections", {}).get(course_id, [])
        course_hidden_sections = course.get("hiddenSections", [])
        modified_hidden_sections = []
        for idx, section in enumerate(course_hidden_sections):
            modified_hidden_sections.append({
                **section,
                "isUnlocked": idx in unlocked_sections or current_user["role"] == "admin"
            })
        
        return {**course, "id": str(course["_id"]), "hiddenSections": modified_hidden_sections}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid course ID")

@router.put("/{course_id}", response_model=Course)
async def update_course(course_id: str, course: CourseCreate, db=Depends(get_db), current_user=Depends(get_current_admin_user)):
    try:
        result = db.courses.update_one(
            {"_id": ObjectId(course_id)},
            {"$set": course.dict()}
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Course not found")
        return {**course.dict(), "id": course_id}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid course ID")

@router.delete("/{course_id}")
async def delete_course(course_id: str, db=Depends(get_db), current_user=Depends(get_current_admin_user)):
    try:
        result = db.courses.delete_one({"_id": ObjectId(course_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Course not found")
        return {"message": "Course deleted successfully"}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid course ID")

@router.post("/upload")
async def upload_course(file: UploadFile = File(...), current_user=Depends(get_current_admin_user)):
    try:
        doc = Document(file.file)
        markdown = ""
        fs = GridFS(db)
        
        # Создаём словарь для хранения изображений из relationships
        image_rels = {}
        for rel in doc.part.rels.values():
            if "image" in rel.target_ref:
                img_data = rel.target_part.blob
                img_filename = rel.target_ref.split('/')[-1]
                file_id = fs.put(img_data, filename=img_filename, content_type="image/jpeg")
                image_rels[rel.reltype + rel.rId] = (img_filename, str(file_id))

        # Проходим по всем элементам документа (параграфы)
        for para in doc.paragraphs:
            # Собираем содержимое параграфа
            para_content = ""
            has_content = False

            # Проходим по всем runs в параграфе
            for run in para.runs:
                run_text = run.text.strip()
                if run_text:
                    para_content += run_text
                    has_content = True

                # Проверяем, есть ли в run изображение
                for element in run._element:
                    if "drawing" in element.tag or "pict" in element.tag:
                        for blip in element.xpath(".//a:blip"):
                            rId = blip.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed")
                            if rId:
                                rel_key = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" + rId
                                if rel_key in image_rels:
                                    img_filename, file_id = image_rels[rel_key]
                                    # Добавляем текст параграфа, если он есть
                                    if para_content:
                                        markdown += para_content + "\n\n"
                                        para_content = ""  # Сбрасываем текст после добавления
                                    # Добавляем изображение
                                    markdown += f"![{img_filename}](/images/{file_id})\n\n"
                                    has_content = True

            # Добавляем оставшийся текст параграфа, если он есть
            if para_content:
                markdown += para_content + "\n\n"
                has_content = True

            # Добавляем дополнительный перенос строки между параграфами, если был контент
            if has_content:
                markdown += "\n"

        # Удаляем лишние переносы строк в конце
        markdown = markdown.strip()

        return {
            "title": file.filename.split(".")[0],
            "description": "Uploaded course",
            "content": markdown
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process file: {str(e)}")

@router.post("/upload-image")
async def upload_image(file: UploadFile = File(...), current_user=Depends(get_current_admin_user)):
    try:
        fs = GridFS(db)
        file_content = await file.read()
        file_id = fs.put(file_content, filename=file.filename, content_type=file.content_type)
        return {"url": f"/images/{str(file_id)}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload image: {str(e)}")

@images_router.get("/images/{file_id}")
async def get_image(file_id: str, database=Depends(get_db)):
    try:
        logger.debug(f"Using database: {database.name}")
        fs = GridFS(database)
        logger.debug(f"Attempting to retrieve file with ID: {file_id}")
        file_metadata = database.fs.files.find_one({"_id": ObjectId(file_id)})
        if not file_metadata:
            logger.error(f"File metadata not found for ID: {file_id}")
            raise HTTPException(status_code=404, detail="File metadata not found")
        logger.debug(f"File metadata found: {file_metadata}")
        chunk_count = database.fs.chunks.count_documents({"files_id": ObjectId(file_id)})
        logger.debug(f"Found {chunk_count} chunks for file ID: {file_id}")
        file = fs.get(ObjectId(file_id))
        logger.info(f"Successfully retrieved file: {file_id}, filename: {file.filename}, content_type: {file.content_type}, length: {file.length}")
        return StreamingResponse(
            io.BytesIO(file.read()),
            media_type=file.content_type,
            headers={"Content-Disposition": f"inline; filename={file.filename}"}
        )
    except Exception as e:
        logger.exception(f"Error retrieving file {file_id}: {str(e)}")
        raise HTTPException(status_code=404, detail=f"Image not found: {str(e)}")

# Добавляем маршрут для разблокировки скрытого раздела
@router.post("/{course_id}/unlock/{section_index}")
async def unlock_section(course_id: str, section_index: int, db=Depends(get_db), current_user=Depends(get_current_user)):
    try:
        if current_user["role"] == "admin":
            raise HTTPException(status_code=403, detail="Admins have all sections unlocked by default")
        
        course = db.courses.find_one({"_id": ObjectId(course_id)})
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        
        if section_index < 0 or section_index >= len(course.get("hiddenSections", [])):
            raise HTTPException(status_code=404, detail="Section not found")
        
        section = course["hiddenSections"][section_index]
        user_points = current_user.get("points", 0)
        if user_points < section["cost"]:
            raise HTTPException(status_code=400, detail="Not enough points to unlock this section")
        
        # Проверяем, не разблокирован ли уже раздел
        unlocked_sections = current_user.get("unlockedSections", {}).get(course_id, [])
        if section_index in unlocked_sections:
            raise HTTPException(status_code=400, detail="Section already unlocked")
        
        # Снимаем баллы и добавляем раздел в разблокированные
        db.users.update_one(
            {"_id": ObjectId(current_user["id"])},
            {
                "$inc": {"points": -section["cost"]},
                "$push": {f"unlockedSections.{course_id}": section_index}
            }
        )
        
        return {"message": "Section unlocked successfully", "remainingPoints": user_points - section["cost"]}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid course ID or section index")