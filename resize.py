import click, os, errno, sys, io
from glob import glob
from PIL import Image

oldSizes, newSizes = [], []
images = glob('*.jpg')
images.extend(glob('*.jpeg'))
images.extend(glob('*.png'))

def mkdir(directory):
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

def prep(value, dry, dirpre, quality):
    if value == 0:
        click.echo('Please use an integer greater than 0')
        sys.exit()
    elif not dry:
        global dirname
        dirname = dirpre + str(value) + 'q' + str(quality)
        mkdir(dirname)
    if len(images) == 0:
        click.echo('Please include some images to resize in your directory')
        sys.exit()
    print(str(len(images)) + ' images to resize...')

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
    for index, file in enumerate(images, start=1):
        with Image.open(file) as imOld:
            oldSize = (os.stat(file).st_size)/1024
            oldSizes.append(oldSize)
            if side == 'width':
                newDim = int(round(imOld.height / imOld.width * value))
                imNew = imOld.resize((int(value), int(newDim)),
                                 Image.ANTIALIAS)
            elif side == 'height':
                newDim = int(round(imOld.width / imOld.height * value))
                imNew = imOld.resize((int(newDim), int(value)),
                                 Image.ANTIALIAS)
            else:
                click.echo('Please specify side as "width" or "height"')
                sys.exit()
            output = io.BytesIO()
            imNew.save(output, 'JPEG', quality=quality)
            newSize = int(len(output.getvalue()))/1024
            newSizes.append(newSize)
            if not dry:
                imNew.save(dirname + '/' + file, 'JPEG', quality=quality)
            if verbose:
                print(file + ': ' + str(imOld.width) + 'x' + str(imOld.height)
                      + ' (' + str(round(oldSize)) + 'kb)' + ' -> ' +
                      str(imNew.width) + 'x' + str(imNew.height) + ' (' +
                      str(round(newSize)) + 'kb)')
    print(str(round((1 - sum(newSizes) / sum(oldSizes)) * 100))
          + '% ' + 'space savings (' + str(round(sum(oldSizes))) + 'kb -> ' +
          str(round(sum(newSizes))) + 'kb)')

@cli.command()
@click.argument('value', type=int)
@click.option('--quality', '-q', default=75, type=click.IntRange(1, 95,
              clamp=True), help='Specify resized image quality (1-95).')
@click.option('--dry', '-d', is_flag=True, help='Do a dry run (recommended to do first).')
@click.option('--verbose', '-v', is_flag=True, help=
              'Verbose output with results of each image conversion.')
def percent(value, quality, dry, verbose):
    """\b
    Resize image(s) to a fraction of their original size.
    Requires VALUE (percentage) as an integer greater than 0."""
    dirpre = 'p'
    prep(value, dry, dirpre, quality)
    for index, file in enumerate(images, start=1):
        with Image.open(file) as imOld:
            oldSize = (os.stat(file).st_size)/1024
            oldSizes.append(oldSize)
            newWidth = int(round(imOld.width * value / 100))
            newHeight = int(round(imOld.height * value / 100))
            imNew = imOld.resize((newWidth, newHeight),
                                 Image.ANTIALIAS)
            output = io.BytesIO()
            imNew.save(output, 'JPEG', quality=quality)
            newSize = int(len(output.getvalue()))/1024
            newSizes.append(newSize)
            if not dry:
                imNew.save(dirname + '/' + file, 'JPEG', quality=quality)
            if verbose:
                print(file + ': ' + str(imOld.width) + 'x' + str(imOld.height)
                      + ' (' + str(round(oldSize)) + 'kb)' + ' -> ' +\
                      str(imNew.width) + 'x' + str(imNew.height) + ' (' +
                      str(round(newSize)) + 'kb)')
    print(str(round((1 - sum(newSizes) / sum(oldSizes)) * 100))
          + '% ' + 'space savings (' + str(round(sum(oldSizes))) + 'kb -> ' +
          str(round(sum(newSizes))) + 'kb)')

if __name__ == '__main__':
    cli()
