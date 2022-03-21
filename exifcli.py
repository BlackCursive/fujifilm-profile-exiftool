'''
Change the Model Number in the EXIF Data - exiftool _DSF1234-xt4.RAF -model=X-T4
'''
import os
import pandas as pd
import typer
import subprocess

# sudo pip3 install tabulate
from tabulate import tabulate

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
args = '-Model -FilmMode -Saturation'

@app.command()
def main():
  modeltype = typer.confirm("Change the camera model to an XT-4?", abort=True)
  if modeltype:
    filetype = typer.prompt("Are you processing JPG or RAF files?")
    if filetype in jpgs:
      cmd = (f"{exiftool} {args} {jpg} -csv")
    elif filetype in rafs:
      cmd = (f"{exiftool} {args} {raf} -csv")
    else:
      message = " is not one of the predefined extensions - jpg, JPG, raf or RAF\n."
      ending = typer.style(f"\nn{filetype}", bold=True, underline=True, )
      typer.secho(ending + message)
      raise typer.Abort()

  # Run Subprocess
  process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=cwd)

  #Pass CSV output Exiftool into a Pandas dataframe
  df = pd.read_csv(process.stdout)

  # Sort dataframe and reset index
  df.sort_values('SourceFile', inplace=True, ignore_index=True)

  # Start row index from 1 instead of zero
  df.index = df.index + 1

  # Copy Film Simulations from Saturation tag to FilmMode tag / Change Output
  def film_mode(df):
      df['FilmMode'] = df['FilmMode'].replace(['F0/Standard (Provia)','F1b/Studio Portrait Smooth Skin Tone (Astia)', 'F2/Fujichrome (Velvia)' ],['Provia / Standard', 'Astia / Soft', 'Velvia / Vivid'])
      df.loc[df['Saturation']=='None (B&W)', 'FilmMode'] = 'B&W'
      df.loc[df['Saturation']=='B&W Red Filter', 'FilmMode'] = 'B&W Red Filter'
      df.loc[df['Saturation']=='B&W Yellow Filter', 'FilmMode'] = 'B&W Yellow Filter'
      df.loc[df['Saturation']=='B&W Green Filter', 'FilmMode'] = 'B&W Green Filter'
      df.loc[df['Saturation']=='B&W Sepia', 'FilmMode'] = 'Sepia'
      df.loc[df['Saturation']=='Acros', 'FilmMode'] = 'Acros'
      df.loc[df['Saturation']=='Acros Red Filter', 'FilmMode'] = 'Acros Red Filter'
      df.loc[df['Saturation']=='Acros Yellow Filter', 'FilmMode'] = 'Acros Yellow Filter'
      df.loc[df['Saturation']=='Acros Green Filter', 'FilmMode'] = 'Acros Green Filter'
      df.rename(columns = {'FilmMode':'Film Mode'}, inplace = True)
      df.fillna('N/A', inplace=True)
      df.drop('Saturation', axis=1, inplace=True)
  film_mode(df)

  # Display formated Pandas dataframe in the terminal
  print(tabulate(df, headers=df.columns, tablefmt="fancy_grid",  stralign=("center")))

  stdout, stderr  = process.communicate()

  if not stdout:
    typer.secho(f'\n{stderr}', fg=typer.colors.BLACK, bold=True)

  # if process.returncode == 0:
  #   typer.secho('Success', fg=typer.colors.GREEN, bold=True)

if __name__ == "__main__":
  app()