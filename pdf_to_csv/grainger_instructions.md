# Dropship Grainger Tickets

Setup: User has download the PO, and has input into LT Aimbot


(Abstract the address, and store it in the csv)

(Customer Number, Just type: W.W. Grainger and it will show up)
PO #
qty
ship date (rounded to the next wednsday)
product #s
price
dropship ? full address or not
stock or custom


## Determine if it is a Grainger Dropship:
1. If 'Grainger' is in the title (It is a grainger, continue)
2. If the 'Ship To:' Address isn't to Grainger or DC (Direct Commerce), than it is a Dropship (Continue)

## How to convert Grainger Dropship PO to a ticket:
1. Check the Product # of an item 
2. If the Product # is in this list: 
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

    ... It is a Stock Product. Else they are custom. 
3. Add a marker in the csv which product is Stock and which is Custom
    For each product do the appropriate process: 

### Custom Products:
1. Click Tickets under Order Processing
2. Click "New Ticket"
3. Type W.W. Grainger into Name section of the Customer No.
4. Enter PO# in Customer PO box
5. Enter in the Ship Date (in the description box on the PO, should be rounded to the next wednesday (Or current wednesday if it is wednesday)) 
6. Enter Qty in Qty box
7. Enter Product#
8. Click "OK" on pop-ups
9. Verify that the Price in Label Traxx matches that in the PO (err on the side of PO if stock. Else throw an error)
10. Copy Description
11. In General Description enter the Line numbers associated for each product included in the ticket (Custom's will only ever have one product on the ticket, ex: "L#3 - ")
12. Paste the Description into General Description after the Line number
13. Check the 5 boxes at the bottom of the page
14. Go to the Products Tab
15. In the note section Enter the Line # with all of the 0s 
16. Check the Qty. If it is less than 30 units (For basic alocation):
    1. Go to the "Common" tab at the top
    2. Click on "Stock Notes"
    3. In the popup, click on "Marked in (IN) Pull from shelves"
    4. Click on Paste
    5. Return to General tab
    6. Change Stock Status to "In" and check mark the box as Done
17. else give em ***
18. Click to the "Address" tab
19. Press on "Location"
20. Go through normal process of searching for address (specifically the city, there are 2 Jacksonville, FL addresses)
23. Click the Doc Button
24. Click on import in the pop-up
25. Navigate to the PO pdf (Either by searching, or pasting a file path)
26. Select it and hit "Open"
27. Hit "OK" on the pop-up
28. Continue Filling out all tickets for the PO

### Stock Products:
1. Click Tickets under Stock Products
2. Click "New Stock Ticket"
3. Enter Customer Number
4. Enter PO# in Customer PO box
5. Enter in the Ship Date (in the description box on the PO, should be rounded to the next wednesday (Or current wednesday if it is wednesday)) 
6. Enter Qty int Qty box
7. Enter Product#
8. Click "OK" on pop-ups
9. Type in the price for the product (the saved one in Label Traxx is wrong)
10. If there are multiple stock products with the same Ship Date, they can be put on the same ticket:
    a) Click the "+" Button
    b) Enter in the total ammount of products on the ticket 
    c) Hit "OK"
    d) Ignore the pop-up regaurding multiple products not being able to go on the same ticket
    e) If there is a pop-up that says there's not enough inventory, through an error:
        "Not enough inventory. Program paused (Click "Continue" , and "OK" on the pop-up to Resume). Contact person in charge of allocating. Product #: xxxxxxxx. Ticket #. " It says include any other information, if there is anything notable 
    f) Continue steps 6-9 for each product

11. Copy Description
12. Enter the Line numbers that are included in the ticket (from the PO, ex: "L#3 - " or "L#1,2,3 - ") in the General Description
13. Paste the Description into General Description after the Line number
14. Remove anything that isn't the same for all products from the "General Description"
15. Go to "Address, Terms" page
19. Press on "Location"
20. Go through normal process of searching for address (specifically the city, there are 2 Jacksonville, FL addresses)
24. Click the Doc Button
25. Click on import in the pop-up
26. Navigate to the PO pdf (Either by searching, or pasting a file path)
27. Select it and hit "Open"
28. Hit "OK" on the pop-up
29. Continue Filling out all tickets for the PO

