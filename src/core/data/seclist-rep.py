from naughty_file_generator import NaughtyFilesGenerator
import pandas as pd

#create all tables

create_db_table_virusfile = '''
CREATE TABLE [IF NOT EXISTS] VirusFile (
	Name TEXT NOTNULL,
	Content TEXT NOTNULL,
) [WITHOUT ROWID];
'''

# files with metadata isLongFileName has no content but with very long file name to break systems that cannot
# handle very long file names

# exclude zipbombs

create_db_table_seclist = '''
CREATE TABLE [IF NOT EXISTS] SecList (
	NaughtyString TEXT NOTNULL,
	Digit TEXT NOTNULL,
    UserName TEXT NOTNULL,
    Password TEXT NOTNULL,
) [WITHOUT ROWID];
'''


# download virus files from Azure Storage. Cannot save as file on device as antimalware tool will block them
    # eicar.txt and lottapixel.jpg | base64 , insert in db

naughtyFilesGen = NaughtyFilesGenerator()

nFilesDF =  naughtyFilesGen.generate_naughty_files()
    
# download rest of strings, digits, usernames, passwords
    #insert into db