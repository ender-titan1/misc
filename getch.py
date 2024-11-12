import sys
import tty
import termios

def getch():
    """
    Reads a keypress from the terminal, including special keys like arrow keys.
    Returns:
        str: A single character string for regular keys or a string representing an arrow key.
    """
    # Set the terminal to raw mode
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
        
        # Check if this is an escape sequence (for arrow keys or other special keys)
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
                return "UNKNOWN_ESCAPE_SEQUENCE"  # Handle other escape sequences if necessary

        return ch  # Return regular key press if not an escape sequence
    finally:
        # Restore the terminal to its original settings
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)