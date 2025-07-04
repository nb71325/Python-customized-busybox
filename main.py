import os
import sys
import shutil
import time

def pwd():
    print(os.getcwd())

def echo(args):
    try:
        if not args:
            raise ValueError("No argument(s) provided for echo")

        newline = True
        output_args = args

        if args[0] == "-n":
            newline = False
            output_args = args[1:]

        output = " ".join(output_args)
        sys.stdout.write(output)
        if newline:
            sys.stdout.write("\n")
        sys.stdout.flush()

    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(-10)

def cat(args):
    try:
        if not args:
            raise ValueError("No argument(s) provided for cat")

        for index, filename in enumerate(args):
            try:
                with open(filename, 'r') as f:
                    content = f.read()
                    sys.stdout.write(content)

                    ## this if is used to display the content of the next files on a different line

                    if not content.endswith('\n'):
                        sys.stdout.write('\n')

            except FileNotFoundError:
                print(f"No such file")
                sys.exit(-20)
            except Exception as e:
                print(f"Cannot read the file: {e}")
                sys.exit(-20)

        sys.stdout.flush()

    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(-20)

def mkdir(args):
    try:
        if not args:
            raise ValueError("No argument(s) provided for mkdir")
        
        for dirname in args:
            try:
                os.makedirs(dirname, exist_ok=True)
            except Exception as e:
                print(f"Cannot create the directory '{dirname}': {e}")
                sys.exit(-30)

        sys.stdout.flush()
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(-30)

def mv(args):
    try:
        if not args:
            raise ValueError("No argument(s) provided for mv")
        
        if len(args) != 2:
            raise ValueError("mv requires exactly 2 arguments: source and destination")
        
        source, destination = args

        try:
            shutil.move(source, destination)
        except FileNotFoundError:
            print(f"Cannot move '{source}': No such file or directory")
            sys.exit(-40)
        except Exception as e:
            print(f"Cannot move '{source}' to '{destination}': {e}")
            sys.exit(-40)

        sys.stdout.flush()
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(-40)

def ln(args):
    try:
        if not args:
            raise ValueError("No argument(s) provided for ln")

        symbolic = False

        # checking for -s or --symbolic option
        if args[0] in ("-s", "--symbolic"):
            symbolic = True
            args = args[1:]

        if len(args) != 2:
            raise ValueError("ln requires exactly 2 arguments: source and destination")

        source, destination = args

        # ensuring that the source exists 
        if not os.path.exists(source):
            raise FileNotFoundError(f"'{source}' does not exist")

        try:
            if symbolic:
                os.symlink(source, destination)
            else:
                os.link(source, destination)
        except Exception as e:
            print(f"Cannot create the link from '{source}' to '{destination}': {e}")
            sys.exit(-50)

        sys.stdout.flush()

    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(-50)

def rmdir(args):
    try:
        if not args:
            raise ValueError("No argument(s) provided for rmdir")
        
        for dirname in args:
            try:
                os.rmdir(dirname)
            except Exception as e:
                print(f"Cannot remove the directory '{dirname}': {e}")
                sys.exit(-60)

        sys.stdout.flush()
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(-60)

def rm(args):
    try:
        if not args:
            raise ValueError("No argument(s) provided for rm")

        recursive = False
        dir_mode = False

        # implementing the commands options
        if args[0] == "-R" or args[0] == "-r" or args[0] == "--recursive":
            recursive = True
            args = args[1:]
        elif args[0] == "--dir":
            dir_mode = True
            args = args[1:]

        if not args:
            raise ValueError("No file(s) or directorie(s) provided for rm")

        for target in args:
            try:
                if recursive:
                    if not os.path.isdir(target):
                        raise FileNotFoundError(f"'{target}' is not a directory or does not exist")
                    shutil.rmtree(target)

                elif dir_mode:
                    if not os.path.isdir(target):
                        raise FileNotFoundError(f"'{target}' is not a directory or does not exist")
                    os.rmdir(target)  # Only works if directory is empty

                else:
                    if not os.path.isfile(target):
                        raise FileNotFoundError(f"'{target}' is not a file or does not exist")
                    os.remove(target)

            except Exception as e:
                print(f"Cannot remove '{target}': {e}")
                sys.exit(-70)

        sys.stdout.flush()

    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(-70)

def ls(args=None):
    try:
        # If args is None or empty 
        if not args or len(args) == 0:
            entries = os.listdir()
            for entry in entries:
                print(f"  {entry}")

        # If first arg is -a or --all 
        elif args[0] in ("-a", "--all"):
            path = "."
            if len(args) > 1 and os.path.isdir(args[1]):
                path = args[1]
            entries = os.listdir(path)
            for entry in entries:
                print(f"  {entry}")

        # If first arg is an existing directory 
        elif os.path.isdir(args[0]):
            path = args[0]
            entries = os.listdir(path)
            for entry in entries:
                print(f"  {entry}")

        else:
            print(f"Unsupported argument '{args[0]}'")
            sys.exit(-80)

        sys.stdout.flush()

    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(-80)

def cp(args):
    try:
     
        if not args:
            raise ValueError("No argument(s) provided for rm")
        
        recursive = False

        # for -r or --recursive
        if args[0] in ("-r", "--recursive"):
            recursive = True
            args = args[1:] 

        if len(args) != 2:
            raise ValueError("cp requires exactly 2 arguments: the target and the destination")
        
        target, destination = args

        # ensuring that the source exists 
        if not os.path.exists(target):
            raise FileNotFoundError(f"'{target}' does not exist")
        
        try:
            if os.path.isdir(target):
                if not recursive:
                    raise IsADirectoryError(f" Use -r or --recursive to copy directories.")
                shutil.copytree(target, destination)
            else:
                shutil.copy(target, destination)
        except Exception as e:
            print(f"Cannot copy '{target}' to '{destination}': {e}")
            sys.exit(-90)
        
        sys.stdout.flush()
    
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(-90)

def touch(args):
    try:
        if not args:
            raise ValueError("No argument(s) provided for touch")

        # default behavior
        change_access = True
        change_modify = True
        create = True
        filenames = []

        # parsing the command options only
        if args[0].startswith("-"):
            for ch in args[0][1:]: 
                if ch == "a":
                    change_modify = False
                elif ch == "m":
                    change_access = False
                elif ch == "c":
                    create = False
                else:
                    print(f"touch: invalid option '-{ch}'")
                    sys.exit(-100)
            filenames = args[1:]  # the remaining args are the filenames
        else:
            filenames = args  # no command given, all args are filenames

        if not filenames:
            raise ValueError("No file(s) specified")

        for filename in filenames:
            if not os.path.exists(filename):
                if create:
                    try:
                        open(filename, 'r').close()
                    except Exception as e:
                        print(f"Cannot create file '{filename}': {e}")
                        sys.exit(-100)
                else:
                    continue  # the file does not exist and create == False

            try:
                current_stat = os.stat(filename)
                atime = current_stat.st_atime if not change_access else time.time()
                mtime = current_stat.st_mtime if not change_modify else time.time()
                os.utime(filename, (atime, mtime))
            except Exception as e:
                print(f"Cannot update timestamps for '{filename}': {e}")
                sys.exit(-100)

        sys.stdout.flush()

    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(-100)

def chmod(args):
    try:
        if not args:
            raise ValueError("No argument(s) provided for chmod")
        
        if len(args) != 2:
            raise ValueError("chmod requires exactly 2 arguments: the rights and the target")
        
        rights_str = args[0]
        target = args[1]

        if not os.path.exists(target):
            raise FileNotFoundError(f"'{target}' does not exist")

        try:
            rights = int(rights_str, 8)  # base 8
        except ValueError:
            raise ValueError(f"Invalid permission mode: {rights_str}. Use octal like 570, 755, etc.")

        os.chmod(target, rights)
        print("chmod applied successfully")

        sys.stdout.flush()

    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(-25)

def main():
    args = sys.argv[1:]
    if not args:
        print("No command provided. Please, type a Linux command.")
        return

    command = args[0]
    command_args = args[1:]

    match command:
        case "pwd":
            pwd()
        case "echo":
            echo(command_args)
        case "cat":
            cat(command_args)
        case "mkdir":
            mkdir(command_args)
        case "mv":
            mv(command_args)
        case "ln":
            ln(command_args)
        case "rmdir":
            rmdir(command_args)
        case "rm":
            rm(command_args)
        case "ls":
            ls(command_args)
        case "cp":
            cp(command_args)
        case "touch":
            touch(command_args)
        case "chmod":
            chmod(command_args)
        case _:
            print(f"Unsupported command: {command}. Please, make sure you have typed the command correctly!")

if __name__ == "__main__":
    main()
