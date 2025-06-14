from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Dict, Optional
from bson import ObjectId
from datetime import datetime
from ..models.task import TaskCreate, TaskUpdate, TaskResponse, TaskStatus
from ..models.user import UserResponse
from ..database.connection import db
from ..routers.auth import get_current_user
from ..core.ai_agent import generate_task_description

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
    redirect_slashes=False
)
@router.get("/participants", response_model=Dict)
async def get_unique_participants(
    current_user: UserResponse = Depends(get_current_user)
):
    # Get unique participants
    participants = db.tasks.distinct("participants")
    unique_participants = list(set([p for p in participants if p]))
    
    # Get task counts
    total_tasks = db.tasks.count_documents({})
    completed_tasks = db.tasks.count_documents({"status": "closed"})
    frozen_tasks = db.tasks.count_documents({"status": "frozen"})
    
    return {
        "participants": unique_participants,
        "counts": {
            "total": total_tasks,
            "completed": completed_tasks,
            "frozen": frozen_tasks
        }
    }
@router.get("/search", response_model=List[TaskResponse])
async def search_tasks(
    title: Optional[str] = Query(None, description="Search by task title"),
    # status: Optional[TaskStatus] = Query(None, description="Filter by task status"),
    current_user: UserResponse = Depends(get_current_user)
):
    # Build query
    query = {"$or": []}
    if title:
        query["$or"].extend([
            {"title": {"$regex": title, "$options": "i"}},
            {"status": {"$regex": title, "$options": "i"}}
        ])

    
    # If no search parameters provided, return all tasks
    if not query["$or"]:
        query = {}
    
    # Execute search
    tasks = list(db.tasks.find(query))
    
    # Format response
    for task in tasks:
        task["id"] = str(task["_id"])
        del task["_id"]
        if not task.get("participants"):
            task["participants"] = []
    
    return tasks
@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task: TaskCreate,
    current_user: UserResponse = Depends(get_current_user)
):
    task_dict = task.model_dump()
    task_dict["created_at"] = datetime.utcnow()
    task_dict["created_by"] = current_user.id
    
    # Ensure participants is a list and not empty
    if not task_dict.get("participants"):
        task_dict["participants"] = []

    
    result = db.tasks.insert_one(task_dict)
    task_dict["id"] = str(result.inserted_id)
    
    # Verify the saved document
    saved_task = db.tasks.find_one({"_id": result.inserted_id})

    
    return task_dict

@router.get("/", response_model=Dict[str, List[TaskResponse]])
async def get_tasks(
    # current_user: UserResponse = Depends(get_current_user)
):
    tasks_by_column = {
        "todo": [],
        "inProgress": [],
        "closed": [],
        "frozen": []
    }

    all_tasks = list(db.tasks.find())

    for task in all_tasks:
        task["id"] = str(task["_id"])
        del task["_id"]
        
        # Ensure participants is a list
        if not task.get("participants"):
            task["participants"] = []

        column = task.get("status", "todo")
        if column in tasks_by_column:
            tasks_by_column[column].append(task)
    
    return tasks_by_column


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: str,
    current_user: UserResponse = Depends(get_current_user)
):
    if not ObjectId.is_valid(task_id):
        raise HTTPException(status_code=400, detail="Invalid task ID")
    
    task = db.tasks.find_one({"_id": ObjectId(task_id)})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task["id"] = str(task["_id"])
    del task["_id"]
    return task

@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: str,
    task_update: TaskUpdate,
    current_user: UserResponse = Depends(get_current_user)
):
    if not ObjectId.is_valid(task_id):
        raise HTTPException(status_code=400, detail="Invalid task ID")
    
    update_data = task_update.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No update data provided")
    
    result = db.tasks.update_one(
        {"_id": ObjectId(task_id)},
        {"$set": update_data}
    )
    
    # if result.modified_count == 0:
    #     raise HTTPException(status_code=404, detail="Task not found")
    
    updated_task = db.tasks.find_one({"_id": ObjectId(task_id)})
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
        
    updated_task["id"] = str(updated_task["_id"])
    del updated_task["_id"]
    return updated_task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: str,
    current_user: UserResponse = Depends(get_current_user)
):
    if not ObjectId.is_valid(task_id):
        raise HTTPException(status_code=400, detail="Invalid task ID")
    
    result = db.tasks.delete_one({"_id": ObjectId(task_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return None

@router.post("/generate-description", response_model=dict)
async def generate_description(
    brief: str = Query(..., description="Brief description of the task"),
    current_user: UserResponse = Depends(get_current_user)
):
    try:
        result = await generate_task_description(brief)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


 