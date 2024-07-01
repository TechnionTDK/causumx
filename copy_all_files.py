import os
import glob
import pyperclip

FILES_TO_EXCLUDE = [
    'XInsight_result_so.json',
    'Temp.csv',
    'so_countries_col_new.csv',
    'environment.yml', 'environment_2.yml', 'Start_here.txt', '.idea', '.git',
    '.DS_Store', '.gitignore', 'fastmri-reproducible-benchmark-master', 'zip',
    'webloc', 'pdf', 'ipynb', 'doc', 'png', 'copy_all_files.py'
]

def copy_text_from_files(folder_path):
    # This will hold the combined contents of all files
    combined_text = ''

    # Define the file patterns to include
    file_patterns = ['**/*.py', '**/*.sh', '**/*.csv']

    for pattern in file_patterns:
        # Walk through all files matching the pattern in the folder, including subdirectories
        for filename in glob.glob(os.path.join(folder_path, pattern), recursive=True):
            # Check if it's a file
            if os.path.isfile(filename):
                filename_name = os.path.basename(filename)

                # Check for exclusion criteria
                if any(ext in filename_name for ext in FILES_TO_EXCLUDE):
                    continue
                if any(exclusion in filename for exclusion in
                       ['fastmri-reproducible-benchmark-master', 'wandb', '.idea', '.git', 'venv']):
                    continue
                if any(filename.endswith(ext) for ext in
                       ['.pdf', '.ipynb', '.doc', '.wandb', '.json', '.png', '.pth', '.DS_Store', '.gitignore', '.zip',
                        '.webloc']):
                    continue

                # Read the content of the file
                print(f'Copying content from {filename}')
                with open(filename, 'r', encoding='utf-8') as file:
                    content = file.read()
                    # Append the filename and content to combined_text
                    combined_text += f'{filename}\n' + '#' * 50 + '\n' + content + '\n\n'

    # Copy the combined text to clipboard
    pyperclip.copy(combined_text)

    # Optionally, print a message that the operation is complete
    print("Files' content copied to clipboard.")

    return combined_text


# Use the function with the path to the folder you want to copy text from
# You'll need to replace 'path_to_your_folder' with the actual path to your folder
# Example usage:
text = copy_text_from_files(os.getcwd())
# print(text)
