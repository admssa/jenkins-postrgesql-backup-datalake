

jenkins job to backup data from postrgesql 
First job take you to create a daily DB (postgres) backup and also (for the exercise) let's assume we have data-lake (besides our applicative DB) and we want to move every day all the data from a specific table that was created X days ago to the data-lake and to delete it from the applicative DB when it was saved in the data lake.
