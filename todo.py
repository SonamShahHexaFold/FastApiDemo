from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Define a model using Pydantic
class Todo(BaseModel):
    id: int
    title: str
    description: str
    completed: bool = False

# In-memory "database"
todos: List[Todo] = []

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Todo API!"}

@app.get("/todos", response_model=List[Todo])
def get_todos():
    return todos

@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@app.post("/todos", response_model=Todo, status_code=201)
def create_todo(todo: Todo):
    todos.append(todo)
    return todo

@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, updated_todo: Todo):
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            todos[index] = updated_todo
            return updated_todo
    raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int):
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            todos.pop(index)
            return
    raise HTTPException(status_code=404, detail="Todo not found")

