from pydoc import doc
from typing import List, Optional, Sequence, Type, TypeVar, Union
from pydantic import BaseModel
from bson.objectid import ObjectId
import json
from fastapi.encoders import jsonable_encoder

PydanticModel = TypeVar("PydanticModel", bound=BaseModel)


# class JSONEncoder(json.JSONEncoder):
#     def default(self, o):
#         if isinstance(o, ObjectId):
#             return str(o)
#         return json.JSONEncoder.default(self, o)


def doc_result_to_model(
    mongodb_result,  doc_model: Type[PydanticModel]
) -> PydanticModel:
# TODO check if data need to be defined
    data = None
    if mongodb_result:
        data = doc_model(**mongodb_result)
    return data


def doc_results_to_model(
    mongodb_results: list, doc_model: Type[PydanticModel]
) -> List[PydanticModel]:
    items = []
    for doc in mongodb_results:
        data = doc_result_to_model(doc,doc_model)
        items.append(data)
    return items
