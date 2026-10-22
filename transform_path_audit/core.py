import math
from .common import number

def quat(values):
    if len(values)!=4:raise ValueError('quaternion')
    for v in values:number(v,-1,1)
    norm=math.sqrt(sum(v*v for v in values))
    if abs(norm-1)>1e-6:raise ValueError('unit_quaternion')
    return tuple(v/norm for v in values)
def mul(a,b):
    w,x,y,z=a;v,i,j,k=b
    return (w*v-x*i-y*j-z*k,w*i+x*v+y*k-z*j,w*j-x*k+y*v+z*i,w*k+x*j-y*i+z*v)
def conj(q):return (q[0],-q[1],-q[2],-q[3])
def rotate(q,v):return mul(mul(q,(0,*v)),conj(q))[1:]
def angular(a,b):return 2*math.acos(min(1,max(0,abs(sum(x*y for x,y in zip(a,b))))))

from collections import deque
from .common import unique_ids,identifier

def compose(edge,prior):
    eq,et=edge;pq,pt=prior;rt=rotate(eq,pt)
    return (mul(eq,pq),tuple(x+y for x,y in zip(rt,et)))
def inverse(transform):
    q,t=transform;i=conj(q);return i,rotate(i,tuple(-v for v in t))
def run(data):
    frames=data['frames'];edges=data['transforms'];root=data['reference'];at=number(data['at'],0,1e12);age=number(data['max_age'],0,1e12)
    if not 1<=len(frames)<=100 or len(set(frames))!=len(frames) or root not in frames or len(edges)>1000:raise ValueError('size_or_frames')
    for f in frames:identifier(f)
    unique_ids(edges);adj={f:[] for f in frames};rejected=[];valid=[]
    for e in edges:
        a,b=e['from'],e['to']
        if a not in adj or b not in adj:raise ValueError('frame')
        q=quat(e['q']);t=e['translation']
        if len(t)!=3:raise ValueError('translation')
        for v in t:number(v,-1e12,1e12)
        timestamp=number(e['time'],0,1e12)
        if timestamp>at or at-timestamp>age:rejected.append({'id':e['id'],'reason':'future' if timestamp>at else 'stale'});continue
        tr=(q,tuple(t));adj[a].append((b,tr,e['id']));adj[b].append((a,inverse(tr),e['id']));valid.append((e,tr))
    transforms={root:((1,0,0,0),(0,0,0))};paths={root:[]};queue=deque([root])
    while queue:
        a=queue.popleft()
        for b,tr,key in adj[a]:
            if b not in transforms:transforms[b]=compose(tr,transforms[a]);paths[b]=paths[a]+[key];queue.append(b)
    pos_tol=number(data.get('translation_tolerance',1e-6),0,1e6);rot_tol=number(data.get('angle_tolerance',1e-6),0,math.pi);conflicts=[]
    for e,tr in valid:
        a,b=e['from'],e['to']
        if a not in transforms or b not in transforms:continue
        predicted=compose(tr,transforms[a]);actual=transforms[b];distance=math.sqrt(sum((x-y)**2 for x,y in zip(predicted[1],actual[1])));angle=angular(predicted[0],actual[0])
        if distance>pos_tol or angle>rot_tol:conflicts.append({'edge':e['id'],'translation_error':distance,'angle_error_radians':angle,'path_to_from':paths[a],'path_to_to':paths[b]})
    return {'consistent_current_component':not conflicts,'conflicts':conflicts,'unreachable_frames':sorted(set(frames)-set(transforms)),'rejected_edges':rejected,'transforms_from_reference':{k:{'q':list(q),'translation':list(t)} for k,(q,t) in transforms.items()},'convention':'p_to = rotate(q,p_from) + translation; q order w,x,y,z'}
