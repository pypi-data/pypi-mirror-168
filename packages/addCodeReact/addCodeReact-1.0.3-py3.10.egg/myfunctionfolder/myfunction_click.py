import click
# importing the required modules
import os
import speech_recognition as sr
import fileinput
import sys

# error messages
INVALID_FILETYPE_MSG = "Error: Invalid file format. %s must be a .js file."
INVALID_PATH_MSG = "Error: Invalid file path/name. Path %s does not exist."


def validate_file(file_name):
    """
    validate file name and path.
    """
    if not valid_path(file_name):
        print(INVALID_PATH_MSG % (file_name))
        quit()
    elif not valid_filetype(file_name):
        print(INVALID_FILETYPE_MSG % (file_name))
        quit()
    return


def valid_filetype(file_name):
    # validate file type
    return file_name.endswith(".js")

def valid_path(path):
    # validate file path
    print(path)
    return os.path.exists(path)


@click.group()
def cli():
  pass


@cli.command(name='addLn')
@click.option('--file_name', type=click.Path(exists=True), prompt="Enter The File Path", help="Provide the file path of the file ")
@click.option("--label", prompt="Enter component label", help="Provide your name")
@click.option("--component", prompt="Enter component type", help="Provide your name")
def addline(file_name,label,component):
    validate_file(file_name)
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.8)

        print("What is the filePath")
        audio1 = r.listen(source)
        text1 =  r.recognize_google(audio1)
        print(text1)

        print("Name the label")
        audio2 = r.listen(source)
        text2 =  r.recognize_google(audio2)
        print(text2)

        print("Name the component")
        audio3 = r.listen(source)
        text3=  r.recognize_google(audio3)
        print(text3)
    
    

    with open(file_name) as f:
        line =  f.readlines()

    line.insert(int(3),"<MainComponent type='"+text3+"' label='"+text2+"' kind = 'secondary' />"+" \n")
    with open(file_name, 'w') as f:
        for l in line:
            f.write(l)

@cli.command(name='DeleteComponent')
@click.option('--file_name', type=click.Path(exists=True), prompt="Enter The File Path", help="Provide the file path of the file ")
@click.option("--label", prompt="Enter component label", help="Provide your name")
def deleteFile(file_name,label):
    validate_file(file_name)
    x = fileinput.input(files=file_name, inplace=1)
    new_text = " "
    for line in x:
        if label in line:
            line = new_text
        sys.stdout.write(line)

@cli.command(name='wel')
def welcome():
    click.echo('Welcome')


if __name__ == '__main__':
    cli()
