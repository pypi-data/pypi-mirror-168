from __future__ import annotations
from typing import Iterator, List
import requests
import json
from typing import Union,Any
from collections import namedtuple
import os
from .protocols import series_id,catalog,series_data,series_data_type
class __base_lookup:
    @property
    def series_info(self)-> Iterator:
        for data in self._lookup_table:
            series_id=data.get("Series ID", None)
            data_type=data.get("Data Type", None)
            industry=data.get("Industry", None)
            supersector=data.get("Supersector", None)
            yield series_id,data_type,industry,supersector
    @property
    def series_id_list(self) -> series_id:
        series=[id_val[0] for id_val in self.series_info]
        return series_id(id=series).id

    def get_seriesId_info(self,id:series_id) -> Union[bool,Any]:
        _id=series_id(id=id).id
        for id_,data_type,industry,supersector in self.series_info:
            if _id == id_:
                return data_type, industry,supersector
        return False

class _api_config:
    endpoint="https://api.bls.gov/publicAPI/v2/timeseries/data/"
    headers = {'Content-type': 'application/json'}
class series_object:
    def __new__(cls, id:series_id) ->series_object:
        obj=object.__new__(cls)
        obj._id=series_id(id=id).id

        obj._data=None
        obj._from_value=None
        obj._to_value=None
        obj.pagination=0
        return obj
    @property
    def _from(self):
        return self._from_value
    @_from.setter
    def _from(self,value:int):
        if not isinstance(value,int):
            raise TypeError("Must be type of int")
        self._from_value=value
        return self._from

    @property
    def _to(self):
        return self._to_value

    @_to.setter
    def _to(self, value: int):
        if not isinstance(value, int):
            raise TypeError("Must be type of int")
        self._to_value = value
        return self._to


    @property
    def get_data(self) ->Iterator:
        if self._from==None or self._to==None:
            raise TypeError("Please specify _from and _to")
        if self._from > self._to:
            raise TypeError(" _from cannot be greater than 2")
        if self._data != None:
            return self._data
        else:
            ### call the api
            if isinstance(self._id,List):
                self._id=self._id
            elif isinstance(self._id,str):
                self._id=[self._id]

            ### Limit 50

            for index_ in range(self.pagination*50,len(self._id),50):
                id_scrap=self._id[index_:index_+50]
                if len(self._id)>50:
                    self.pagination+=1

                # print(id_scrap)


                data_requests=json.dumps({"seriesid":id_scrap,"startyear":str(self._from),"endyear":str(self._to),"catalog":"true", "registrationkey":self.token})
                response=requests.post(_api_config.endpoint,data=data_requests,headers=_api_config.headers)
                self._data=json.loads(response.text)

                yield self._data

class _base:
    def __setattr__(self, attr, value) -> None:
        object.__setattr__(self, attr, value)
    # def __getattr__(self, item):
    #     raise TypeError( f"object not found {item}")
    def __getattribute__(self, item):
        return object.__getattribute__(self, item)


    @property
    def __getseriesobject__(self) -> series_object:
        for attri in self.__dict__:
            attri_val=self.__getattribute__(attri)
            if isinstance(attri_val,series_object):
                return attri_val
class __add_series(_base):
    def add_custom_series(self,series: series_id) ->object:
        obj=self._new()
        series=series_id(id=series).id
        obj.__setattr__("all_series", series_object(series))
        series_obj = obj.__getattribute__("all_series")
        series_obj.token = self.token
        return obj
    def add_all_series(self):
        ### This will have to return id with an array max 50
        obj=self._new()
        obj.__setattr__("all_series", series_object(self.series_id_list))
        series_obj = obj.__getattribute__("all_series")
        series_obj.token = self.token
        return obj
class labor_force(__base_lookup,__add_series):
    path=os.path.dirname(__file__)
    f=open(os.path.join(path,"labor_series.json"))
    _lookup_table=json.load(f)
    def __init__(self):
        self._from_value = None
        self._to_value = None
        self._token=None
        self.__token_list=None
    @property
    def token(self):
        return self._token
    @token.setter
    def token(self,value):
        if isinstance(value,List):
            self.__token_list=value

        self._token=value
        return self.token



    @classmethod
    def _new(cls):
        return cls()

    @property
    def _from(self):
        return self._from_value

    @_from.setter
    def _from(self, value: int):
        if not isinstance(value, int):
            raise TypeError("Must be type of int")
        self._from_value = value
        return self._from

    @property
    def _to(self):
        return self._to_value

    @_to.setter
    def _to(self, value: int):
        if not isinstance(value, int):
            raise TypeError("Must be type of int")
        self._to_value = value
        return self._to


    def __iter__(self) -> Iterator:
            series_node=self.__getseriesobject__
            series_node._from=self._from
            series_node._to=self._to
            for data in series_node.get_data:
                while True:
                    status=data["status"]
                    if status == "REQUEST_NOT_PROCESSED":
                        self.__token_list.pop(0)
                        if isinstance(self.__token_list,List):
                            if len(self.__token_list)==0:
                                yield ("API Limit Reach")
                        elif self.__token_list==None:
                            yield ("API Limit Reach")
                        else:
                            raise TypeError("Unknown value for Token_list")
                        self.token=self.__token_list
                        series_node.token=self.token
                    else:
                        break
                ### if not succes return to this loo


                for series in data["Results"]["series"]:

                    series_id=series["seriesID"]
                    data_type,industry,supersector=self.get_seriesId_info(series_id)

                    datas=series.get("data",{})
                    catalog_ = series.get("catalog",{})
                    catalog_["series_id"]=series_id
                    catalog_["industry"]=industry
                    catalog_["supersector"]=supersector
                    for data in datas:
                        yield(series_data(**data).dict(),catalog(**catalog_).dict(),series_data_type(data_type=data_type).dict())






