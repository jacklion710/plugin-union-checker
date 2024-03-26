# main.py
from graphics import Window

# Ideas for later
# User can specify a custom directory for their plugin locatio
# Display any common sense reminders such as that windows doesn't support audio units (AU) formats
# Checkboxes for determining which folders to visit
# Detect what DAWs are present

def main():
    window = Window()
    window.mainloop()

if __name__ == "__main__":
    main()