# Quiz Application

This is a Quiz Application built with Flask. It allows users to take quizzes and view corrections.

## Project Structure

The project has the following structure:

- `App/`: Main application package.
  - `__init__.py`: Initializes the Flask application.
  - `forms.py`: Contains WTForms form definitions.
  - `model.py`: Contains SQLAlchemy database models.
  - `route.py`: Contains routes for the application.
  - `static/`: Contains static files like CSS and JavaScript.
  - `templates/`: Contains Jinja2 templates.
  - `utils.py`: Contains utility functions.
- `import_quiz_data.py`: Script to import quiz data.
- `instance/`: Contains instance-specific configuration files.
- `myenv/`: Contains the Python virtual environment.
- `quiz_data.json`: Contains quiz data.
- `requirements.txt`: Contains Python dependencies for the project.
- `run.py`: Main entry point to run the application.

## Setup

1. Clone the repository.
2. Create a Python virtual environment and activate it.
3. Install the dependencies with `pip install -r requirements.txt`.
4. Run the application with `python run.py`.

## Usage

1. Register a new user.
2. Log in with the new user.
3. Take a quiz.
4. View corrections.

## Contributing

Contributions are welcome. Please submit a pull request.

## License

This project is licensed under the MIT License.