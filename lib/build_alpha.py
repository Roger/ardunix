import config
import os.path

src_files = ('pins_arduino.c', 'wiring.c', 'wiring_analog.c',
      'wiring_digital.c', 'wiring_pulse.c', 'wiring_shift.c', 'WInterrupts.c')
src = [os.path.join(config.path.arduino, fname) for fname in src_files]
cxxsrc = [os.path.join(config.path.arduino, fname) for fname in 
                      ('HardwareSerial.cpp', 'WMath.cpp', 'Print.cpp')]
format = 'ihex'

# Debugging format.
# Native formats for AVR-GCC's -g are stabs [default], or dwarf-2.
# AVR (extended) COFF requires stabs, plus an avr-objcopy run.
debug = 'stabs'
opt = 's'

# Place -D or -U options here
cdefs = '-DF_CPU='+config.main.f_cpu
cxxdefs = '-DF_CPU='+config.main.f_cpu

# Place -I options here
cincs = '-I'+config.path.arduino
cxxincs = '-I'+config.path.arduino

# Compiler flag to set the C Standard level.
# c89   - "ANSI" C
# gnu89 - c89 plus GCC extensions
# c99   - ISO C99 standard (not yet fully implemented)
# gnu99 - c99 plus GCC extensions
cstandard = '-std=gnu99'
cdebug = '-g'+debug
cwarn = '-Wall -Wstrict-prototypes'
ctuning = '-funsigned-char -funsigned-bitfields -fpack-struct -fshort-enums'
#CEXTRA = -Wa,-adhlns=$(<:.c=.lst)

cflags = cdebug + cdefs + cincs + '-o' + opt + cwarn + cstandard # + cextra
cxxflags = cdefs + cincs '-o' + opt
#ASFLAGS = -Wa,-adhlns=$(<:.S=.lst),-gstabs 
ldflags = '-lm'

# Programming support using avrdude. Settings and variables.
avrdude_write_flash = '-U flash:w:applet/%s.hex'
avrdude_flags = '-V -F -C ' + os.path.join(
                config.path.avrdude_path, 'avrdude.conf')+\
                '-p ' + mcu + '-P' + config.main.port + '-c' +\
                config.main.avrdude_programmer + '-b '+ config.main.upload_rate

# Program settings
cc = os.path.join(config.path.avr_tools_path, 'avr-gcc')
cxx = os.path.join(config.path.avr_tools_path, 'avr-g++')
objcopy = os.path.join(config.path.avr_tools_path, 'avr-objcopy')
objdump = os.path.join(config.path.avr_tools_path, 'avr-objdump')
ar  = os.path.join(config.path.avr_tools_path, 'avr-ar')
size = os.path.join(config.path.avr_tools_path, 'avr-size')
nm = os.path.join(config.path.avr_tools_path, 'avr-nm')
avrdude = config.path.avr_tools_path, 'avrdude')

# Define all object files.
OBJ = $(SRC:.c=.o) $(CXXSRC:.cpp=.o) $(ASRC:.S=.o)

# Define all listing files.
LST = $(ASRC:.S=.lst) $(CXXSRC:.cpp=.lst) $(SRC:.c=.lst)

# Combine all necessary flags and optional flags.
# Add target processor to flags.
ALL_CFLAGS = -mmcu=$(MCU) -I. $(CFLAGS)
ALL_CXXFLAGS = -mmcu=$(MCU) -I. $(CXXFLAGS)
ALL_ASFLAGS = -mmcu=$(MCU) -I. -x assembler-with-cpp $(ASFLAGS)

for i in globals().copy(): print i
