import sys
import tty
import termios

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
        
        if ch == '\x1b':  # Escape character
            ch += sys.stdin.read(2)  # Read the next two characters
            if ch == '\x1b[A':
                return "UP_ARROW"
            elif ch == '\x1b[B':
                return "DOWN_ARROW"
            elif ch == '\x1b[C':
                return "RIGHT_ARROW"
            elif ch == '\x1b[D':
                return "LEFT_ARROW"
            else:
                return "UNKNOWN_ESCAPE_SEQUENCE"  # Handle other escape sequences 

        return ch  # Return regular key press if not an escape sequence
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)