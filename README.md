Receipt Reader

Upload pictures of receipts into the Receipts folder and run the main program. The main will iterate through the folder and it will send out a JSON file. The processor will read the
JSON files and will return pieces of data from the recipt like the total, store name, address, items, number of recipts and more in a CSV and an Excel file.

This program uses an OCR API(key will need to be changed) that takes in pictures and returns data. It also uses Pandas to take the simplified data and put it into CSV and Excel files to
be saved and viewed later.

I plan on further updating to automaticlly seperate receipt data by date.
