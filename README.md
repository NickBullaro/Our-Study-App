# Contributors

- Jason Molisani
- Mitchell Mecca
- Nick Bullaro
- Navado Wray

# Getting Up and Running (do this once)
1. Clone this repository and navigate to the root folder within the terminal
2. Make sure you can execute the setup shell scripts with the following two lines
   - `chmod 764 PSQLsetup.sh`
   - `chmod 764 reactSetup.sh`
3. Run the setup shell scripts:
   - `./PSQLsetup.sh`
   - `./reactSetup.sh`

# Getting Back Up and Running Locally (Do this every time other than the first)
1. In one terminal, navigate to the repository's root folder and execute `npm run watch`
2. Leaving that running, open a second terminal, navigate to the root folder (again) and start the app with `python app.py`