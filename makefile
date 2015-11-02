# PipeHub should be a shared library
# then there should be a C process or shell/Python script processing shell options and configuring pipe-hub

vpath %.c src
vpath %.h include

# to pass the include directory to gcc
CFLAGS = -I include -std=c99

pipe-hub: pipe-hub.o CAENVMECalls.o PipeHub.o
	#gcc pipe-hub.c PipeHub.o CAENVMECalls.o -o pipe-hub
	# make does not use the correct path for files in directories
	gcc $(CFLAGS) -o $@ $^

pipe-hub.o: pipe-hub.c PipeHub.h
	# gcc -I include -c $<
	gcc $(CFLAGS) -c $<

# PipeHub.o: PipeHub.c CAENVMECalls.h CAENVMECalls.o
# PipeHub.o: PipeHub.c CAENVMECalls.o
PipeHub.o: PipeHub.c CAENVMECalls.h
	gcc $(CFLAGS) -c $<

# also the header of CAEN library should be included
CAENVMECalls.o: CAENVMECalls.c
	gcc $(CFLAGS) -c $<



clear:
	rm *.o

