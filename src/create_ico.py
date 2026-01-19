import os
from PIL import Image

def create_ico():
    try:
        # Assuming this script is in src/
        base_dir = os.path.dirname(os.path.abspath(__file__))
        assets_dir = os.path.join(base_dir, 'assets', 'icons')
        png_path = os.path.join(assets_dir, 'pdf_to_excel.png')
        ico_path = os.path.join(assets_dir, 'pdf_to_excel.ico')
        
        if not os.path.exists(png_path):
            print(f"Warning: PNG icon not found at {png_path}")
            return
            
        # Always recreate to ensure it's correct
        print("Creating ICO file from PNG...")
        img = Image.open(png_path)
        # Save as ICO (containing 256x256, 128x128, 64x64, 48x48, 32x32, 16x16)
        img.save(ico_path, format='ICO', sizes=[(256,256), (128,128), (64,64), (48,48), (32,32), (16,16)])
        print(f"ICO created at {ico_path}")

    except Exception as e:
        print(f"Error creating icon: {e}")

if __name__ == "__main__":
    create_ico()
