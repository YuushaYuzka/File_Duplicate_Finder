import os
from collections import defaultdict
import pandas as pd
import datetime

title = "🔍 Duplicate File Finder With Python"
subtitle = "By Filename"

# total width of the line
width = 55  

print("\n" + "-" * width)
print(title.center(width, "-"))
print(subtitle.center(width, "-"))
print("-" * width + "\n")


while True:
    # ask user for folder paths
    folders_input = input(
        r"Please enter folder absolute paths (e.g. C:\Program Files (x86)\Google): "
    ).strip()

    if folders_input.lower() == "exit":
        print("Exiting program. Goodbye 👋")
        break

    # split and clean input
    folders = []  # empty list to store valid folder inputs
    for f in folders_input.split(","):
        f = f.strip()
        if f:  # make sure it's not empty
            folders.append(f)

    if not folders:
        print("⚠️ No folder paths entered, please try again.\n")
        continue

    # ✅ validate that all folders exist
    valid_folders = []
    for folder in folders:
        if not os.path.isdir(folder):
            print(f"❌ Folder not found: {folder}")
        else:
            valid_folders.append(folder)

    if not valid_folders:
        print("⚠️ No valid folders found. Please re-enter correct paths.\n")
        continue

    # reset maps every loop
    file_map = defaultdict(list)
    duplicates = {}

    # walk through folders
    for folder in valid_folders:
        for root, _, files in os.walk(folder):
            for f in files:
                file_map[f].append(os.path.join(root, f))

    # find duplicates
    for f, paths in file_map.items():
        if len(paths) > 1:
            duplicates[f] = paths

    if not duplicates:
        print("✅ No duplicate files found.\n")
        break
    else:
        print("\n🗂️ Duplicate files found:")
        # for name, paths in duplicates.items():
        #     print(f"\n{name}:")
        #     for path in paths:
        #         print(f"  - {path}")
        for x in sorted(duplicates):
            print(f"{x} ("+str(len(duplicates[x]))+")")

    while True:
        print("")
        print("-" * 55)
        print("Choose Action :")
        print("1. Specific File Directory")
        print("2. Delete All Duplicates (keep latest modified)")
        print("3. Export Duplicates List to Excel")
        print("4. Delete Multiple Specific Files (comma separated)")
        print("-" * 55)
        
        while True:
            choice = input("\nEnter choice (1, 2, 3, or 4): ").strip()
            choices = ["1","2","3","4"]
            if choice not in choices:
                print("Invalid Option Please Choose (1, 2, 3, or 4)")
                continue
            else:
                break

        if choice == '1':
            while True:
                file_name = input("\nEnter the exact file name (e.g. example.txt): ").strip()
                if file_name in duplicates:
                    print(f"\nDuplicate paths for '{file_name}':")
                    for path in duplicates[file_name]:
                        try:
                            modified_time = os.path.getmtime(path)
                            formatted_time = datetime.datetime.fromtimestamp(modified_time).strftime("%Y-%m-%d %H:%M:%S")
                            print(f"  - {path}  (Modified: {formatted_time})")
                        except Exception as e:
                            print(f"  - {path}  ⚠️ Could not read timestamp ({e})")
                    break
                else:
                    print(f"\n⚠️ No duplicates found for '{file_name}'.")
                    continue


        elif choice == '2':
            while True:
                confirm = input("\nDo you want to delete duplicates (keep the latest one)? (y/n): ").lower()
                if confirm in ["y","n"]:    
                    if confirm == 'y':
                        for name, paths in duplicates.items():
                            try:
                                # Sort paths by modified time descending (latest first)
                                paths_sorted = sorted(paths, key=lambda p: os.path.getmtime(p), reverse=True)
                                latest = paths_sorted[0]  # keep the newest
                                to_delete = paths_sorted[1:]  # delete the rC:\Users\yuush\Downloads\Duplicate_finder_python\folder_a\sub_folder_a\cat.csvest

                                print(f"\nKeeping newest file: {latest}")
                                for path in to_delete:
                                    try:
                                        os.remove(path)
                                        print(f"🗑️ Deleted old duplicate: {path}")
                                    except Exception as e:
                                        print(f"⚠️ Could not delete {path}: {e}")
                            except Exception as e:
                                print(f"\n⚠️ Error processing '{name}': {e}")

                        print("\n✅ All older duplicates removed, latest files kept.")
                        break
                    else:
                        print("\nNo files deleted.\n")
                        break
                else:
                    print("Invalid Input Choose (y/n)")
                    continue

        elif choice == '3':
        # Convert duplicates dict into DataFrame with 3 columns
            export_data = []
            for name, paths in duplicates.items():
                for path in paths:
                    try:
                        modified_time = os.path.getmtime(path)
                        # Convert timestamp to readable datetime
                        modified_date = datetime.datetime.fromtimestamp(modified_time).strftime('%Y-%m-%d %H:%M:%S')
                    except Exception:
                        modified_date = "N/A"

                    export_data.append({
                        "File Name": name,
                        "Directory": path,
                        "Last Modified": modified_date
                    })

            # Create DataFrame
            df = pd.DataFrame(export_data)

            base_path = os.path.join(os.getcwd(), "duplicate_files.xlsx")
            export_path = base_path

            # ✅ check if file exists, append (1), (2), etc.
            counter = 1
            while os.path.exists(export_path):
                export_path = os.path.join(
                    os.getcwd(), f"duplicate_files({counter}).xlsx"
                )
                counter += 1

            try:
                df.to_excel(export_path, index=False)
                print(f"\n📂 Duplicate file list exported successfully to: {export_path}\n")
            except PermissionError:
                print(f"\n⚠️ Cannot write to '{export_path}'. Please close the Excel file if it's open and try again.\n")
            
            

        elif choice == '4':
            while True:
                
                files_input = input("\nEnter file names separated by commas (e.g. a.txt, b.txt, c.txt): ").strip()
                file_names = [f.strip() for f in files_input.split(",") if f.strip()]

                if not file_names:
                    print("\n⚠️ No file names entered. Please try again.\n")
                    continue

                files_found = False  # track if any matches exist

                for file_name in file_names:
                    if file_name in duplicates:
                        files_found = True
                        print(f"\nDuplicate paths for '{file_name}':")
                        for path in duplicates[file_name]:
                            try:
                                modified_time = os.path.getmtime(path)
                                formatted_time = datetime.datetime.fromtimestamp(modified_time).strftime('%Y-%m-%d %H:%M:%S')
                                print(f"  - {path}  (Modified: {formatted_time})")
                            except Exception as e:
                                print(f"  - {path}  ⚠️ Could not read timestamp ({e})")
                    else:
                        print(f"\n⚠️ No duplicates found for '{file_name}'.")
                    print("")  # spacing

                if not files_found:
                    continue
                else:
                    break

            while True:
                confirm = input("Would you like to delete duplicates (keep latest modified)? (y/n): ").lower()
                if confirm in ["y","n"]:    
                    while True:    
                        if confirm == 'y':
                            for file_name in file_names:
                                if file_name in duplicates:
                                    try:
                                        paths = duplicates[file_name]
                                        paths_sorted = sorted(paths, key=lambda p: os.path.getmtime(p), reverse=True)
                                        latest = paths_sorted[0]  # keep the newest
                                        to_delete = paths_sorted[1:]  # delete older ones

                                        print(f"\nKeeping newest file: {latest}")
                                        for path in to_delete:
                                            try:
                                                os.remove(path)
                                                print(f"🗑️ Deleted old duplicate: {path}")
                                            except Exception as e:
                                                print(f"⚠️ Could not delete {path}: {e}")
                                    except Exception as e:
                                        print(f"⚠️ Error processing '{file_name}': {e}")

                            print("\n✅ Selected duplicates cleaned up, latest versions kept.\n")
                        else:
                            print("\nNo files deleted.\n") 
                            break
                        break
                else:
                    print("invalid input choose (y/n)")
                    continue
                break
        print("")
        print("-" * 55)
        print("Choose Action :")
        print("1. Restart The Program ")
        print("2. Exit Program")
        print("-" * 55)
        while True:
            ending = input("\nEnter choice (1 or 2): ").strip()
            endings = ["1","2"]
            if ending not in endings:
                print("Invalid Option Please Choose (1 or 2)")
                continue
            else:
                break

        if ending == "1":
            continue
        break

    if ending == "2":
        input("Press any key to exit... ")       
        break
    
