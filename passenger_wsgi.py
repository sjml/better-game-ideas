import sys, os

# Switch to the virtualenv if we're not already there
INTERP = os.path.abspath("env/bin/python")
if sys.executable != INTERP: os.execl(INTERP, INTERP, *sys.argv)

from better_game_ideas_web import app as application

if __name__ == '__main__':
    application.run(debug=False)
