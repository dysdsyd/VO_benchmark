#!/usr/bin/env python3

## ===========================================================================
## Objective:
##          ROB 530 Project - Automate txt file reader for results
##
## Files required:
##          generate_results.py (this file)
##          ../data/output/TXX_name/ATE/01.txt (example data file)
##          ../data/output/TXX_name/RPE/01.txt (example data file)
##          ../data/dataset/poses/XX.txt (ground truth file from KITTI poses)
##
## Authors: 
##          TAA         04/08/2021      Initial Coding
## ===========================================================================

import numpy as np, glob, os, csv, xlsxwriter, pandas as pd;

###############################################################################
############################## Problem 2 - 3D Graph Slam ######################
###############################################################################

class read_txt():
    def __init__(self):
        writer = pd.ExcelWriter('exported_data.xlsx', engine = 'xlsxwriter');

        # load ground truth
        self.load_gt(); 

        # for each test pair, do analysis
        out_ate_rmse_lst = []; out_sum_ate_lst = []; 
        out_rpe_rmse_lst = []; out_sum_rpe_lst = []; 
        dir_lst = os.listdir('../data/output');
        for dir_n in dir_lst:
            if dir_n[0] != 'T':
                continue;
            test_id = dir_n;

            # ate read and consolidate data
            grand_sum = 0; grand_sample = 0;
            for txt_fnamae in glob.glob('../data/output/' + dir_n + '/ate/*.txt'):
                with open(txt_fnamae) as txtfile:
                    for ln_num, dat in enumerate(txtfile):
                        if ln_num == 9:
                            rmse = dat.split('\t')[-1];
                traj_id = txt_fnamae[-6:-4];
                out_ate_rmse_lst.append([test_id, traj_id, rmse]);

                grand_sum += float(rmse)**2 * (self.gt_len[traj_id] - 1); 
                grand_sample += (self.gt_len[traj_id] - 1);
            out_sum_ate_lst.append([test_id, grand_sum, grand_sample]);


            # rpe read and consolidate data
            grand_sum = 0; grand_sample = 0;
            for txt_fnamae in glob.glob('../data/output/' + dir_n + '/rpe/*.txt'):
                with open(txt_fnamae) as txtfile:
                    for ln_num, dat in enumerate(txtfile):
                        if ln_num == 9:
                            rmse = dat.split('\t')[-1];
                traj_id = txt_fnamae[-6:-4];

                out_rpe_rmse_lst.append([test_id, traj_id, rmse]);
                grand_sum += float(rmse)**2 * (self.gt_len[traj_id] - 1); 
                grand_sample += (self.gt_len[traj_id] - 1);
            out_sum_rpe_lst.append([test_id, grand_sum, grand_sample]);

        self.save_to_file(writer, out_ate_rmse_lst, out_sum_ate_lst, 
            code = 'ATE');
        self.save_to_file(writer, out_rpe_rmse_lst, out_sum_rpe_lst, 
            code = 'RPE');
        writer.save();
 
    def load_gt(self):
        # read all ground truth files 
        gt_dict = {}; gt_len = {};
        for txt_fnamae in glob.glob('../data/dataset/poses/*.txt'):
            with open(txt_fnamae) as f:
                dat = csv.reader(f, delimiter = ' '); 
                dat_arr = np.asarray([r for r in dat]).astype(float);
                gt_dict[txt_fnamae.split('.')[0][-2:]] = dat_arr;
                gt_len[txt_fnamae.split('.')[0][-2:]] = len(dat_arr);

        # return class object
        self.gt_dict = gt_dict; self.gt_len = gt_len;

    # extract trajectory from data
    def t_from_dat(self, data):
        return(data[:, [3, 7, 11]]);

    def save_to_file(self, writer, out_lst, sum_lst, code = 'ATE'):
        # send to excel file
        out_arr = np.asarray(out_lst);
        df = pd.DataFrame({
            'test_id': out_arr[:,0], 
            'traj_id': out_arr[:,1], 
            code: out_arr[:,2]});

        # make row = test pair name, column = KITTI sequence id
        unmelt_df = df.pivot(index = 'test_id', 
            columns = 'traj_id').astype('float');

        # add sum of RMSE, by square all data, times number of sample
        # then add across diff sequence, divide by total sample, and sqrt
        sum_arr = np.asarray(sum_lst);
        df = pd.DataFrame({
            'test_id': sum_arr[:,0], 
            'All_'+code : np.sqrt( np.asarray(sum_arr[:,1]).astype(float) / np.asarray(sum_arr[:,2]).astype(float))});
        df = df.set_index('test_id');
        unmelt_df = unmelt_df.join(df);

        # save it
        unmelt_df.to_excel(writer, sheet_name = code + '_rmse_each_traj');

        # now, take only the grand rmse sum, make a square table to compare between descriptor and detector. 
        test_id = list(unmelt_df.index);
        df2 = pd.DataFrame({
            'Detector': [t.split('_')[1] for t in test_id], 
            'Descriptor': [t.split('_')[2] for t in test_id], 
            code: unmelt_df['All_'+code]});

        unmelt_df = df2.pivot(index = 'Detector', columns = 'Descriptor');

        # save it
        unmelt_df.to_excel(writer, sheet_name = code + '_rmse_square');

    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        pass

    def __del__(self):
        pass

###############################################################################
############################## MAIN FUNCTION ##################################
###############################################################################
def main():
    ###########################################################################
    ############################## PARAMETERS #################################
    ###########################################################################

    ###########################################################################
    ############################## CODE SECTION ###############################
    ###########################################################################
    ############ Do not change, unless you know what you are doing ############
    rt = read_txt();

if __name__ == '__main__':
    main();
