#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach
import math


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the player records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("TRUNCATE ROUNDS CASCADE")
    DB.commit()

        # Update matches and wins
    query = '''
                UPDATE REGISTERED_PLAYERS
                SET MATCHES = 0
            '''
    c.execute(query)
    DB.commit()

    DB.close()

def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("TRUNCATE REGISTERED_PLAYERS CASCADE")
    DB.commit()
    DB.close()


def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    c = DB.cursor()

    c.execute("SELECT count(*) from REGISTERED_PLAYERS")
    count = c.fetchall()
    DB.close()
    count = count[0]
    count = count[0]

    if count == None:
        count = 0

    return count


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    DB = connect()
    c = DB.cursor()
    c.execute("INSERT INTO REGISTERED_PLAYERS (NAME, MATCHES) VALUES (%s, %s)", (name, 0))
    DB.commit()
    DB.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB = connect()
    c = DB.cursor()

    query = '''
                SELECT * FROM WINTRACKER;
            '''

    c.execute(query)
    standing = c.fetchall()
    DB.close()

    return standing


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect()
    c = DB.cursor()

    # Update ROUNDS with winner and loser of match
    query = '''
                INSERT INTO ROUNDS (WINNER_ID, LOSER_ID)
                VALUES (%s, %s)
            '''

    c.execute(query, (winner, loser))
    DB.commit()

    # Update matches in REGISTERED_PLAYERS
    query = '''
                UPDATE REGISTERED_PLAYERS
                    SET MATCHES = (MATCHES + 1)
                WHERE PLAYER_ID = %s OR PLAYER_ID = %s
            '''
    c.execute(query, (winner, loser))
    DB.commit()

    DB.close()

def alreadyMatched(id1, id2):
    """Checks if two players have already been matched

    Args:
      id1:  the id number of a player
      id2:  the id number of a player
    """

    DB = connect()
    c = DB.cursor()

    query = '''
                SELECT WINNER_ID,
                       LOSER_ID
                FROM ROUNDS
                WHERE WINNER_ID = %s AND LOSER_ID = %s
            '''
    c.execute(query, (id1, id2))

    result = c.fetchall()

    if result:
        return True
    else:
        return False



 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    # We need to find out more about our current state and numbers
    player_count = countPlayers()
    total_rounds = math.log(player_count)/math.log(2)
    total_matches = total_rounds * player_count

    # Created the lists we will use to match the players
    player_list = playerStandings()
    match_list = [ ]
    unmatched_list = [ ]

    # separate our results for easier handling
    player_id = [seq[0] for seq in player_list]
    name = [seq[1] for seq in player_list]
    matches = [seq[3] for seq in player_list]


    
    # Creates pairings for zero matches
    if matches[0]  == 0:

        counter = 0

        while (counter <= (player_count / 2) + 2):
            match_list.append((player_id[counter], name[counter], player_id[counter + 1], name[counter + 1]))
            counter = counter + 2

    if matches[0] > 0 and matches[0] <= total_rounds:

        counter = 0
        # Initial loop to find matched players and place already matched in a unmatched list
        while (counter < player_count):
            if alreadyMatched(player_id[counter], player_id[counter + 1]) == False:
                match_list.append((player_id[counter], name[counter], player_id[counter + 1], name[counter + 1]))
            if alreadyMatched(player_id[counter], player_id[counter + 1]) == True:
                unmatched_list.append((player_id[counter], name[counter], player_id[counter + 1], name[counter + 1]))
            counter = counter + 2

        counter = 0
        # Secondary loop over our unmatched list to match remaining players
        if len(unmatched_list) > 0:
            while len(unmatched_list) > 0:
                match_list.append((player_id[counter], name[counter], player_id[counter + 1], name[counter + 1]))
                unmatched_list.pop(counter)
                unmatched_list.pop(counter + 1)


    return match_list











