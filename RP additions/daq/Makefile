CFLAGS = -O3 -march=armv7-a -mtune=cortex-a9 -mfpu=neon -mfloat-abi=hard

all: daq-server

daq-server: daq-server.c
	gcc $(CFLAGS) -o $@ $^ -lm -lpthread


clean:
	rm -f daq-server
