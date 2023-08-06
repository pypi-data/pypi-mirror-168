# importing the required modules
import os
import argparse

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

def addLine(args):
    filename = args.addLine[2]
    lineNumber = args.addLine[3]
    component = args.addLine[0]
    label = args.addLine[1]

    validate_file(filename)

    with open(filename) as f:
        line =  f.readlines()

    line.insert(int(lineNumber),"<MainComponent type='"+component+"' label='"+label+"' kind = 'secondary' />"+" \n")
    with open(filename, 'w') as f:
        for l in line:
            f.write(l)

def addLineForImport(args):
    filename = args.addLineForImport[0]

    validate_file(filename)

    with open(filename) as f:
        line =  f.readlines()

    line.insert(int(0),'import MainComponent from "sample-npm-package-react-t";'+" \n")
    with open(filename, 'w') as f:
        for l in line:
            f.write(l)

def main():
    # create parser object
    parser = argparse.ArgumentParser(description="A text file manager!")

    # defining arguments for parser object   

    parser.add_argument(
        "-addLine",
        "--addLine",
        type=str,
        nargs=4,
        metavar=("component_type","label","filename","lineNumber"),
        help="add components to the file given"
    )
    parser.add_argument(
        "-addImport",
        "--addLineForImport",
        type=str,
        nargs=1,
        metavar=("filename"),
        help="add import statement to the file given"
    )

    # parse the arguments from standard input
    args = parser.parse_args()

    # calling functions depending on type of argument
    if args.addLine != None:
        addLine(args)
    elif args.addLineForImport != None:
        addLineForImport(args)


if __name__ == "__main__":
    # calling the main function
    main()
