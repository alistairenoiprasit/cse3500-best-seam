from resizeable_image import ResizeableImage
import timeit

def main():
    filedir = 'Generate_Images_Folder/image_13x13.png'
    image = ResizeableImage(filedir)
    print(filedir)
    # Time DP method
    dp_time = timeit.timeit(lambda: image.best_seam(True), number=3)

    # Time naive method
    naive_time = timeit.timeit(lambda: image.best_seam(False), number=1)

    print(f"DP method: {dp_time:.6f} seconds for 3 runs")
    print(f"Average DP time: {dp_time / 3:.6f} seconds per run")
    print(f"Naive method: {naive_time / 1:.6f} seconds per run")


if __name__ == "__main__":
    main()