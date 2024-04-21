# app/routes.py
from flask import render_template, request, abort, render_template_string
from app import app
from ortools.sat.python import cp_model
import pandas as pd
import numpy as np

#Example Data
def generateActorData(n):
    df = pd.DataFrame()
    df['Actor Name'] = ['Actor ' + str(i) for i in range(n)]
    df['Salary per day'] = np.random.randint(1000, 20000, n) #Salary between $1000 and $20000
    return df

def generateScenes(n, actors):
    df = pd.DataFrame()
    df['Scene Name'] = ['Scene ' + str(i) for i in range(n)]
    df['Actors'] = [np.random.choice(actors, np.random.randint(1, len(actors)+1), replace=False) for i in range(n)]
    return df

def convertActorsTodf(names, salaries):
    # Create a DataFrame from the lists of names and salaries
    data = {'Actor Name': names, 'Salary per day': [int(salary) for salary in salaries]}
    df = pd.DataFrame(data)
    return df

def convertScenesTodf(names, actors):
    # Create a DataFrame from the lists of names and actors
    data = {'Scene Name': names, 'Actors': [actor.split(',') for actor in actors]}
    df = pd.DataFrame(data)
    return df

#User Input

def solverOrtools(actors, scenes, maxSceneperDay, maxNumDays=np.inf):

    model = cp_model.CpModel()
    solver = cp_model.CpSolver()

    #Variables

    x = {(i,d):model.NewBoolVar(f"Actor_{i}_Day_{d}") for i in actors.index for d in range(maxNumDays)}
    y = {(s,d):model.NewBoolVar(f"Scene_{s}_Day_{d}") for s in scenes.index for d in range(maxNumDays)}

    #Constraints

    # Max 4 scenes per day
    for d in range(maxNumDays):
        model.Add(sum(y[s,d] for s in scenes.index) <= maxSceneperDay)

    # Each scene must be recorded once
    for s in scenes.index:
        model.Add(sum(y[s,d] for d in range(maxNumDays)) == 1)

    # Actors for a scene must be present on day of shooting
    for s in range(len(scenes)):
        for d in range(maxNumDays):
            for a in range(len(actors)):
                if actors.loc[a, 'Actor Name'] in scenes.loc[s, 'Actors']:
                    model.AddImplication(y[s, d], x[a, d])

    # Objective
    model.Minimize(sum(x[a, d] * actors['Salary per day'][a] for a in range(len(actors)) for d in range(maxNumDays)))

    solver.Solve(model)

    if solver.StatusName() == 'OPTIMAL':
        print("Objective value:", solver.ObjectiveValue())
        
        #Create a dataframe to show the schedule
        schedule = pd.DataFrame(index=actors['Actor Name'], columns=range(maxNumDays))
        for a in range(len(actors)):
            for d in range(maxNumDays):
                schedule.loc[actors.loc[a, 'Actor Name'], d] = solver.Value(x[a, d])

        #Remove columns where no actor is working
        schedule = schedule.loc[:, (schedule != 0).any(axis=0)]
        
        #Replace the column index with counting from 1
        schedule.columns = range(1, schedule.shape[1]+1)

        return schedule

    if solver.StatusName() == 'INFEASIBLE':
        print("No solution found")
        print("Please add more days or reduce the number of scenes")

    return None

@app.route('/')
def index():
    try:
        with open('templates/index.html', 'r') as f:
            template_content = f.read()
        return template_content
    except FileNotFoundError:
        abort(404)

@app.route('/submit', methods=['POST'])
def submit():
    maxNumDays = int(request.form['maxNumDays'])
    maxSceneperDay = int(request.form['maxSceneperDay'])
    
    # Retrieve actor and scene data from form fields
    actorNames = request.form.getlist('actorName[]')
    actorSalaries = request.form.getlist('actorSalary[]')
    sceneNames = request.form.getlist('sceneName[]')
    sceneActors = request.form.getlist('sceneActors[]')
    
    # Convert form data to DataFrames
    actors = convertActorsTodf(actorNames, actorSalaries)
    scenes = convertScenesTodf(sceneNames, sceneActors)
    
    print("maxNumDays:", maxNumDays)
    print("maxSceneperDay:", maxSceneperDay)
    print("Actors:")
    print(actors)
    print("Scenes:")
    print(scenes)

    schedule = solverOrtools(actors, scenes, maxSceneperDay, maxNumDays)

    if schedule is None:
        return "No feasible schedule found. Please adjust your inputs."

    return render_template_string(render_schedule_table(schedule))

def render_schedule_table(schedule_df):
    table_html = '<div class="table-container">'
    table_html += '<table class="table is-bordered is-hoverable is-fullwidth">'
    
    # Table Head
    table_html += '<thead><tr><th>Actor</th>'
    for col in schedule_df.columns:
        table_html += f'<th>Day {col}</th>'
    table_html += '</tr></thead>'
    
    # Table Body
    table_html += '<tbody>'
    for index, row in schedule_df.iterrows():
        table_html += f'<tr><td>{index}</td>'
        for val in row:
            cell_class = 'has-background-success' if val == 1 else 'has-background-danger'
            table_html += f'<td class="{cell_class}">{val}</td>'
        table_html += '</tr>'
    table_html += '</tbody>'
    
    table_html += '</table>'
    table_html += '</div>'  # Close table-container div

    return table_html

