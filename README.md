"""
Wikipedia Edit Tracker (Ethan King & Keer Wang)
A command-line tool to retrieve recent edit history for Wikipedia articles. When the user runs the script and gives
the name of a wikipedia page it will then connect to Wikipedias API to grab the last 30 changes made to the page.
Every change shows the time of the edit and the username of the editor from newest to oldest. If the page name
redirects the user then the code will tell the user the name of the redirected page. The code also handles many errors
such as no page name being provided (Using exit code 1), if the page doesn't exist (Using exit code 2), and if a network error occurs (Using exit code 3). The script is designed
to help users, like journalists, keep track of changes made to selected wikipedia pages easily.
"""
