# Streamlit Incidents App

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://mush-difficulty-curve.streamlit.app/)

Streamlit app to retro-engineer Mush incident formula :

![Screen](https://cdn.discordapp.com/attachments/513701275305639947/1137117539042857030/Screenshot_2023-08-04_at_22-18-43_Streamlit.png)

# Launch locally

```bash
conda create -n fds_logs_analysis python=3.10 -y 
conda activate fds_logs_analysis 
pip install -r requirements.txt
streamlit run app.py
```

If you are on Linux / have `make` installed, you can also use the Makefile :

```bash
conda create -n fds_logs_analysis python=3.10 -y 
conda activate fds_logs_analysis
make install
make run
```