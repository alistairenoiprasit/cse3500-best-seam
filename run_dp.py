from resizeable_image import ResizeableImage
def main():
    image = ResizeableImage('Generate_Images_Folder/10x10.png')
    seam = image.best_seam(True)
    print(seam)

if __name__ == "__main__":
    main()