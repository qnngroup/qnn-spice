import sys
import os
import shutil
from pathlib import Path

# Move to using similar to any(ext in name for ext in [".asy", ".lib"])
# for all types of lib and asy..

is_file = lambda name: any(ext in name for ext in [".asy", ".lib", ".asc"])

def make_symlink(source, destination, wsl) :
    # make symlink unless using wsl, in which case copy files
    if wsl:
        shutil.copy(source, destination)
    else:
        os.symlink(source, destination)
    


if __name__=="__main__":
   
    wsl = "--wsl" in sys.argv  # check if executing from wsl, in which case no links, just copy files
    if sys.argv[1] == "--update-symlinks":
        if wsl :
            print("Your files are being copied, not linked")

        LTSPICE_LIB_PATH = sys.argv[2]
        
        os.makedirs(LTSPICE_LIB_PATH+"/sym/qnn-spice", exist_ok=True)
        os.makedirs(LTSPICE_LIB_PATH+"/sub/qnn-spice", exist_ok=True)
        
        files_asy = []
        files_lib = []
        
        if os.path.exists("models.md"):
        
            models = open("models.md", "r").read()
            
            last_dir = []
            dest_dir = []
            last_dir_size = [-1]

            for line in models.split("\n"):
                
                indents = (len(line) - len(line.lstrip()))
                
                try:
                    loc = line.split("- ")[1].split(":")[0]
                
                    if ":" in line:
                        name = line.split("- ")[1].split(":")[1].lstrip().rstrip()
                        path = line.split("- ")[1].split(":")[0].lstrip().rstrip()
                    elif is_file(line):
                        
                        if ":" in line:
                            name = line.split("- ")[1].split(":")[1].rstrip().lstrip()
                            path = line.split("- ")[1].split(":")[0].rstrip().lstrip()
                        else:
                            name = line.split("- ")[1].rstrip().lstrip()
                            path = name
                    else:
                        name = "."
                        path = line.split("- ")[1].lstrip().rstrip()
                    
                    if not is_file(name): 
                        
                        while indents < last_dir_size[-1]:
                            
                            last_dir = last_dir[:-1]
                            dest_dir = dest_dir[:-1]
                            last_dir_size = last_dir_size[:-1]
                        
                        if indents == last_dir_size[-1]:
                            
                            last_dir[-1] = path+"/"
                            dest_dir[-1] = name+"/"
                            
                        else: # indents > prev_indents
                            
                            last_dir.append(path+"/")
                            dest_dir.append(name+"/")
                            last_dir_size.append(indents)
                        
                    if ".asy" in name: files_asy.append((''.join(last_dir) + path, 
                                                        (''.join(dest_dir)).replace("./", ""),
                                                        name
                                                        ))
                    if (".lib" in name or ".asc" in name): files_lib.append((''.join(last_dir) + path, 
                                                                            (''.join(dest_dir)).replace("./", ""),
                                                                            name
                                                                            ))
                    
                except:
                    
                    print("skipping line:", line)
            
            for src, dest, dest_filename in files_asy:
                
                os.makedirs(LTSPICE_LIB_PATH + "/sym/qnn-spice/" + dest, exist_ok=True)

                # copies if in wsl
                make_symlink(os.getcwd() + "/" + src, LTSPICE_LIB_PATH + "/sym/qnn-spice/" + dest + dest_filename, wsl)
                
                print("    ADDED:", dest_filename)
            
            for src, dest, dest_filename in files_lib:
                
                os.makedirs(LTSPICE_LIB_PATH + "/sub/qnn-spice/" + dest, exist_ok=True)
                
                inner_symlink = LTSPICE_LIB_PATH + "/sub/qnn-spice/" + dest + dest_filename

                make_symlink(os.getcwd() + "/" + src, inner_symlink, wsl)  # copies if in wsl
                
                outer_symlink = LTSPICE_LIB_PATH + "/sub/" + dest_filename.split("/")[-1]
                
                if os.path.exists(outer_symlink):
                    Path(outer_symlink).unlink(missing_ok=True)
                    
                make_symlink(inner_symlink, outer_symlink, wsl)
                
                print("    ADDED:", dest_filename)
                
        else:
            
            print("SKIPPING: NO MODEL FILE IN DIRECTORY")