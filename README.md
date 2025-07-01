# sp_constraints
Design demo of supply planning constraints.

# install venv
sudo apt install python3.12-venv
python3 -m venv .venv

# activate the python virtual environment

sgromme@DESKTOP-397HU7D:~/source/sp_constraints$ source .venv/bin/activate
(.venv) sgromme@DESKTOP-397HU7D:~/source/sp_constraints$ 

# Start Jupyter without a password (Use only on a secure, local machine, as it disables security)
jupyter notebook --NotebookApp.token='' --NotebookApp.password=''


# Constraints How, When and Why?

1. The contraints need to be compatable with Python pulp and need to run in a distributed heuristic planner.


# Streamlit
streamlit run ./source/supply_constraints_dashboard.py