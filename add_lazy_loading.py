import re
import os

def add_lazy_loading(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find img tags without loading attribute
    # This is a simple heuristic. It looks for <img ... > and checks if loading= is missing.
    
    def replace_func(match):
        img_tag = match.group(0)
        if 'loading=' in img_tag:
            return img_tag
        
        # Insert loading="lazy" before the closing >
        # Handle /> for self-closing tags
        if '/>' in img_tag:
            return img_tag.replace('/>', ' loading="lazy" />')
        else:
            return img_tag.replace('>', ' loading="lazy">')

    # Pattern matches <img followed by anything until >
    # Non-greedy match
    pattern = r'<img[^>]+>'
    
    new_content = re.sub(pattern, replace_func, content)
    
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Successfully added loading=\"lazy\" to images in {file_path}")
    else:
        print("No changes needed or no images found.")

if __name__ == "__main__":
    add_lazy_loading("index.html")
