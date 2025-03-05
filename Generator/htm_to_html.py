import os

def rename_htm_to_html(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.htm'):
                old_path = os.path.join(root, file)
                new_path = os.path.join(root, file[:-4] + '.html')
                os.rename(old_path, new_path)
                print(f'Renamed: {old_path} -> {new_path}')

if __name__ == '__main__':
    base_dir = 'd:/COC不全书/COC7thChm'
    rename_htm_to_html(base_dir)
