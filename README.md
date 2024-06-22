# Movie Scheduling Application

This Flask-based web application optimizes the scheduling of actors for scenes in a movie production using OR-tools. It allows users to input constraints such as the number of days available, maximum scenes per day, actors' availability, and scene requirements to generate an optimized shooting schedule.

### Live Demo
[Link Here](https://moviescheduling.onrender.com/)
Note: Due to free plan, might take longer the first time.

### Math Perspective into it
[Notion page Here](https://inzaghi.notion.site/Optimize-Movie-Shooting-Schedule-Artifact-5-56a647d0cc004cbb888874d4a949f1d2)

## Features

- **Input Form**: Users can specify the number of days available (`maxNumDays`), maximum scenes that can be shot in a day (`maxSceneperDay`), actors' names, and their daily salaries, as well as scenes with required actors.
  
- **OR-tools Integration**: Utilizes OR-tools' constraint programming to compute an optimized schedule based on specified constraints and objectives.

- **Output**: Generates a JSON response displaying the scheduled days for each actor, providing an overview of the optimal shooting schedule.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/InMDev/MovieScheduling.git
   cd MovieScheduling
   ```

2. Install dependencies using pip:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the Flask application:

   ```bash
   python app.py
   ```

2. Open your web browser and navigate to `http://localhost:5000`.

3. Fill out the form with the required inputs:

   - **maxNumDays**: Number of days available for shooting.
   - **maxSceneperDay**: Maximum scenes that can be shot in a single day.
   - **Actors**: Enter the names and daily salaries of actors.
   - **Scenes**: Provide scene names and the actors required for each scene.

4. Submit the form to generate the optimized schedule.

## Files

- **app/routes.py**: Contains the Flask routes and the integration with OR-tools for scheduling.
- **templates/index.html**: HTML template for the web interface.

## Example Data Generation

- **Data Generation Functions**:
  - `generateActorData(n)`: Generates `n` random actors with random salaries.
  - `generateScenes(n, actors)`: Generates `n` random scenes with actors chosen from a given list.
  - `convertActorsTodf(names, salaries)`: Converts actor names and salaries into a pandas DataFrame.
  - `convertScenesTodf(names, actors)`: Converts scene names and required actors into a pandas DataFrame.

## OR-tools Solver Function

- **solverOrtools(actors, scenes, maxSceneperDay, maxNumDays)**: Implements the OR-tools CP model for scheduling actors to scenes under specified constraints.

## Notes

- This application assumes that the user inputs are valid and follow the expected format.
- Additional error handling and validation may be required for deployment in production environments.
- Customize the application as per your specific movie production scheduling needs.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Feel free to further customize this README to include additional details or instructions specific to your application or deployment environment.
