'''
Change the Model Number in the EXIF Data - exiftool _DSF1234-xt4.RAF -model=X-T4
'''
import os
import pandas as pd
import time
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
raf = "-ext raf ."

# Acccept any case input from user
rafs = ["raf", "RAF"]

#Argument file
args = '-Model -FilmMode -Saturation'

@app.command()
def main():
  cmd_one = (f"{exiftool} {args} {raf} -csv")
  filetype = typer.prompt("If you would like to change the camera model of your Fujifilm RAW files to an XT-4?\nType in the extenstion 'RAF'")
  if filetype in rafs:
    cmd_one = (f"{exiftool} {args} {raf} -csv")
  else:
    message = " is not one of the predefined extensions - raf or RAF.\n"
    ending = typer.style(f"\nn{filetype}", bold=True, underline=True, )
    typer.secho(ending + message)
    raise typer.Abort()

  # Run 1st Subprocess
  pre_process = subprocess.Popen(cmd_one, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=cwd)

  #Pass CSV output Exiftool into a Pandas dataframe
  df_pre_process = pd.read_csv(pre_process.stdout)

  # Rename column
  df_pre_process.rename(columns = {'Model':'Model (Before)'}, inplace = True)

  print(tabulate(df_pre_process, headers=df_pre_process.columns, tablefmt="fancy_grid",  stralign=("center")))

  # Run 2nd Subprocess - convert model
  cmd_two = (f"{exiftool} -model=X-T4 {raf} -csv")
  mid_process = subprocess.Popen(cmd_two, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=cwd)

  #Sleep for 2 seconds
  time.sleep( 2 )

  # Run 1st Subprocess again
  post_process = subprocess.Popen(cmd_one, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=cwd)

  #Pass CSV output Exiftool into a Pandas dataframe
  df_post_process = pd.read_csv(post_process.stdout)

  # Function to process whichever data
  def post_film_mode(df_any_process):
    df_any_process.sort_values('SourceFile', inplace=True, ignore_index=True)
    df_any_process.index = df_any_process.index + 1
    df_any_process['FilmMode'] = df_any_process['FilmMode'].replace(['F0/Standard (Provia)','F1b/Studio Portrait Smooth Skin Tone (Astia)', 'F2/Fujichrome (Velvia)' ],['Provia / Standard', 'Astia / Soft', 'Velvia / Vivid'])
    df_any_process.loc[df_any_process['Saturation']=='None (B&W)', 'FilmMode'] = 'B&W'
    df_any_process.loc[df_any_process['Saturation']=='B&W Red Filter', 'FilmMode'] = 'B&W Red Filter'
    df_any_process.loc[df_any_process['Saturation']=='B&W Yellow Filter', 'FilmMode'] = 'B&W Yellow Filter'
    df_any_process.loc[df_any_process['Saturation']=='B&W Green Filter', 'FilmMode'] = 'B&W Green Filter'
    df_any_process.loc[df_any_process['Saturation']=='B&W Sepia', 'FilmMode'] = 'Sepia'
    df_any_process.loc[df_any_process['Saturation']=='Acros', 'FilmMode'] = 'Acros'
    df_any_process.loc[df_any_process['Saturation']=='Acros Red Filter', 'FilmMode'] = 'Acros Red Filter'
    df_any_process.loc[df_any_process['Saturation']=='Acros Yellow Filter', 'FilmMode'] = 'Acros Yellow Filter'
    df_any_process.loc[df_any_process['Saturation']=='Acros Green Filter', 'FilmMode'] = 'Acros Green Filter'
    df_any_process = df_any_process.merge(df_pre_process,on=['SourceFile', 'FilmMode', 'Saturation'], how='left')
    df_any_process.rename(columns = {'FilmMode':'Film Mode'}, inplace = True)
    df_any_process.drop('Saturation', axis=1, inplace=True)
    df_any_process.fillna('N/A', inplace=True)
    df_any_process = df_any_process[['SourceFile', 'Film Mode', 'Model (Before)', 'Model']]
    print(tabulate(df_any_process, headers=df_any_process.columns, tablefmt="fancy_grid", stralign=("center")))
  post_film_mode(df_post_process)

  # Subprocess PIPE outputs
  stdout_mid_process, stderr_mid_process  = mid_process.communicate()

  if not stdout_mid_process:
    typer.secho(f'\n{stderr_mid_process}', fg=typer.colors.BLACK, bold=True)

if __name__ == "__main__":
  app()