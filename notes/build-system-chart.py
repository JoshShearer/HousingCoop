import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, sys
plt.rcParams["text.parse_math"]=False
OUT=sys.argv[1]
SURF="#fcfcfb"; INK="#0b0b0b"; INK2="#52514e"; GRID="#e6e5e1"
C=["#2a78d6","#eb6834","#1baf7a"]
systems=[("Barndominium",176,38,57),("Stick-built 2x4",229,61,90),("SIP-only",270,67,70),("Steel frame kit",270,68,90),("Timber frame + SIP",330,103,75)]
fig,ax=plt.subplots(figsize=(10,5.4),dpi=160); fig.patch.set_facecolor(SURF); ax.set_facecolor(SURF)
ys=range(len(systems))[::-1]
for y,(name,m,h,d) in zip(ys,systems):
    ax.barh(y,m,color=C[0],height=0.58); ax.barh(y,h,left=m+1.5,color=C[1],height=0.58); ax.barh(y,d,left=m+h+3,color=C[2],height=0.58)
    ax.text(m/2,y,f"${m}K",ha="center",va="center",fontsize=9,color="white")
    ax.text(m+1.5+h/2,y,f"${h}K",ha="center",va="center",fontsize=8.5,color="white")
    ax.text(m+h+3+d/2,y,f"${d}K",ha="center",va="center",fontsize=8.5,color="white")
    coop=m+h; ax.plot([coop+1.5,coop+1.5],[y-0.38,y+0.38],color=INK,lw=1.6)
    ax.text(m+h+d+8,y,f"co-op ${coop}K · contractor ${round((m+h+d)*1.18/5)*5}K",va="center",fontsize=9,color=INK)
ax.set_yticks(list(ys)); ax.set_yticklabels([s[0] for s in systems],fontsize=10,color=INK)
for sp in ["top","right","left"]: ax.spines[sp].set_visible(False)
ax.spines["bottom"].set_color(GRID); ax.xaxis.grid(True,color=GRID,lw=0.8); ax.set_axisbelow(True)
ax.tick_params(colors=INK2,labelsize=9,length=0); ax.set_xlim(0,640)
ax.set_xticks([0,100,200,300,400,500]); ax.set_xticklabels(["$0","$100K","$200K","$300K","$400K","$500K"])
ax.set_title("What a 2,000 sq ft house costs by build system",loc="left",fontsize=13,color=INK,weight="bold",pad=30)
ax.text(0,1.08,"Construction cost with the 18% contractor margin removed. Black tick: co-op cost when members do all doable work.",transform=ax.transAxes,fontsize=9.5,color=INK2)
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=C[0],label="Materials"),Patch(color=C[1],label="Labor that must be hired"),Patch(color=C[2],label="Labor members can do")],loc="lower right",frameon=False,fontsize=9,ncol=3,bbox_to_anchor=(1,-0.2))
fig.text(0.01,0.01,"Modeled from Neuhaus 2026 cost tiers, NAHB 2024 cost shares, RSMeans labor shares and kit cost guides. East of Austin, standard finish, slab; excludes land and lot utilities.",fontsize=7.5,color=INK2)
fig.tight_layout(rect=(0,0.05,1,1)); fig.savefig(OUT,facecolor=SURF)
