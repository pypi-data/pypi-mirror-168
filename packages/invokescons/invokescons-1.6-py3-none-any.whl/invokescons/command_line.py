import os
import sys
import shlex
import subprocess
import SCons.Script

def main():
    arguments = sys.argv
    command = []
    if (len(arguments) > 1):
        arguments = arguments[1:]
        for i in range(len(arguments)):
            argument = arguments[i]
            arguments[i] = "arguments.append(\""+shlex.quote(argument)+"\")"
        if (len(arguments) > 1):
            arguments = "; ".join(arguments)
        else:
            arguments = arguments[0]
        command.append(sys.executable)
        command.append("-c")
        command.append("import sys; import SCons.Script; arguments = []; "+arguments+"; sys.argv += arguments; print(str(sys.argv)); SCons.Script.main()")
        print(str(command))
        result = None
        try:
          process = subprocess.Popen(command, env=os.environ(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
          while True:
            line = process.stdout.readline()
            if ((len(line) == 0) and not (process.poll() == None)):
              break
            print(line.decode("UTF-8").strip())
          output = process.communicate()[0]
          exit = process.returncode
          if (exit == 0):
            result = output
        except:
          pass
        print(str(result))
    else:
        SCons.Script.main()
    return 0
