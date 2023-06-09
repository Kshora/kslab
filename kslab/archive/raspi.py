import pandas as pd
from graph_tools import *

class Raspi:
    def __init__(self, bpath="", timestamp=""):
        # from os.path import join, exists, expanduser
        # from os import makedirs
        from datetime import date

        self.bpath = bpath
        self.stamp = timestamp
        self.date = date.today()
        # self.ppath = join(expanduser('~'), 'Dropbox','lab','programs','OxygenExperiments','out','raspi',str(self.date))
        # if not exists(self.ppath):
        #     makedirs(f'../../out/raspi/{self.date}') #必要に応じてmakedirできるようにしたほうが良い

        self.load_data()
        if self.file_type == "out":
            self.convert_signals()
            self.update_signals()

    def load_data(self):
        """load data"""
        from datetime import datetime
        import os

        ls = os.listdir(self.bpath)
        ls_tmp = [l for l in ls if l.endswith("_temp.csv")]
        ls_adc = [l for l in ls if not l.endswith("_tmp.csv")]
        self.tmp_path = [l for l in ls_tmp if self.stamp in l]
        self.adc_path = [l for l in ls_adc if self.stamp in l]
        if len(self.tmp_path) == 0 and len(self.adc_path) == 0:
            raise FileNotFoundError(f"no data found for {self.stamp}")
        elif len(self.tmp_path) != 0:
            self.tmp_path = self.tmp_path[0]
            self.adc_path = self.adc_path[0]
            self.tmp = pd.read_csv(os.path.join(self.bpath, self.tmp_path))
            self.adc = pd.read_csv(os.path.join(self.bpath, self.adc_path))
        else:
            self.tmp_path = ""
            self.adc_path = self.adc_path[0]
            self.adc = pd.read_csv(os.path.join(self.bpath, self.adc_path))
        
        if self.tmp_path.startswith("out"):
            self.file_type = "out"
            self.tc = pd.read_csv(os.path.join(self.bpath, f"out_{self.stamp}_temp.csv"))
        
        
        
        self.tmp = pd.read_csv(os.path.join(self.bpath, self.tmp_path))
        if self.tmp.startswith("out"):
            self.file_type = "out"
            self.tc = pd.read_csv(os.path.join(self.bpath, f"out_{self.stamp}_temp.csv"))
            self.adc = pd.read_csv(os.path.join(self.bpath, f"out_{self.stamp}.csv"))
        elif os.path.exists(os.path.join(self.bpath, f"cu_{self.stamp}_temp.csv")):
            self.file_type = "cu"
            self.tc = pd.read_csv(os.path.join(self.bpath, f"cu_{self.stamp}_temp.csv"),skiprows=7,header=None,names=["date","time","T","PresetT"])
            self.adc = pd.read_csv(os.path.join(self.bpath, f"cu_{self.stamp}.csv"),skiprows=8,header=None,names=["date","time","P1","P2","Ip","B1","B2","IGmode","IGscale","QMS_signal","P1_c","P2_c","Ip_c","B1_c","B2_c"])
        else:
            raise FileNotFoundError(f"out_{self.stamp}_temp.csv or cu_{self.stamp}_temp.csv not found")
        
        if self.file_type == "out":
            start = datetime.strptime(self.stamp, "%Y%m%d_%H%M%S")
            self.adc.insert(0, "date", start + pd.to_timedelta(self.adc["time"], unit="s"))
            self.tc.insert(0, "date", start + pd.to_timedelta(self.tc["time"], unit="s"))
        self.start = datetime.strptime(self.stamp, "%Y%m%d_%H%M%S")
        if self.file_type == "out":
            self.end = self.tc['date'][len(self.tc)-1].to_pydatetime()
        else:
            pass

    def convert_signals(self):
        """convert ADC signals from raw volts to proper units
        pu: upstream pressure, plasma chamber
        pd: downstream pressure, permeation chamber
        ip: plasma current

        """
        # 11.46 convert Pfeiffer signal to pressure
        self.pu = 10 ** (1.667 * self.adc["P2"] - 11.46)
        # convert linear IG signal to pressure
        self.pd = self.adc["P1"] * 10 ** self.adc["IGscale"]
        # plasma current from hall sensor
        def iconv(v):
            return 5 / 1 * (v - 2.52)

        self.ip = iconv(self.adc["Ip"])
        self.t = self.adc["date"]

    def update_signals(self):
        """Update corresponding columns in self.adc with
        converted ones
        """
        self.adc.insert(1, "pu", self.pu)
        self.adc.insert(1, "pd", self.pd)
        self.adc.insert(1, "ip", self.ip)

    def plot(self, **kws):
        """Plot time traces"""
        import matplotlib.dates as mdates
        import matplotlib.pylab as plt
        from matplotlib.ticker import LogLocator, AutoMinorLocator

        fro = kws.get("fro", self.start)
        tto = kws.get("tto", self.end)

        a = fro.strftime("%Y%m%d%H%M%S")
        b = tto.strftime("%Y%m%d%H%M%S")
        df_adc = self.adc.query(f"{a} < date < {b}")
        df_tc = self.tc.query(f"{a} < date < {b}")

        fig = plt.figure(figsize=(12, 8), facecolor="w")
        gs = plt.GridSpec(4, 1)
        gs.update(left=0.1, right=0.95, wspace=0.2, hspace=0.14)
        ax0 = plt.subplot(gs[:2, 0])  # sharex=ax0
        axs = [ax0] + [plt.subplot(gs[i, 0], sharex=ax0) for i in range(2, 4)]

        plottrig = 0

        def plot_trig(axt):
            axt.plot(df_adc["datetime"], df_adc["QMS_signal"], "C2", label="trig")
            axt.set_yticks([])

        if plottrig:
            twins = [ax.twinx() for ax in [axs[0], axs[1], axs[2]]]
            [plot_trig(ax) for ax in twins]
            twins[0].legend(loc=1, bbox_to_anchor=[0.2, 1.2])

        ax = axs[0]
        ax.plot(df_adc["date"], df_adc["pd"], "-", c="k", label="Permeation Chamber")
        ax.plot(df_adc["date"], df_adc["pu"], "-", c="C3", label="Plasma Chamber")
        ax.locator_params(axis="y", nbins=6)

        ax.legend(loc=1, ncol=2, bbox_to_anchor=[1.0, 1.2])

        ax = axs[1]

        ax.plot(df_adc["date"], df_adc["ip"] - df_adc["ip"][:100].mean(), "k")

        ax = axs[2]
        ax.plot(df_tc["date"], df_tc["T"], c="k")
        ax.plot(df_tc["date"], df_tc["PresetT"], "C2--")
        plt.xticks(rotation=25, ha="right")

        gridalpha = kws.get("gridalpha", [0.1, 0.3])
        [customgrid(ax, gridalpha=gridalpha) for ax in axs]
        [customticks(ax) for ax in axs]
        axs[0].set_yscale("log")


        lbls = ["P [Torr]", "$I_p$ [A]", "T [$^{\circ }$C]"]
        [ax.set_ylabel(l) for l, ax in zip(lbls, axs)]
        axs[-1].set_xlabel(f"time")

        lims = kws.get("lims", [[5e-8, 2e-2], [-0.2, 2.5], [0, 1000]])
        [ax.set_ylim(l) for ax, l in zip(axs, lims)]
        axs[-1].locator_params(axis="y", nbins=5)  # increas number of major ticks for T plot
        locmax = LogLocator(base=10, subs=(1.0,), numticks=100)
        axs[0].yaxis.set_major_locator(locmax)

        [ax.xaxis.set_minor_locator(AutoMinorLocator(2)) for ax in axs]
        [ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %H:%M")) for ax in axs]

        # [ax.axes.xaxis.set_ticklabels([]) for ax in axs[:-1]]
        [plt.setp(ax.get_xticklabels(), visible=False) for ax in axs[:-1]]

        ax = axs[-1]
        plt.sca(ax)  # set current axis
        plt.xticks(rotation=25, ha="right")
        ax = axs[0]
        ax.text(
            -0.05, 1.07, self.start.strftime("%Y, %d %b, %a, %H:%M"), transform=ax.transAxes,
        )

        self.df_adc = df_adc
        self.df_tc = df_tc

        # return fig

