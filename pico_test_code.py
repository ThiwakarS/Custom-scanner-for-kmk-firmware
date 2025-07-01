import time
import board
import digitalio
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC

class KeypadEvent:
    """KeyEvent-compatible object that KMK expects"""
    def __init__(self, key_number, pressed=True):
        self.key_number = key_number
        self.pressed = pressed
        self.released = not pressed
        self.timestamp = time.monotonic_ns()

class MultiplexerScanner:
    def __init__(self, select_pins, signal_pin, mux_en_pin):
        self.select_lines = []
        for pin in select_pins:
            sel = digitalio.DigitalInOut(pin)
            sel.direction = digitalio.Direction.OUTPUT
            sel.value = False
            self.select_lines.append(sel)
        
        self.signal = digitalio.DigitalInOut(signal_pin)
        self.signal.direction = digitalio.Direction.INPUT 
        # self.signal.pull = digitalio.Pull.UP  # Assuming active low
        # im having an external pullup resistor. if you dont have one uncomment this.
        
        self.mux1_pin = digitalio.DigitalInOut(mux_en_pin)
        self.mux1_pin.direction = digitalio.Direction.OUTPUT
        self.mux1_pin.value = False
        # Enable the mux by pulling it to ground.        
        
        
        self._key_count = 16
        self.coord_mapping = list(range(self._key_count))  # Simple 0-15 mapping
        self.offset = 0  # Will be set by KMK if needed
        
        # Track previous state for change detection
        self._prev_state = [True] * self._key_count  # True = not pressed (active low)
    
    def set_channel(self, channel):
        """
        Set select lines for a specific channel (0-15).
        """
        for i in range(4):  # for 4-bit address
            self.select_lines[i].value = (channel >> i) & 1
    
    def scan_for_changes(self):
        """
        Called by KMK's main loop to get key state changes.
        Returns a KeypadEvent object if there's a change, None otherwise.
        """
        current_state = [True] * self._key_count
        
        # Scan all channels
        for ch in range(self._key_count):
            self.set_channel(ch)
            time.sleep(0.01)  # Small delay for signal to stabilize
            current_state[ch] = self.signal.value
        
        # Check for changes and return the first one found
        for ch in range(self._key_count):
            if current_state[ch] != self._prev_state[ch]:
                # State changed
                is_pressed = not current_state[ch]  # Active low
                self._prev_state[ch] = current_state[ch]
                return KeypadEvent(ch, is_pressed)
        
        return None  # No changes
    
    def key_count(self):
        """
        Total number of keys.
        """
        return self._key_count
    
    def deinit(self):
        """
        Optional cleanup
        """
        for sel in self.select_lines:
            sel.deinit()
        self.signal.deinit()

# Keyboard setup
keyboard = KMKKeyboard()
mux_scanner = MultiplexerScanner(
    select_pins=[board.GP10, board.GP11, board.GP12, board.GP13],  # S0-S3
    signal_pin=board.GP28  # MUX common output
    mux_en_pin=board.GP14
)

keyboard.matrix = mux_scanner

keyboard.keymap = [
    [KC.A, KC.B, KC.C, KC.D,
     KC.E, KC.F, KC.G, KC.H,
     KC.I, KC.J, KC.K, KC.L,
     KC.M, KC.N, KC.O, KC.P]
]

if __name__ == '__main__':
    keyboard.go()