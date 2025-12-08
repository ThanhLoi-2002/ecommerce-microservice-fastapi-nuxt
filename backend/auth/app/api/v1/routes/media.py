from typing import List
from fastapi import APIRouter, HTTPException, status, UploadFile, File
from app.common.middleware.response_wrapper import ResponseInterceptorRoute
from app.core.cloudinary_config import cloudinary
import cloudinary.uploader

router = APIRouter(route_class=ResponseInterceptorRoute)


@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    try:
        # Upload lên Cloudinary
        result = cloudinary.uploader.upload(
            file.file, folder="fastapi"  # Thư mục trên Cloudinary
        )
        return {
            "url": result["secure_url"],
            "public_id": result["public_id"],
            "format": result["format"],
            "resource_type": result["resource_type"],
        }

    except Exception as e:
        print(f"uploadFile: ${e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )

@router.post("/upload/multiple")
async def upload_multiple(files: List[UploadFile] = File(...)):
    results = []
    for file in files:
        upload = cloudinary.uploader.upload(file.file, folder="multi")
        results.append(upload["secure_url"])
    return results

@router.delete("/delete/{public_id:path}") # Sử dụng :path để hỗ trợ public_id có dấu /
async def delete_file(public_id: str):
    result = cloudinary.uploader.destroy(public_id)
    return result