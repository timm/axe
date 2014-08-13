def life(width=40,height=40,generations=500,prob=0.15,wait=0.1,seed=1):
  import numpy,os,time,random
  if seed: random.seed(seed)
  def pause(): time.sleep(wait)
  def clear(): os.system('cls' if os.name == 'nt' else 'clear')
  def stars(x): return "*" if x==1 else " "
  def play_life(a,width=10,height=10):
    xmax, ymax = a.shape
    b = a.copy() # copy grid & Rule 2
    for x in range(xmax):
      for y in range(ymax):
        n = numpy.sum(a[max(x - 1, 0):min(x + 2, xmax), 
                        max(y - 1, 0):min(y + 2, ymax)]) - a[x, y]
        if a[x, y]:
          if n < 2 or n > 3:
            b[x, y] = 0 # Rule 1 and 3
        elif n == 3:
          b[x, y] = 1 # Rule 4
    return(b)
  def randoms(p):
    for line in life:
      for n in range(len(line)):
        if line[n] != 1:
          line[n] = 0 if random.random() > p else 1
  life = numpy.zeros((width, height), dtype=numpy.byte)
  randoms(prob)
  for i in range(generations):
    clear()
    print "generation:", i,"of",generations,"\n"
    life = play_life(life)
    print ""
    for line in life: 
      print ' '.join(map(stars,line))
    randoms(prob/1000.0)
    
    pause()

