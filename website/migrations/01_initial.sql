CREATE TABLE users(
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    name TEXT NOT NULL,
    password TEXT NOT NULL,
    email TEXT NOT NULL,
    admin BOOLEAN NOT NULL
);

CREATE TABLE articles(
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    tags TEXT NOT NULL
);

CREATE TABLE booking_prices(
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    type TEXT NOT NULL,
    price INT NOT NULL,
    max_per_day INT NOT NULL
);

CREATE TABLE bookings(
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    price_id INT NOT NULL,
    time DATE NOT NULL,
    user_id INT NOT NULL,

    FOREIGN KEY (price_id) REFERENCES booking_prices(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE article_visits(
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    article_id INT NOT NULL,

    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE
);

