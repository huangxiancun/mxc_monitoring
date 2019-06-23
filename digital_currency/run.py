# -*- coding: utf-8 -*-

# Author : 'hxc'

# Time: 2019/6/11 8:17 PM

# File_name: 'run.py'

"""
Describe: this is a demo!
"""

from mxc.mxc import *
import pickle



class MXC_Monitoring(object):
    """
    抹茶交易所满足三角套利的币进行监控类
    """

    def __init__(self, u, is_update_data = False):
        """
        初始化
        """
        print()
        print("******************** 投资有风险，谨慎，谨慎，再谨慎！********************")
        print("******************** 一定要记住，不要监控没有行情的币！！！，没用，不好卖！！！********************")
        print('******************** 一定要选择选择有行情的币！！！********************')
        print()

        btc_usdt_ask_bid = get_depth('btc_usdt', 1)['data']
        eth_usdt_ask_bid = get_depth('eth_usdt', 1)['data']
        mx_usdt_ask_bid = get_depth('mx_usdt', 1)['data']

        self.btc_usdt_ask = btc_usdt_ask_bid['asks'][0]['price']
        self.btc_usdt_bid = btc_usdt_ask_bid['bids'][0]['price']

        self.eth_usdt_ask = eth_usdt_ask_bid['asks'][0]['price']
        self.eth_usdt_bid = eth_usdt_ask_bid['bids'][0]['price']

        self.mx_usdt_ask = mx_usdt_ask_bid['asks'][0]['price']
        self.mx_usdt_bid = mx_usdt_ask_bid['bids'][0]['price']

        self.is_update_data = is_update_data #因为抹茶经常不断的上币，因此需要隔一段的时间进行update一下三角套利的币。
        self.u = u #利润+手续费的

    def judge_your_pairs(self):

        """
        获取满足三角套利的币，可以过一段时间执行一次，然后会得倒一个文件，该文件会记录满足的币的名称。
        :return:
        """
        # 获取抹茶所有交易对
        trade_pairs = get_symbols()['data']
        # print(trade_pairs)
        btc_pairs = []
        eth_pairs = []
        usdt_pairs = []
        for i in trade_pairs:
            if "usdt" in i :
                i = i.replace('_usdt','')
                usdt_pairs.append(i)
            elif 'btc' in i :
                i = i.replace('_btc', '')
                btc_pairs.append(i)
            elif 'eth' in i:
                i = i.replace('_eth', '')
                eth_pairs.append(i)
            else:
                pass

        usdt_btc_pairs = [j for j in usdt_pairs if j in btc_pairs]
        print("btc个数有：",len(usdt_btc_pairs))
        print(usdt_btc_pairs)
        usdt_btc_pairs_str = '-'.join(usdt_btc_pairs)
        usdt_btc_pairs_output = open('./data/usdt_btc_pairs.pkl', 'wb')
        pickle.dump(usdt_btc_pairs_str, usdt_btc_pairs_output)
        usdt_btc_pairs_output.close()

        usdt_eth_pairs = [k for k in usdt_pairs if k in eth_pairs]
        print("eth个数有：",len(usdt_eth_pairs))
        print(usdt_eth_pairs)
        usdt_eth_pairs_str = '-'.join(usdt_eth_pairs)
        usdt_eth_pairs_output = open('./data/usdt_eth_pairs.pkl', 'wb')
        pickle.dump(usdt_eth_pairs_str, usdt_eth_pairs_output)
        usdt_eth_pairs_output.close()

        usdt_btc_eth_pairs = [m for m in usdt_pairs if (m in btc_pairs and m in eth_pairs)]
        print("既btc有eth也有的个数：",len(usdt_btc_eth_pairs))
        print(usdt_btc_eth_pairs)
        usdt_btc_eth_pairs_str = '-'.join(usdt_btc_eth_pairs)
        usdt_btc_eth_pairs_output = open('./data/usdt_btc_eth_pairs.pkl','wb')
        pickle.dump(usdt_btc_eth_pairs_str,usdt_btc_eth_pairs_output)
        usdt_btc_eth_pairs_output.close()


    def run(self,your_pairs,money):
      """
      持续监控,一个或者多个币
      :return:
      """
      if self.is_update_data:
        #更新数据
        self.judge_your_pairs()

      usdt_btc_pairs_pkl = open('./data/usdt_btc_pairs.pkl', 'rb')
      usdt_btc_pairs_str= pickle.load(usdt_btc_pairs_pkl)
      print(usdt_btc_pairs_str.upper())

      usdt_eth_pairs_pkl = open('./data/usdt_eth_pairs.pkl', 'rb')
      usdt_eth_pairs_str = pickle.load(usdt_eth_pairs_pkl)
      print(usdt_eth_pairs_str.upper())

      usdt_btc_eth_pairs_pkl = open('./data/usdt_btc_eth_pairs.pkl', 'rb')
      usdt_btc_eth_pairs_str = pickle.load(usdt_btc_eth_pairs_pkl)
      print(usdt_btc_eth_pairs_str.upper())

      print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>进行监控>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
      while 1:
          self.do_monitoring(your_pairs,money)

    def do_monitoring(self,your_pairs,money):

        """
        监控
        :return:
        """
        i = your_pairs[0] #暂时支持一个币
        x_usdt_ask_bid = get_depth(i + '_usdt',2)['data']
        x_btc_ask_bid = get_depth(i + '_btc',2)['data']

        #卖一，卖二  ----> x/usdt
        x_usdt_ask_1 = float(x_usdt_ask_bid['asks'][0]['price'])
        x_usdt_ask_2 = float(x_usdt_ask_bid['asks'][1]['price'])

        # 卖一，卖二  ----> x/btc
        x_btc_ask_1 = float(x_btc_ask_bid['asks'][0]['price'])
        x_btc_ask_2 = float(x_btc_ask_bid['asks'][0]['price'])


        #买一，买二  ---->x/usdt
        x_usdt_bid_1 = float(x_usdt_ask_bid['bids'][0]['price'])
        x_usdt_bid_2 = float(x_usdt_ask_bid['bids'][1]['price'])

        #买一，买二  ---->x/btc
        x_btc_bid_1 = float(x_btc_ask_bid['bids'][0]['price'])
        x_btc_bid_2 = float(x_btc_ask_bid['bids'][1]['price'])

        #路径1：u->【x/usdt】->x->【x/btc】->btc->【btc/usdt】->u

        num_1 = money/x_usdt_ask_1

        profit1 = (num_1 * x_btc_bid_1 * float(self.btc_usdt_bid)) - money


        # 路径2：u->【btc/usdt】->btc->【x/btc】->x->【x/usdt】->u

        num_2 = money / (float(self.btc_usdt_bid))

        profit2 = ((num_2 / x_btc_ask_1) * x_usdt_ask_1) - money


        if profit1>self.u:
            print(profit1)
            print('#路径1：u->【x/usdt】->x->【x/btc】->btc->【btc/usdt】->u')
        elif profit2 >self.u:
            print(profit2)
            print('# 路径2：u->【btc/usdt】->btc->【x/btc】->x->【x/usdt】->u')
        else:
            print()
            print('>>>>111111>>>>', profit1)
            print()
            print('>>>>222222>>>>', profit2)








if __name__ == '__main__':

    mxc_monitor = MXC_Monitoring(8,is_update_data= False)
    print("btc:","UGAS-NNB-IRIS-BSV-ANKR-ONT-ATOM-LBTC-ELF-BTT-SNT-RIF-ETC-TIC")

    temp = input("请输入你要监控的币（支持一个或者多个输入以英文逗号分割）：")
    money = input("请输入你入场的本金（单位：u/个）：")

    temp_list = temp.split(',')
    mxc_monitor.run(temp_list,float(money))

