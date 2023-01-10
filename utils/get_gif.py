import os
from PIL import Image

def get_gif_from_imgs(outfiles_path):
    """
    Fetches all the images in OUTPUT FILES and creates a .GIF out of them.
    Args:
        outfiles_path (str): path to the OUTPUT_FILES folder.
    Returns: .GIF file saved in the same directory
    """

    # Fetch .jpg images
    list_dir = os.listdir(outfiles_path)
    for f in list_dir[:]:  # NB: list_dir[:] makes a copy
        if not(f.endswith('.jpg')):
            list_dir.remove(f)

    img, *imgs = [Image.open(os.path.join(outfiles_path, f)) for f in list_dir]  # sorted(list_dir, key=lambda f: int(f.split('_')[1]))
    img.save(fp=os.path.join(outfiles_path, 'aa_frames_gif.gif'), format='GIF', append_images=imgs, 
             save_all=True, duration=200, loop=0)

if __name__ == "__main__":
    outfiles_path = "/Users/pedromartinez/Library/CloudStorage/OneDrive-BusinessmannAS/novo_vibration_vials/data/frames_cropped"
    get_gif_from_imgs(outfiles_path)