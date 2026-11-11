from pathlib import Path
import json,math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon,Circle,Patch
from matplotlib.lines import Line2D
from matplotlib.colors import LinearSegmentedColormap,LightSource,BoundaryNorm
S=json.loads(Path('validation/reset-a/terrain-survey.json').read_text());C=json.loads(Path('validation/reset-a/comparison.json').read_text());D=json.loads(Path('validation/reset-a/layout-details.json').read_text());P=json.loads(Path('validation/reset-a/profiles.json').read_text());g=S['grid'];step=g['step'];axis=np.arange(g['n'])*step+g['min'];H=np.array(g['heights']).reshape(g['n'],g['n']);F=np.array(g['fractions']).reshape(H.shape);X,Z=np.meshgrid(axis,axis);gz,gx=np.gradient(H,step);slope=np.hypot(gx,gz)*100;out=Path('docs/urban-atlas/reset-a');out.mkdir(parents=True,exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'savefig.facecolor':'#f8f6ef'})
soil=LinearSegmentedColormap.from_list('island',['#e5dfba','#b9c797','#8aa57b','#667e6c','#d2cdb6'])

def world(r,u,v):
 a=math.radians(r['angle']);f=np.array([math.cos(a),math.sin(a)]);q=np.array([-f[1],f[0]]);mid=18 if r['template']=='hub'else 24;return np.array(r['centre'])+q*u+f*(v-mid)
def rect(r,u,v,w,d):return np.array([world(r,x,z)for x,z in[(u-w/2,v-d/2),(u+w/2,v-d/2),(u+w/2,v+d/2),(u-w/2,v+d/2)]])
def base(ax,centre,span=46):
 masked=np.ma.masked_where(F>.98,H);ax.set_facecolor('#e0edf0');ax.imshow(masked,extent=[axis[0],axis[-1],axis[-1],axis[0]],cmap=soil,vmin=10,vmax=50,interpolation='none');ax.contour(X,Z,masked,levels=np.arange(10,51,2),colors='#72816a',alpha=.55,linewidths=.45)
 for trail in S['trails']:
  p=np.array(trail['points']);ax.plot(p[:,0],p[:,1],color='#90744e',ls=(0,(3,2)),lw=1.1,alpha=.7)
 p=np.array(S['stream']);ax.plot(p[:,0],p[:,1],color='#4398af',lw=2.2)
 b=np.array(S['boundary']);ax.plot(b[:,0],b[:,1],color='#6d7d73',lw=1)
 ax.set(xlim=(centre[0]-span,centre[0]+span),ylim=(centre[1]+span,centre[1]-span),xlabel='World X · metres',ylabel='World Z · metres (north = −Z)');ax.set_aspect('equal');ax.grid(alpha=.12,color='#314441');ax.tick_params(labelsize=8)
 # 10 m scale and north arrow, aligned to world axes.
 x=centre[0]-40;z=centre[1]+39;ax.plot([x,x+10],[z,z],lw=3,color='#203f3b');ax.text(x+5,z-1.8,'10 m',ha='center',fontsize=9,weight='bold');ax.annotate('N',xy=(centre[0]+38,centre[1]-39),xytext=(centre[0]+38,centre[1]-29),ha='center',fontsize=11,weight='bold',arrowprops=dict(arrowstyle='-|>',color='#203f3b',lw=1.5))
for k,r in C.items():
 d=D[k];fig=plt.figure(figsize=(14,10.3),facecolor='#f8f6ef');ax=fig.add_axes([.055,.12,.665,.79]);panel=fig.add_axes([.755,.13,.22,.76]);panel.axis('off');base(ax,r['centre']);title='A · SALVAGE THE CURRENT SITE'if k=='A'else'B · RE-SITE AS ONE CIVIC CLUSTER';fig.text(.055,.957,title,fontsize=20,weight='bold',color='#203f3b');fig.text(.055,.925,'R0-RESET-A  |  Scaled layout study on accepted terrain  |  UNBUILT — owner decision pending',fontsize=10,color='#52625d')
 hull=np.array(r['hull']);ax.add_patch(Polygon(hull,facecolor='none',edgecolor='#ad805b',ls=':',lw=1.5))
 if k=='A':
  for old in S['plots']:
   id,u,v,w,dep,h=old;ax.add_patch(Polygon([[36+u-w/2,44-v-dep/2],[36+u+w/2,44-v-dep/2],[36+u+w/2,44-v+dep/2],[36+u-w/2,44-v+dep/2]],facecolor='none',edgecolor='#59665f',ls='--',lw=.8,alpha=.65))
  ax.plot([36,36,35,26.2],[44,9,12.6,12.6],ls='--',lw=1,color='#566660',alpha=.6);ax.add_patch(Polygon([[17.5,3],[30.5,3],[30.5,15],[17.5,15]],facecolor='none',edgecolor='#59665f',ls='--',lw=.8,alpha=.6))
 for p in r['program']:
  col='#d8a273'if p['kind']=='building'else '#f1dfbe'if p['id']=='square'else '#eee7ce'if p['kind']=='public'else '#c7b5ce';edge='#825839'if p['kind']=='building'else '#917e55'if p['kind']=='public'else '#715b87';ax.add_patch(Polygon(p['polygon'],facecolor=col,edgecolor=edge,lw=1.2,ls='--'if p['kind']=='reserve'else '-',zorder=4))
  if p['kind']=='building':
   c=world(r,p['u'],p['v']);ax.text(*c,p['id'],ha='center',va='center',fontsize=10,weight='bold',zorder=10,bbox=dict(facecolor='#fcf6e9',edgecolor='none',alpha=.8,pad=1));front=p['u']+(p['w']/2 if p['u']<0 else-p['w']/2);q=world(r,front,p['v']);b=world(r,front+(1.7 if p['u']<0 else-1.7),p['v']);ax.annotate('',xy=b,xytext=q,arrowprops=dict(arrowstyle='-|>',color='#343f3a',lw=1.1),zorder=11)
  if p['id']=='guild':
   c=world(r,p['u'],p['v']);ax.text(*c,'G\n10 × 8 m\nRESERVE',ha='center',va='center',fontsize=7.8,color='#443351',weight='bold',zorder=8)
 for p in r['program'][:4]:
  edge=(7 if k=='B'and p['id']in ['B3','B4']else 3)*(1 if p['u']>0 else -1);front=p['u']-np.sign(p['u'])*p['w']/2;ax.add_patch(Polygon(rect(r,(edge+front)/2,p['v'],abs(edge-front),2.4),facecolor='#f1dfbe',edgecolor='#917e55',lw=.6,zorder=6))
 for roof in d['roofs']:ax.add_patch(Polygon(roof['polygon'],facecolor='none',edgecolor='#795b44',lw=.8,zorder=7))
 sq=next(p for p in r['program']if p['id']=='square');fc=world(r,0,sq['v']);ax.add_patch(Circle(fc,1.4,facecolor='#78aaa5',edgecolor='#315c5a',lw=1,zorder=9));ax.text(*fc,'F',ha='center',va='center',fontsize=8,color='white',weight='bold',zorder=10);ax.add_patch(Polygon(rect(r,3.8,sq['v']+4,4.6,4.2),facecolor='#ac7652',edgecolor='#6c503c',lw=1,zorder=8));c=world(r,3.8,sq['v']+4);ax.text(*c,'P',fontsize=8,ha='center',va='center',color='white',zorder=10)
 route=np.array(d['arrival']['line']+r['primaryCoreRoute'][1:]);ax.plot(route[:,0],route[:,1],color='#176683',lw=3.2,zorder=12);ax.scatter(*r['entry'],s=36,facecolor='white',edgecolor='#176683',zorder=13)
 # Open axis is reserved; this is a plan sightline, not a verified player render.
 a=world(r,0,3);b=world(r,0,next(p for p in r['program']if p['id']=='guild')['v']-4);ax.plot([a[0],b[0]],[a[1],b[1]],color='#73538e',ls=(0,(2,2)),lw=1.3,zorder=12)
 if k=='A':optional=np.array(P[k]['optionalHighland']['line'])
 else:optional=np.array([r['entry'],[26,49],[22,42],[16,36],[12,29],[11,22],[6,15],[-5,5]])
 ax.plot(optional[:,0],optional[:,1],color='#307d59',ls=(0,(4,3)),lw=2,zorder=5)
 trees=np.array([[t['x'],t['z']]for t in S['trees']]);ax.scatter(trees[:,0],trees[:,1],s=13,facecolor='#3e7157',alpha=.35,zorder=3);ids=d['combinedTreeConflictIds'];ax.scatter(trees[ids,0],trees[ids,1],s=43,facecolor='none',edgecolor='#b44e43',lw=1.2,zorder=14)
 ax.scatter(27,57,s=60,marker='o',c='#176683',edgecolor='white',zorder=15);ax.annotate('Original arrival',xy=(27,57),xytext=(10,14),textcoords='offset points',fontsize=9,weight='bold',bbox=dict(facecolor='#f8f6ef',edgecolor='none',alpha=.9,pad=2),zorder=15)
 ax.scatter(27,60,s=55,marker='s',facecolor='#bed8df',edgecolor='#36728a',zorder=14);ax.annotate('Future skyport tie',xy=(27,60),xytext=(8,12),textcoords='offset points',fontsize=8,zorder=15)
 ax.scatter(-5,5,s=35,marker='^',c='#307d59',zorder=15);ax.annotate('Highland trail junction',xy=(-5,5),xytext=(8,-12),textcoords='offset points',fontsize=8,color='#285c42',zorder=15,bbox=dict(facecolor='#f8f6ef',edgecolor='none',alpha=.85,pad=1))
 panel.text(0,1,'PROPOSED CAPACITY',weight='bold',fontsize=11,color='#203f3b');panel.text(0,.953,f"4 existing buildings\n182 m² square reservation\n80 m² Guild reservation\n6 m clear promenade\n{r['areaContiguousEnvelope']:.0f} m² cluster envelope",va='top',linespacing=1.55,fontsize=10)
 panel.text(0,.727,'MEASURED COMPARISON',weight='bold',fontsize=11,color='#203f3b');panel.text(0,.68,f"Primary route: {d['totalProposedPrimaryHorizontalLength']:.1f} m\nCore: {d['core']['horizontalLength']:.1f} m\nCivic grade: {abs(r['grade'])*100:.0f}%\nEntry level: {r['h0']:.2f} m\nSquare level: {sq['floor']:.2f} m\nResidual support: {r['supportAfterBoundedGradingRange'][1]:.2f} m max\nTrunk conflicts: {len(ids)}",va='top',linespacing=1.55,fontsize=10)
 panel.text(0,.365,'KEY TRADE-OFF',weight='bold',fontsize=11,color='#203f3b');panel.text(0,.322,('Fewer tree conflicts; long uphill\napproach and retained structures.\nSquare re-centred on the axis.'if k=='A'else'Lower supports; more tree moves.\nSkyport level and long optional\nhighland return need owner review.'),va='top',linespacing=1.5,fontsize=9.5)
 handles=[Line2D([0],[0],color='#176683',lw=3,label='Primary route proposal'),Line2D([0],[0],color='#307d59',ls='--',lw=2,label='Optional trail link (untested)'),Line2D([0],[0],color='#73538e',ls=':',lw=1.5,label='Reserved civic sightline'),Line2D([0],[0],color='#795b44',lw=.9,label='Approved-model envelope'),Line2D([0],[0],marker='o',ms=7,mfc='none',mec='#b44e43',ls='none',label='Potential tree conflict')];panel.legend(handles=handles,loc='lower left',bbox_to_anchor=(-.03,.045),frameon=False,fontsize=8.5,handlelength=2)
 inset=ax.inset_axes([.015,.745,.21,.21]);inset.set_facecolor('#f4f2e9');inset.imshow(np.ma.masked_where(F>.98,H),extent=[axis[0],axis[-1],axis[-1],axis[0]],cmap=soil,vmin=10,vmax=50);bd=np.array(S['boundary']);inset.plot(bd[:,0],bd[:,1],color='#516b5b',lw=.6)
 for key,rr in C.items():
  hh=np.array(rr['hull']);inset.add_patch(Polygon(hh,facecolor='none',edgecolor='#b06f3d'if key=='A'else '#176683',lw=1.5));inset.text(*rr['centre'],key,fontsize=7,weight='bold')
 inset.scatter(-45,-49,s=12,c='#43594a',marker='^');inset.scatter(-72,38,s=10,c='#4398af');inset.set(xlim=(-110,110),ylim=(110,-110),xticks=[],yticks=[]);inset.set_aspect('equal');inset.set_title('ISLAND LOCATOR',fontsize=7,pad=3)
 fig.text(.055,.06,'F = reused fountain  ·  P = reused pavilion  ·  arrows = frontage directions  ·  dashed Guild = planning reserve only',fontsize=9,color='#435c53');fig.text(.055,.035,'Exact game height sampler at 0.5 m spacing. Earthworks, thresholds, tree moves, sightlines and controller routes are proposals, not installed geometry.',fontsize=8.5,color='#52625d');fig.savefig(out/f'alternative-{k.lower()}.png',dpi=170);fig.savefig(out/f'alternative-{k.lower()}.svg');plt.close(fig)
# Same-scale elevation and raw-slope comparison, plus continuous route sections.
fig,axes=plt.subplots(3,2,figsize=(14,13),facecolor='#f8f6ef');fig.suptitle('ACTUAL TERRAIN + PROPOSED CIVIC SECTIONS',fontsize=18,weight='bold',color='#203f3b',y=.976);cmap=plt.get_cmap('YlOrRd',5);norm=BoundaryNorm([0,8,12,25,40,150],5)
for col,(k,r)in enumerate(C.items()):
 for row in [0,1]:
  ax=axes[row,col];raw=np.ma.masked_where(F>.98,H if row==0 else slope);im=ax.imshow(raw,extent=[axis[0],axis[-1],axis[-1],axis[0]],cmap=soil if row==0 else cmap,vmin=10 if row==0 else None,vmax=50 if row==0 else None,norm=None if row==0 else norm,interpolation='none');ax.contour(X,Z,np.ma.masked_where(F>.98,H),levels=np.arange(10,51,2),colors='#4f6259',linewidths=.4,alpha=.4);hp=np.array(r['hull']);ax.add_patch(Polygon(hp,facecolor='none',edgecolor='#234b52',lw=1.8));c=r['centre'];ax.set(xlim=(c[0]-31,c[0]+31),ylim=(c[1]+31,c[1]-31));ax.set_aspect('equal');ax.tick_params(labelsize=8);ax.set_title(f"{k} · {'Elevation (m)'if row==0 else 'Raw terrain grade (%)'}",loc='left',fontsize=11,weight='bold');fig.colorbar(im,ax=ax,shrink=.76,pad=.02)
 ax=axes[2,col];arrival=P[k]['arrival'];core=P[k]['core'];aa=D[k]['arrival']['sampledDesignLevels'];cc=D[k]['core']['sampledDesignLevels'];x=np.array([q['s']for q in arrival['rows']]+[arrival['length']+q['s']for q in core['rows'][1:]]);raw=np.array([q['y']for q in arrival['rows']]+[q['y']for q in core['rows'][1:]]);design=np.array(aa+cc[1:]);ax.plot(x,raw,color='#88714e',lw=1.8,label='Actual terrain at route');ax.plot(x,design,color='#176683',lw=2,label='Unbuilt route grade');ax.fill_between(x,raw,design,where=design>=raw,color='#d9ab70',alpha=.38);ax.fill_between(x,raw,design,where=design<raw,color='#88aaa2',alpha=.5);ax.axvline(arrival['length'],color='#aaa499',ls=':',lw=1);ax.text(arrival['length']+.6,23.2,'Market entry',fontsize=8,rotation=90,va='top');ax.set(xlabel='Horizontal walking distance (m)',ylabel='Elevation (m)',ylim=(12,24),xlim=(0,78));ax.grid(alpha=.2);ax.legend(fontsize=8,loc='lower right');ax.set_title(f'{k} · Same scale, arrival → Guild reserve',loc='left',fontsize=11,weight='bold')
fig.text(.06,.022,'Terrain is unchanged. Grade maps use 1 m centred finite differences on a 0.5 m sampler grid; extreme local faces remain visible.\nSections show a design grade only. They do not demonstrate built support, collision continuity, traversal or rendered landmark visibility.',fontsize=9,color='#52625d');fig.subplots_adjust(left=.065,right=.965,top=.94,bottom=.085,wspace=.24,hspace=.27);fig.savefig(out/'terrain-comparison.png',dpi=160);fig.savefig(out/'terrain-comparison.svg');plt.close(fig)
print('Saved two scaled plans and terrain/route comparison.')
