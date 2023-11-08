import pandas as pd
from .graph_tools import *
from datetime import datetime, date
import os
import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import AutoMinorLocator, LogLocator
from matplotlib import rcParams

class Raspi:

    def __init__(self, bpath="", timepath=""):

        self.bpath = bpath
        self.timepath = timepath
        self.date = date.today()

        self.load_data()

        self.__update_data()

        rcParams["font.size"] = 28

    def load_data(self):
        """load data"""

        self.path = [l for l in os.listdir(self.bpath) if l.endswith(".csv") and self.timepath in l]
        self.config = {}

        try:
            self.path = os.path.join(self.bpath,self.path[0])
            import re
            with open(self.path) as f:
                reader = csv.reader(f)
                for row in reader:
                    if row[0].startswith("#"):
                        if len(row) > 1:
                            self.config[re.sub('[# :]','',row[0])] =  [re.sub('[ ]','',r) for r in row[1:]]
                        if 'Data' in row[0]:
                            break
                    else:
                        break
            self.data = pd.read_csv(self.path,names=self.config['Columns'],comment='#')
        except IndexError:
            raise FileNotFoundError(f"no data found for {self.timepath}")
    

        
    def __update_data(self):
        self.data['datetime'] = self.data['date'].apply(lambda x: int(x.translate(str.maketrans({' ': '', '-': '', ':': ''})).split('.')[0]))
        self.start_time = self.data['datetime'].iloc[0]
        self.end_time = self.data['datetime'].iloc[-1]

    def prepera_dataset(self):
        self.experiment_dataset = []
        self.calibration_dataset = []
        data = pd.DataFrame()
        flag = 0
        for i in range(len(self.data)):
            col = self.data.iloc[[i]]
            if col['QMS_signal'].iloc[0] == 1:
                data = pd.concat([data, col])
                flag = 1
            elif col['QMS_signal'].iloc[0] == 2:
                data = pd.concat([data, col])
                flag = 2
            if col['QMS_signal'].iloc[0] == 0 and flag == 1:
                if len(data) > 20:
                    self.experiment_dataset.append(data)
                    flag = 0
                    data = pd.DataFrame()
                else:
                    flag = 0
                    data = pd.DataFrame()
            elif col['QMS_signal'].iloc[0] == 0 and flag == 2:
                if len(data) > 20:
                    self.calibration_dataset.append(data)
                    flag = 0
                    data = pd.DataFrame()
                else:
                    flag = 0
                    data = pd.DataFrame()

        
    def plot(self, **kws):
        """plot data"""
        xlabel = kws.get("xlabel", "time")
        yscale = kws.get("yscale", "linear")

        xlim = kws.get("xlim", None)

        st = kws.get("st", self.start_time)
        et = kws.get("et", self.end_time)

        fig = plt.figure(figsize=(16,18),dpi=50,facecolor='w')
        gs = fig.add_gridspec(3, 1, height_ratios=[1,1,1],hspace=0.15)
        ax0 = plt.subplot(gs[0, 0])
        ax1 = plt.subplot(gs[1, 0],sharex=ax0)
        ax2 = plt.subplot(gs[2, 0],sharex=ax0)
        self.axs = [ax0,ax1,ax2]

        self.time_formatter(st=st,et=et)

        self.plot_pressure(st=st,et=et,xlabel=xlabel,yscale=yscale,fig=None,ax=self.axs[0],xlim=xlim)
        self.plot_current(st=st,et=et,xlabel=xlabel,fig=None,ax=self.axs[1],xlim=xlim)
        self.plot_mfc(st=st,et=et,xlabel=xlabel,fig=None,ax=self.axs[2],xlim=xlim)

        [ax.tick_params(axis='x', which='both', bottom=True, top=False, labelbottom=False) for ax in self.axs[:-1]]
        [ax.set_xlabel('') for ax in self.axs[:-1]]
        

        

        fig = plt.figure(figsize=(16, 9),dpi=50,facecolor='w')

    def plot_pressure(self,**kws):
        # plot pressure data
        """
        separate plot axis for upstream and downstream
        ax1 for upstream Pu, Bu
        ax2 for downstream Pd, Bd
        """

        pressures = {"upstream" :{
                                "data": ["Pu_c","Bu_c"],
                                "color": ["#c9004d","#ffb405"], 
                                "label": ["Pu","Bu"]
                                },
                     "downstream" :{
                                "data": ["Pd_c","Bd_c"],
                                "color": ["#6ac600","#00a3af"],
                                "label": ["Pd","Bd"]
                                }
                    }
        
        xlabel = kws.get("xlabel", "time")
        yscale = kws.get("yscale", "linear")

        xlim = kws.get("xlim", None)

        st = kws.get("st", self.start_time)
        et = kws.get("et", self.end_time)

        threads = kws.get("threads", pressures["upstream"]["label"] + pressures["downstream"]["label"] + ["upstream","downstream"])


        self.pu_lim = kws.get("pu_lim", (1e-7, 1e-2))
        self.pd_lim = kws.get("pd_lim", (1e-8, 1e-5))



        fig = kws.get("fig", False)
        if fig == False:
            fig = plt.figure(figsize=(16,9),dpi=50,facecolor='w')
            ax = fig.add_subplot(111)
        else:
            ax = kws.get("ax",False) # plot ax for upstream
            if ax == False:
                raise ValueError("ax must be specified if fig is specified")
        axx = kws.get("axx", ax.twinx()) # plot ax for downstream
        axs = [ax,axx]

        self.time_formatter(st=st,et=et)


        if "upstream" in threads:
            pressure = pressures["upstream"]
            [axs[0].plot(self.plot_data[xlabel],self.plot_data[pressure["data"][i]],label=pressure["label"][i],c=pressure["color"][i]) for i in range(2)]
                    
            
        if "downstream" in threads:
            pressure = pressures["downstream"]
            [axs[1].plot(self.plot_data[xlabel],self.plot_data[pressure["data"][i]],label=pressure["label"][i],c=pressure["color"][i]) for i in range(2)]


        pressure = pressures["upstream"]
        if "Pu" in threads and not "upstream" in threads:
            axs[0].plot(self.plot_data[xlabel],self.plot_data[pressure["data"][0]],label=pressure["label"][0],c=pressure["color"][0])
        if "Bu" in threads and not "upstream" in threads:
            axs[0].plot(self.plot_data[xlabel],self.plot_data[pressure["data"][1]],label=pressure["label"][1],c=pressure["color"][1])
        pressure = pressures["downstream"]
        if "Pd" in threads and not "downstream" in threads:
            axs[1].plot(self.plot_data[xlabel],self.plot_data[pressure["data"][0]],label=pressure["label"][0],c=pressure["color"][0])
        if "Bd" in threads and not "downstream" in threads:
            axs[1].plot(self.plot_data[xlabel],self.plot_data[pressure["data"][1]],label=pressure["label"][1],c=pressure["color"][1])
        axs[0].set_ylim(self.pu_lim)
        axs[1].set_ylim(self.pd_lim)
        axs[0].set_ylabel('P upstream (Torr)',fontsize=34)
        axs[1].set_ylabel('P douwnstream (Torr)',fontsize=34)
        if set(["Pu","Bu"]) <= set(threads) or "upstream" in threads: 
            axs[0].legend(loc=1, ncol=2, bbox_to_anchor=[0.36, 1.17],fontsize=24)
        if set(["Pd","Bd"]) <= set(threads) or "downstream" in threads:
            axs[1].legend(loc=1, ncol=2, bbox_to_anchor=[0.9, 1.17],fontsize=24)

        [ax.set_yscale(yscale) for ax in axs]
        if xlabel == "date":
            xticks_label = [i for n,i in enumerate(self.plot_data[xlabel]) if n%(len(self.plot_data)//10) == 0]
            axs[0].set_xticks(xticks_label)
            axs[0].set_xticklabels([i[11:19] for i in xticks_label],rotation=45,ha='right')
            self.xtick_label = xticks_label

        if xlim is not None:
            [ax.set_xlim(xlim) for ax in axs]



        axs[1].spines['right'].set_color('r')
        axs[1].yaxis.label.set_color('r')
        axs[1].tick_params(axis='y', colors='r')

        grid_visual(axs[0])
        ticks_visual(axs[0])
        ticks_visual(axs[1])


    def plot_current(self,**kws):
        # plot current data
        xlabel = kws.get("xlabel", "time")
        yscale = kws.get("yscale", "linear")

        xlim = kws.get("xlim", None)

        st = kws.get("st", self.start_time)
        et = kws.get("et", self.end_time)

        fig = kws.get("fig", False)
        if fig == False:
            fig = plt.figure(figsize=(16,9),dpi=50,facecolor='w')
            ax = fig.add_subplot(111)
        else:
            ax = kws.get("ax",False) # plot ax for upstream
            if ax == False:
                raise ValueError("ax must be specified if fig is specified")

        self.time_formatter(st=st,et=et)

        ax.plot(self.plot_data[xlabel],self.plot_data["Ip_c"],label="Ip",c="#8d3de3")
        ax.set_xlabel('Time (s)',fontsize=34)
        ax.set_ylabel('Current (A)',fontsize=34)
        ax.set_yscale(yscale)

        if "PresetV_cathode" in self.config["Columns"]:
            ax2 = ax.twinx()
            ax2.plot(self.plot_data[xlabel],self.plot_data["PresetV_cathode"],label="PresetV",c="#ff0000")
            ax2.set_ylabel('PresetV (V)',fontsize=34)
            ax2.spines['right'].set_color('r')
            ax2.yaxis.label.set_color('r')
            ax2.tick_params(axis='y', colors='r')
            ax2.set_yscale(yscale)


        if xlabel == "date":
            xticks_label = [i for n,i in enumerate(self.plot_data[xlabel]) if n%(len(self.plot_data)//10) == 0]
            ax.set_xticks(xticks_label)
            ax.set_xticklabels([i[11:19] for i in xticks_label],rotation=45,ha='right')
            self.xtick_label = xticks_label

        if xlim is not None:
            ax.set_xlim(xlim)

        grid_visual(ax)
        ticks_visual(ax)

    def plot_mfc(self,**kws):
        # plot mfc data
        # PresetP and sig are plotted in the same figure
        xlabel = kws.get("xlabel", "time")
        yscale = kws.get("yscale", "linear")

        xlim = kws.get("xlim", None)

        st = kws.get("st", self.start_time)
        et = kws.get("et", self.end_time)

        threads = kws.get("threads", ["mfc1","mfc2"])

        fig = kws.get("fig", False)
        if fig == False:
            fig = plt.figure(figsize=(16,9),dpi=50,facecolor='w')
            ax = fig.add_subplot(111)
        else:
            ax = kws.get("ax",False) # plot ax for upstream
            if ax == False:
                raise ValueError("ax must be specified if fig is specified")

        self.time_formatter(st=st,et=et)

        mfc = { "mfc1": {"data":["PresetV_mfc1","MFC1_c"],
                         "color":["k","k"],
                         "line_style":["--","-"],
                         "label":["PresetV1","MFC1 sig"],
                         },
                "mfc2": {"data":["PresetV_mfc2","MFC2_c"],
                         "color":["r","r"],
                         "line_style":["--","-"],
                         "label":["PresetV2","MFC2 sig"],
                         },
                }

        
        [[ax.plot(self.plot_data[xlabel],self.plot_data[mfc[thread]["data"][i]],label=mfc[thread]["label"][i],c=mfc[thread]["color"][i],ls=mfc[thread]["line_style"][i]) for thread in threads] for i in range(2)]
        ax.set_xlabel('Time (s)',fontsize=34)
        ax.set_ylabel('Voltage (V)',fontsize=34)
        ax.set_yscale(yscale)
        if xlabel == "date":
            xticks_label = [i for n,i in enumerate(self.plot_data[xlabel]) if n%(len(self.plot_data)//10) == 0]
            ax.set_xticks(xticks_label)
            ax.set_xticklabels([i[11:19] for i in xticks_label],rotation=45,ha='right')
            self.xtick_label = xticks_label
        
        ax.legend(loc=1, ncol=4, bbox_to_anchor=[1.0, 1.17],fontsize=24)

        if xlim is not None:
            ax.set_xlim(xlim)

        grid_visual(ax)
        ticks_visual(ax)

    def show_calibration(self,**kws):
        # show calibration data
        self.plot_data = kws.get("data", None)
        if self.plot_data is None:
            self.time_formatter(**kws)
        pass
    

    def time_formatter(self,**kws):
        st = kws.get("st", self.start_time)
        et = kws.get("et", self.end_time)

        if type(st) == datetime:
            st = int(st.strftime("%Y%m%d%H%M%S"))
        if type(et) == datetime:
            et = int(et.strftime("%Y%m%d%H%M%S"))

        self.plot_data = self.data.query(f"{st} <= datetime <= {et}")

        
