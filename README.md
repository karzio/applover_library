# applover_library
Recruitment task

## Small overview

The solution should work with just 

```shell
docker-compose build
docker-compose up
```

If it does, the docs are under: 

```djangourlpath
localhost:80/docs
```

I've added simple user and user's card endpoints, just to create them.
There is only validation on card_id, as it was supposed to be 6 digits.


Having card_id, the book can be added. Then there can be added a book_loan
object, which is responsible for our book loans' history. 

On books list we can see if the book is loaned or not. I've decided on
following logic: 
book_loan has an end_date and when adding new book_loan object it's set
to null. There is endpoint for updating book_loan and it only updates
the end_date. When there are NO book_loan objects with end_date set 
as null, then the book can be loaned, and we can see a status change on
the book list. We can confirm if it works properly checking the book_loan
list endpoint, where end_date is returned. 


### Features

The rest of the features should be as stated in the task. 

We can add a book, delete it, get all the books, update the state of the book
(by updating to book loan objects). There's also a validation for the user card
numbers and for book ids. 

### Future features

Of course, the above are the 'explicit' features but as a developer I know that
this should come with features that weren't stated explicitly, especially when
I have decided on the specific construct of book loans. But I didn't make it on 
time, so some things are missing, even though they should be thought of based on
how the system is constructed. Here are some of the features I didn't have time 
to incorporate:

- checking if there are multiple book loans without an end_date (which would suggest that
several people can loan the same book in the same time)
- validating if there are dates overlapping for the same book
- validating if several people are loaning the same book in the same time

I think that would be the most important improvements.