CREATE TABLE public.stocks_customuser
(
    id  SERIAL NOT NULL PRIMARY KEY,
    email    VARCHAR(254),
    password VARCHAR(50),
    is_staff    BOOLEAN DEFAULT false,
    is_superuser    BOOLEAN DEFAULT false,
    last_login TIMESTAMP
)

CREATE TABLE public.stocks_orderevent
(
    id  SERIAL NOT NULL PRIMARY KEY,
    serv  INTEGER,
    ord  INTEGER
);

GRANT ALL ON ALL TABLES IN SCHEMA public to postgres;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO postgres;

ALTER TABLE public.stocks_customuser
ALTER COLUMN password TYPE VARCHAR(254);
