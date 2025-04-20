import os
import shutil
import tempfile
import base64

from fastapi import UploadFile, File, HTTPException, APIRouter, Body
from fastapi.responses import JSONResponse, HTMLResponse

from GestureRecognition import GestureRecognizer

router = APIRouter()


@router.post("/recognize-gesture/")
async def recognize_gesture(file: UploadFile = File(...)):
    """
    上传图片进行手势识别
    """
    # 创建临时文件保存上传的图像
    temp_dir = tempfile.mkdtemp()
    temp_file_path = os.path.join(temp_dir, file.filename)

    try:
        # 保存上传的文件
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 初始化手势识别器
        recognizer = GestureRecognizer()

        # 调用run_on_image方法，设置no_display=True
        result = recognizer.run_on_image(temp_file_path, no_display=True)

        return JSONResponse(content={"gesture": result})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理失败: {str(e)}")

    finally:
        # 清理临时文件
        shutil.rmtree(temp_dir)


@router.post("/process-camera-gesture/")
async def process_camera_gesture(data: dict = Body(...)):
    """
    处理从前端摄像头捕获的图像数据，并进行手势识别
    """
    try:
        # 从请求体中获取Base64编码的图像
        image_data = data.get("image")
        if not image_data:
            raise HTTPException(status_code=400, detail="未提供图像数据")
        
        # 移除Base64前缀（如果有）
        if "base64," in image_data:
            image_data = image_data.split("base64,")[1]
        
        # 创建临时目录和文件
        temp_dir = tempfile.mkdtemp()
        temp_file_path = os.path.join(temp_dir, "camera_capture.jpg")
        
        # 解码Base64数据并保存为图像文件
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(base64.b64decode(image_data))
        
        # 初始化手势识别器并处理图像
        try:
            recognizer = GestureRecognizer()
            result = recognizer.run_on_image(temp_file_path, no_display=True)
            return JSONResponse(content={"gesture": result})
        except Exception as e:
            print(f"处理图像时出错: {str(e)}")
            return JSONResponse(content={"gesture": "错误", "error": str(e)})
    
    except Exception as e:
        print(f"处理失败: {str(e)}")
        return JSONResponse(content={"gesture": "错误", "error": str(e)})
    
    finally:
        # 清理临时文件
        if "temp_dir" in locals():
            shutil.rmtree(temp_dir)

