import subprocess
import time
import traceback
import multiprocessing

# run script for hyperparameter tuning

def run_line(cmd, gpu):
    if gpu == 0:
        try:
            with open("rs_log.txt", "a") as f:
                f.write(f"running {cmd} gpus 0-3\n")
            subprocess.run(cmd + ' --new_weights --gpu=0,1,2,3', shell=True)
            clear(cmd)
        except:
            print(traceback.format_exc())
    else:
        try:
            with open("rs_log.txt", "a") as f:
                f.write(f"running {cmd} gpus 4-7\n")
            subprocess.run(cmd + ' --new_weights --gpu=4,5,6,7', shell=True)
            clear(cmd)
        except:
            print(traceback.format_exc())

def clear(cmd):
    lines = []
    for x in cmd:
        if "--path_dir" in x:
            with open("../../save/" + x[x.rfind("=") + 1:] + "/all.log", "r") as f:
                y = f.read()
                if "Training complete" not in y:
                    return
                else:
                    print(cmd, "clearing this")

    with open("run_lines.txt", "r") as f:
        ls = f.read().split("\n")
        for line in ls:
            if len(line) == 0 or line[0] == "#":
                lines.append(line)
            elif line == cmd:
                lines.append("# " + line)
            else:
                lines.append(line)
        with open("run_lines_save.txt", "w") as g:
            for l in ls:
                g.write(l + "\n")
    
    with open("run_lines.txt", "w") as f:
        for line in lines:
            f.write(line + "\n")

with open("run_lines.txt", "r") as f:
    ls = f.read().split("\n")
    previous_run = None
    for line in ls:
        if len(line) == 0 or line[0] == "#":
            continue

        if previous_run == None:
            p = multiprocessing.Process(target=run_line, args=(line,0))
            p.start()
            previous_run = p
        else:
            p = multiprocessing.Process(target=run_line, args=(line,1))
            p.start()
            previous_run.join()
            p.join()
            previous_run = None
