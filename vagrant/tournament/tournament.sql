-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


CREATE TABLE REGISTERED_PLAYERS(
   PLAYER_ID SERIAL PRIMARY KEY,
   NAME           TEXT    NOT NULL,
   WINS            INT     NOT NULL,
   MATCHES			INT 	NOT NULL
);

CREATE TABLE ROUNDS(
   WINNER_ID        INT    NOT NULL,
   LOSER_ID			INT    NOT NULL
);