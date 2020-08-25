# streamlit-template

## Python Dev Tools Setup
Change into `backend` directory.  
Run `pipenv install --dev` to install the env.  
Run `pipenv shell`.  
Run `pre-commit install` to initialize the git hooks.  
Run `pre-commit run --all-files` if there are file that were committed before adding the git hooks. 
Run `pytest --cov-config=.coveragerc --cov=app/package` to run tests.  
Note: Currently, `pipenv_to_requirements` must be run manually to sync `requirements.txt` and `requirements-dev.txt`.  