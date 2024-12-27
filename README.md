## Setup Environment - Anaconda 
conda create --name main-ds python=3.9
conda activate main-ds
pip freeze > requirements.txt
pip install -r requirements.txt

## Setup Environment - Shell/Terminal
mkdir submission
cd submissiom
pipenv install
pipenv shell
pip install -r requirements.txt

## Run streamlit app
streamlit run dashboard.py# project-ml
# e-commerce-analyst
