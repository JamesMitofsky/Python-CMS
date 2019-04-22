import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pickle


#Package install: pip install gspread oauth2client

def main():
    #Loading requirements
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    client = gspread.authorize(creds)
    # Opens first sheet // trying to figure out how to iterate over all sheets, opening them one by one
    # data = sheet.get_all_records()


    #Enter file interested in searching for text in
    file_to_open = 'index.html'
    #Read file to convert it to a searchable string
    infile = open(file_to_open, 'r')
    infile_string = infile.read().replace("\n", " ")
    infile.close()
    print(infile_string)

    # files = ['index.html']
    # #For file in files, open file
    # for file in files:
    #     infile = open(file, 'r')
    #     infile_string = infile.read().replace("\n", " ")
    #     infile.close()

    

    #Open serialized file for comparing current against requested content
    input_published_text = open('published_text.txt', 'rb')
    #Withdraw stored published text value and save to variable
    published_text = pickle.load(input_published_text)
    #Close serialized file
    input_published_text.close()


    #Create list of sheets to enable 'for loop' later on
    # home = client.open('Update Hub: LDU Website').sheet1
    # about = client.open('Update Hub: LDU Website').sheet2
    # contact = client.open('Update Hub: LDU Website').sheet3
    # sheets = [home]
    spreadsheet = client.open('Update Hub: LDU Website')
    sheet = spreadsheet.sheet1

    #One time startup: content must be written in to give targeting baseline
    # content1 = "This website was created to document and organize smaller, usually assignment related projects."
    # content2 = "Here's my website which meets the mid-term requirements for the fall follies website. In particular, I worked on creating folding, card based elements."
    # content3 = "Albiet somewhat outside of the exam requirements, I built this dyanmically responsive website for my fall follies project."
    # published_text = [content1, content2, content3]


    #Iterate through all sheets available

    #For the length of however much data is stored in the document, iterate through
    for i in range(len(published_text)):
        #Set a y starting position for the google sheet so that it ignores the header
        y_position = i + 2
        #If the published content field doesn't match the requested content, execute following
        if published_text[i] != sheet.cell(y_position, 2).value:
            #Print published and unpublished versions of content
            print("New content:\n\tlist:",published_text[i], "\n\tsheet:", sheet.cell(y_position, 2).value, "\n")
            #Overwrite old content (published) with the new content given from cell with matching index
            infile_string = infile_string.replace(published_text[i], sheet.cell(y_position, 2).value)
            #Update the published text list to reflect the new content to check against next time
            published_text[i] = sheet.cell(y_position, 2).value
        else:
            print("Existing content matches Google Sheet.\n")


    #Print final list readout
    print("Final list output", published_text)

    #Overwrite the file which was originally being read, exporting the altered string to the file.
    outfile = open(file_to_open, 'w')
    outfile.write(infile_string)
    outfile.close()

    #Compile the published_text list through serializing to allow for checking next time
    output_published_text = open('published_text.txt', 'wb')
    pickle.dump(published_text, output_published_text)
    output_published_text.close()





main()