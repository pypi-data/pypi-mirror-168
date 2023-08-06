def bubblesort(A):
    n=len(A)
    for i in range (n-1):
        for j in range (0,n-1-i):
            if(A[j]>A[j+1]):
               c=A[j]
               A[j]=A[j+1]
               A[j+1]=c
    return       

def insertionsort(A):
    n=len(A)
    for i in range (1,n-1):
      j=i-1
      key=A[i]
      while(j>=0 and key<A[j]):
          A[j+1]=A[j]
          j=j-1
      A[j+1]=key    
    return  
        
def selectionsort(A):
    n=len(A)
    for i in range (0,n-2):
        min=i
        for j in range (i+1,n-1):
            if(A[min]>A[j]):
                min=j
        if(min!=i):
            c=A[i]
            A[i]=A[min]
            A[min]=c        
    return