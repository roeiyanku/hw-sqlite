import sqlite3

def net_support_for_candidate1(candidate1:str, candidate2:str)->int:
    """Return #people preferring candidate1 minus #people preferring candidate2 (by Q6 rankings).

    >>> net_support_for_candidate1("בני גנץ", "יאיר לפיד")
    47
    >>> net_support_for_candidate1("יאיר לפיד", "בני גנץ")
    -47
    """
    conn = sqlite3.connect("poll.db")
    col1, col2 = [conn.execute("SELECT Variable FROM codes_for_questions WHERE Label = ?",
                               (c,)).fetchone()[0] for c in (candidate1, candidate2)]
    return conn.execute(f'SELECT SUM("{col1}" < "{col2}") - SUM("{col1}" > "{col2}") '
                        'FROM list_of_answers').fetchone()[0]

def condorcet_winner()->str:
    """Return the candidate who beats all others in pairwise comparisons, or "אין" if none exists.

    >>> condorcet_winner()
    'נפתלי בנט'
    """
    conn = sqlite3.connect("poll.db")
    candidates = [row[0] for row in
                  conn.execute("SELECT Label FROM codes_for_questions WHERE Variable LIKE 'Q6%'")]
    winners = [c for c in candidates
               if all(net_support_for_candidate1(c, other) > 0 for other in candidates if other != c)]
    return winners[0] if winners else "אין"


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())

    # Use this code for testing via console input-output:
    # party = input()
    # if party == "condorcet_winner":
    #     print(condorcet_winner())
    # else:
    #     candidate1,candidate2 = party.split(",")
    #     print(net_support_for_candidate1(candidate1,candidate2))
