# Movie Production Scheduler

This Flask application helps in scheduling actors for scenes in a movie production using OR-tools. It allows users to input actors, scenes, and constraints to generate an optimized schedule.

## Features

- **Input Form**: Users can specify the number of days available, maximum scenes per day, actors' names, and their daily salaries, as well as scenes with required actors.
- **OR-tools Integration**: Uses OR-tools' constraint programming to optimize the schedule based on specified constraints.
- **Output**: Provides a JSON response showing the scheduled days for each actor.

## Requirements

- Python 3.x
- Flask
- pandas
- numpy
- ortools

## Installation

1. Clone the repository:

   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the Flask application:

   ```bash
   python app.py
   ```

2. Open your web browser and go to `http://localhost:5000`.

3. Fill out the form with the required inputs:
   - Number of days available for shooting (`maxNumDays`).
   - Maximum scenes that can be shot in a day (`maxSceneperDay`).
   - Actors' names and their respective salaries per day.
   - Scenes' names and the actors required for each scene.

4. Submit the form to generate the optimized schedule.

## Files

- **app/routes.py**: Contains the Flask routes and the OR-tools integration for scheduling.
- **templates/index.html**: HTML template for the web interface.

## Example Data Generation

- `generateActorData(n)`: Generates `n` random actors with random salaries.
- `generateScenes(n, actors)`: Generates `n` random scenes with actors chosen from a given list.
- `convertActorsTodf(names, salaries)`: Converts actor names and salaries into a pandas DataFrame.
- `convertScenesTodf(names, actors)`: Converts scene names and required actors into a pandas DataFrame.

## OR-tools Solver Function

- `solverOrtools(actors, scenes, maxSceneperDay, maxNumDays)`: Implements the OR-tools CP model for scheduling actors to scenes under specified constraints.

## Notes

- This application assumes that the user inputs are valid and follow the expected format.
- Adjustments to the code or additional error handling may be necessary for deployment in production environments.

---

Feel free to customize this README with additional details or specific instructions based on your application's needs and deployment environment.
