# Arduino Makefile
# Arduino adaptation by mellis, eighthave, oli.keller
#
# This makefile allows you to build sketches from the command line
# without the Arduino environment (or Java).
#
# Detailed instructions for using the makefile:
#
#  1. Copy this file into the folder with your sketch. There should be a
#     file with the same name as the folder and with the extension .pde
#     (e.g. foo.pde in the foo/ folder).
#
#  2. Modify the line containg "INSTALL_DIR" to point to the directory that
#     contains the Arduino installation (for example, under Mac OS X, this
#     might be /Applications/arduino-0012).
#
#  3. Modify the line containing "PORT" to refer to the filename
#     representing the USB or serial connection to your Arduino board
#     (e.g. PORT = /dev/tty.USB0).  If the exact name of this file
#     changes, you can use * as a wildcard (e.g. PORT = /dev/tty.usb*).
#
#  4. Set the line containing "MCU" to match your board's processor. 
#     Older one's are atmega8 based, newer ones like Arduino Mini, Bluetooth
#     or Diecimila have the atmega168.  If you're using a LilyPad Arduino,
#     change F_CPU to 8000000.
#
#  5. At the command line, change to the directory containing your
#     program's file and the makefile.
#
#  6. Type "make" and press enter to compile/verify your program.
#
#  7. Type "make upload", reset your Arduino board, and press enter to
#     upload your program to the Arduino board.
#
# $Id$

TARGET_NAME = ASCIITable
TARGET_PATH = data/examples/Communication/ASCIITable
BUILD_PATH = /tmp/$(TARGET_NAME)
APPLET_PATH=$(BUILD_PATH)/applet
INSTALL_DIR = /mnt/storage/ardunix
PORT = /dev/ttyUSB0
UPLOAD_RATE = 19200
AVRDUDE_PROGRAMMER = stk500v1
AVR_TOOLS_PATH = /usr/bin
MCU = atmega168
F_CPU = 16000000

############################################################################
# Below here nothing should be changed...
ARDUINO = $(INSTALL_DIR)/hardware/cores/arduino
AVRDUDE_PATH = $(INSTALL_DIR)/hardware/tools
SRC = $(ARDUINO)/pins_arduino.c $(ARDUINO)/wiring.c \
$(ARDUINO)/wiring_analog.c $(ARDUINO)/wiring_digital.c \
$(ARDUINO)/wiring_pulse.c $(ARDUINO)/wiring_shift.c \
$(ARDUINO)/WInterrupts.c
CXXSRC = $(ARDUINO)/HardwareSerial.cpp $(ARDUINO)/WMath.cpp \
$(ARDUINO)/Print.cpp
FORMAT = ihex


# Name of this Makefile (used for "make depend").
MAKEFILE = Makefile

# Debugging format.
# Native formats for AVR-GCC's -g are stabs [default], or dwarf-2.
# AVR (extended) COFF requires stabs, plus an avr-objcopy run.
DEBUG = stabs

OPT = s

# Place -D or -U options here
CDEFS = -DF_CPU=$(F_CPU)
CXXDEFS = -DF_CPU=$(F_CPU)

# Place -I options here
CINCS = -I$(ARDUINO)
CXXINCS = -I$(ARDUINO)

# Compiler flag to set the C Standard level.
# c89   - "ANSI" C
# gnu89 - c89 plus GCC extensions
# c99   - ISO C99 standard (not yet fully implemented)
# gnu99 - c99 plus GCC extensions
CSTANDARD = -std=gnu99
CDEBUG = -g$(DEBUG)
CWARN = -Wall -Wstrict-prototypes
CTUNING = -funsigned-char -funsigned-bitfields -fpack-struct -fshort-enums
#CEXTRA = -Wa,-adhlns=$(<:.c=.lst)

CFLAGS = $(CDEBUG) $(CDEFS) $(CINCS) -O$(OPT) $(CWARN) $(CSTANDARD) $(CEXTRA)
CXXFLAGS = $(CDEFS) $(CINCS) -O$(OPT)
#ASFLAGS = -Wa,-adhlns=$(<:.S=.lst),-gstabs 
LDFLAGS = -lm


# Programming support using avrdude. Settings and variables.
AVRDUDE_PORT = $(PORT)
AVRDUDE_WRITE_FLASH = -U flash:w:$(APPLET_PATH)/$(TARGET_NAME).hex
AVRDUDE_FLAGS = -V -F -C $(INSTALL_DIR)/hardware/tools/avrdude.conf \
-p $(MCU) -P $(AVRDUDE_PORT) -c $(AVRDUDE_PROGRAMMER) \
-b $(UPLOAD_RATE)

# Program settings
CC = $(AVR_TOOLS_PATH)/avr-gcc
CXX = $(AVR_TOOLS_PATH)/avr-g++
OBJCOPY = $(AVR_TOOLS_PATH)/avr-objcopy
OBJDUMP = $(AVR_TOOLS_PATH)/avr-objdump
AR  = $(AVR_TOOLS_PATH)/avr-ar
SIZE = $(AVR_TOOLS_PATH)/avr-size
NM = $(AVR_TOOLS_PATH)/avr-nm
AVRDUDE = $(AVRDUDE_PATH)/avrdude
REMOVE = rm -f
MV = mv -f

# Define all object files.
OBJ = $(SRC:.c=.o) $(CXXSRC:.cpp=.o) $(ASRC:.S=.o)

# Define all listing files.
LST = $(ASRC:.S=.lst) $(CXXSRC:.cpp=.lst) $(SRC:.c=.lst)

# Combine all necessary flags and optional flags.
# Add target processor to flags.
ALL_CFLAGS = -mmcu=$(MCU) -I$(BUILD_PATH) $(CFLAGS)
ALL_CXXFLAGS = -mmcu=$(MCU) -I$(BUILD_PATH) $(CXXFLAGS)
ALL_ASFLAGS = -mmcu=$(MCU) -I$(BUILD_PATH) -x assembler-with-cpp $(ASFLAGS)


# Default target.
all: applet_files build sizeafter

build: elf hex 

applet_files: $(TARGET_PATH)/$(TARGET_NAME).pde
	# Here is the "preprocessing".
	# It creates a .cpp file based with the same name as the .pde file.
	# On top of the new .cpp file comes the WProgram.h header.
	# At the end there is a generic main() function attached.
	# Then the .cpp file will be compiled. Errors during compile will
	# refer to this new, automatically generated, file. 
	# Not the original .pde file you actually edit...
	test -d $(APPLET_PATH) || mkdir -p $(APPLET_PATH)
	echo '#include "WProgram.h"' > $(APPLET_PATH)/$(TARGET_NAME).cpp
	# oh, i'm a h4x
	echo 'extern "C" void __cxa_pure_virtual() {}  ' >> $(APPLET_PATH)/$(TARGET_NAME).cpp
	cat $(TARGET_PATH)/$(TARGET_NAME).pde >> $(APPLET_PATH)/$(TARGET_NAME).cpp
	cat $(ARDUINO)/main.cxx >> $(APPLET_PATH)/$(TARGET_NAME).cpp

elf: $(APPLET_PATH)/$(TARGET_NAME).elf
hex: $(APPLET_PATH)/$(TARGET_NAME).hex
eep: $(APPLET_PATH)/$(TARGET_NAME).eep
lss: $(APPLET_PATH)/$(TARGET_NAME).lss 
sym: $(APPLET_PATH)/$(TARGET_NAME).sym

# Program the device.  
upload: $(APPLET_PATH)/$(TARGET_NAME).hex
	/mnt/storage/ardunix/lib/pulsedtr.py $(PORT)
	$(AVRDUDE) $(AVRDUDE_FLAGS) $(AVRDUDE_WRITE_FLASH)


	# Display size of file.
HEXSIZE = $(SIZE) --target=$(FORMAT) $(APPLET_PATH)/$(TARGET_NAME).hex
ELFSIZE = $(SIZE)  $(APPLET_PATH)/$(TARGET_NAME).elf
sizebefore:
	@if [ -f $(APPLET_PATH)/$(TARGET_NAME).elf ]; then echo; echo $(MSG_SIZE_BEFORE); $(HEXSIZE); echo; fi

sizeafter:
	@if [ -f $(APPLET_PATH)/$(TARGET_NAME).elf ]; then echo; echo $(MSG_SIZE_AFTER); $(HEXSIZE); echo; fi


# Convert ELF to COFF for use in debugging / simulating in AVR Studio or VMLAB.
COFFCONVERT=$(OBJCOPY) --debugging \
--change-section-address .data-0x800000 \
--change-section-address .bss-0x800000 \
--change-section-address .noinit-0x800000 \
--change-section-address .eeprom-0x810000 


coff: $(APPLET_PATH)/$(TARGET_NAME).elf
	$(COFFCONVERT) -O coff-avr $(APPLET_PATH)/$(TARGET_NAME).elf $(TARGET_NAME).cof


extcoff: $(TARGET_NAME).elf
	$(COFFCONVERT) -O coff-ext-avr $(APPLET_PATH)/$(TARGET_NAME).elf $(TARGET_NAME).cof


.SUFFIXES: .elf .hex .eep .lss .sym

.elf.hex:
	$(OBJCOPY) -O $(FORMAT) -R .eeprom $< $@

.elf.eep:
	-$(OBJCOPY) -j .eeprom --set-section-flags=.eeprom="alloc,load" \
	--change-section-lma .eeprom=0 -O $(FORMAT) $< $@

# Create extended listing file from ELF output file.
.elf.lss:
	$(OBJDUMP) -h -S $< > $@

# Create a symbol table from ELF output file.
.elf.sym:
	$(NM) -n $< > $@

# Link: create ELF output file from library.
$(APPLET_PATH)/$(TARGET_NAME).elf: $(TARGET_PATH)/$(TARGET_NAME).pde $(APPLET_PATH)/core.a 
	$(CC) $(ALL_CFLAGS) -o $@ $(APPLET_PATH)/$(TARGET_NAME).cpp -L. $(APPLET_PATH)/core.a $(LDFLAGS)

$(APPLET_PATH)/core.a: $(OBJ)
	@for i in $(OBJ); do echo $(AR) rcs $(APPLET_PATH)/core.a $$i; $(AR) rcs $(APPLET_PATH)/core.a $$i; done



# Compile: create object files from C++ source files.
.cpp.o:
	$(CXX) -c $(ALL_CXXFLAGS) $< -o $@ 

# Compile: create object files from C source files.
.c.o:
	$(CC) -c $(ALL_CFLAGS) $< -o $@ 


# Compile: create assembler files from C source files.
.c.s:
	$(CC) -S $(ALL_CFLAGS) $< -o $@


# Assemble: create object files from assembler source files.
.S.o:
	$(CC) -c $(ALL_ASFLAGS) $< -o $@


# Automatic dependencies
%.d: %.c
	$(CC) -M $(ALL_CFLAGS) $< | sed "s;$(notdir $*).o:;$*.o $*.d:;" > $@

%.d: %.cpp
	$(CXX) -M $(ALL_CXXFLAGS) $< | sed "s;$(notdir $*).o:;$*.o $*.d:;" > $@


# Target: clean project.
clean:
	$(REMOVE) $(APPLET_PATH)/$(TARGET_NAME).hex $(APPLET_PATH)/$(TARGET_NAME).eep $(APPLET_PATH)/$(TARGET_NAME).cof $(APPLET_PATH)/$(TARGET_NAME).elf \
	$(APPLET_PATH)/$(TARGET_NAME).map $(APPLET_PATH)/$(TARGET_NAME).sym $(APPLET_PATH)/$(TARGET_NAME).lss $(APPLET_PATH)/core.a \
	$(OBJ) $(LST) $(SRC:.c=.s) $(SRC:.c=.d) $(CXXSRC:.cpp=.s) $(CXXSRC:.cpp=.d)

.PHONY:	all build elf hex eep lss sym program coff extcoff clean $(APPLET_PATH)_files sizebefore sizeafter

-include $(SRC:.c=.d)
-include $(CXXSRC:.cpp=.d)
