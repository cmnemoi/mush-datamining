# Data

- raw_logs.zip : raw logs from 1710 "lambda" Mush ships in ZIP format
  - The archive architecture is the following:

```yaml
- 1 # Mush ship id
  - Jin_Su.txt # Character logs (contains only character logs, not global logs like tremor or electric shock logs)
  - Frieda.txt
  - ...
  - NERON.txt # NERON announcements
- 2
- 3
- ...
- 1710
```
- player_logs.csv : player logs extracted from the `raw_logs.zip` 1710 Mush ships and merged in a single CSV file
- player_logs.zip : the `player_logs.csv` file in ZIP format
- NERON_annoucements.csv : NERON announcements extracted from the `raw_logs.zip` 1710 Mush ships and merged in a single CSV file
- blaster_twinpedia.csv : Answers from a Twinpedia survey about blaster damage
- couteau_twinpedia.csv : Answers from a Twinpedia survey about knife damage
- mush.db : A SQLite database containing the `player_logs` table for online usage



