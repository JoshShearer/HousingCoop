# Refresh the Friendstead material price charts. See the vault note "Building Materials Price History".
# Fetch: for id in WPU0811 WPU0831 WPU081 WPU1333 WPU1321 WPU137 WPU1331 WPU1017 WPU1074 WPU102 WPU1392 WPU0721 WPUSI012011 WPUIP2311001; do curl -sL "https://fred.stlouisfed.org/graph/fredgraph.csv?id=$id" -o fred/$id.csv; done
# Run: uv run --with matplotlib --with pandas python ppi-charts.py fred "/home/joshshearer/Documents/Notes/Attachments"
import sys, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path
FRED = Path(sys.argv[1]); OUT = Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
SURF="#fcfcfb"; INK="#0b0b0b"; INK2="#52514e"; GRID="#e6e5e1"
C=["#2a78d6","#eb6834","#1baf7a","#eda100"]
def load(sid):
    df=pd.read_csv(FRED/f"{sid}.csv", na_values=".")
    df.columns=["date","v"]; df["date"]=pd.to_datetime(df["date"]); return df.set_index("date")["v"].dropna()
NAMES={
 "WPU0811":"Softwood lumber","WPU0831":"Softwood plywood","WPU081":"Lumber, all",
 "WPU1333":"Ready-mix concrete","WPU1321":"Sand, gravel, crushed stone","WPU137":"Gypsum (drywall)","WPU1331":"Concrete block and brick",
 "WPU1017":"Steel mill products","WPU1074":"Pre-engineered metal buildings","WPU102":"Nonferrous metals (copper, aluminum)","WPU1392":"Insulation materials","WPU0721":"Plastic construction products (PVC, vinyl)",
 "WPUSI012011":"Construction materials, all","WPUIP2311001":"Inputs to residential construction (goods)",
}
S={k:load(k) for k in NAMES}
BASE=pd.Timestamp("2020-01-01")
def idx(s): return s/s.loc[BASE]*100
def chart(fname,title,sub,ids,start="2015-01-01"):
    fig,ax=plt.subplots(figsize=(10,5.6),dpi=160); fig.patch.set_facecolor(SURF); ax.set_facecolor(SURF)
    ends=[]
    for i,sid in enumerate(ids):
        s=idx(S[sid]); s=s[s.index>=start]
        ax.plot(s.index,s.values,color=C[i],lw=2,solid_capstyle="round")
        ends.append([s.index[-1],s.iloc[-1],f"{NAMES[sid]}  {s.iloc[-1]:.0f}",C[i]])
    lo,hi=ax.get_ylim(); gap=(hi-lo)*0.045
    order=sorted(range(len(ends)),key=lambda k:ends[k][1]); ys=[ends[k][1] for k in order]
    for j in range(1,len(ys)):
        if ys[j]-ys[j-1]<gap: ys[j]=ys[j-1]+gap
    for j,k in enumerate(order):
        x,y0,lab,col=ends[k]; x2=x+pd.Timedelta(days=75)
        ax.plot([x,x2],[y0,ys[j]],color=col,lw=0.9,clip_on=False)
        ax.text(x2+pd.Timedelta(days=20),ys[j],lab,va="center",fontsize=9,color=INK,clip_on=False)
    ax.axhline(100,color=INK2,lw=0.8,ls=(0,(3,3)))
    ax.text(pd.Timestamp(start),101.5,"Jan 2020 = 100",fontsize=8.5,color=INK2)
    for sp in ["top","right","left"]: ax.spines[sp].set_visible(False)
    ax.spines["bottom"].set_color(GRID); ax.yaxis.grid(True,color=GRID,lw=0.8); ax.set_axisbelow(True)
    ax.tick_params(colors=INK2,labelsize=9,length=0)
    ax.xaxis.set_major_locator(mdates.YearLocator(1 if start>="2015" else 2)); ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.set_xlim(pd.Timestamp(start),pd.Timestamp("2027-01-01"))
    ax.set_title(title,loc="left",fontsize=13,color=INK,weight="bold",pad=18)
    ax.text(0,1.02,sub,transform=ax.transAxes,fontsize=9.5,color=INK2)
    fig.text(0.01,0.01,"Source: BLS Producer Price Index via FRED, monthly, not seasonally adjusted, through Sept 2026. Indexed to Jan 2020 = 100.",fontsize=8,color=INK2)
    fig.tight_layout(rect=(0,0.03,0.82,1)); fig.savefig(OUT/fname,facecolor=SURF); plt.close(fig)
chart("friendstead-ppi-wood.png","Wood products: the 2021 spike unwound, but not to 2019","Producer price index, softwood lumber and plywood, 2015 to Sept 2026",["WPU0811","WPU0831","WPU081"])
chart("friendstead-ppi-concrete.png","Concrete and drywall rose and stayed up","Producer price index, ready-mix, aggregates, gypsum, 2015 to Sept 2026",["WPU1333","WPU1321","WPU137","WPU1331"])
chart("friendstead-ppi-metals.png","Metals and envelope materials","Producer price index, steel, pre-engineered metal buildings, nonferrous, insulation, 2015 to Sept 2026",["WPU1017","WPU1074","WPU102","WPU1392"])
chart("friendstead-ppi-overview.png","All construction materials since 2000","Producer price index composites, 2000 to Sept 2026",["WPUSI012011","WPUIP2311001","WPU0721"],start="2000-01-01")
# summary table
rows=[]
for sid,n in NAMES.items():
    s=S[sid]; last=s.iloc[-1]
    def pct(d): 
        try: return (last/s.loc[pd.Timestamp(d)]-1)*100
        except KeyError: return float("nan")
    pk=s[s.index>=BASE]; peak=pk.idxmax()
    rows.append((n,sid,pct("2015-01-01"),pct("2020-01-01"),(last/pk.max()-1)*100,peak.strftime("%b %Y"),pct("2025-09-01")))
print("| Material | FRED | Since Jan 2015 | Since Jan 2020 | From post-2020 peak | Peak month | Last 12 months |")
print("|---|---|---|---|---|---|---|")
for r in rows: print(f"| {r[0]} | {r[1]} | {r[2]:+.0f}% | {r[3]:+.0f}% | {r[4]:+.0f}% | {r[5]} | {r[6]:+.1f}% |")
