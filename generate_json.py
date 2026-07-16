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
        # %ai use kar rahe hain jo "Author Date" (ISO 8601 format) deti hai
        cmd = f'git log -1 --format=%ai -- "{filepath}"'
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, text=True)
        output = result.stdout.strip()
        
        if output:
            # GitHub ka format parse karne ke liye
            # Format: 2026-07-16 16:00:00 +0530
            date_str = output.split(' ')[0] + ' ' + output.split(' ')[1]
            commit_time = time.mktime(time.strptime(date_str, "%Y-%m-%d %H:%M:%S"))
            return (time.time() - commit_time) / (24 * 3600)
        else:
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
