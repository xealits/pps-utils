# PipeHub should be a shared library
# then there should be a startup process,
# written in C, shell, Python,
# which parses shell options
# and starts PipeHub with this configuration

vpath %.c src
vpath %.h include

# to pass the include directory to gcc
CFLAGS = -I include -std=c99

# default target, C startup process for PipeHub
#gcc pipe-hub.c PipeHub.o CAENVMECalls.o -o pipe-hub
# make does not use the correct path for files in directories
pipe-hub: pipe-hub.o CAENVMECalls.o PipeHub.o
	#          > All together, the main process with [ C startup pipe-hub ]
	gcc $(CFLAGS) -o $@ $^

# gcc -I include -c $<
pipe-hub.o: pipe-hub.c PipeHub.h
	#          > [ The C startup pipe-hub object ]
	gcc $(CFLAGS) -c $<

# PipeHub.o: PipeHub.c CAENVMECalls.h CAENVMECalls.o
# PipeHub.o: PipeHub.c CAENVMECalls.o
# PipeHub.o: PipeHub.c CAENVMECalls.h PipeHub.h
# tecnically, the object does not depend on the header file
# (in a normal language they should be one thing)
PipeHub.o: PipeHub.c CAENVMECalls.h
	#          > [ The PipeHub object ]
	gcc $(CFLAGS) -c $<

# also the header of CAEN library should be included
CAENVMECalls.o: CAENVMECalls.c
	#          > [ The CAENVMECalls lib interface object ]
	gcc $(CFLAGS) -c $<



clear:
	rm *.o
