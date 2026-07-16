import os
import json
import time

base_raw_url = "https://raw.githubusercontent.com/s-n-t-ni-a-p/res-rk/main/"

folders = {
    "S": "Videos",
    "RK": "Radha Krishna",
    "O": "Others",
    "R": "Radha",
    "K": "Krishna"
}

# ⭐ NAYA LOGIC: Git history ke bajaye file ka actual modification time check karein
def get_file_age_in_days(filepath):
    try:
        if os.path.exists(filepath):
            # File modify hone ka time nikalta hai
            file_mtime = os.path.getmtime(filepath)
            return (time.time() - file_mtime) / (24 * 3600)
        return 999.0
    except Exception:
        return 999.0

wallpaper_list = []

for folder, category_name in folders.items():
    if os.path.exists(folder):
        files = os.listdir(folder)
        
        # Valid files filter
        valid_files = [
            f for f in files 
            if f.endswith(('.jpg', '.jpeg', '.png', '.mp4')) and not f.startswith('thumb_')
        ]
        
        def get_num(filename):
            try: return int(filename.split('.')[0])
            except ValueError: return 0
        
        valid_files.sort(key=get_num, reverse=True)
        
        for file in valid_files:
            file_url = f"{base_raw_url}{folder}/{file}"
            # Yahan naya logic call ho raha hai
            age_in_days = get_file_age_in_days(os.path.join(folder, file))
            is_new = "true" if age_in_days <= 10.0 else "false"
            
            wallpaper_list.append({
                "url": file_url,
                "category": category_name,
                "isNew": is_new
            })

with open("wallpapers.json", "w") as f:
    json.dump(wallpaper_list, f, indent=2)
