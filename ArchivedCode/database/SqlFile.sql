use sceneseeker;

CREATE TABLE users (
    private_key INT AUTO_INCREMENT PRIMARY KEY,
    identifier INT, -- Foreign key pointing to other tables
    username VARCHAR(255),
    password VARCHAR(255), -- Hashed password
    email VARCHAR(255)
);

CREATE TABLE recommendations (
    user_id INT, -- Foreign key pointing to users table
    recommended_1 INT,
    recommended_2 INT,
    recommended_3 INT,
    recommended_4 INT,
    recommended_5 INT,
    recommended_6 INT,
    recommended_7 INT,
    recommended_8 INT,
    recommended_9 INT,
    recommended_10 INT
);

CREATE TABLE friends (
    user_id_1 INT,
    user_id_2 INT
    -- You might want to add additional fields here if needed
);

CREATE TABLE watched_movies (
    user_id INT,
    movie_id INT, -- Assuming movie IDs are strings
    timestamp TIMESTAMP,
    PRIMARY KEY (user_id, movie_id)
);

CREATE TABLE reviews (
    user_id INT,
    movie_id INT,
    timestamp TIMESTAMP,
    review_text TEXT,
    PRIMARY KEY (user_id, movie_id)
);

CREATE TABLE follows (
	user_id_1 INT,
	user_id_2 INT
);

CREATE TABLE watched_movies (
	user_id INT,
	movie_id INT,
	timestamp TIMESTAMP,
	PRIMARY KEY (user_id, movie_id)
);

CREATE TABLE reviews (
	user_id INT,
	movie_id INT,
	timestamp TIMESTAMP,
	review_text TEXT,
	PRIMARY KEY (user_id, movie_id)
);







