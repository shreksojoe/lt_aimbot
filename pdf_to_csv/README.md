
Input pdf, convert to csv, determine stock or dropship, convert to json


If Grainger in title, than csv 1: Grainger -- done

Under "Original" is the Customer PO -- done

Under Customer PO is the date -- done
    If on a wednsday, continue: -- done
    Else move it to next wednsday -- done

If csv row contains: "Page" and "of", than skip it -- done

Stock or dropship right after the first "Email" -- done

Find the row with "Line# -- done
under that row, the second cell is the product number, 


PO:
pdf -> large csv -> condensed csv -> json instructions -> multiple tickets


QTY will be the 4th

Stock if it's in here:
    10Y376
    8X606
    10Y373
    8EE38
    8E085
    10Y374
    8EEP0
    10Y370
    8E984
    9WA32
    10Y372
    8EE37
    10Y371
    8NCA9
    8AY66
    9WC95
    10Y495
Else Custom

Stock and Custom mixed in with the order.

1. Drop Ship or not (Check Ship To address. If Grainger Warehouse or DC (Distibution Center), than no, else yes
2. Each individual product is either Stock or Custom (Description and "Buyers Part#" and compare that with sheets)

For Repeat orders:
    1. Click Tickets under Order Processing
    2. Click "New Ticket"
    3. Enter Customer Number
    4. Enter PO # in Customer PO box
    5. Enter ship date into the box (2 weeks form the date the PO came in ask about this)
    6. Enter Quantity in the qty box
    7. Enter Item number
    8. Copy and Paste the description into the general description box
    9. Check all five boxes at the bottom of the page
    10. Set stock status to "Hld"
    11. Click on the Address tab
    12. Click on "Location and choose the right address
    13. Check that the order was entered correctly
    14. Change stock status back to ***

If Custom Product: 
    1. Enter as repeat
    2. Ship date in the description column, Move Date to next wednesday (exception: dropship)
       (If ship dates differ go to earliest)
       after "Ship Date: "
    3. When Entering the product# ok on popup's
       after line number (ex: 00001) under "Buyer's Part #"
    Verify that the price matches between the LT product and the PO (In case of discrepencies and it is a Stock product go with PO, if not a stock, than through an error) 
    4. print "L#x - " and the first number under Line# with no 0s 
    5. Copy description, and paste General Description textbox
    6. Go to Products Tab at the top
    7. Enter that Line # with all the zeros (in the "Note" section)
    To do this, click once on the line, move over and click the line again, otherwise you will be taken to another page.  In that case just cancel out
    9. Go to "Common" tab at the top and follow
    10. Click "Auto Allocate" button (beneeth Stock Allocation Status field)
        ~ if there is material available the allocated and remaining columns will change
        ~ if the remaining column shows 0:
            1. go to the general tab 
            2. change the Stock Status to In
            3. check mark the box as Done
        ~ else:
            1. Add the ticket matierial to the Waiting on Material list
            2. go to the general tab
            3. change the Stock Status to 'Ord', and leave the box unchecked
            4. Save the ticket
    11. Check the ticket Quantity
        ~ if qty is less than 30 units
            1. click the common tab
            2. click the "stock notes"
            3. In the popup, click on "Marked in (IN) Pull from shelves"
            4. Paste 
            5. Return to the general tab
            6. change Stock Status to In 
            7. checkmark box as Done
        ~ else:
            continue
        
    12. Go to "Address" Tab
    13. Click "Location"
    14. Click the "Ship To" City (2 Jacksonfille FL addr in LT)
    15. Copy Paste the # into the PO No. Box (ex: 4647641964)
    This pulls up all the Tickets associated with the PO
    16. Go into the first ticket:
    17. Click Doc Tab
    18. Click Import on the pop up
    19. Search the file path of the PO (ctrl+F and ctrl+P to find the PO#) & click on it
    20. Hit OK
    21. Click on to the next Ticket (Next to the home button)
    22. Back to step 1

If Stock Product:
    1. Select "New Stock Ticket" and enter the same way as a custom except....
    2. Multiple stock products can be put on one ticket as long as they are on the same PO and ship dates are the same:
    3. Click the Plus button
    4. Enter the ammount of unique products on the ticket in the "Request for Information" (Hit ok)
    5. Ignore the pop up regaurding Products not being able to go on the same ticket
    6. If there is a pop-up that says there's not enough inventory, through an error to slack the person in charge of allocating (include the product# ticket# and what the problem is). After that is exited out of continue entering in the ticket
    7. Add the Line# in the General Desciption (no zeros) (Found under "Line#" at the bottom left of the PO) For multiple linesdo a L#1,2 etc
    8. Remove anything that is unique to a specific ticket from the general description
    9. Check no boxes at the bottom of the ticket
    10. Go to "Address, Terms" page
    11. Fill in address and shipping info
    12. Check if the ticket's where entered correctly
    13. Pricing in LT should match pricing in the PO (through error for inconsistancies, change to mirror PO)
    14. Add PO's in the Doc tab (same as custom)

If a Dropship:
    1. Enter tickets the same way you would for custom and stock
    2. Differences are:
        ~ The ship date on the ticket should match the ship date on the PO (no round to wednesday)
        ~ The Address has to be put in manually:
            1. Under the "Ship To:" section of the PO
            2. Go to Address tab in LT
            3. Press on "Location"
            5. Press the "State" column header
            6. Double click the "Grainger Dropship Acct" (which will open it up)
            7. Fill in the address as listed on the PO
            8. (Leave the bottom 3 lines as they are: "Attention, Email", "Instructions, Via"k "Ship via", and "Freight Acct. No."
            9. Grainger dropships are always shipped Fed Ex Ground, 3RD PARTY with the Account in LT
        


    

