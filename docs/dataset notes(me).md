#Letterboxd data is saved super weird 
#profile.csv - username, given name, FAVORITES***
#diary.csv usefeul contents - 
    Per movie - name, release year, rating
    ratings.csv is all duplicate info
    watched.csv has more data BC not all ratings are logged movies 
    likes/films seems helpful, 
comments is worthless (i think), reviews and watchlist also seem unhelpful for now

based on data available per user(not much), the main stuff that can be used seems to be 
raw score(maybe something else like percentile w this?) and likes(4 favorites also exists but thats a small sample)
and using those to apply a weighted score for various criteria (i.e. 80s movies tend to score higher, Wes Anderson tends to score higher), creating a list of priorities
using an external database such as TMBD that will filter for those priorities
