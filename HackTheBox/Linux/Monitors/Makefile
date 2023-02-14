obj-m +=reverse-shell.o
all:
	make -C /lib/modules/4.15.0-151-generic/build M=$(shell pwd) modules
clean:
	make -C /lib/modules/4.15.0-151-generic/build M=$(shell pwd) clean
