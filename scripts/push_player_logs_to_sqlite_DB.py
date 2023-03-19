import sqlite3
import pandas as pd

from utils import load_player_logs

if __name__ == '__main__':
    print('Loading player logs...')
    player_logs = load_player_logs()
    print('Done!')
    print('Opening connection to SQLite DB...')
    connection = sqlite3.connect('../data/mush.db')
    print('Done!')
    print('Pushing player logs to SQLite DB...')
    player_logs.to_sql('player_logs', connection, if_exists='replace', index=False)
    print('Done! End of script.')

    