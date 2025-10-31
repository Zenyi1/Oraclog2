from fastapi import APIRouter, HTTPException
from ..models import Rule
from ..storage.storage import rules_storage

router = APIRouter()

@router.post("/")
async def create_rule(rule: Rule):
    try:
        rule.id = len(rules_storage) + 1
        rules_storage.append(rule.dict())
        return rule
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating rule: {e}")

@router.get("/")
async def get_rules():
    try:
        return {"rules": rules_storage}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving rules: {e}")

@router.delete("/{rule_id}")
async def delete_rule(rule_id: int):
    try:
        for i, rule in enumerate(rules_storage):
            if rule["id"] == rule_id:
                rules_storage.pop(i)
                return {"message": "Rule deleted successfully"}
        raise HTTPException(status_code=404, detail="Rule not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting rule: {e}")