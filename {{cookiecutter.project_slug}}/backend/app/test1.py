from pydantic import BaseModel, Field


class TMDB_Category(BaseModel):
    id: str = Field(alias="_id")
    description: str = Field(alias="strCategoryDescription")


data = {
    "_id": "Beef",
    "strCategoryDescription": "Beef is ..."
}


obj = TMDB_Category.parse_obj(data)

# {'name': 'Beef', 'description': 'Beef is ...'}
print(obj.dict())