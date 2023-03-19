mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"icdk5b4zf@relay.firefox.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml