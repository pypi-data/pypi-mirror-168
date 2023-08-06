from pydantic import BaseModel,StrictStr
from typing import List, Union,Any

class series_id(BaseModel):
    id: Union[List[StrictStr],StrictStr]





class catalog(BaseModel):
    series_id:Any=None
    series_title:Any=None
    seasonality:Any = None
    survey_name:Any=None
    survey_abbreviation:Any=None
    measure_data_type: Any=None
    area:Any=None
    area_type:Any=None
    industry:Any =None
    supersector:Any =None

class series_data(BaseModel):
    year:Any=None
    period:Any=None
    value:Any=None
    periodName:Any=None

class series_data_type(BaseModel):
    data_type:Any=None






