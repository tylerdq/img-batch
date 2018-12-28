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
@click.argument('pixels', type=int)
@click.option('--quality', '-q', default=90, type=int,
              help='Specify resized image quality (0-100).')
def width(pixels, quality):
    """\b
    Resize image(s) proportionally, given desired width.
    Requires PIXELS as an integer greater than 0."""
    if pixels == 0:
        click.echo('PIXELS must be an integer greater than 0.')
        sys.exit()
    dirname = 'w' + str(pixels) + 'q' + str(quality)
    mkdir(dirname)
    for file in os.listdir(cwd):
        if file.lower().endswith(('.jpg', '.png', '.jpeg')):
            with Image.open(file) as image:
                origWidth, origHeight = image.size
                newWidth = pixels
                newHeight = origHeight / origWidth * pixels
                image = image.resize((int(newWidth), int(newHeight)),
                                     Image.ANTIALIAS)
                os.chdir(dirname)
                image.save(file, 'JPEG', quality=quality)
                os.chdir(cwd)


@cli.command()
@click.argument('pixels', type=int)
@click.option('--quality', '-q', default=90, type=int,
              help='Specify resized image quality (0-100).')
def height(pixels, quality):
    """\b
    Resize image(s) proportionally, given desired height.
    Requires PIXELS as an integer greater than 0."""
    if pixels == 0:
        click.echo('PIXELS must be an integer greater than 0.')
        sys.exit()
    dirname = 'h' + str(pixels) + 'q' + str(quality)
    mkdir(dirname)
    for file in os.listdir(cwd):
        if file.lower().endswith(('.jpg', '.png', '.jpeg')):
            with Image.open(file) as image:
                origWidth, origHeight = image.size
                newHeight = pixels
                newWidth = origWidth / origHeight * pixels
                image = image.resize((int(newWidth), int(newHeight)),
                                     Image.ANTIALIAS)
                os.chdir(dirname)
                image.save(file, 'JPEG', quality=quality)
                os.chdir(cwd)


@cli.command()
@click.argument('percentage', type=int)
@click.option('--quality', '-q', default=90, type=int,
              help='Specify resized image quality (1-99).')
def percent(percentage, quality):
    """\b
    Resize image(s) to be a proportion of their original size.
    Requires PERCENTAGE as an integer greater than 0."""
    if percentage == 0:
        click.echo('PERCENTAGE must be an integer greater than 0.')
        sys.exit()
    dirname = str(percentage) + 'pq' + str(quality)
    mkdir(dirname)
    for file in os.listdir(cwd):
        if file.lower().endswith(('.jpg', '.png', '.jpeg')):
            with Image.open(file) as image:
                origWidth, origHeight = image.size
                newWidth = origWidth * percentage / 100
                newHeight = origHeight * percentage / 100
                image = image.resize((int(newWidth), int(newHeight)),
                                     Image.ANTIALIAS)
                os.chdir(dirname)
                image.save(file, 'JPEG', quality=quality)
                os.chdir(cwd)

if __name__ == '__main__':
    cli()
