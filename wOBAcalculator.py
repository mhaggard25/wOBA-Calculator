from bs4 import BeautifulSoup
import requests
from decimal import Decimal

# Greeting
print("\n\n*** wOBA Calculator ***")

print("This program calculates a player's wOBA for any given year. You must provide the link to the baseball reference page.")
print(" (Protip: just search '[player name] [year] batting' and follow the link to the baseball-reference site) \n\n")

year = input("First, what year would you like to look at?: ")

# Get the url of the player from a specific year from the user
url = input("Please provide the appropriate url: ")
print("\n")
headers = {'User-Agent': 'Mozilla/5.0'}
response = requests.get(url, headers = headers)

# GET THE PLAYER'S NAME FROM THE PAGE

# Find all of the tables in the page
soup = BeautifulSoup(response.content, 'html.parser')
stat_table = soup.find_all('table')

# Get the player's name and convert it into regular text
name = soup.find('h1', itemprop = 'name').text

# Pick the correct table
stat_table = stat_table[4]

# Create this to hold the stats.
stats_list = []

# Add the stats to the stats list that I created
for row in stat_table.find_all('tfoot'):
    for cell in row.find_all('td'):
        stats_list.append(cell.text)

# I need to remove the empty strings
while("" in stats_list) : 
    stats_list.remove("")

# Connect to fangraphs page and get the yearly constants information
url = 'https://www.fangraphs.com/guts.aspx?type=cn'
headers = {'User-Agent': 'Mozilla/5.0'}
response = requests.get(url, headers = headers)

# find the correct table and extract it with indexing.
soup = BeautifulSoup(response.content, 'html.parser')
year_table = soup.find_all('table', class_ = "rgMasterTable")
year_table = year_table[0]

# Make the year list to hold the yearly multipliers for a bit 
year_list = []

# get information from each cell. (Should make this pick year here.)
for row in year_table.find_all('tr'):
    if row.find(text = year):
        for cell in row.find_all('td'):
            year_list.append(cell.text)

# Make the variables to hold the constants and stat positions in the array
UBB_CONSTANT = float(year_list[3])
HBP_CONSTANT =  float(year_list[4])
SINGLES_CONSTANT = float(year_list[5])
DOUBLES_CONSTANT = float(year_list[6])
TRIPLES_CONSTANT = float(year_list[7])
HR_CONSTANT = float(year_list[8])

ab = int(stats_list[2])
bb = int(stats_list[9])
ibb = int(stats_list[10])
sf = int(stats_list[14])
ubb = bb - ibb
hbp = int(stats_list[12])
doubles = int(stats_list[5])
triples = int(stats_list[6])
hr = int(stats_list[7])
singles = int(stats_list[4])-(doubles + triples + hr)

wOBA = float(((UBB_CONSTANT * ubb) + (HBP_CONSTANT * hbp) + (SINGLES_CONSTANT * singles) + (DOUBLES_CONSTANT * doubles) + (TRIPLES_CONSTANT * triples) + (HR_CONSTANT * hr))/(ab + bb - ibb + sf + hbp))

# Round it to 3 decimal places
wOBA = Decimal(wOBA)
output = round(wOBA, 3)

print(name + "'s wOBA in " + year + " is: ", output)

input("Press 'Enter' to exit")