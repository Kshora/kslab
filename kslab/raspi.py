import pandas as pd
from graph_tools import *
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

        rcParams["font.size"] = 28

    def load_data(self):
        """load data"""

        self.path = [l for l in os.listdir(self.bpath) if l.endswith(".csv") and self.timepath in l]
        self.data_config = {}

        try:
            self.path = os.path.join(self.bpath,self.path[0])
            print(self.path)
            with open(self.path) as f:
                reader = csv.reader(f)
                for row in reader:
                    if row[0].startswith("#"):
                        if not len(row) == 1:
                            head = row[0].replace(' ','').replace('#','').split(':')
                            self.data_config[head[0]] = [head[1]] + row[1:]
                    else:
                        break

            self.data = pd.read_csv(self.path,names=self.data_config['Columns'],comment='#')
        except IndexError:
            raise FileNotFoundError(f"no data found for {self.timepath}")
    

        
    def update_data(self):
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
        self.plot_data = kws.get("data", None)
        if self.plot_data is None:
            self.time_formatter(**kws)
        

        

        fig = plt.figure(figsize=(16, 9),dpi=50,facecolor='w')

    def plot_pressure(self,**kws):
        # plot pressure data
        """
        separate plot axis for upstream and downstream
        ax1 for upstream Pu, Bu
        ax2 for downstream Pd, Bd
        """
        xlabel = kws.get("xlabel", "time")
        yscale = kws.get("yscale", "linear")

        st = kws.get("st", self.start_time)
        et = kws.get("et", self.end_time)

        self.pu_lim = kws.get("pu_lim", (1e-7, 1e-2))
        self.pd_lim = kws.get("pd_lim", (1e-8, 1e-5))

        plot_upstream = kws.get("plot_upstream", True)
        plot_downstream = kws.get("plot_downstream", True)

        self.plot_data = kws.get("data", None)
        fig = kws.get("fig", plt.figure(figsize=(16,9),dpi=50,facecolor='w'))
        ax1 = kws.get("ax1", fig.add_subplot(111)) # plot ax for upstream
        ax2 = kws.get("ax2", ax1.twinx()) # plot ax for downstream
        axs = [ax1,ax2]
        self.time_formatter(st=st,et=et)
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
        
        if plot_upstream:
            pressure = pressures["upstream"]
            [axs[0].plot(self.plot_data[xlabel],self.plot_data[pressure["data"][i]],label=pressure["label"][i],c=pressure["color"][i]) for i in range(2)]
            axs[0].set_ylim(self.pu_lim)
            axs[0].set_ylabel('Pressure upstream (Torr)',fontsize=34)
            axs[0].set_xlabel('Time (s)',fontsize=34)
            axs[0].legend(loc='upper left')
                    
            
        if plot_downstream:
            pressure = pressures["downstream"]
            [axs[1].plot(self.plot_data[xlabel],self.plot_data[pressure["data"][i]],label=pressure["label"][i],c=pressure["color"][i]) for i in range(2)]
            axs[1].set_ylim(self.pd_lim)
            axs[1].set_ylabel('Pressure douwnstream (Torr)',fontsize=34)
            axs[1].legend(loc='upper right')

        [ax.set_yscale(yscale) for ax in axs]
        if xlabel == "date":
            xticks_label = [i for n,i in enumerate(self.plot_data[xlabel]) if n%(len(self.plot_data)//10) == 0]
            ax1.set_xticks(xticks_label)
            ax1.set_xticklabels([i[11:19] for i in xticks_label],rotation=45,ha='right')
            self.xtick_label = xticks_label



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

        st = kws.get("st", self.start_time)
        et = kws.get("et", self.end_time)

        self.plot_data = kws.get("data", None)
        fig = kws.get("fig", plt.figure(figsize=(16,9),dpi=50,facecolor='w'))
        ax = kws.get("ax", fig.add_subplot(111))

        self.time_formatter(st=st,et=et)
        ax.plot(self.plot_data[xlabel],self.plot_data["Ip_c"],label="Ip",c="#8d3de3")
        ax.set_xlabel('Time (s)',fontsize=34)
        ax.set_ylabel('Current (A)',fontsize=34)
        ax.set_yscale(yscale)
        if xlabel == "date":
            xticks_label = [i for n,i in enumerate(self.plot_data[xlabel]) if n%(len(self.plot_data)//10) == 0]
            ax.set_xticks(xticks_label)
            ax.set_xticklabels([i[11:19] for i in xticks_label],rotation=45,ha='right')
            self.xtick_label = xticks_label

        grid_visual(ax)
        ticks_visual(ax)

    def plot_mfc(self,**kws):
        # plot mfc data
        # PresetP and sig are plotted in the same figure
        xlabel = kws.get("xlabel", "time")
        yscale = kws.get("yscale", "linear")

        st = kws.get("st", self.start_time)
        et = kws.get("et", self.end_time)

        self.plot_data = kws.get("data", None)
        fig = kws.get("fig", plt.figure(figsize=(16,9),dpi=50,facecolor='w'))
        ax = kws.get("ax", fig.add_subplot(111))

        mfc = { "mfc1": {"data":["PresetV1","MFC1_c"],
                         "color":["k","k"],
                         "line_style":["--","-"],
                         "label":["PresetV1","MFC1_sig"],
                         },
                "mfc2": {"data":["PresetV2","MFC2_c"],
                         "color":["r","r"],
                         "line_style":["--","-"],
                         "label":["PresetV2","MFC2_sig"],
                         },
                }

        self.time_formatter(st=st,et=et)
        for i in mfc:
            [ax.plot(self.plot_data[xlabel],self.plot_data[mfc[i]["data"][j]],label=mfc[i]["label"][j],c=mfc[i]["color"][j],ls=mfc[i]["line_style"][j]) for j in range(2)]
        ax.set_xlabel('Time (s)',fontsize=34)
        ax.set_ylabel('Voltage (V)',fontsize=34)
        ax.set_yscale(yscale)
        if xlabel == "date":
            xticks_label = [i for n,i in enumerate(self.plot_data[xlabel]) if n%(len(self.plot_data)//10) == 0]
            ax.set_xticks(xticks_label)
            ax.set_xticklabels([i[11:19] for i in xticks_label],rotation=45,ha='right')
            self.xtick_label = xticks_label
        
        ax.legend(loc='upper right')

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

        
