"""Deterministic Euclidean travelling-salesperson heuristic, depot at index zero."""
import math

def distance(a,b):return math.hypot(a[0]-b[0],a[1]-b[1])
def length(points,route):
    return sum(distance(points[route[i]],points[route[(i+1)%len(route)]]) for i in range(len(route))) if route else 0

def solve(points):
    if not 1<=len(points)<=100:raise ValueError('Supply 1 to 100 points')
    if any(len(p)!=2 or any(type(v) not in (int,float) or not math.isfinite(v) or abs(v)>10000 for v in p) for p in points):
        raise ValueError('Each point must have two finite coordinates within +/-10000')
    remaining=set(range(1,len(points)));route=[0]
    while remaining:
        nxt=min(remaining,key=lambda j:(distance(points[route[-1]],points[j]),j))
        route.append(nxt);remaining.remove(nxt)
    initial=length(points,route);passes=0
    while passes<100:
        improved=False
        for i in range(1,len(route)-1):
            for j in range(i+1,len(route)):
                a,b=route[i-1],route[i];c,d=route[j],route[(j+1)%len(route)]
                if distance(points[a],points[c])+distance(points[b],points[d]) < distance(points[a],points[b])+distance(points[c],points[d])-1e-9:
                    route[i:j+1]=reversed(route[i:j+1]);improved=True
        passes+=1
        if not improved:break
    final=length(points,route)
    return {'route':route,'nearest_neighbour_length':initial,'optimised_length':final,
            'saved_percent':round((initial-final)/initial*100,2) if initial else 0,'passes':passes}
