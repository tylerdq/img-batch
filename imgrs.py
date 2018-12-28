import click, os, errno, sys
from PIL import Image

cwd = os.getcwd()


def mkdir(directory):
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


@click.group()
def cli():
    pass


@cli.command()
@click.argument('unit')
@click.option('--width', '-w', default=-1,
              help='Specify resized image width (in UNIT).')
@click.option('--height', '-h', default=-1,
              help='Specify resized image height (in UNIT).')
@click.option('--quality', '-q', default=100,
              help='Specify resized image quality (0-100).')
def resize(unit, width, height, quality):
    """Utility to change image dimensions without cropping."""
    ### Check if unit is pixels or percent
    mkdir('resized')
    for file in os.listdir(cwd):
        if file.lower().endswith(('.jpg', '.png', '.jpeg')):
            with Image.open(file) as image:
                origWidth, origHeight = image.size
                if width != -1 and height != -1:
                    if unit == 'pixel':
                        newWidth = width
                        newHeight = height
                        if width == -1:
                            newHeight = height
                            newWidth = origWidth / origHeight * height
                        if height == -1:
                            newWidth = width
                            newHeight = origHeight / origWidth * width
                    elif unit == 'percent':
                        if width == -1:
                            width = 100
                        if height == -1:
                            height = 100
                        newWidth = origWidth * width / 100
                        newHeight = origHeight * height / 100
                    else:
                        click.echo('UNIT must be either "pixel" or "percent"')
                        sys.exit()
                else:
                    newWidth = origWidth
                    newHeight = origHeight
                if newWidth > origWidth or newHeight > origHeight:
                    input(file + ' is too small (output will be pixelated) <Enter> to continue.')
                ### Use TBD function to handle proportions of dimensions?
                image = image.resize((newWidth, newHeight), Image.ANTIALIAS)
                os.chdir('resized')
                image.save(file, 'JPEG', quality=quality)
                os.chdir(cwd)


@cli.command()
@click.argument('unit')
@click.option('--width', '-w', help='Specify resized image width (in UNIT).')
@click.option('--height', '-h', help='Specify resized image height (in UNIT).')
@click.option('--quality', '-q', default=100,
              help='Specify resized image quality (0-100).')
def crop(unit, width, height, quality):
    """Utility to change image dimensions by cropping."""
    mkdir('cropped')
    for file in os.listdir(cwd):
        if file.lower().endswith(('.jpg', '.png', '.jpeg')):
            with Image.open(file) as image:
                image = image.resize((width, height), Image.ANTIALIAS)
                os.chdir('resized')
                image.save(file, 'JPEG', quality=quality)
                os.chdir(cwd)

if __name__ == '__main__':
    cli()
