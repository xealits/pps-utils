# PipeHub should be a shared library
# then there should be a startup process,
# written in C, shell, Python,
# which parses shell options
# and starts PipeHub with this configuration

vpath %.c src
vpath %.h include

# to pass the include directory to gcc
#CFLAGS = -I include -std=c99
CFLAGS = -I include -DLINUX -std=gnu99
CFLAGS_CAEN = -lCAENVME -L/usr/lib/ -I /usr/include
CFLAGS_TEST = -I include/test

# default target, C startup process for PipeHub
#gcc pipe-hub.c PipeHub.o CAENVMECalls.o -o pipe-hub
# make does not use the correct path for files in directories
pipe-hub: pipe-hub.o CAENVMECalls.o PipeHub.o
	#          > All together, the main process with [ C startup pipe-hub ]
	gcc $(CFLAGS) $(CFLAGS_CAEN) -o $@ $^


# gcc -I include -c $<
pipe-hub.o: pipe-hub.c PipeHub.h
	#          > [ The C startup pipe-hub object ] [TEST]
	gcc $(CFLAGS) $(CFLAGS_CAEN) -c $<



# PipeHub.o: PipeHub.c CAENVMECalls.h CAENVMECalls.o
# PipeHub.o: PipeHub.c CAENVMECalls.o
# PipeHub.o: PipeHub.c CAENVMECalls.h PipeHub.h
# now the PipeHub.h contains some definitions, used in PipeHub.c
PipeHub.o: PipeHub.c PipeHub.h CAENVMECalls.h
	#          > [ The PipeHub object ]
	gcc $(CFLAGS) -c $<

# also the header of CAEN library should be included
CAENVMECalls.o: CAENVMECalls.c
	#          > [ The CAENVMECalls lib interface object ]
	gcc $(CFLAGS) $(CFLAGS_CAEN) -c $<




# test version
# with the dummy CAENVMElib
pipe-hub-test: pipe-hub-test.o CAENVMECalls-test.o PipeHub.o CAENVMElib.o
	#          > All together, the main process with [ C startup pipe-hub ] [TEST]
	gcc $(CFLAGS) $(CFLAGS_TEST) -o $@ $^

pipe-hub-test.o: pipe-hub.c PipeHub.h
	#          > [ The C startup pipe-hub object ]
	gcc $(CFLAGS) $(CFLAGS_TEST) -c $< -o $@

CAENVMECalls-test.o: CAENVMECalls.c
	#          > [ The CAENVMECalls lib interface object ]
	gcc $(CFLAGS) $(CFLAGS_TEST) -c $< -o $@

CAENVMElib.o: CAENVMElib.c
	gcc $(CFLAGS) $(CFLAGS_TEST) -c $<


clear:
	rm *.o

