import datetime
import pandas as pd
import numpy as np
from hbshare.fe.XZ import db_engine
from hbshare.fe.XZ import functionality
from scipy import interpolate
import  os

util=functionality.Untils()
hbdb=db_engine.HBDB()
plot=functionality.Plot(1000,600)
localdb=db_engine.PrvFunDB().engine

class FOF_analysis:

    def __init__(self,dir,end_date):

        raw_df=pd.read_excel(dir)
        # remove '未定义',keep 审核通过 take
        raw_df = raw_df[(raw_df['审核状态'] == '审核通过') & (raw_df['投资类型'] != '未定义')]

        raw_df['交易日期'] = raw_df['交易日期'].astype(str).str.replace('-', '')
        raw_df = raw_df[raw_df['交易日期'] <= end_date]

        self.trading_flow=raw_df
        self.prv_jjflmap= dict(zip(['c','d','b','Z','1','2','3','4','5','7','8','0'], ['其他','多策略','多空仓型','组合型','股票型'
                                    ,'债券型','货币型','宏观策略','市场中性','套利型','管理期货','其他']))
        self.prv_ejflmap =dict(zip(['Z001','Z002','c005','c006','c007','1001','1002','2001','2002','2003','2004','8003','8004','8005','8006','0'
                     ],['MOM','FOF','其他策略','期权策略','其他衍生品','主观多头','量化多头','纯债策略','强债策略','转债策略','债券其他','量化趋势','量化套利','管理期货复合','主观CTA','其他'
                     ]))
        self.mu_jjflmap= dict(zip(['1', '2', '3','0'], ['股票型', '债券型', '混合型','其他']))
        self.mu_ejflmap =dict(zip(['13', '14', '15', '16', '21', '22', '23', '24', '25', '26', '27', '28', '34', '35', '36', '37',
                     '38',
                     '41', '42','0'
                     ],['普通股票型', '股票型', '增强指数型', '被动指数型', '被动指数型债券', '短期纯债型', '混合债券型一级', '混合债券型二级', '增强指数型债券', '债券型',
                     '中长期纯债型',
                     '可转换债券型', '平衡混合型', '灵活配置型', '混合型', '偏股混合型', '偏债混合型', '股票多空', '商品型','其他'
                     ]))

    def fromtrading2holding(self,start_date=None):

        if(start_date is None):
            start_date='0'

        # read trading details

        raw_df = self.trading_flow


        raw_df=pd.merge(raw_df.drop_duplicates(['产品名称','投资基金代码','交易日期','指令类型'])[['产品名称', '投资基金'
            , '投资基金代码', '指令类型', '投资类型', '交易日期', '确认净值','审核状态']]
                        ,raw_df.groupby(['产品名称','投资基金代码','交易日期','指令类型']).sum()[['认申购金额','赎回份额','赎回费']].reset_index()
                        ,how='inner',on=['产品名称','投资基金代码','交易日期','指令类型'])

        #combine the same action happend in one day


        for product in raw_df['产品名称'].unique():
            df = raw_df[raw_df['产品名称'] == product]
            df = df.sort_values('交易日期')
            nav_df = pd.read_excel(r"E:\FOF分析\{}基金净值数据.xls".format(product))
            nav_df['日期'] = nav_df['日期'].astype(str).str.replace('-', '')
            nav_df = nav_df.sort_values('日期')
            date_list = nav_df['日期'].tolist()
            hold_df = []

            for i in range(len(date_list)):

                date = date_list[i]

                buy = df[(df['投资类型'] == '申购') & (df['交易日期'] == date)][['投资基金代码', '认申购金额', '确认净值']]
                sell = df[(df['投资类型'] == '赎回') & (df['交易日期'] == date)][['投资基金代码', '赎回份额', '确认净值', '赎回费']]

                if (i == 0):
                    tempdf = pd.DataFrame(columns=['date', 'jjdm', 'quant', 'cbprice','buyprice', 'sellprice'])
                    tempdf['date'] = [date]
                else:
                    tempdf = hold_df[i - 1].copy()

                # buy
                if (len(buy) > 0):
                    buy['buy_quant'] = buy['认申购金额'] / buy['确认净值']

                    tempdf = pd.merge(tempdf, buy[['投资基金代码', 'buy_quant', '确认净值']]
                                      , how='outer', left_on='jjdm', right_on='投资基金代码')

                    tempdf.loc[tempdf['buy_quant'].notnull(), 'cbprice'] = ((tempdf.loc[tempdf['buy_quant'].notnull()][
                                                                             'cbprice']*tempdf.loc[tempdf['buy_quant'].notnull()][
                                                                             'quant']).fillna(0)+tempdf.loc[tempdf['buy_quant'].notnull()][
                                                                             '确认净值']*tempdf.loc[tempdf['buy_quant'].notnull()][
                                                                             'buy_quant'])/\
                                                                           (tempdf.loc[tempdf['buy_quant'].notnull()][
                                                                             'quant'].fillna(0)+tempdf.loc[tempdf['buy_quant'].notnull()][
                                                                             'buy_quant'])

                    tempdf.loc[tempdf['buy_quant'].notnull(), 'quant'] = tempdf.loc[tempdf['buy_quant'].notnull()][
                                                                             'quant'].fillna(0) \
                                                                         + tempdf.loc[tempdf['buy_quant'].notnull()][
                                                                             'buy_quant']
                    tempdf.loc[tempdf['buy_quant'].notnull(), 'jjdm'] = tempdf.loc[tempdf['buy_quant'].notnull()][
                        '投资基金代码']
                    tempdf.loc[tempdf['buy_quant'].notnull(), 'buyprice'] = tempdf.loc[tempdf['buy_quant'].notnull()][
                        '确认净值']

                    tempdf.drop(['buy_quant', '投资基金代码', '确认净值'], axis=1, inplace=True)
                    tempdf = tempdf[tempdf['jjdm'].notnull()]
                # sell
                if (len(sell) > 0):
                    tempdf = pd.merge(tempdf, sell[['投资基金代码', '赎回份额', '确认净值']]
                                      , how='left', left_on='jjdm', right_on='投资基金代码')

                    tempdf.loc[tempdf['赎回份额'].notnull(), 'cbprice'] = ((tempdf.loc[tempdf['赎回份额'].notnull()][
                                                                             'cbprice']*tempdf.loc[tempdf['赎回份额'].notnull()][
                                                                             'quant']).fillna(0)-tempdf.loc[tempdf['赎回份额'].notnull()][
                                                                             '确认净值']*tempdf.loc[tempdf['赎回份额'].notnull()][
                                                                             '赎回份额'])/\
                                                                           (tempdf.loc[tempdf['赎回份额'].notnull()][
                                                                             'quant'].fillna(0)-tempdf.loc[tempdf['赎回份额'].notnull()][
                                                                             '赎回份额'])


                    tempdf.loc[tempdf['赎回份额'].notnull(), 'quant'] = tempdf.loc[tempdf['赎回份额'].notnull()][
                                                                        'quant'].fillna(0) \
                                                                    - tempdf.loc[tempdf['赎回份额'].notnull()]['赎回份额']
                    #if left quant<100,make it 0
                    tempdf.loc[(tempdf['赎回份额'].notnull())&(tempdf['quant']<=100), 'quant']=0

                    tempdf.loc[tempdf['赎回份额'].notnull(), 'sellprice'] = tempdf.loc[tempdf['赎回份额'].notnull()]['确认净值']
                    tempdf.drop(['赎回份额', '投资基金代码', '确认净值'], axis=1, inplace=True)

                tempdf['date'] = date

                if(date==start_date ):

                    gzb=pd.read_excel(r"E:\FOF分析\{0}\{1}\{2}_(SNQ525)新方程大类配置稳健型私募证券投资基金_基金估值表.xls"
                                      .format(product,start_date[0:6]
                            ,start_date[0:4]+"-"+start_date[4:6]+"-"+start_date[6:8])).iloc[2:-3]
                    gzb.columns=gzb.iloc[0]
                    gzb=gzb[((gzb['科目代码'].astype(str).str.startswith('11050201'))
                            |(gzb['科目代码'].astype(str).str.startswith('11090601')))&
                            ((gzb['科目代码'].astype(str)!='11090601')
                            &(gzb['科目代码'].astype(str)!='11050201'))][['科目代码','科目名称','市价']]

                    gzb.loc[(gzb['科目代码'].str.startswith('11090601'))
                            &(~gzb['科目代码'].str.startswith('11090601S')), '科目代码'] ="S"+ \
                        gzb[(gzb['科目代码'].str.startswith('11090601'))
                            &(~gzb['科目代码'].str.startswith('11090601S'))]['科目代码'].str[-6:-1]

                    gzb['科目代码']=gzb['科目代码'].str[-6:-1]
                    tempdf['科目代码']=tempdf['jjdm'].astype(str).str[-6:-1]
                    tempdf=pd.merge(tempdf,gzb,how='left',on='科目代码')
                    tempdf['cbprice']=tempdf['市价']
                    tempdf.drop(['科目名称','市价','科目代码'],axis=1,inplace=True)
                    tempdf=tempdf[tempdf['quant']!=0]

                hold_df.append(tempdf)

            hold_df = pd.concat(hold_df, axis=0)
            hold_df = pd.merge(hold_df, nav_df[['日期', '资产净值', '资产份额', '单位净值']]
                               , how='left', left_on='date', right_on='日期')
            hold_df['jjdm']=[("000000"+x)[-6:] for x in hold_df['jjdm'].astype(str).tolist()]
            jjdm_list = hold_df['jjdm'].unique().tolist()

            # get prv list and mutual list
            sql = "select jjdm,jjjc,cpfl,jjfl,ejfl from st_fund.t_st_gm_jjxx where jjdm in ({}) and cpfl='2'" \
                .format(util.list_sql_condition([("000000" + x)[-6:] for x in jjdm_list]))
            mutual_fund = hbdb.db2df(sql, db='funduser')

            sql = "select jjdm,jjjc,cpfl,jjfl,ejfl from st_hedge.t_st_jjxx where jjdm in ({}) and cpfl='4'" \
                .format(util.list_sql_condition(jjdm_list))
            prv_fund = hbdb.db2df(sql, db='highuser')
            #
            # sql="select jjdm,jjjc,cpfl,jjfl,ejfl from st_fixed.t_st_jjxx where jjdm in ({0}) "\
            #     .format(util.list_sql_condition(jjdm_list))
            # fix_fund=hbdb.db2df(sql, db='fixeduser')

            # read fund nav from DB

            # for prv fund
            sql = "select jjdm,jzrq,jjjz from st_hedge.t_st_jjjz where jjdm in ({0}) and jzrq>='{1}' and jzrq<='{2}'" \
                .format(util.list_sql_condition(prv_fund['jjdm'].tolist()), date_list[0], date_list[-1])
            prv_nav = hbdb.db2df(sql, db='highuser')

            # for mutual fund
            sql = "select jjdm,jzrq,jjjz from st_fund.t_st_gm_jjjz where jjdm in ({0}) and jzrq>='{1}' and jzrq<='{2}'" \
                .format(util.list_sql_condition(mutual_fund['jjdm'].tolist()), date_list[0], date_list[-1])
            mutual_nav = hbdb.db2df(sql, db='funduser')
            mutual_nav['jzrq'] = mutual_nav['jzrq'].astype(str)

            hold_nan = hold_df[hold_df['jjdm'].isin(list((set(hold_df['jjdm'].unique()).difference(set(mutual_fund['jjdm'].tolist()))).difference(set(prv_fund['jjdm'].tolist()))))]

            hold_df_mu = pd.merge(hold_df[hold_df['jjdm'].isin(mutual_fund['jjdm'].tolist())], mutual_nav
                                  , how='left', left_on=['jjdm', 'date'], right_on=['jjdm', 'jzrq'])
            hold_df_mu=pd.merge(hold_df_mu,mutual_fund,how='left',on='jjdm')

            hold_df_prv = pd.merge(hold_df[hold_df['jjdm'].isin(prv_fund['jjdm'].tolist())], prv_nav
                                   , how='left', left_on=['jjdm', 'date'], right_on=['jjdm', 'jzrq'])
            hold_df_prv=pd.merge(hold_df_prv,prv_fund,how='left',on='jjdm')

            hold_df = pd.concat([hold_nan, hold_df_prv], axis=0)
            hold_df = pd.concat([hold_df, hold_df_mu], axis=0).sort_values('date').drop(['jzrq', '日期'], axis=1)

            hold_df.to_excel(r"E:\FOF分析\{}基金持仓数据.xlsx".format(product), index=False)

            print(product + ' Done ')

    def fund_attribution(self,hold_df,if_prv):

        if(if_prv):
            # prv ret
            mu_df = hold_df[hold_df['cpfl'] == '私募基金']
            mu_df['ejfl'] = mu_df['ejfl'].fillna(0).astype(int).astype(str)
            mu_df['jjfl'] = mu_df['jjfl'].fillna(0).astype(str).str.replace('.0','')
            jjfl_map = self.prv_jjflmap
            for index in jjfl_map.keys():
                mu_df.loc[mu_df['jjfl'] == index, 'jjfl'] = jjfl_map[index]
            ejfl_map = self.prv_ejflmap
            for index in ejfl_map.keys():
                mu_df.loc[mu_df['ejfl'] == index, 'ejfl'] = ejfl_map[index]
        else:

            # mutual ret
            mu_df = hold_df[hold_df['cpfl'] == '公募基金']
            mu_df['ejfl'] = mu_df['ejfl'].astype(int).astype(str)
            mu_df['jjfl'] = mu_df['jjfl'].fillna(0).astype(int).astype(str)
            jjfl_map = self.mu_jjflmap
            for index in jjfl_map.keys():
                mu_df.loc[mu_df['jjfl'] == index, 'jjfl'] = jjfl_map[index]
            ejfl_map = self.mu_ejflmap
            for index in ejfl_map.keys():
                mu_df.loc[mu_df['ejfl'] == index, 'ejfl'] = ejfl_map[index]

        mu_df['资产净值']=mu_df['资产净值'].astype(str).str.replace(',','').astype(float)
        snapshot = mu_df[mu_df['date'] == mu_df['date'].max()]

        # plot.plotly_pie(snapshot.groupby('jjfl').count()['jjdm'], '私募基金一级分类分布')
        # plot.plotly_pie(snapshot.groupby('ejfl').count()['jjdm'], '私募基金二级分类分布')

        nrel_ret = snapshot[snapshot['quant'] != 0]
        nrel_ret['revenue'] = (nrel_ret['jjjz'] - nrel_ret['cbprice'])*nrel_ret['quant']
        nrel_ret['ret']=nrel_ret['jjjz']/nrel_ret['cbprice']-1
        nrel_ret['cb_w']=(nrel_ret['cbprice']*nrel_ret['quant'])/nrel_ret['资产净值']
        nrel_ret['cb']=(nrel_ret['cbprice']*nrel_ret['quant'])

        nrel_ret['rel'] = False

        rel_ret = mu_df[mu_df['quant'] == 0].drop_duplicates(['jjdm', 'sellprice'])[['jjdm','date','sellprice']]
        if (len(rel_ret) > 0):
            for row in rel_ret.index:
                rel_ret.loc[row,'cbprice']=mu_df[(mu_df['jjdm']==rel_ret.loc[row]['jjdm'])
                            &(mu_df['date']<rel_ret.loc[row]['date'])].iloc[-1]['cbprice']
                rel_ret.loc[row,'sellquant']=mu_df[(mu_df['jjdm']==rel_ret.loc[row]['jjdm'])
                            &(mu_df['date']<rel_ret.loc[row]['date'])].iloc[-1]['quant']
                rel_ret.loc[row,'资产净值']=mu_df[(mu_df['jjdm']==rel_ret.loc[row]['jjdm'])
                            &(mu_df['date']==rel_ret.loc[row]['date'])].iloc[-1]['资产净值']

            rel_ret['revenue'] = rel_ret['sellquant'] * (rel_ret['sellprice'] - rel_ret['cbprice'])
            rel_ret['ret']=rel_ret['sellprice']/ rel_ret['cbprice']-1
            rel_ret['cb_w'] = (rel_ret['cbprice']* rel_ret['sellprice'])/ rel_ret['资产净值']
            rel_ret['cb'] = (rel_ret['cbprice']* rel_ret['sellprice'])

        else:
            rel_ret['revenue']=0
            rel_ret['ret'] = 0
            rel_ret['cb_w'] = 0
            rel_ret['cb'] = 0

        rel_ret=pd.merge(rel_ret[['jjdm','revenue','ret','cb_w','cb']]
                             ,mu_df.drop_duplicates(['jjdm', 'cpfl'])[['jjdm', 'jjjc', 'cpfl', 'jjfl', 'ejfl']]
                             ,how='left',on='jjdm')
        rel_ret['rel']=True

        return [rel_ret, nrel_ret]

    @staticmethod
    def attribution_by_class(fund_attribution):

        cpfl_att = fund_attribution.groupby('cpfl').sum()[['revenue', 'ret_times_w', 'cb_w', 'cb']]
        known_tr = abs(cpfl_att['revenue'].sum())
        plot.plotly_jjpic_bar(cpfl_att[['revenue']] / known_tr, '公私募基金收益分布')
        cpfl_att['ret'] = cpfl_att['ret_times_w'] / cpfl_att['cb_w']
        plot.plotly_jjpic_bar(cpfl_att[['ret']], '公私募基金收益率分布')

        attack_asset_jjfl = ['股票型', '混合型']
        CTA_asset_jjfl = ['管理期货']
        statrage_att = \
            fund_attribution[fund_attribution['jjfl'].isin(attack_asset_jjfl
                                                           + CTA_asset_jjfl)].groupby('jjfl').sum()[
                ['revenue', 'ret_times_w', 'cb_w', 'cb']]
        plot.plotly_jjpic_bar(statrage_att[['revenue']] / abs(statrage_att['revenue'].sum()), '超一级策略收益分布')
        statrage_att['ret'] = statrage_att['revenue'] / statrage_att['cb']
        plot.plotly_jjpic_bar(statrage_att[['ret']], '超一级策略收益率分布')

        fund_attribution = pd.concat([fund_attribution
                                         , statrage_att.reset_index().rename(columns={'jjfl': 'jjdm'})], axis=0)

        stock_asset_jjfl = ['主观多头', '量化多头', '指数增强型', '偏股混合型', '灵活配置型', '普通股票型']
        fund_attribution.loc[(fund_attribution['ejfl'] == '量化多头')
                             & ((fund_attribution['jjjc'].str.contains('指数') | (
            fund_attribution['jjjc'].str.contains('指增')))), 'ejfl'] = '指数增强型'

        plot.plotly_jjpic_bar(fund_attribution[fund_attribution['ejfl'].isin(stock_asset_jjfl
                                                                   )].groupby('ejfl').count()['jjdm'].to_frame('持仓数量').sort_values('持仓数量',ascending=False)
                        , '进攻性资产数量分布')

        stock_att = fund_attribution[fund_attribution['ejfl'].isin(stock_asset_jjfl
                                                                   )].groupby('ejfl').sum()[
            ['revenue', 'ret_times_w', 'cb_w', 'cb']]

        plot.plotly_pie(stock_att[['cb_w']],'进攻性资产持仓成本分布')
        plot.plotly_jjpic_bar(stock_att[['revenue']] / abs(stock_att['revenue'].sum()), '进攻性资产收益分布')
        stock_att['ret'] = stock_att['revenue'] / stock_att['cb']
        plot.plotly_jjpic_bar(stock_att[['ret']], '进攻性资产收益率分布')
        fund_attribution = pd.concat([fund_attribution
                                         , stock_att.reset_index().rename(columns={'ejfl': 'jjdm'})], axis=0)

        index_enhance_att = fund_attribution[fund_attribution['ejfl'] == '指数增强型']
        for type in ['300', '500', '1000']:
            index_enhance_att.loc[index_enhance_att['jjjc'].str.contains(type)
            , 'index_enhance_type'] = type + 'zz'
        index_enhance_att = index_enhance_att.groupby('index_enhance_type').sum()[
            ['revenue', 'ret_times_w', 'cb_w', 'cb']]
        index_enhance_att['ret'] = index_enhance_att['revenue'] / index_enhance_att['cb']
        fund_attribution = pd.concat([fund_attribution
                                         ,
                                      index_enhance_att.reset_index().rename(columns={'index_enhance_type': 'jjdm'})],
                                     axis=0)
        return  fund_attribution

    @staticmethod
    def generate_index_enhance_index(start_date,end_date):

        quant_pool_in = \
        pd.read_excel(r"C:\Users\xuhuai.zhe\Documents\WXWork\1688858146292774\Cache\File\2022-08\私募量化基金池 - 202207.xlsx"
                      , sheet_name='量化池列表')[['入池时间', '基金代码', '二级策略']]
        quant_pool_out = \
        pd.read_excel(r"C:\Users\xuhuai.zhe\Documents\WXWork\1688858146292774\Cache\File\2022-08\私募量化基金池 - 202207.xlsx"
                      , sheet_name='出池记录')[['入池时间', '基金代码', '出池时间', '二级策略']]
        quant_pool = pd.concat([quant_pool_out, quant_pool_in], axis=0)
        quant_pool = quant_pool[(quant_pool['二级策略'].isin(['500指数增强', '1000指数增强', '300指数增强']))]
        quant_pool['入池时间'] = quant_pool['入池时间'].astype(str).str.replace('-', '').str[0:6]
        quant_pool['出池时间'] = quant_pool['出池时间'].astype(str).str.replace('-', '').str[0:6]
        quant_pool.drop_duplicates('基金代码', inplace=True)

        sql = "select jjdm,hb1y,tjyf from st_hedge.t_st_sm_yhb where jjdm in ({0}) and tjyf>='{1}' and tjyf<='{2}' and hb1y!=99999" \
            .format(util.list_sql_condition(quant_pool['基金代码'].tolist())
                    ,start_date,end_date)
        quant_pool_nav = hbdb.db2df(sql, db='highuser')
        quant_pool_nav = pd.merge(quant_pool_nav, quant_pool, how='left'
                                  , left_on='jjdm', right_on='基金代码')
        quant_pool_nav = quant_pool_nav[(quant_pool_nav['入池时间'] < quant_pool_nav['tjyf'])
                                        & (quant_pool_nav['出池时间'] >= quant_pool_nav['tjyf'])]
        quant_pool_nav = quant_pool_nav.groupby(['二级策略', 'tjyf']).mean()['hb1y'].to_frame('量化池') / 100

        quant_pool_nav=quant_pool_nav.reset_index().pivot_table('量化池', 'tjyf', '二级策略')

        return (quant_pool_nav+1).cumprod()

    def get_bmk_return(self,start_date,end_date):

        sql = """select zsdm,jyrq,spjg from st_hedge.t_st_sm_zhmzs 
        where jyrq>='{0}' and jyrq<='{1}' and zsdm in ('HB0018','HB1001','HB1002')""" \
            .format(start_date, end_date)

        howbuy_index_ret = hbdb.db2df(sql, db='highuser').pivot_table('spjg', 'jyrq', 'zsdm')


        # get market mutual index return

        sql = """select zqdm,jyrq,spjg from st_market.t_st_zs_hqql 
        where jyrq>='{0}' and jyrq<='{1}' and zqdm in ('885001')""" \
            .format(start_date, end_date)

        mu_index_ret = hbdb.db2df(sql, db='alluser').pivot_table('spjg', 'jyrq', 'zqdm')


        index_enhance_index = \
            self.generate_index_enhance_index(str(start_date)[0:6]
                                              , str(end_date)[0:6])

        return  howbuy_index_ret,mu_index_ret,index_enhance_index

    @staticmethod
    def brinson_wise_analysis(fund_attribution,howbuy_index_ret
                              , mu_index_ret, index_enhance_index):

        return_table_list=[]

        #calculate ideal asset weight by BLM assumption that all asset allocation submit to mean variance model

        prv_stock_ret= \
            (np.power((howbuy_index_ret['HB1001'].iloc[-1]/ howbuy_index_ret['HB1001'].iloc[0])
                     ,len(howbuy_index_ret)/52)-1)

        mu_stock_ret= \
            (np.power((mu_index_ret['885001'].iloc[-1]/ mu_index_ret['885001'].iloc[0])
                     ,len(mu_index_ret)/250)-1)

        prv_quant_ret= \
            (np.power((howbuy_index_ret['HB1002'].iloc[-1]/ howbuy_index_ret['HB1002'].iloc[0])
                     ,len(howbuy_index_ret)/52)-1)

        if (prv_stock_ret < 0 or mu_stock_ret < 0 or prv_quant_ret < 0):

            min_ret=np.min([prv_stock_ret,mu_stock_ret,prv_quant_ret])
            prv_stock_ret=prv_stock_ret-min_ret+0.03
            mu_stock_ret = mu_stock_ret - min_ret+0.03
            prv_quant_ret = prv_quant_ret - min_ret+0.03


        prv_stock_sharp= \
            prv_stock_ret/\
            (howbuy_index_ret['HB1001'].pct_change().std()*np.sqrt(52))

        mu_stock_sharp= \
            mu_stock_ret/\
            (mu_index_ret['885001'].pct_change().std()*np.sqrt(250))

        prv_quant_sharp= \
            prv_quant_ret/\
            (howbuy_index_ret['HB1002'].pct_change().std()*np.sqrt(52))


        total_sharp=prv_stock_sharp+mu_stock_sharp+prv_quant_sharp
        prv_stock_bmk_w=prv_stock_sharp/total_sharp
        mu_stock_bmk_w = mu_stock_sharp / total_sharp
        prv_quant_bmk_w = prv_quant_sharp / total_sharp

        howbuy_index_ret = howbuy_index_ret.iloc[-1] / howbuy_index_ret.iloc[0] - 1
        mu_index_ret = mu_index_ret.iloc[-1] / mu_index_ret.iloc[0] - 1
        index_enhance_index=(index_enhance_index.iloc[-1]-1).to_frame('ret')

        # equit asset return reasoning

        equit_att = \
            fund_attribution[fund_attribution['jjdm'].isin(['主观多头'
                                                               , '量化多头', '指数增强型', '偏股混合型', '灵活配置型', '普通股票型'])][
                ['jjdm', 'ret', 'cb_w']]

        equit_att.loc[equit_att.index[-1] + 1] = np.array(['量化股票'
                                                              , (equit_att['ret'] * equit_att['cb_w']).loc[
                                                               equit_att['jjdm'].isin(['量化多头', '指数增强型'])].sum() /
                                                           equit_att['cb_w'].loc[
                                                               equit_att['jjdm'].isin(['量化多头', '指数增强型'])].sum()
                                                              , equit_att['cb_w'].loc[
                                                               equit_att['jjdm'].isin(['量化多头', '指数增强型'])].sum()])
        equit_att[['ret', 'cb_w']] = equit_att[['ret', 'cb_w']].astype(float)

        equit_att.loc[equit_att.index[-1] + 1] = np.array(['公募偏股'
                                                              , (equit_att['ret'] * equit_att['cb_w']).loc[
                                                               equit_att['jjdm'].isin(
                                                                   ['灵活配置型', '偏股混合型', '普通股票型'])].sum() /
                                                           equit_att['cb_w'].loc[equit_att['jjdm'].isin(
                                                               ['灵活配置型', '偏股混合型', '普通股票型'])].sum()
                                                              , equit_att['cb_w'].loc[equit_att['jjdm'].isin(
                ['灵活配置型', '偏股混合型', '普通股票型'])].sum()])
        equit_att[['ret', 'cb_w']] = equit_att[['ret', 'cb_w']].astype(float)

        equit_att.loc[equit_att['jjdm'] == '主观多头', 'index_ret'] = howbuy_index_ret.loc['HB1001']
        equit_att.loc[equit_att['jjdm'] == '量化股票', 'index_ret'] = howbuy_index_ret.loc['HB1002']
        equit_att.loc[equit_att['jjdm'] == '公募偏股', 'index_ret'] = mu_index_ret.loc['885001']
        equit_att = equit_att[equit_att['index_ret'].notnull()]

        # arrange the bmk weight
        equit_att.loc[equit_att['jjdm'] == '主观多头', 'bmk_w'] = prv_stock_bmk_w
        equit_att.loc[equit_att['jjdm'] == '量化股票', 'bmk_w'] = prv_quant_bmk_w
        equit_att.loc[equit_att['jjdm'] == '公募偏股', 'bmk_w'] = mu_stock_bmk_w

        equit_att['cb_w'] = equit_att['cb_w'] / equit_att['cb_w'].sum()
        # return allocation
        total_extra_ret = (equit_att['ret'] * equit_att['cb_w']).sum() -(equit_att['index_ret'] * equit_att['bmk_w']).sum()
        allocation_extraret = ((equit_att['cb_w'] - equit_att['bmk_w']) * equit_att['index_ret']).sum()
        selection_extraret = (equit_att['bmk_w'] * (equit_att['ret'] - equit_att['index_ret'])).sum()
        other_extraret = ((equit_att['cb_w'] - equit_att['bmk_w']) * (equit_att['ret'] - equit_att['index_ret'])).sum()

        extra_ret_table = pd.DataFrame(index=['总超额', '资产配置/择时能力', '选基能力', '其他']
                                       , columns=['超额收益']
                                       ,
                                       data=[total_extra_ret, allocation_extraret, selection_extraret, other_extraret])
        return_table_list.append(extra_ret_table)
        extra_ret_table['超额收益'] = extra_ret_table['超额收益'].map("{:.2%}".format)
        plot.plotly_table(extra_ret_table.reset_index(drop=False), 500, '')


        # index enhance asset return reasoning
        index_enhance_att = \
            fund_attribution[fund_attribution['jjdm'].isin(['1000zz', '500zz', '300zz'])][['jjdm', 'ret', 'cb_w']]

        index_enhance_att.loc[index_enhance_att['jjdm'] == '1000zz', 'index_ret'] = index_enhance_index.loc['1000指数增强'][
            'ret']
        index_enhance_att.loc[index_enhance_att['jjdm'] == '500zz', 'index_ret'] = index_enhance_index.loc['500指数增强'][
            'ret']
        index_enhance_att.loc[index_enhance_att['jjdm'] == '300zz', 'index_ret'] = index_enhance_index.loc['300指数增强'][
            'ret']
        index_enhance_att = index_enhance_att[index_enhance_att['index_ret'].notnull()]

        # arrange the bmk weight
        index_enhance_att.loc[index_enhance_att['jjdm'] == '1000zz', 'bmk_w'] = 0.1
        index_enhance_att.loc[index_enhance_att['jjdm'] == '500zz', 'bmk_w'] = 0.8
        index_enhance_att.loc[index_enhance_att['jjdm'] == '300zz', 'bmk_w'] = 0.1

        index_enhance_att['cb_w'] = index_enhance_att['cb_w'] / index_enhance_att['cb_w'].sum()
        # return allocation
        total_extra_ret = (index_enhance_att['ret'] * index_enhance_att['cb_w']).sum() \
                          --(index_enhance_att['index_ret'] * index_enhance_att['bmk_w']).sum()
        allocation_extraret = (
                    (index_enhance_att['cb_w'] - index_enhance_att['bmk_w']) * index_enhance_att['index_ret']).sum()
        selection_extraret = (
                    index_enhance_att['bmk_w'] * (index_enhance_att['ret'] - index_enhance_att['index_ret'])).sum()
        other_extraret = ((index_enhance_att['cb_w'] - index_enhance_att['bmk_w']) * (
                    index_enhance_att['ret'] - index_enhance_att['index_ret'])).sum()

        extra_ret_table = pd.DataFrame(index=['总超额', '资产配置/择时能力', '选基能力', '其他']
                                       , columns=['超额收益']
                                       ,
                                       data=[total_extra_ret, allocation_extraret, selection_extraret, other_extraret])
        return_table_list.append(extra_ret_table)
        extra_ret_table['超额收益'] = extra_ret_table['超额收益'].map("{:.2%}".format)
        plot.plotly_table(extra_ret_table.reset_index(drop=False), 500, '')

        return  return_table_list

    @staticmethod
    def fund_lable_analysis(hold_df):

        hold_df['资产净值']=hold_df['资产净值'].astype(str).str.replace(',','').astype(float)


        def mutual_lable_analysis(hold_df):

            mu_lable=hold_df[(hold_df['cpfl']=='公募基金')
                             &(hold_df['ejfl'].isin([13,35,37]))][['date'
                ,'jjdm','jjjc','jjjz','quant','资产净值']]

            #read style lable from local db

            max_asofdate=pd.read_sql("select max(asofdate) as date from jjpic_value_p_hbs"
                                     ,con=localdb)['date'][0]
            sql="SELECT jjdm,`风格偏好`,`成长绝对暴露(持仓)`,`价值绝对暴露(持仓)` from jjpic_value_p_hbs where jjdm in ({0}) and  asofdate='{1}'"\
                .format(util.list_sql_condition(mu_lable['jjdm'].unique().tolist()),max_asofdate)
            value_pic=pd.read_sql(sql,con=localdb)

            sql="SELECT jjdm,`规模偏好`,`大盘绝对暴露(持仓)`,`中盘绝对暴露(持仓)`,`小盘绝对暴露(持仓)` from jjpic_size_p_hbs where jjdm in ({0}) and  asofdate='{1}'"\
                .format(util.list_sql_condition(mu_lable['jjdm'].unique().tolist()),max_asofdate)
            size_pic=pd.read_sql(sql,con=localdb)


            #read industry type lable from local db
            max_asofdate=pd.read_sql("select max(asofdate) as date from jjpic_industry_p"
                                     ,con=localdb)['date'][0]
            sql="SELECT jjdm,`一级行业类型` from jjpic_industry_p where jjdm in ({0}) and  asofdate='{1}'"\
                .format(util.list_sql_condition(mu_lable['jjdm'].unique().tolist()),max_asofdate)
            industry_pic=pd.read_sql(sql,con=localdb)

            mu_lable=pd.merge(mu_lable,value_pic,how='left',on='jjdm')
            mu_lable = pd.merge(mu_lable, size_pic, how='left', on='jjdm')
            mu_lable = pd.merge(mu_lable, industry_pic, how='left', on='jjdm')

            mu_lable['持仓权重']=mu_lable['quant']*mu_lable['jjjz']/mu_lable['资产净值']

            for col in ['成长绝对暴露(持仓)','价值绝对暴露(持仓)','大盘绝对暴露(持仓)', '中盘绝对暴露(持仓)', '小盘绝对暴露(持仓)']:
                mu_lable[col]=mu_lable[col]*mu_lable['持仓权重']

            value_pic=mu_lable.groupby(['date',
                                        '风格偏好']).sum()[['持仓权重']].reset_index().pivot_table('持仓权重','date','风格偏好').fillna(0)

            value_pic2=mu_lable.groupby('date').sum()[['成长绝对暴露(持仓)','价值绝对暴露(持仓)']]
            size_pic = mu_lable.groupby(['date'
                                            , '规模偏好']).sum()[['持仓权重']].reset_index().pivot_table('持仓权重','date','规模偏好').fillna(0)

            size_pic2 = mu_lable.groupby('date').sum()[['大盘绝对暴露(持仓)', '中盘绝对暴露(持仓)', '小盘绝对暴露(持仓)']]
            industry_pic = mu_lable.groupby(['date'
                                                , '一级行业类型']).sum()[['持仓权重']].reset_index().pivot_table('持仓权重','date','一级行业类型').fillna(0)


            return  value_pic,value_pic2,size_pic,size_pic2,industry_pic

        def prv_lable_analysis(hold_df):

            prv_lable = hold_df[(hold_df['cpfl'] == '私募基金')
                                & (hold_df['ejfl'].isin([1001]))][['date'
                , 'jjdm', 'jjjc', 'jjjz', 'quant', '资产净值']]

            file_name_list = os.listdir(r"E:\GitFolder\docs\净值标签")
            file_name_list.sort()
            fold_name = ''
            for name in file_name_list:
                if (name.startswith('全部私募打标结果')):
                    fold_name = name
                    break
            prv_pic = pd.read_excel(r"E:\GitFolder\docs\净值标签\{}".format(fold_name), sheet_name='数据')
            prv_lable = pd.merge(prv_lable, prv_pic[['jjdm', '大小盘', '成长价值']]
                                 , how='left', on='jjdm')
            return  prv_lable

        value_pic,value_pic2,size_pic,size_pic2,industry_pic=mutual_lable_analysis(hold_df)

        data, layout=plot.plotly_area(value_pic.T*100,'公募风格类型分布时序'
                                      ,range_upper=value_pic.sum(axis=1).max()*110)
        plot.plot_render(data, layout)

        data, layout=plot.plotly_area(value_pic2.T*100,'公募持仓打穿后成长价值分布'
                                      ,range_upper=value_pic2.sum(axis=1).max()*110)
        plot.plot_render(data, layout)

        data, layout=plot.plotly_area(size_pic.T*100, '公募市值类型分布时序'
                                      ,range_upper=size_pic.sum(axis=1).max()*110)
        plot.plot_render(data, layout)

        data, layout=plot.plotly_area(size_pic2.T*100,'公募持仓打穿后大中小盘分布'
                                      ,range_upper=size_pic2.sum(axis=1).max()*110)
        plot.plot_render(data, layout)

        data, layout=plot.plotly_area(industry_pic.T*100, '公募行业类型分布时序',
                                      range_upper=industry_pic.sum(axis=1).max()*110)
        plot.plot_render(data, layout)


    def holding_analysis(self,dir,start_date):

        hold_df=pd.read_excel(dir)
        if(start_date is not None):
            hold_df=hold_df[hold_df['date']>=int(start_date)]
        #mark prv fix income fund as prv
        hold_df.loc[(hold_df['cpfl'].isnull()) & (hold_df['jjdm'] != '000nan'), 'cpfl'] = 4
        hold_df.loc[hold_df['cpfl']==4,'cpfl']='私募基金'
        hold_df.loc[hold_df['cpfl'] == 2, 'cpfl'] = '公募基金'

        total_ret=hold_df[['date','资产净值','资产份额', '单位净值']].drop_duplicates('资产份额',keep='first')
        total_ret['quant_change']=total_ret['资产份额'].diff(1)
        total_ret['revenue']=total_ret['单位净值']*total_ret['quant_change']
        #fof_revenue=total_ret.iloc[-1]['资产净值']-total_ret.iloc[0]['资产净值']-total_ret['revenue'].sum()

        #ret distribution by prv and mutual

        prv_attribution=self.fund_attribution(hold_df,if_prv=True)
        mutual_attribution=self.fund_attribution(hold_df,if_prv=False)
        fund_attribution=[]
        for attr in [prv_attribution,mutual_attribution]:
            fund_attribution.append(attr[0][['jjdm','jjjc','cpfl','jjfl','ejfl','revenue','ret','cb_w','cb','rel']])
            fund_attribution.append(attr[1][['jjdm','jjjc','cpfl','jjfl','ejfl','revenue','ret','cb_w','cb','rel']])
        fund_attribution=pd.concat(fund_attribution,axis=0).reset_index(drop=True)

        fund_attribution['ret_times_w']=fund_attribution['ret']*fund_attribution['cb_w']

        fund_attribution=self.attribution_by_class(fund_attribution)

        howbuy_index_ret, mu_index_ret, index_enhance_index=self.get_bmk_return(hold_df['date'].iloc[0]
                                                                                ,hold_df['date'].iloc[-1])

        #fund_attribution.to_excel(dir.replace('基金持仓数据','基金收益贡献'),index=False)

        ret_table_list=self.brinson_wise_analysis(fund_attribution, howbuy_index_ret
                              , mu_index_ret, index_enhance_index)
        pd.concat(ret_table_list,axis=0).to_excel(dir.replace('基金持仓数据','brinsion能力拆解'))

        #self.fund_lable_analysis(hold_df)


    #trading analysis part

    def trade_date_preprocessing(self,weight_his_dir,hold_data_dir,start_date):

        #read stratage weight history data from local file

        stratage_weight_his=pd.read_excel(weight_his_dir)
        stratage_weight_his['日期']=stratage_weight_his['日期'].astype(str)
        stratage_weight_his=stratage_weight_his[stratage_weight_his['日期']>=start_date]
        stratage_weight_his.columns=[x.replace('(%)','占比') for x in stratage_weight_his.columns]
        stratage_weight_his['沪深300']=(stratage_weight_his['沪深300占比']+100)/100

        #get bmk index ret
        howbuy_index_ret,mu_index_ret,index_enhance_index=\
            self.get_bmk_return( stratage_weight_his['日期'].iloc[0]
                             ,stratage_weight_his['日期'].iloc[-1])
        mu_index_ret.index=mu_index_ret.index.astype(str)

        for col in howbuy_index_ret.columns:
            howbuy_index_ret[col]=howbuy_index_ret[col]/howbuy_index_ret[col].iloc[0]
        for col in mu_index_ret.columns:
            mu_index_ret[col]=mu_index_ret[col]/mu_index_ret[col].iloc[0]


        #read fund class info and FOF nav info
        hold_df = pd.read_excel(hold_data_dir)[['jjdm','cpfl','jjfl','ejfl']].drop_duplicates('jjdm',keep='last')
        hold_df.loc[hold_df['cpfl'].isnull(),'cpfl']=4
        fof_nav= pd.read_excel(hold_data_dir)[['date','资产净值','资产份额','单位净值']].drop_duplicates('date',keep='last')
        fof_nav['date']=fof_nav['date'].astype(str)
        for col in ['资产净值','资产份额','单位净值']:
            fof_nav[col]=\
                fof_nav[col].astype(str).str.replace(',','').astype(float)


        #read trading flow
        trading_detail=self.trading_flow[self.trading_flow['产品名称']==product]
        trading_detail=trading_detail[trading_detail['交易日期']>=start_date]
        trading_detail['投资基金代码']=trading_detail['投资基金代码'].astype(str)
        trading_detail=pd.merge(trading_detail,hold_df
                                ,how='left',left_on='投资基金代码',right_on='jjdm').drop('投资基金代码',axis=1)
        trading_detail=pd.merge(trading_detail,fof_nav
                                ,how='left',left_on='交易日期',right_on='date').drop('交易日期',axis=1)

        #data cleaning
        trading_detail.loc[(trading_detail['cpfl'].isnull())
                           &(trading_detail['投资基金'].str.startswith('CTA')),'jjfl']='8'
        trading_detail.loc[(trading_detail['cpfl'].isnull())
                           &(trading_detail['投资基金'].str.startswith('CTA')),'cpfl']=4
        trading_detail['ejfl']=trading_detail['ejfl'].fillna(0).astype(int).astype(str)
        trading_detail['jjfl'] = trading_detail['jjfl'].fillna(0).astype(str).str.replace('.0', '')
        trading_detail[['认申购金额','赎回份额','确认净值','单位净值']]=\
            trading_detail[['认申购金额','赎回份额','确认净值','单位净值']].astype(float)
        trading_detail['资产净值']=trading_detail['资产净值'].astype(str).str.replace(',', '').astype(float)
        trading_detail['资产份额']=trading_detail['资产份额'].astype(str).str.replace(',', '').astype(float)

        #rename the fund class name by chinese
        trading_detail.loc[trading_detail['cpfl']==4,'jjfl']\
            =[self.prv_jjflmap[x] for x in trading_detail[trading_detail['cpfl']==4]['jjfl']]
        trading_detail.loc[trading_detail['cpfl']==4,'ejfl']\
            =[self.prv_ejflmap[x] for x in trading_detail[trading_detail['cpfl']==4]['ejfl']]

        trading_detail.loc[trading_detail['cpfl']==2,'jjfl']\
            =[self.mu_jjflmap[x] for x in trading_detail[trading_detail['cpfl']==2]['jjfl']]
        trading_detail.loc[trading_detail['cpfl']==2,'ejfl']\
            =[self.mu_ejflmap[x] for x in trading_detail[trading_detail['cpfl']==2]['ejfl']]

        trading_detail.loc[trading_detail['投资类型']=='申购','change_w']\
            =trading_detail[trading_detail['投资类型']=='申购']['认申购金额']/\
             trading_detail[trading_detail['投资类型']=='申购']['资产净值']*100
        trading_detail.loc[trading_detail['投资类型']=='赎回','change_w']\
            =trading_detail[trading_detail['投资类型']=='赎回']['赎回份额']\
             /trading_detail[trading_detail['投资类型']=='赎回']['确认净值']/\
             trading_detail[trading_detail['投资类型']=='赎回']['资产净值']*-100

        #trading analysis
        #merge index ret data
        trading_data=pd.merge(stratage_weight_his[['日期','沪深300']]
                             ,howbuy_index_ret,how='left',left_on='日期',right_index=True)
        trading_data=pd.merge(trading_data
                             ,mu_index_ret,how='left',left_on='日期',right_index=True)
        trading_data['ym']=trading_data['日期'].str[0:6]
        trading_data=pd.merge(trading_data
                             ,index_enhance_index,how='left',left_on='ym',right_index=True)

        #using liner interpolation to make up missed data
        for indexname in howbuy_index_ret.columns.tolist()\
                         +mu_index_ret.columns.tolist()\
                         +index_enhance_index.columns.tolist():

            temp = trading_data[indexname].reset_index(drop=True)
            tempnotnull=temp[temp.notnull()]
            f = interpolate.interp1d(tempnotnull.index.values, tempnotnull.values, kind='cubic')
            ynew = f(temp.iloc[tempnotnull.index[0]:tempnotnull.index[-1]].index.values)
            temp.loc[tempnotnull.index[0]:tempnotnull.index[-1]-1]=ynew
            trading_data[indexname]=temp



        #merge weight change by class
        trading_data=pd.merge(trading_data
                             ,trading_detail[trading_detail['jjfl'] == '管理期货'].groupby('date').sum()['change_w'].to_frame('CTA_weight_change')
                             ,how='left',left_on='日期',right_index=True)

        trading_data=pd.merge(trading_data
                             ,trading_detail[trading_detail['ejfl'] == '量化多头'].groupby('date').sum()['change_w'].to_frame('量化多头_weight_change')
                             ,how='left',left_on='日期',right_index=True)

        for type in ['300','500','1000']:
            trading_detail.loc[(trading_detail['jjdm'].str.contains(type))
                             &(trading_detail['ejfl']=='量化多头'),'sjfl']=type+'指增'
            trading_data = pd.merge(trading_data
                                    , trading_detail[trading_detail['sjfl']==type+'指增'].groupby(
                    'date').sum()['change_w'].to_frame(type+'指增_weight_change')
                                    , how='left', left_on='日期', right_index=True)

        trading_data=pd.merge(trading_data
                             ,trading_detail[trading_detail['ejfl'] == '主观多头'].groupby('date').sum()['change_w'].to_frame('主观多头_weight_change')
                             ,how='left',left_on='日期',right_index=True)

        trading_data=pd.merge(trading_data
                             ,trading_detail[trading_detail['ejfl'].isin(['偏股混合型','灵活配置型','普通股票型'])].groupby('date').sum()['change_w'].to_frame('公募偏股_weight_change')
                             ,how='left',left_on='日期',right_index=True)

        trading_data=pd.merge(trading_data
                             ,trading_detail[~trading_detail['jjfl'].isin(['混合型',
        '股票型','管理期货'])].groupby('date').sum()['change_w'].to_frame('其他_weight_change')
                             ,how='left',left_on='日期',right_index=True)

        fof_nav['FOF净申赎'] = fof_nav['资产份额'].diff(1) * fof_nav['单位净值']
        trading_data=pd.merge(trading_data,fof_nav[['date','资产份额','资产净值']]
                              ,how='left',left_on='日期',right_on='date').drop('date',axis=1).set_index('日期')

        #
        trading_data.rename(columns={'HB0018':'好买CTA指数',
                                     'HB1001':'好买私募股多指数',
                                     'HB1002':'好买量化多头指数',
                                     '885001':'公募偏股混指数'},inplace=True)

        return  trading_data,trading_detail,fof_nav

    @staticmethod
    def define_trading_type(trading_data):

        # lable negative trading
        #add two columns 资产净值T+14 and 资产净值T-14
        trading_data['资产份额T+14']=trading_data['资产份额'].iloc[14:].tolist() + 14 * [np.nan]
        trading_data['资产份额T-14'] = 14 * [np.nan]+trading_data['资产份额'].iloc[0:-14].tolist()
        trading_data['调仓类型']=''
        trading_data.loc[((trading_data['CTA_weight_change']>0)
                         |(trading_data['量化多头_weight_change']>0)
                         |(trading_data['主观多头_weight_change']>0)
                         |(trading_data['公募偏股_weight_change']>0)
                         |(trading_data['其他_weight_change']>0))
                         &((trading_data['资产份额T-14']<trading_data['资产份额'])
                           |(trading_data.index<=trading_data.index[13])),'调仓类型']='被动增仓'

        trading_data.loc[((trading_data['CTA_weight_change']<0)
                         |(trading_data['量化多头_weight_change']<0)
                         |(trading_data['主观多头_weight_change']<0)
                         |(trading_data['公募偏股_weight_change']<0)
                         |(trading_data['其他_weight_change']<0))
                         &((trading_data['资产份额T+14']<trading_data['资产份额'])|
                           (trading_data.index<=trading_data.index[13])),'调仓类型']='被动减仓'

        trading_data.loc[((trading_data['CTA_weight_change'].notnull())
                         |(trading_data['量化多头_weight_change'].notnull())
                         |(trading_data['主观多头_weight_change'].notnull())
                         |(trading_data['公募偏股_weight_change'].notnull())
                         |(trading_data['其他_weight_change'].notnull())
                         )
                         &(trading_data['调仓类型']==''),'调仓类型']='主动'


        return  trading_data

    def fof_trading_analysis(self,weight_his_dir,hold_data_dir,start_date,product):


        #trade data pre processing
        trading_data,trading_detail,fof_nav=\
            self.trade_date_preprocessing(weight_his_dir,hold_data_dir,start_date)


        #*******define trading type : positive or negative *******
        trading_data=self.define_trading_type(trading_data)

        negative_trade=trading_data[trading_data['调仓类型'].str.contains('被动')]
        negative_trade_summary=pd.DataFrame(index=negative_trade['调仓类型'].unique().tolist())
        for type in negative_trade['调仓类型'].unique().tolist():
            for asset in ['CTA','量化多头','主观多头','公募偏股','其他']:
                negative_trade_summary.loc[type,asset]= \
                    len(negative_trade[(negative_trade['调仓类型'] == type)
                                       & (negative_trade[asset + "_weight_change"].notnull())])

        positive_trade=trading_data[(trading_data['调仓类型']=='主动')]
        positive_trade=positive_trade.reset_index(drop=False)
        positive_trade_block=[]

        jjfl2stratage_map=dict(zip(['管理期货','股票型','混合型','其他','债券型','市场中性','套利型','多策略']
                                   ,['CTA','进攻性资产','进攻性资产','稳健性资产','稳健性资产','稳健性资产','稳健性资产','稳健性资产']))

        def define_trade_type(inputdf):

            block_detail=inputdf.copy()
            block_detail['操作类型']=[jjfl2stratage_map[x] for x in block_detail['jjfl']]

            buy_ytm=block_detail[block_detail['change_w']>0].mean()['YTM']
            sell_ytm = block_detail[block_detail['change_w'] < 0].mean()['YTM']

            if (buy_ytm>sell_ytm ):
                if_win = '胜'
            else:
                if_win = '败'

            if(len(block_detail['操作类型'].unique())>1):

                block_detail=block_detail.groupby('操作类型').sum()[['change_w']]
                trade_type = ''

            else:
                if(len(block_detail['ejfl'].unique())>1):
                    block_detail = block_detail.groupby('ejfl').sum()[['change_w']]
                    trade_type = ''
                else:
                    trade_type = '置换{}资产'.format(block_detail['ejfl'].unique()[0])

            if(trade_type==''):
                for index in block_detail.index.tolist():

                    if(block_detail.loc[index]['change_w']>0):
                        trade_dir='买'
                    else:
                        trade_dir='卖'
                    trade_type+=trade_dir+index+";"

            return  trade_type,if_win


        i=0
        while (i<len(positive_trade)):
            t0=datetime.datetime.strptime(positive_trade.iloc[i]['日期']
                                          , '%Y%m%d')
            t_14=(t0+datetime.timedelta(days=14)).strftime('%Y%m%d')
            tempdf=positive_trade[(positive_trade['日期']>=positive_trade.iloc[i]['日期'])
                           &(positive_trade['日期']<=t_14)]

            increase_asset=0
            decrease_asset=0
            for col in ['CTA','量化多头','主观多头','公募偏股','其他']:
                increase_asset+=len(tempdf[tempdf[col+'_weight_change']>0])
                decrease_asset+=len(tempdf[tempdf[col+'_weight_change']<0])
            if(increase_asset>0 and decrease_asset>0):
                positive_trade_block.append(tempdf)
                i=tempdf.index[-1]
            else:
                i+=1

        for i in range(len(positive_trade_block)):
            block=positive_trade_block[i]
            block_detail=\
                trading_detail[trading_detail['date'].isin(block['日期'].unique())][['jjdm','cpfl','jjfl','ejfl','date','change_w','投资基金']]


            sql = "select jjdm,jzrq,jjjz from st_fund.t_st_gm_jjjz where jjdm in ({0}) and jzrq>='{1}' and jzrq<='{2}'" \
                .format(util.list_sql_condition(block_detail[block_detail['cpfl']==2]['jjdm'].tolist())
                        , block_detail['date'].iloc[0], fof_nav['date'].iloc[-1])
            mutual_nav = hbdb.db2df(sql, db='funduser')
            if(len(mutual_nav)>0):
                mutual_nav=mutual_nav.pivot_table('jjjz','jzrq','jjdm')
                for col in mutual_nav.columns:
                    block_detail.loc[block_detail['jjdm']==col,'YTM']=\
                        mutual_nav[mutual_nav[col].notnull()][col].iloc[-1]\
                        /mutual_nav[mutual_nav[col].notnull()][col].iloc[0]-1

            sql = "select jjdm,jzrq,jjjz from st_hedge.t_st_jjjz where jjdm in ({0}) and jzrq>='{1}' and jzrq<='{2}'" \
                .format(util.list_sql_condition(block_detail[block_detail['cpfl']==4]['jjdm'].tolist())
                        , block_detail['date'].iloc[0], fof_nav['date'].iloc[-1])
            prv_nav = hbdb.db2df(sql, db='highuser')
            if(len(prv_nav)>0):
                prv_nav=prv_nav.pivot_table('jjjz','jzrq','jjdm')
                for col in prv_nav.columns:
                    block_detail.loc[block_detail['jjdm']==col,'YTM']=\
                        prv_nav[prv_nav[col].notnull()][col].iloc[-1]\
                        /prv_nav[prv_nav[col].notnull()][col].iloc[0]-1

            block_detail['trade_group']=i+1

            trade_type, if_win=define_trade_type(block_detail)
            block_detail['操作类型']=trade_type
            block_detail['操作结果'] = if_win

            positive_trade_block[i]=block_detail

        positive_trade_block=pd.concat(positive_trade_block,axis=0)
        positive_trade_block['change_w']=positive_trade_block['change_w']/100
        for col in ['change_w','YTM']:
            positive_trade_block[col] = \
                positive_trade_block[col].map("{:.2%}".format)


        weight_change_trade=\
            trading_detail[trading_detail['date'].isin(
                list(set(positive_trade['日期']).difference(set(positive_trade_block['date'].tolist()))))]

        #plot result
        plot.plotly_table(negative_trade_summary.reset_index(drop=False), 1000, '')
        # plot.plotly_table(positive_trade_block[['trade_group','date','投资基金','YTM','change_w'
        #     ,'jjfl','ejfl','操作类型','操作结果']],1500,'')
        # positive_trade_block[['trade_group', 'date', '投资基金', 'YTM', 'change_w'
        #     , 'jjfl', 'ejfl', '操作类型', '操作结果']].to_excel(product+'交易细节.xlsx')
        weight_change_trade[['date','投资基金', '投资类型','jjfl', 'ejfl','change_w']].to_excel(product+'其他交易细节.xlsx')


        # data, layout=plot.plotly_line_and_bar(trading_data[['好买CTA指数']]
        #                                           ,trading_data[['CTA_weight_change']]
        #                                       ,product[0:-6]+'CTA交易时序')
        # plot.plot_render(data, layout)
        #
        # data, layout=plot.plotly_line_and_bar(trading_data[['好买私募股多指数']]
        #                                           ,trading_data[['主观多头_weight_change']]
        #                                       ,product[0:-6]+'私募股多交易时序')
        # plot.plot_render(data, layout)
        #
        # data, layout=plot.plotly_line_and_bar(trading_data[['好买量化多头指数']]
        #                                           ,trading_data[['量化多头_weight_change']]
        #                                       ,product[0:-6]+'量化多头交易时序')
        # plot.plot_render(data, layout)
        #
        # data, layout=plot.plotly_line_and_bar(trading_data[['公募偏股混指数']]
        #                                           ,trading_data[['公募偏股_weight_change']]
        #                                       ,product[0:-6]+'公募偏股交易时序')
        # plot.plot_render(data, layout)



if __name__ == '__main__':

    #fa.fromtrading2holding(start_date='20211101')

    fa=FOF_analysis(dir=r"E:\FOF分析\交易流水.xlsx",end_date='20220825')
    #'新方程大类配置稳健型私募证券投资基金',
    for product in ['新方程大类配置稳健型私募证券投资基金','新方程私享精选FOF5号私募证券投资基金']:

        fa.holding_analysis(dir=r"E:\FOF分析\{}基金持仓数据.xlsx".format(product),start_date='20211101')
        # fa.fof_trading_analysis(weight_his_dir=r"E:\FOF分析\{}一级策略时序图.xlsx".format(product)
        #                         ,hold_data_dir=r"E:\FOF分析\{}基金持仓数据.xlsx".format(product)
        #                         ,start_date='20211101',product=product)


