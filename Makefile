syn_moho: syn_moho.o flat.o offset.o slope.o antiform.o synform.o fault.o
	$(LINK.c) -o $@ $@.o flat.o offset.o slope.o antiform.o synform.o fault.o
	gcc $@.o -o $@ flat.o offset.o slope.o antiform.o synform.o fault.o

flat.o: flat.c
	gcc -c flat.c

offset.o: offset.c
	gcc -c offset.c

slope.o: slope.c
	gcc -c slope.c

fault.o: fault.c
	gcc -c fault.c

antiform.o: antiform.c
	gcc -c antiform.c
  
synform.o: synform.c
	gcc -c synform.c
	
getintp.o: getintp.c
	gcc -c getintp.c

Intp.o: Intp.c
	gcc -c Intp.c
  
clean: 
      rm -f *.o
