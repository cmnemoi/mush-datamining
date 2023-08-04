install: setup-env-variables
	pip install -r requirements.txt

setup-env-variables:
	cp .streamlit/secrets.toml.dev .streamlit/secrets.toml

run:
	streamlit run incidents/app.py