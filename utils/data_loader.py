# ========================================
# utils/data_loader.py
# ========================================

import os
from glob import glob
import pandas as pd

def load_subtitles_dataset(dataset_path):
    subtitles_paths = glob(os.path.join(dataset_path, '*.ass'))

    print(f"Found subtitle files: {subtitles_paths}")

    scripts = []
    episode_num = []

    for path in subtitles_paths:
        if not os.path.isfile(path):
            print(f"Skipping non-file path: {path}")
            continue

        with open(path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            lines = lines[27:]
            lines = [",".join(line.split(',')[9:]) for line in lines]

        lines = [line.replace('\\N', ' ') for line in lines]
        script = " ".join(lines)

        try:
            episode = int(path.split('-')[-1].split('.')[0].strip())
        except ValueError:
            episode = -1

        scripts.append(script)
        episode_num.append(episode)

    df = pd.DataFrame({"episode": episode_num, "script": scripts})
    return df
