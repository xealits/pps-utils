# correct C organization -- with rake and meaningful directories

it's similar to python packages structure

what to be done for the project, in C, in Python and in linux?

CAEN lib is the "driver" of the whole VME bus with boards for the application,
it is called by all [PC-based] linux-based stuff (by the "controling" part of the DAQ system)
I need:
* a test version of the lib
* a python utility for manual/quick access, for tests, prototyping and building experimental stuff
  for example board "adaptors" are implemented here first
* a fast "run" process in C
  with some cooperation/IPC fetures for additional (DQM) processes
  and some additional features:
    variable amount and set of cards in the process (without recompilation/change of source for this),
    with good log/reporting with full listing of card configs,
   (in principle the preliminary checks,
    config listing can be obtained from by a Python module,
    then the module launches the C "run-process")
    visible current parameters of the running process
   (not sure if it's possible -- with shared memory? just environment variables?
    it would be nice to expose exactly the numbers in memory, which the process runs on)
    changing output to memory disk for speed
* "a run" is a comlpex operation, for programming and running operations it must be taken apart into simple parts;
  a run configures the boards, logs the config, reads them, logs errors and full buffers, writes the binary
  -- the "reader" part can be separated from configuration;
  operations should have a unified and flexible system, there are diverse tasks,
  like testing and running in all kinds of configurations,
  but they should be carried out in similar manner, without "context-switching" between different systems;
  the system is naturally composed of all the physical and software parts:
  the bus, the boards, the CPU with linux and daq
* a set of linux administration facilities to organize this in 1 DAQ system, text interface for now
  (logging, control group)
* the gui is for later
  not clear what to show in GUI??
  in principle -- show all, but in convenient visualization, in general more readable interface,
  to prepare for that everything should be done in "protocol-based" fashion,
  i.e. with json/UBF-like parseble interfaces between modules of the system,
  not text-readable, which requires some glue to parse,
  text-readable output is a human interface feature, it's like GUI, but done in ASCII typography






# parts of the daq system

the bus, the boards, the CPU with linux and daq


## the bus

special class for the bus?

A C object file defines 1 object. Make it executable and run many processes on linux and it is sort of a class.

The bus in Python is a pythonic object, with automatic exit when needed etc,
but in C you operate it manualy, handling signals to exit etc.
Is one implementation for both languages possible?


## the boards




## the CPU with linux and daq

log, communications (messaging stack -- dqm could probably run from the log alone?)









# organizational ideas

* linux (unix?) is an interpreter
  it is a programmable environment on its' own,
  the DAQ is a program of linux, its' facilities and userland packages, not a program on its' own
* good logging of the system (probably I need some flexibility for tests, code tests, more "public" tests, real runs etc)
* good IPC facility, simple, manageable and easily extendable (message queues for starters)
* possibility of cron daily reports for shifts
  this is a feature of DAQ overall, as part of a linux machine, not 1 run of bunch of processes,
  it uncovers this structure, should be well organized,
  similar feature would be to record the git hash or hash of binary content of files before the run
* C sources of the project are organized with meningful directories and rake from Ruby
* "detailed manual control" utilities with access to VME and all boards done in Python
  for prototyping and testing
* adapter pattern for the boards, the bus, maybe other parts of the system (like the record process)
  it means full access to all and exactly the same interfaces of the parts of the system
* "procol-based" interfaces of different parts of the project
  i.e. all programs implement some parsable protocol for their interfaces,
  not human-readable text -- that's a matter of representation, of human interface,
  it's the same as GUI, it's typography in ASCII
* DAQ will be first implemented in text
* then GUI will be naturally added, thanks to the programmable protocols of the project,
  it should have convenient "visualizations of quantitative information"
  and in general readable representation of the system
  (typography, text+graphic, grid, abstract/perfect skeuomorphism, warm/cold colours etc)

