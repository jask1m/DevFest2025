from typing import List
from utils.models import Criteria

class CriteriaStorage:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            from utils.existing_criteria import NETWORK_CRITERIA
            self._criteria_list = NETWORK_CRITERIA
            self._initialized = True
    
    def get_criteria(self) -> List[Criteria]:
        return self._criteria_list
    
    def update_criteria(self, new_criteria: List[Criteria]):
        self._criteria_list = new_criteria
        
    def append_criteria(self, criteria: Criteria):
        self._criteria_list.append(criteria)