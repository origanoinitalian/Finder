import os


def list_files_and_contents(root_dir, output_file):
    # Define extensions and files to exclude
    excluded_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.txt', '.log', '.git', '.idea','json','.gitignore', '.csv')
    excluded_files = {'get_code.py'}

    # Directories to exclude (e.g., venv, .idea for PyCharm settings)
    excluded_dirs = {'.venv', '.idea', '.git', '.pytest_cache', '.processors'}

    with open(output_file, 'w', encoding='utf-8') as outfile:
        for dirpath, dirnames, filenames in os.walk(root_dir):
            # Exclude specified directories
            dirnames[:] = [d for d in dirnames if d not in excluded_dirs]

            for filename in filenames:
                # Skip files with excluded extensions or specific names
                if filename.lower().endswith(excluded_extensions) or filename in excluded_files:
                    continue

                file_path = os.path.join(dirpath, filename)
                # Get the relative file path
                relative_path = os.path.relpath(file_path, root_dir)
                outfile.write(f'***{relative_path}\n')

                try:
                    with open(file_path, 'r', encoding='utf-8') as infile:
                        content = infile.read()
                    outfile.write(content + '\n')
                except Exception as e:
                    outfile.write(f'Could not read file: {e}\n')
                    continue


if __name__ == '__main__':
    root_directory = '/Users/alismac/Desktop/University/master/Data Mining and applications/heartbeat/Finder'
    output_filename = 'mainout.txt'
    list_files_and_contents(root_directory, output_filename)