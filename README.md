# PropertyMetrics

## Zillow Scraping
The first problem I set out to solve was programatically scraping info from zillow listings.
For this I started by using requests and beautiful soup to scrape certain metrics for each url that I am interested in.
I initially ran into a 403 error, but once I formatted the request to mimic a browser, I was able to get the listing homepage.
That got me some basic listing info, however by just pulling the static html from the homepage I did not have access to the all remaining info under the "Show more" sections on the listing.
Those buttons loads additional content dynamically using JavaScript, so I needed a tool that could control a web browser and interact with the page as a user would.
For this I went with Selenium as allows you to simulate clicks, scrolls, and other interactions needed to scrape to the remaining listing info.
