# Vanna.AI Streamlit App
<img width="1392" alt="Screenshot 2023-06-23 at 3 49 45 PM" src="./assets/vanna_demo.gif">

## Installation

This project uses Poetry, so the first thing is to install it. 

```bash
pip install poetry
```

Poetry allows to

1. Install and manage the dependencies of the project
2. Create a clean virtual environment that is fully isolated from your current Python environment


Packages are listed in the `pyproject.toml` file. 

To install them, simply run:

```bash
poetry install --with dev
```

## Usage

If you're running the app locally, please add a `.env` file at the root of the project with your crendentials:

```bash
VANNA_API_KEY=...
GCP_PROJECT_ID=...
```

To create a Vanna API key, please refer to this [link](https://vanna.ai/).

Then run the app with this command:

```bash
poetry run streamlit run app.py
```

## License
[MIT](https://choosealicense.com/licenses/mit/)
