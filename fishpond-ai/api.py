from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
import uvicorn
import tempfile
from GestureRecognition import GestureRecognizer

app = FastAPI(title="手势识别API")

# 添加CORS中间件，允许前端跨域调用
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，生产环境中应该限制为你的前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/recognize-gesture/")
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

@app.get("/")
async def root():
    return {"message": "手势识别API服务正在运行，请使用 /recognize-gesture/ 端点上传图片"}

if __name__ == "__main__":
    uvicorn.run(app, port=8000) 