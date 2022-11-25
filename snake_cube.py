import numpy as np
import sys
from Solution import printCube
dbg=1
dim=3
seq = np.array([3,2,2,2,1,1,1,2,2,1,1,2,1,2,1,1,2], np.int8)
def testAllDir(cube,idx,seq,iseq,dir0):
   if iseq==len(seq):
      print('Completed')
      return 1
   elif iseq==0:
      d = np.nditer(np.array([3]))
      dir0=2
   else:
      d = np.nditer(np.array([1,-1,2,-2,3,-3]))
   if dbg:
      print('%6.2f%%, iseq %3d/%3d, seq=%d, dir0=%d starting at idx=<%d,%d,%d>' % ((iseq+1)/len(seq)*100,iseq+1,len(seq),seq[iseq],dir0,idx[0],idx[1],idx[2]))
   while not d.finished:
      if dbg>2:
         print('- dir0 (%d) --> dir1 (%d)' % (dir0,d[0]))
      if not abs(d[0])==abs(dir0):
         idx1  = idx.copy()
         if addseq(cube,idx1,seq[iseq],d[0],iseq+1):
            if iseq==len(seq):
               return 1
            dir1=d[0]
            iseq+=1
            if testAllDir(cube,idx1,seq,iseq,dir1):
               return 1
            else:
               if dbg>2:
                  print('All direction filled')
               iseq-=1
               clearAll(cube,iseq+1)
               if dbg:
                  print('%6.2f%%, iseq %3d/%3d, seq=%d, dir0=%d starting at idx=<%d,%d,%d>' % ((iseq+1)/len(seq)*100,iseq+1,len(seq),seq[iseq],dir0,idx[0],idx[1],idx[2]))
      elif dbg>2:
         print("    Skipping direction d[0]=%d, same as dir0=%d" % (d[0],dir0))
      d.iternext()
   return 0
def addseq(cube,idx,seqlen,dir1,ival):
   if dbg>2:
      print('    adding %d times %d starting from idx=<%d,%d,%d>' % (seqlen,ival,idx[0],idx[1],idx[2]))
   idx2=idx.copy()
   if dir1==1:
      vect = cube[idx2[0]+1::,idx2[1]    ,idx2[2]]
      idx2[0]+=seqlen
   elif dir1==-1:
      vect = cube[:idx2[0]:  ,idx2[1]    ,idx2[2]]
      idx2[0]-=seqlen
   elif dir1==2:
      vect = cube[idx2[0]    ,idx2[1]+1::,idx2[2]]
      idx2[1]+=seqlen
   elif dir1==-2:
      vect = cube[idx2[0]    ,:idx2[1]:  ,idx2[2]]
      idx2[1]-=seqlen
   elif dir1==3:
      vect = cube[idx2[0]    ,idx2[1]    ,idx2[2]+1::]
      idx2[2]+=seqlen
   elif dir1==-3:
      vect = cube[idx2[0]    ,idx2[1]    ,:idx2[2]:]
      idx2[2]-=seqlen
   else:
      print('      Error, %d is not a valid direction' % dir1)
      return 0
   if len(vect)<seqlen:
      if dbg>2:
         print('      Error, sequence length (%d) too long for given space (%d)' % (seqlen,len(vect)))
      return 0
   elif len(vect)==seqlen:
      vectLen = vect
   else:
      if dir1>0:
         vectLen = vect[0:seqlen]
      else:
         vectLen = vect[-1:len(vect)-seqlen-1:-1]
   if sum(vectLen)>0:
      if dbg>2:
         print('      Error, space already filled',vectLen)
      return 0
   vectLen+=ival
   idx[0]=idx2[0]
   idx[1]=idx2[1]
   idx[2]=idx2[2]
   return 1
def clearAll(cube,iseq):
   it = np.nditer(cube, op_flags=['readwrite'])
   while not it.finished:
      if it[0]>=iseq:
         it[0]=0
      it.iternext()
   if dbg>2:
      print('      clearAll iseq=%d' % iseq)
cube = np.zeros( (dim, dim, dim), np.int8 )
if dbg:
   print(seq)
if sum(seq)-dim**3:
   print("Error, the sum of all pieces, %d\ndoes not match with the dimension of the cube %s**3=%s\n" % (sum(seq), dim, dim**3))
else:
   print("OK, the sum of all pieces, %d\nmatches with the dimension of the cube %s**3=%s\n" % (sum(seq), dim, dim**3))
iseq=0
dir0=0
itstart = np.nditer(cube[0:dim,0:dim,0:dim-seq[0]+1], flags=['multi_index'])
while not itstart.finished:
   p = np.array([itstart.multi_index[0],
                 itstart.multi_index[1],
                 itstart.multi_index[2]-1], np.int8)
   if testAllDir(cube,p,seq,iseq,dir0):
      break
   itstart.iternext()
printCube(cube)
