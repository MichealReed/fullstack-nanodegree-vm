-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

CREATE TABLE REGISTERED_PLAYERS(
   PLAYER_ID SERIAL PRIMARY KEY,
   NAME      TEXT   NOT NULL,
   MATCHES   INT    NOT NULL   
);

CREATE TABLE ROUNDS(
   ROUND_ID		    SERIAL	   	      PRIMARY KEY,
   WINNER_ID        INT REFERENCES    REGISTERED_PLAYERS(PLAYER_ID),
   LOSER_ID			INT REFERENCES    REGISTERED_PLAYERS(PLAYER_ID)
);

CREATE VIEW WINTRACKER
AS
  SELECT REGISTERED_PLAYERS.PLAYER_ID,
         REGISTERED_PLAYERS.NAME,
         COUNT(ROUNDS.WINNER_ID) AS WINS,
		 REGISTERED_PLAYERS.MATCHES
  FROM   REGISTERED_PLAYERS
         LEFT JOIN ROUNDS
                ON REGISTERED_PLAYERS.PLAYER_ID = ROUNDS.WINNER_ID
  GROUP  BY REGISTERED_PLAYERS.PLAYER_ID
  ORDER  BY WINS;
  