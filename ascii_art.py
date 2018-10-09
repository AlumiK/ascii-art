import argparse

from PIL import Image


def get_args():
    parser = argparse.ArgumentParser(
        description='create beautiful ascii arts',
        allow_abbrev=False
    )
    parser.add_argument(
        '-c',
        '--charset',
        type=str,
        default='$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,"^`\'. ',
        nargs='?',
        help='set the charset used in the output'
    )
    parser.add_argument(
        '-r',
        '--ratio',
        type=float,
        default=2.25,
        nargs='?',
        help='set image aspect ratio'
    )
    parser.add_argument(
        '-m',
        '--max-dim',
        type=int,
        default=96,
        nargs='?',
        help='set the max size of the output'
    )
    parser.add_argument(
        'infile',
        metavar='IMG',
        type=str,
        nargs=1,
        help='original image'
    )
    return parser.parse_args()


def get_grayscale_image(infile, max_dim, ratio):
    img = Image.open(infile)
    if img.size[0] > max_dim:
        t_width = max_dim
        t_height = int(img.size[1] * max_dim / img.size[0] / ratio)
    else:
        t_height = int(max_dim / ratio)
        t_width = int(img.size[0] * max_dim / img.size[1])
    return img.resize((t_width, t_height), Image.LANCZOS).convert('L')


def get_ascii_art(img, charset):
    pixels = list(img.getdata())
    step = 256 / len(charset)
    width, height = img.size
    for y in range(0, height):
        for x in range(0, width):
            index = int(pixels[x + y * width] / step)
            print(charset[index], end='')
        print()


if __name__ == '__main__':
    args = get_args()
    image = get_grayscale_image(args.infile[0], args.max_dim, args.ratio)
    get_ascii_art(image, args.charset)