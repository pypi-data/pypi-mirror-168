# -*- coding: utf-8 -*-

from hbshare.fe.asset_allocation.mean_variance_solver import MaxReturn, MinRisk
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class EF:
    def __init__(self, asset_list, ret, cov, risk_free_rate, lb_list, ub_list, total_weight, weight):
        self.asset_list = asset_list
        self.ret = np.matrix(ret)
        self.cov = np.matrix(cov)
        self.target_risk = 99
        self.target_return = -99
        self.risk_free_rate = risk_free_rate
        self.lb_list = lb_list
        self.ub_list = ub_list
        self.total_weight = total_weight
        self.weight = weight
        self.w_star = self.weight[self.asset_list].T if len(self.weight.dropna()) > 0 else None

    def solve(self):
        # 最小方差组合（最左侧点）
        min_weight, min_status = MinRisk(self.asset_list, self.ret, self.cov, self.target_return, self.lb_list, self.ub_list, self.total_weight).solve()
        if min_status == 'optimal':
            min_ret = (np.matrix(pd.DataFrame(min_weight).loc[self.asset_list]).T * self.ret)[0, 0]
        else:
            min_ret = self.ret.mean()
        # 最大收益组合（最上侧点）
        max_weight, max_status = MaxReturn(self.asset_list, self.ret, self.cov, self.target_risk, self.lb_list, self.ub_list, self.total_weight).solve()
        if max_status == 'optimal':
            max_ret = (np.matrix(pd.DataFrame(max_weight).loc[self.asset_list]).T * self.ret)[0, 0]
        else:
            max_ret = self.ret.max()
        # 有效前沿曲线
        delta = ((max_ret - min_ret) / 20.0) - 1e-8
        ret_list = [min_ret] + [(min_ret + delta * i) for i in range(1, 20)] + [max_ret]
        weight_P, sigma_P, r_P = [], [], []
        for ret in ret_list:
            weight, status = MinRisk(self.asset_list, self.ret, self.cov, ret, self.lb_list, self.ub_list, self.total_weight).solve()
            if status == 'optimal':
                weight = pd.DataFrame(weight).loc[self.asset_list]
            else:
                weight = pd.DataFrame(index=self.asset_list, columns=[0], data=np.nan)
            sigma2 = (np.matrix(weight).T * self.cov * np.matrix(weight))[0, 0]
            sigma = np.sqrt(sigma2)
            r = (np.matrix(weight).T * self.ret)[0, 0]
            weight_P.append(weight)
            sigma_P.append(sigma)
            r_P.append(r)
        # 优化组合
        if self.w_star is not None:
            sigma2_star = (np.matrix(self.w_star).T * self.cov * np.matrix(self.w_star))[0, 0]
            sigma_star = np.sqrt(sigma2_star)
            r_star = (np.matrix(self.w_star).T * self.ret)[0, 0]
        else:
            sigma_star = np.nan
            r_star = np.nan
        # # 有效前沿曲线绘制
        # plt.figure(figsize=(6, 6))
        # plt.plot(sigma_P, r_P, 'o-', color='#F04950')
        # plt.plot(sigma_star, r_star, 'o', color='#6268A2')
        # plt.show()

        # 数据结果
        ef_weight = pd.concat(weight_P, axis=1).T
        ef_weight.index = range(len(ef_weight))
        ef_weight.loc[:, 'cash'] = 1.0 - ef_weight.sum(axis=1)
        ef_weight.loc['result', :] = self.weight.iloc[0]
        sigma = pd.DataFrame(sigma_P)
        sigma.columns = ['sigma']
        sigma.loc['result', 'sigma'] = sigma_star
        r = pd.DataFrame(r_P)
        r.columns = ['r']
        r.loc['result', 'r'] = r_star
        ef_weight = pd.concat([ef_weight, sigma, r], axis=1)
        return ef_weight