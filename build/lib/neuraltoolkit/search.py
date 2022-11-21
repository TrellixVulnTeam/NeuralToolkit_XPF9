import sys
sys.setrecursionlimit(10**6)
import os, fnmatch
from pathlib import Path

def drive_search(path=None, extension="kwik", follow_links=True, verbose=True, files=False):
    pattern = f"*.{extension}"
    total_size = 0
    s = 0
    result = dict()
    try:
        for root, _, f, rootfd in os.fwalk(path, follow_symlinks=follow_links):
            for name in f:
                if fnmatch.fnmatch(name, pattern):
                    if not files: 
                      pdir = os.path.join(Path(root).parent.absolute())
                      if pdir not in result.keys(): result[pdir] = list()
                    else: result[root] = list()
                    s = sum([os.stat(name, dir_fd=rootfd).st_size for name in f if fnmatch.fnmatch(name, pattern)])
                    total_size += s
                    if not files:
                       [result[pdir].append(root.split('/')[-1])]
                    if files: 
                      [result[root].append(name) for name in f if fnmatch.fnmatch(name, pattern)]
                    if verbose and files:
                        print(f"found \033[4m{s}\033[0m consuming ", end="")
                        print(s,  end="")
                        print(f" bytes ({s/1024**2} megabytes) in \033[4m{len(f)}\033[0m non-directory files")
                    break

        if verbose:
          if not files: 
            for dir, files in result.items(): print(f"found \033[4m{len(files)}\033[0m directories containing {extension} files in \033[4m{dir}\033[0m")

          print(f"\n================================================================================")
          print(f"total \033[4m{total_size}\033[0m bytes ({s/1024**2} megabytes) founded of {pattern[1:]} files")

    except Exception as e:
        print(e)
    
    finally:
        return result