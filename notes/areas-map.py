import json, math, sys
geo = json.load(open(sys.argv[1]))
CONSIDER = ["Bastrop","Caldwell","Guadalupe","Comal","Hays","Blanco","Burnet","Gillespie","Llano","Kendall","Williamson","Travis"]
CONTEXT = ["Lee","Fayette","Bexar","Kerr","Mason","San Saba","Lampasas","Bell","Milam","Gonzales","Wilson","Kimble","Medina","Bandera","Lavaca","Colorado","Falls","Coryell","McCulloch","DeWitt","Karnes","Atascosa","Washington","Burleson"]
K=300; CL=0.864
def P(lon,lat): return (20+(lon+99.5)*K*CL, 70+(31.0-lat)*K)
def dp(pts,eps):
    if len(pts)<3: return pts
    (x1,y1),(x2,y2)=pts[0],pts[-1]; dx,dy=x2-x1,y2-y1; L=math.hypot(dx,dy) or 1e-9
    dmax,idx=0,0
    for i in range(1,len(pts)-1):
        x,y=pts[i]; d=abs(dy*x-dx*y+x2*y1-y2*x1)/L
        if d>dmax: dmax,idx=d,i
    if dmax>eps: return dp(pts[:idx+1],eps)[:-1]+dp(pts[idx:],eps)
    return [pts[0],pts[-1]]
feat={f['properties']['NAME']:f for f in geo['features'] if f['properties']['STATE']=='48'}
paths=[]; cents=[]
for name in CONSIDER+CONTEXT:
    f=feat[name]; g=f['geometry']; polys=g['coordinates'] if g['type']=='MultiPolygon' else [g['coordinates']]
    d=""; allpts=[]
    for poly in polys:
        for ring in poly:
            pts=[P(lon,lat) for lon,lat in ring]; allpts+=pts
            h=len(pts)//2; pts=dp(pts[:h+1],0.7)[:-1]+dp(pts[h:],0.7)
            d+="M"+"L".join(f"{x:.0f} {y:.0f}" for x,y in pts)+"Z"
    cx=sum(p[0] for p in allpts)/len(allpts); cy=sum(p[1] for p in allpts)/len(allpts)
    paths.append({"name":name,"status":"considered" if name in CONSIDER else "context","d":d})
    cents.append({"name":name,"status":"considered" if name in CONSIDER else "context","x":round(cx),"y":round(cy)})
pins=[
 ("Elgin","Bastrop","east",30.350,-97.370,26000),("Smithville","Bastrop","east",30.009,-97.159,31900),
 ("Lockhart","Caldwell","east",29.885,-97.670,31500),("Luling","Caldwell","east",29.681,-97.648,20600),
 ("Liberty Hill","Williamson","east",30.665,-97.923,43000),("Wimberley","Hays","south",29.997,-98.099,43400),
 ("Kyle","Hays","south",29.989,-97.877,60400),("Niederwald","Hays","south",29.998,-97.751,46800),
 ("Seguin","Guadalupe","south",29.569,-97.965,16600),("Kingsbury","Guadalupe","south",29.651,-97.806,15000),
 ("Fischer","Comal","south",29.977,-98.263,38000),("Canyon Lake","Comal","south",29.875,-98.262,55800),
 ("Spring Branch","Comal","south",29.892,-98.418,104900),("New Braunfels","Comal","south",29.703,-98.124,109500),
 ("Blanco","Blanco","west",30.098,-98.422,24000),("Johnson City","Blanco","west",30.277,-98.412,28300),
 ("Burnet","Burnet","west",30.758,-98.228,27500),("Bertram","Burnet","west",30.743,-98.056,45000),
 ("Fredericksburg","Gillespie","west",30.275,-98.872,24700),("Harper","Gillespie","west",30.300,-99.244,19300),
 ("Llano","Llano","west",30.759,-98.675,12100),("Comfort","Kendall","west",29.968,-98.905,66500),
 ("Spicewood","Travis","west",30.476,-98.155,69700),
]
pinrows=[{"town":t,"county":c,"region":r,"lat":la,"lon":lo,"perAcre":pa} for t,c,r,la,lo,pa in pins]
json.dump({"paths":paths,"counties":cents,"pins":pinrows},open("mapdata.json","w"))
# SVG for the vault PNG
col={"east":"#1f5fa8","south":"#c2571a","west":"#2e7d4f"}
o=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 600" width="1520" height="1200" font-family="Inter, Helvetica, Arial, sans-serif" font-size="12">',
   '<rect width="760" height="600" fill="#ffffff"/>']
for p in paths:
    if p["status"]=="context": o.append(f'<path d="{p["d"]}" fill="#f4f4f2" stroke="#c9c9c4" stroke-width="0.8"/>')
for p in paths:
    if p["status"]=="considered": o.append(f'<path d="{p["d"]}" fill="#e9eef5" stroke="#6b7280" stroke-width="1.1"/>')
for c in cents:
    if c["status"]=="considered":
        ox,oy={"Caldwell":(0,22),"Guadalupe":(-40,-14),"Burnet":(-40,-12),"Hays":(-30,-12),"Comal":(-30,0),"Blanco":(0,-20),"Travis":(-10,-16)}.get(c["name"],(0,0))
        o.append(f'<text x="{c["x"]+ox}" y="{c["y"]+oy}" text-anchor="middle" font-size="10" fill="#6b7280" letter-spacing="0.8">{c["name"].upper()}</text>')
ax,ay=P(-97.743,30.267)
o.append(f'<path d="M{ax} {ay-9} l2.6 5.4 6 .9-4.3 4.2 1 6-5.3-2.8-5.3 2.8 1-6-4.3-4.2 6-.9z" fill="#111827"/><text x="{ax+9}" y="{ay+4}" font-weight="600" fill="#111827">Austin</text>')
for r in pinrows:
    x,y=P(r["lon"],r["lat"]); c=col[r["region"]]
    o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.5" fill="{c}" stroke="#fff" stroke-width="1.2"/>')
    dx,dy,anc=7,4,"start"
    if r["town"] in ("Niederwald","Bertram","Spring Branch","Luling","Wimberley","Elgin","Johnson City"): dx,dy,anc=(0,-8,"middle")
    if r["town"] in ("Kyle","Kingsbury","Seguin","New Braunfels"): dx,dy,anc=(0,14,"middle")
    if r["town"] in ("Lockhart","Harper","Fischer","Burnet"): dx,anc=(-7,"end")
    o.append(f'<text x="{x+dx:.1f}" y="{y+dy:.1f}" text-anchor="{anc}" font-size="11" fill="#111827">{r["town"]}</text>')
o.append('<text x="20" y="30" font-size="16" font-weight="600" fill="#111827">Where Friendstead could land: three arcs round Austin</text>')
o.append('<text x="20" y="48" font-size="11" fill="#6b7280">Towns with 15 to 60 acre listings opened October 2026; shaded counties are under consideration. Pin positions approximate.</text>')
lx=20; ly=580
for k,lab in (("east","East (base case), 25 to 35 miles"),("south","South, 25 to 55 miles"),("west","West, 45 to 80 miles")):
    o.append(f'<circle cx="{lx+5}" cy="{ly-4}" r="4.5" fill="{col[k]}"/><text x="{lx+14}" y="{ly}" font-size="11" fill="#111827">{lab}</text>'); lx+=215
o.append('</svg>')
open("map.svg","w").write("\n".join(o))
print(len(json.dumps(paths)), "bytes of paths;", len(pinrows), "pins")
