import click, os, errno, sys, io
from PIL import Image


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
@click.option('--quality', '-q', default=75, type=click.IntRange(1, 95,
              clamp=True), help='Specify resized image quality (1-95).')
@click.option('--dry', '-d', is_flag=True, help='Do a dry run (recommended to do first).')
def width(pixels, quality, dry):
    """\b
    Resize image(s) proportionally, given desired width.
    Requires PIXELS as an integer greater than 0."""
    if pixels == 0:
        click.echo('PIXELS must be an integer greater than 0.')
        sys.exit()
    cwd = os.getcwd()
    if dry:
        sizes = []
        x = 0
    else:
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
                if dry:
                    x = x + 1
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
    if dry:
        print(str(x) + ' images totaling ' + '~' + str(round(sum(sizes)/1000)) + 'kb')


@cli.command()
@click.argument('pixels', type=int)
@click.option('--quality', '-q', default=75, type=click.IntRange(1, 95,
              clamp=True), help='Specify resized image quality (1-95).')
@click.option('--dry', '-d', is_flag=True, help='Do a dry run (recommended to do first).')
def height(pixels, quality, dry):
    """\b
    Resize image(s) proportionally, given desired height.
    Requires PIXELS as an integer greater than 0."""
    if pixels == 0:
        click.echo('PIXELS must be an integer greater than 0.')
        sys.exit()
    cwd = os.getcwd()
    if dry:
        sizes = []
        x = 0
    else:
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
                if dry:
                    x = x + 1
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
    if dry:
        print(str(x) + ' images totaling ' + '~' + str(round(sum(sizes)/1000)) + 'kb')


@cli.command()
@click.argument('percentage', type=int)
@click.option('--quality', '-q', default=75, type=click.IntRange(1, 95,
              clamp=True), help='Specify resized image quality (1-95).')
@click.option('--dry', '-d', is_flag=True, help='Do a dry run (recommended to do first).')
def percent(percentage, quality, dry):
    """\b
    Resize image(s) to be a proportion of their original size.
    Requires PERCENTAGE as an integer greater than 0."""
    if percentage == 0:
        click.echo('PERCENTAGE must be an integer greater than 0.')
        sys.exit()
    cwd = os.getcwd()
    if dry:
        sizes = []
        x = 0
    else:
        dirname = 'p' + str(percentage) + 'q' + str(quality)
        mkdir(dirname)
    for file in os.listdir(cwd):
        if file.lower().endswith(('.jpg', '.png', '.jpeg')):
            with Image.open(file) as image:
                origWidth, origHeight = image.size
                newWidth = int(round(origWidth * percentage / 100))
                newHeight = int(round(origHeight * percentage / 100))
                image = image.resize((newWidth, newHeight),
                                     Image.ANTIALIAS)
                if dry:
                    x = x + 1
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
    if dry:
        print(str(x) + ' images totaling ' + '~' + str(round(sum(sizes)/1000)) + 'kb')


if __name__ == '__main__':
    cli()
