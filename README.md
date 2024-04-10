# YOUR BASIC WEBSCRAPER

### General information

This webscrapes has 2 components

1. Tracking Returndeals from bol.com & coolblue
2. Tracking product prices on different sites (currently 3 websites supported)
   * bol.com
   * coolblue.be
   * amazon.com.be

These components are configured to output the data to a MySQL database.

## TODO
### In no particular order

* Adding more supported sites
  * [ ] Krefel
    * Previous tests shows there is a need for dynamic loading
    * Tests show a timeout in request, potentialy blocking requests, extra safeguards needed
  * [ ] MediaMarkt (WIP)
    * 403 Error: Needed extra safeguards to circumvent the block
* Adding csv support
* Cleaning code and directories
