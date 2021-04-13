import os
from os import listdir, walk, system
from os.path import isfile, join
import glob
gt = {"00": "../data/dataset/poses/00.txt",
      "01": "../data/dataset/poses/01.txt",
      "02": "../data/dataset/poses/02.txt",
      "03": "../data/dataset/poses/03.txt",
      "04": "../data/dataset/poses/04.txt",
      "05": "../data/dataset/poses/05.txt",
      "06": "../data/dataset/poses/06.txt",
      "07": "../data/dataset/poses/07.txt",
      "08": "../data/dataset/poses/08.txt",
      "09": "../data/dataset/poses/09.txt",
     }
# dirs = [dir for dir in listdir() if dir[0] == "T"]
# print(dirs)
output_dir = join(os.getcwd(), "../data/output")
if not os.path.isdir(output_dir):
      os.mkdir(output_dir)
for dir in listdir():
      if dir[0] == "T":
            curr = join(os.getcwd(), dir)
            out = join(output_dir, dir)
            out_ate = join(out, "ate")
            out_rpe = join(out, "rpe")
            if not os.path.isdir(out):
                  os.mkdir(out)
            if not os.path.isdir(out_ate):
                  os.mkdir(out_ate)
            if not os.path.isdir(out_rpe):
                  os.mkdir(out_rpe)
            files = [os.path.splitext(f)[0] for f in listdir(curr) if isfile(join(curr, f))]
            for file in files:
                  ground_truth = gt[file]
                  txt_file = join(dir, file + ".txt")
                  # print(txt_file)
                  out_name = dir[4:] + file
                  out_txt = out_name + ".txt"
                  out_ate_name = join(out_ate, out_name)
                  out_ate_txt =  join(out_ate, out_txt)
                  out_rpe_name = join(out_rpe, out_name)
                  out_rpe_txt =  join(out_rpe, out_txt)
                  # print(out_name)
                  system("evo_rpe kitti {} {} --save_plot {} > {}".format(ground_truth, txt_file, out_rpe_name, out_rpe_txt))
                  system("evo_ape kitti {} {} --save_plot {} > {}".format(ground_truth, txt_file, out_ate_name, out_ate_txt))

