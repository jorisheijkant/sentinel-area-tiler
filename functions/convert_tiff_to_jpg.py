from PIL import Image

def convert_tiff_to_jpg(tiff_path: str, jpg_path: str, size: tuple[int, int] = (1000, 1000)):
    with Image.open(tiff_path) as img:
        img.resize(size, Image.LANCZOS).convert("RGB").save(jpg_path, "JPEG", quality=90)
