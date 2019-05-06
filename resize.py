import click, os, errno, sys, io
from glob import glob
from PIL import Image

cwd = os.getcwd()
oldSizes = []
newSizes = []

def mkdir(directory):
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def prep(value, dry, dirpre, quality):
    if value == 0:
        click.echo('Please use an integer greater than 0.')
        sys.exit()
    elif not dry:
        global dirname
        dirname = dirpre + str(value) + 'q' + str(quality)
        mkdir(dirname)


def globber():
    global images
    images = glob('*.jpg')
    images.extend(glob('.*jpeg'))
    images.extend(glob('.*png'))


def report(index, sizes):
    print(str(index) + ' images totaling ' + '~' + str(round(sum(sizes)/1000)) + 'kb')


@click.group()
def cli():
    pass


@cli.command()
@click.argument('side')
@click.argument('value', type=int)
@click.option('--quality', '-q', default=75, type=click.IntRange(1, 95,
              clamp=True), help='Specify resized image quality (1-95).')
@click.option('--dry', '-d', is_flag=True, help=
              'Do a dry run (recommended to do first).')
@click.option('--verbose', '-v', is_flag=True, help=
              'Verbose output with results of each image conversion.')
def pixel(side, value, quality, dry, verbose):
    """\b
    Resize image(s) proportionally, given desired side length in pixels.
    Requires SIDE ("width" or "height").
    Requires VALUE (pixels) as an integer greater than 0."""
    dirpre = side[0]
    prep(value, dry, dirpre, quality)
    globber()
    for index, file in enumerate(images, start=1):
        with Image.open(file) as im:
            output = io.BytesIO()
            im.save(output, 'JPEG')
            oldSize = int(len(output.getvalue()))
            output.close()
            oldSizes.append(oldSize)
            if side == 'width':
                newDim = int(round(im.height / im.width * value))
                image = im.resize((int(value), int(newDim)),
                                 Image.ANTIALIAS)
            elif side == 'height':
                newDim = int(round(im.width / im.height * value))
                image = im.resize((int(newDim), int(value)),
                                 Image.ANTIALIAS)
            else:
                click.echo('Please specify side as "width" or "height".')
                sys.exit()
            output = io.BytesIO()
            image.save(output, 'JPEG', quality=quality)
            newSize = int(len(output.getvalue()))
            output.close()
            newSizes.append(newSize)
            if not dry:
                os.chdir(dirname)
                image.save(file, 'JPEG', quality=quality)
                os.chdir(cwd)
            if verbose:
                print(file + ' - Original:' + str(im.width) + 'x' + str(im.height) + '=~' + str(round(oldSize/1000)) + 'kb' + '; Resized:' + str(image.width) + 'x' + str(image.height) + '=~' + str(round(newSize/1000)) + 'kb')
    print(str(index) + ' total images (~' + str(round(sum(oldSizes)/1000)) + 'kb -> ~' + str(round(sum(newSizes)/1000)) + 'kb)')


@cli.command()
@click.argument('value', type=int)
@click.option('--quality', '-q', default=75, type=click.IntRange(1, 95,
              clamp=True), help='Specify resized image quality (1-95).')
@click.option('--dry', '-d', is_flag=True, help='Do a dry run (recommended to do first).')
def width(value, quality, dry):
    """\b
    Resize image(s) proportionally, given desired width.
    Requires VALUE (pixels) as an integer greater than 0."""
    dirpre = 'w'
    prep(value, dirpre, quality)
    globber()
    for index, file in enumerate(images, start=1):
        with Image.open(file) as image:
            origWidth, origHeight = image.size
            newWidth = value
            newHeight = int(round(origHeight / origWidth * value))
            image = image.resize((int(newWidth), int(newHeight)),
                                 Image.ANTIALIAS)
            if dry:
                output = io.BytesIO()
                image.save(output, 'JPEG', quality=quality)
                contents = int(len(output.getvalue()))
                output.close()
                print(file + ' Original=' + str(origWidth) + 'x' + str(origHeight) + ' Resized=' + str(newWidth) + 'x' + str(newHeight) + ', ' + '~' + str(round(contents/1000)) + 'kb')
                sizes.append(contents)
            else:
                os.chdir(dirname)
                image.save(file, 'JPEG', quality=quality)
                os.chdir(cwd)
    report(index, sizes)


@cli.command()
@click.argument('value', type=int)
@click.option('--quality', '-q', default=75, type=click.IntRange(1, 95,
              clamp=True), help='Specify resized image quality (1-95).')
@click.option('--dry', '-d', is_flag=True, help='Do a dry run (recommended to do first).')
def height(value, quality, dry):
    """\b
    Resize image(s) proportionally, given desired height.
    Requires VALUE (pixels) as an integer greater than 0."""
    dirpre = 'h'
    prep(value, dirpre, quality)
    globber()
    for index, file in enumerate(images, start=1):
        with Image.open(file) as image:
            origWidth, origHeight = image.size
            newHeight = value
            newWidth = int(round(origWidth / origHeight * value))
            image = image.resize((int(newWidth), int(newHeight)),
                                 Image.ANTIALIAS)
            if dry:
                output = io.BytesIO()
                image.save(output, 'JPEG', quality=quality)
                contents = int(len(output.getvalue()))
                output.close()
                print(file + ' Original=' + str(origWidth) + 'x' + str(origHeight) + ' Resized=' + str(newWidth) + 'x' + str(newHeight) + ', ' + '~' + str(round(contents/1000)) + 'kb')
                sizes.append(contents)
            else:
                os.chdir(dirname)
                image.save(file, 'JPEG', quality=quality)
                os.chdir(cwd)
    report(index, sizes)


@cli.command()
@click.argument('value', type=int)
@click.option('--quality', '-q', default=75, type=click.IntRange(1, 95,
              clamp=True), help='Specify resized image quality (1-95).')
@click.option('--dry', '-d', is_flag=True, help='Do a dry run (recommended to do first).')
def percent(value, quality, dry):
    """\b
    Resize image(s) to be a proportion of their original size.
    Requires VALUE (percentage) as an integer greater than 0."""
    dirpre = 'p'
    prep(value, dirpre, quality)
    globber()
    for index, file in enumerate(images, start=1):
        with Image.open(file) as image:
            origWidth, origHeight = image.size
            newWidth = int(round(origWidth * value / 100))
            newHeight = int(round(origHeight * value / 100))
            image = image.resize((newWidth, newHeight),
                                 Image.ANTIALIAS)
            if dry:
                output = io.BytesIO()
                image.save(output, 'JPEG', quality=quality)
                contents = int(len(output.getvalue()))
                output.close()
                print(file + ' Original=' + str(origWidth) + 'x' + str(origHeight) + ' Resized=' + str(newWidth) + 'x' + str(newHeight) + ', ' + '~' + str(round(contents/1000)) + 'kb')
                sizes.append(contents)
            else:
                os.chdir(dirname)
                image.save(file, 'JPEG', quality=quality)
                os.chdir(cwd)
    report(index, sizes)


if __name__ == '__main__':
    cli()
