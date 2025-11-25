import os
from PIL import Image

def compress_images(directory, max_width=1280, quality=80):
    """
    Compresses images in the given directory recursively.
    - Resizes images if width > max_width
    - Optimizes and reduces quality for JPEGs
    - Optimizes PNGs
    """
    
    # Supported extensions
    valid_extensions = {'.jpg', '.jpeg', '.png', '.webp'}
    
    count = 0
    saved_space = 0

    print(f"Starting compression in {directory}...")

    for root, dirs, files in os.walk(directory):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext not in valid_extensions:
                continue
            
            file_path = os.path.join(root, file)
            
            try:
                original_size = os.path.getsize(file_path)
                
                with Image.open(file_path) as img:
                    # Check if resize is needed
                    width, height = img.size
                    if width > max_width:
                        ratio = max_width / width
                        new_height = int(height * ratio)
                        img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
                        print(f"Resized {file}: {width}x{height} -> {max_width}x{new_height}")
                    
                    # Save logic
                    if ext in ['.jpg', '.jpeg']:
                        img.save(file_path, 'JPEG', optimize=True, quality=quality)
                    elif ext == '.png':
                        # For PNG, we can't set quality the same way, but optimize=True helps
                        # If it's RGBA, keep it. If RGB, maybe convert to JPG? 
                        # For safety, we just optimize PNGs.
                        img.save(file_path, 'PNG', optimize=True)
                    elif ext == '.webp':
                        img.save(file_path, 'WEBP', quality=quality)
                
                new_size = os.path.getsize(file_path)
                saved = original_size - new_size
                if saved > 0:
                    saved_space += saved
                    count += 1
                    print(f"Compressed {file}: {original_size/1024:.1f}KB -> {new_size/1024:.1f}KB")
                
            except Exception as e:
                print(f"Error processing {file_path}: {e}")

    print(f"\nFinished! Compressed {count} images.")
    print(f"Total space saved: {saved_space / (1024*1024):.2f} MB")

if __name__ == "__main__":
    # Target directory
    target_dir = os.path.join("assets", "vis_results")
    
    if os.path.exists(target_dir):
        compress_images(target_dir)
    else:
        print(f"Directory not found: {target_dir}")
