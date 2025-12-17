from pydantic import BaseModel
from typing import List, Optional

class Feature(BaseModel):
    name: str
    dtype: str # INT64, FLOAT, STRING

class FeatureView(BaseModel):
    name: str
    entity_name: str    
    view_sql: str        
    features: List[Feature]

    def to_dict(self):
        return self.dict()