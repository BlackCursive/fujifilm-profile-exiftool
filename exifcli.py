'''
Change the Model Number in the EXIF Data - exiftool _DSF1234-xt4.RAF -model=X-T4
'''
import os
import typer
import subprocess

# Current directory of where the script resides
cwd = os.path.dirname(os.path.realpath(__file__))

# Initializing typer.Typer app and removes default option from --help
app = typer.Typer(add_completion=False)

# ExifTool Directory
exiftool = "exiftool/exiftool"

# Script will be applied to either all JPG or RAF files
jpg = "-ext jpg ."
raf = "-ext raf ."

# Acccept any case input from user
jpgs = ["jpg", "JPG"]
rafs = ["raf", "RAF"]

#Argument file
args = r"-@ args.txt"

@app.command()
def main():
  modeltype = typer.confirm("Change the camera model to an XT-4?")
  if modeltype:
    filetype = typer.prompt("Are you processing JPG or RAF files?")
    if filetype in jpgs:
      cmd = (f"{exiftool} {args} {jpg}")
    elif filetype in rafs:
      cmd = (f"{exiftool} {args} {raf}")
      print(cmd)
    else:
      message = " is not one of the predefined extensions - jpg, JPG, raf or RAF\n."
      ending = typer.style(f"\nn{filetype}", bold=True, underline=True, )
      typer.secho(ending + message)
      raise typer.Abort()
  else:
    raise typer.Abort()


  process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=cwd)

  # for line in process.stdout:
  #   print(line.rstrip())
  #   if "X-E1" in line:
  #     print("WTF - YES YES YES")

  while True:
    line = process.stdout.readline()
    if "X-E1" in line:
      print("WTF - YES YES YES")
    if not line:
        break
    print(line.rstrip())

  stdout, stderr  = process.communicate()

  if not stdout:
    typer.secho(f'\n{stderr}', fg=typer.colors.RED, bold=True)

  if process.returncode == 0:
    typer.secho('Success', fg=typer.colors.GREEN, bold=True)

if __name__ == "__main__":
  app()
