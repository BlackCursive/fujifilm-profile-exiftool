'''
Change the Model Number in the EXIF Data to an X-T4
'''
import os
import pandas as pd
import time
import typer
import subprocess

from pathlib import Path
from tabulate import tabulate

# Initializing typer.Typer app and removes default option from --help
app = typer.Typer(add_completion=False)

# Current directory of where the script resides
home_dir = Path.cwd()

# RAW Files Directory
raf_files = home_dir / 'raf_files'

# If raf_files folder does not exist then it is created
if Path(raf_files).is_dir():
  pass
else:
  print(f"The following folder has been created: {raf_files}")
  raf_files.mkdir(parents=False, exist_ok=True)
  time.sleep( 1 )

# String representation of home directory needed for Pandas str replacement - Would not use Path from pathlib
raf_files_str_dir = (f"{home_dir}/raf_files/")

# ExifTool Directory
exiftool = home_dir / "exiftool/exiftool"

# Script will be applied to either all JPG or RAF files
raf = "-ext raf"

# Acccept any case input from user
rafs = ["raf", "RAF"]

#Argument file
args = '-Model -FilmMode -Saturation'

# Check for which operating system then issue appropriate clear command
def clear_screen():
  if(os.name == 'posix'):
    os.system('clear')
  else:
    os.system('cls')

@app.command()
def main():
  jpg_file_ext = [".jpg", ".jpeg", ".JPG"]
  raf_file_ext = [".raf", ".RAF"]

  # List comprehension that appends the file extensions of every file in the raf_files directory
  raf_dir_ext = [raf_dir_file_ext.suffix for raf_dir_file_ext in Path(raf_files).iterdir()]

  # - list items within another list
  jpg_dir_ext_valid = any(jpg_file in jpg_file_ext for jpg_file in raf_dir_ext)
  raf_dir_ext_valid = any(raw_file in raf_file_ext for raw_file in raf_dir_ext)

  # Checks if jpgs are in the raf_files directory
  if jpg_dir_ext_valid:
    typer.secho(f"Please note there are files with either one of these extensions{jpg_file_ext}\nin the raf_files folder but they will not be affected.\n", bold=True)

  # Checks if rafs are in the raf_files directory
  if not raf_dir_ext_valid:
    typer.secho(f"There aren't any Fujifilm RAW files in the 'raf_files' folder.\n", fg=typer.colors.RED, underline=True, bold=True)
    raise typer.Abort()

  filetype = typer.prompt("\nIf you would like to change the camera model of your Fujifilm RAW files to an XT-4 place\nthem in the raf_files folder then please type in the extenstion 'RAF' for confirmation")
  if filetype in rafs:
    cmd_one = (f"{exiftool} {args} {raf_files} {raf} -csv")
  else:
    message = " is not one of the predefined extensions - raf or RAF.\n"
    ending = typer.style(f"\nn{filetype}", bold=True, underline=True, )
    typer.secho(ending + message)
    raise typer.Abort()

  # Run 1st Subprocess
  pre_process = subprocess.Popen(cmd_one, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=home_dir)

  #Pass CSV output Exiftool into a Pandas dataframe
  df_pre_process = pd.read_csv(pre_process.stdout)

  # Rename column
  df_pre_process.rename(columns = {'Model':'Model (Before)'}, inplace = True)

  ### print(tabulate(df_pre_process, headers=df_pre_process.columns, tablefmt="fancy_grid",  stralign=("center")))

  # Run 2nd Subprocess - convert model
  cmd_two = (f"{exiftool} -model=X-T4 {raf} {raf_files} -csv")
  mid_process = subprocess.Popen(cmd_two, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=home_dir)

  #Sleep for 2 seconds then clear the screen
  time.sleep( 1 )
  clear_screen()

  # Run 1st Subprocess again
  post_process = subprocess.Popen(cmd_one, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=home_dir)

  #Pass CSV output Exiftool into a Pandas dataframe
  df_post_process = pd.read_csv(post_process.stdout)

  # Function to process whichever data
  def post_film_mode(df_any_process):
    # Aborts program if there isn't any simulation metadata - possibly a file other than a Fujifilm raf but with the extension
    if 'FilmMode' not in df_any_process.columns:
      typer.secho("The files in the raf_files directory do not contain any Fujifilm Film Simulation metadata.\nPlease double check your files and rerun the program.", fg=typer.colors.RED, underline=True, bold=True)
      raise typer.Abort()
    df_any_process = df_any_process.merge(df_pre_process,on=['SourceFile', 'FilmMode', 'Saturation'], how='left')
    df_any_process.sort_values('SourceFile', inplace=True, ignore_index=True)
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
    df_any_process.index = df_any_process.index + 1
    df_any_process.rename(columns = {'FilmMode':'Film Mode'}, inplace = True)
    df_any_process.drop('Saturation', axis=1, inplace=True)
    df_any_process.fillna('N/A', inplace=True)
    df_any_process['SourceFile'] = df_any_process['SourceFile'].str.replace(raf_files_str_dir, "") ########
    df_any_process = df_any_process[['SourceFile', 'Film Mode', 'Model (Before)', 'Model']]
    total = df_post_process.shape[0]
    with typer.progressbar(length=total, label="Processing Photos\t") as progress:
        for value in progress:
            # Fake processing time
            time.sleep(0.1)
            total += 1
    print("\n")
    print(tabulate(df_any_process, headers=df_any_process.columns, tablefmt="fancy_grid", stralign=("center")))
  post_film_mode(df_post_process)

  # Subprocess PIPE outputs
  stdout_mid_process, stderr_mid_process  = mid_process.communicate()

  # Standard ouput & suffix on process files
  if not stdout_mid_process:
    typer.secho(f'\n{stderr_mid_process}', fg=typer.colors.BLACK, bold=True)
    typer.secho(f"Backups are made of processed files with the suffix '_original' added to the filename. \n", fg=typer.colors.BLACK, bold=True)

  # Close standard output
  pre_process.stdout.close()
  mid_process.stdout.close()
  post_process.stdout.close()

if __name__ == "__main__":
  app()