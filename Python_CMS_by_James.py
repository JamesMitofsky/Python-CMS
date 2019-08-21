#James Tedesco
#CS21D
#Description: This program is a CMS which reads updated content from a Google Spreadsheet. It does this through a string replace method,
 #allowing values to persist over runs through serializing a list object.


#Import necessary APIs
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pickle
#Run dependancy: "pip install gspread oauth2client"


#Declare main function
def main():
    #Declare scope of sheets operation
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    #Grab credentials from JSON file (not included to protect my key, but you can call Google's API pretty easily to create your own.
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    client = gspread.authorize(creds)


    #Enter website file interested in searching for text in
    file_to_open = 'index.html'
    #Read file to convert to a searchable string
    infile = open(file_to_open, 'r')
    infile_string = infile.read().replace("\n", " ")
    infile.close()

    #Print to confirm initial starting string
    print(infile_string)


    #Open serialized file for comparing current against requested content
    input_published_text = open('published_text.txt', 'rb')
    #Withdraw stored published text value and save to variable
    published_text = pickle.load(input_published_text)
    #Close serialized file
    input_published_text.close()


    #This needs to be uncommented for a one time startup. Content must be written in to give a string targeting baseline
    # content1 = "This website was created to document and organize smaller, usually assignment related projects."
    # content2 = "Here's my website which meets the mid-term requirements for the fall follies website. In particular, I worked on creating folding, card based elements."
    # content3 = "Albiet somewhat outside of the exam requirements, I built this dyanmically responsive website for my fall follies project."
    # published_text = [content1, content2, content3]


    #Open the relevant spreadsheet, using multiple steps for clarity's sake
    spreadsheet = client.open('Update Hub: LDU Website')
    sheet = spreadsheet.sheet1


    #For the length of however much data is stored in the unserialized list, iterate through all values
    for i in range(len(published_text)):
        #Set a y starting position for the Google Sheet so that it ignores the header. It needs to be plus two because Sheets doesn't recognize a zero position.
        y_position = i + 2
        #Filter out reading empty cells to prevent an empty list value from being created.
        if sheet.cell(y_position, 2).value != "":
            #If the published content field doesn't match the requested content
            if published_text[i] != sheet.cell(y_position, 2).value:
                #Print published and unpublished versions of content
                print("New content:\n\tlist:",published_text[i], "\n\tsheet:", sheet.cell(y_position, 2).value, "\n")
                #Overwrite old content (published) with the new content given from cell with matching index
                infile_string = infile_string.replace(published_text[i], sheet.cell(y_position, 2).value)
                #Update the published text list to reflect the new content to check against next time
                published_text[i] = sheet.cell(y_position, 2).value
            #If cell matches list value, indicate no action taken on account of such
            else:
                print("Existing content matches Google Sheet.\n")
        #If cell is empty, indicate no action will be taken and former value will remain
        else:
            print("Empty cell, the previously entered content remains: '" + published_text[i] + "'\n")


    #Print to confirm final string
    print("Final list output", published_text)


    #Overwrite the file which was originally being read, exporting the altered string to the file.
    outfile = open(file_to_open, 'w')
    outfile.write(infile_string)
    outfile.close()


    #Compile the published_text list through serializing to allow for checking next time
    output_published_text = open('published_text.txt', 'wb')
    pickle.dump(published_text, output_published_text)
    output_published_text.close()


#Call main function
main()