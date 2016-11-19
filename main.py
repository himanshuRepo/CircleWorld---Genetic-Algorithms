"""
    Author

References
    http://as.ynchrono.us/2007/12/filesystem-structure-of-python-project_21.html
    http://pygametutorials.wikidot.com/tutorials-basic
    https://www.cs.ucsb.edu/~pconrad/cs5nm/topics/pygame/drawing/
"""

# __author__ == "Michael Iuzzolino"
# __email__ == "Michael.Iuzzolino@colorado.edu"

from resources.circleWorld import App


def main():
    circleWorld = App()
    circleWorld.launch()

if __name__ == "__main__":
    main()
