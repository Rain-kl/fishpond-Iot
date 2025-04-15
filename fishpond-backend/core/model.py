import json

from pydantic import BaseModel as PydanticBaseModel


class BaseModel(PydanticBaseModel):
    def json_str(self):
        return json.dumps(self.model_dump(), ensure_ascii=False)


class ZXDataModel(BaseModel):
    TYPE: str = ""
    PN: str = ""
    A0: str = ""
    A1: str = ""
    A2: str = ""
    A3: str = ""
    A4: str = ""
    A5: str = ""
    A6: str = ""
    A7: str = ""
    D1: str = ""
    updated: str = ""  # 修正了类型为str


class ZXResponseModel(BaseModel):
    method: str
    addr: str
    data: ZXDataModel
