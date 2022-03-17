'''
Change the Model Number in the EXIF Data - exiftool _DSF1234-xt4.RAF -model=X-T4
'''
import typer
import subprocess

# Initializing typer.Typer app and removes default option from --help
app = typer.Typer(add_completion=False)

# ExifTool Directory
exiftool = "exiftool/exiftool"

# Script will be applied to eith all JPG or RAF files
jpg = "*.JPG *.jpg"
raf = "*.RAF *.raf"

@app.command()
def main(filetype: str = typer.Option(..., prompt="Are these JPG or RAF files?")):
  if filetype == 'JPG':
    cmd = (f"{exiftool} -Make '-Model' '-FilmMode' '-Saturation' {jpg}")
  elif filetype == 'RAF':
    cmd = (f"{exiftool} -Make '-Model' '-FilmMode' '-Saturation' {raf}")
  else:
    cmd = (f"{exiftool} -Make '-Model' '-FilmMode' '-Saturation' {raf} {jpg}")

  # REMOVE ON UPLOAD ###
  print(cmd)

  p1 = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines = True)

  out, err = p1.communicate()

  if out:
    print(f'\nOuput:\n {out}')
  else:
    print(f'error: {err}')

  if p1.returncode == 0:
    typer.secho('Success', fg=typer.colors.GREEN, bold=True)
  else:
    typer.secho('Failed', fg=typer.colors.WHITE, bg=typer.colors.RED, bold=True)

if __name__ == "__main__":
  app()