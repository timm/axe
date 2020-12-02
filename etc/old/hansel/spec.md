R={R1,R2,...}

R= (p=options, j=objectives)

* _<,>,=_ is worse, better, same is is defined over p.
* Distance "_D_" is defined over j
    * D(r,r)=0
    * D(r1,r2) = D(r2,r1)
    * D(r1,r3) &le; D(r1,r2) + D(r2,r3)
 
def mix(r1,r2):

+ ws = r1.u + r2.u
+ w1 = r1.u/ws
+ w2 = r2.u/ws
+ new = (r1 * w1 + r2 * w2) / ws
+ new.u = ws
+ return new
  
v = <pos,u>
close=Close()  
Pop = 20 random R  
while True:  

   + one = any(Pop)  
   + two,d2,three,d3 = nearest(one,Pop)
   + a,c = D(one,two), D(one,three)
   + x = (a^2 * c^2 - b^2)/(2c)
   + y = (a^2 - x^2)^0.5
   + c2 = close(d2)
   + c3 = close(d3)
   + cy = close(y) 
   + if c2 and two.dead
       one = dead
       
       
       
   
   
   Pop += R

_Close_ 