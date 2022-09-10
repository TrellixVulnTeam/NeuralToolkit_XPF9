import sys
sys.setrecursionlimit(10**6)
import os, fnmatch
from pathlib import Path
# from ipywidgets import interact, interactive, fixed, interact_manual
# from IPython.display import display

class NeuralDataSet:

    def find(path=None, pattern="*.kwik", follow_links=True, verbose=True, files=False):
        result = dict()
        try:
            for root, _, f, rootfd in os.fwalk(path, follow_symlinks=follow_links):
                for name in f:
                    if fnmatch.fnmatch(name, pattern):
                        if not files: pdir = os.path.join(Path(root).parent.absolute())
                        if pdir not in result.keys(): result[pdir] = 0
                        else: result[root] = 0
                        s = sum([os.stat(name, dir_fd=rootfd).st_size for name in f if fnmatch.fnmatch(name, pattern)])
                        if not files: result[pdir] += s
                        if files: result[root] += s
                        if verbose and files:
                            print("found \033[4m"+root+"\033[0m consuming ", end="")
                            print(s,  end="")
                            print(f" bytes ({s/1024**2} megabytes) in \033[4m{len(f)}\033[0m non-directory files")
                        break

            if verbose and not files: 
                for dir, size in result.items(): print(f"found \033[4m{size}\033[0m bytes of {pattern[1:]} files in \033[4m{dir}\033[0m")
            
            print(f"\n================================================================================")
            print(f"total \033[4m{sum(result.values())}\033[0m bytes ({s/1024**2} megabytes) readed of {pattern[1:]} files")

        except Exception as e:
            print(e)
        
        finally:
            return result.keys()