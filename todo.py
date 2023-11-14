from taipy.gui import Gui, notify
from taipy import Config
import pandas as pd

tasks = pd.DataFrame({
    "Type":[],
    "Name":[],
    "Completed":[]
})

tasks["Completed"] = tasks["Completed"].astype("bool")

task_name=""
task_type=""

page = """
# TODO Schedular

Enter Task: <|{task_name}|input|>  
Type: <|{task_type}|selector|lov=Personal;Home;Work|dropdown|>  
<|Add Task|button|on_action=on_task_add|>

<|{tasks}|table|filter|editable|editable[Type]=False|on_edit=on_task_edit|on_delete=on_task_delete|style=style_completed|>
"""

def style_completed(_1, _2, values):
    if(values["Completed"]):
        return "strikeout"

def on_task_edit(state, var_name, payload):
    if(var_name == "tasks"):
        index = payload["index"]
        col = payload["col"]
        value = payload["user_value"]

        new_tasks = state.tasks.copy()
        new_tasks.loc[index, col] = value
        state.tasks = new_tasks
        notify(state, "I", "Task Updated.")   

def on_task_delete(state, var_name, payload):
    if(var_name == "tasks"):
        index = payload["index"]
        state.tasks = state.tasks.drop(index=index)
        notify(state, "E", "Task Deleted.")    

def on_task_add(state, var_name, payload):
    if(state.task_name == "" or state.task_type == ""):
        notify(state, "E", "Task Name or Task Type Not Set.")
        return False
    _task_type = state.task_type
    _task_name = state.task_name
    _isCompleted = False
    new_data = pd.DataFrame([[_task_type, _task_name, _isCompleted]], columns=state.tasks.columns)
    state.tasks = pd.concat([new_data, state.tasks], axis=0, ignore_index=True)
    notify(state, "S", "New Task Added Successfully.")

Gui(page, css_file="todo.css").run(use_reloader=True)