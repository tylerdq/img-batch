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
@click.option('--quality', '-q', default=90,
              help='Specify resized image quality (0-100).')
def pixel(unit, width, height, quality):
    """Utility to change image dimensions without cropping."""
    mkdir('resized')
    for file in os.listdir(cwd):
        if file.lower().endswith(('.jpg', '.png', '.jpeg')):
            with Image.open(file) as image:
                origWidth, origHeight = image.size
                # if width != -1 and height != -1:
                if width > 0:  # FOR DEBUGGING. REMOVE.
                    if unit == 'pixel':
                        newWidth = width
                        newHeight = height
                        if width == -1:
                            newHeight = height
                            newWidth = origWidth / origHeight * height
                        if height == -1:
                            newWidth = width
                            newHeight = origHeight / origWidth * width
                else:
                    newWidth = origWidth
                    newHeight = origHeight
                if newWidth > origWidth or newHeight > origHeight:
                    input(file + ' is too small (output will be pixelated) <Enter> to continue.')
                ### Use TBD function to handle proportions of dimensions?
                image = image.resize((int(newWidth), int(newHeight)), Image.ANTIALIAS)
                os.chdir('resized')
                image.save(file, 'JPEG', quality=quality)
                os.chdir(cwd)


@cli.command()
@click.argument('percentage')
@click.option('--quality', '-q', default=90,
              help='Specify resized image quality (1-99).')
def percent(percentage, quality):
    """Utility to resize image to be a percentage of original size."""
    try:
        percentage = int(percentage)
    except ValueError:
        click.echo('PERCENTAGE must be an integer greater than 0.')
        sys.exit()
    if percentage == 0:
        click.echo('PERCENTAGE must be an integer greater than 0.')
        sys.exit()
    if percentage >= 100:
        while True:
            answer = input('Percentage >99. Dimensions will be unchanged (if 100) or image pixelated (if >100).\nContinue? (y/n): ')
            if answer == 'y':
                break
            elif answer == 'n':
                click.echo('Exited with no conversion.')
                sys.exit()

    mkdir('resized')
    for file in os.listdir(cwd):
        if file.lower().endswith(('.jpg', '.png', '.jpeg')):
            with Image.open(file) as image:
                origWidth, origHeight = image.size
                newWidth = origWidth * percentage / 100
                newHeight = origHeight * percentage / 100
                image = image.resize((int(newWidth), int(newHeight)), Image.ANTIALIAS)
                os.chdir('resized')
                image.save(file, 'JPEG', quality=quality)
                os.chdir(cwd)

if __name__ == '__main__':
    cli()
