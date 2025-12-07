# pip3 install neo4j-driver
# python3 main.py

import time
from neo4j import GraphDatabase, basic_auth
from neo4j.exceptions import ServiceUnavailable
import logging


driver = GraphDatabase.driver(
    "neo4j+s://2a9865c8.databases.neo4j.io",
    auth=basic_auth("neo4j", "VOQ_aOTU3FIC5NBslltZqfY3xCQvNkzH2jNwircWigk"),
)

# How many reviews does each Mission Impossible movie have?
cypher_query1 = """
MATCH (m:Movie)<-[:RATED]-(u:User)
WHERE m.title CONTAINS 'Mission:'
WITH m, count(*) AS reviews
RETURN m.title AS movie, reviews
ORDER BY reviews DESC LIMIT 5;
"""

# Items similar to the item you’re looking at now
cypher_query2 = """
MATCH p=(m:Movie {title: 'Inception'})
       -[:ACTED_IN|IN_GENRE|DIRECTED*2]-()
RETURN p LIMIT 25
"""

# Users who got this item, also got that other item.
cypher_query3 = """
MATCH (m:Movie {title: 'Inception'})<-[:RATED]-
      (u:User)-[:RATED]->(rec:Movie)
WITH rec, COUNT(*) AS usersWhoAlsoWatched
ORDER BY usersWhoAlsoWatched DESC LIMIT 25
RETURN rec.title AS recommendation, usersWhoAlsoWatched
"""

# Find movies most similar to "Inception" based on shared genres
# Find similar movies by common genres
cypher_query4 = """
MATCH (m:Movie)-[:IN_GENRE]->(g:Genre)
              <-[:IN_GENRE]-(rec:Movie)
WHERE m.title = 'Inception'
WITH rec, collect(g.name) AS genres, count(*) AS commonGenres
RETURN rec.title, genres, commonGenres
ORDER BY commonGenres DESC LIMIT 2;
"""

# Recommend movies similar to those the user has already watched
# Content recommendation by overlapping genres
cypher_query5 = """
MATCH (u:User {name: 'Angelica Rodriguez'})-[r:RATED]->(m:Movie),
      (m)-[:IN_GENRE]->(g:Genre)<-[:IN_GENRE]-(rec:Movie)
WHERE NOT EXISTS{ (u)-[:RATED]->(rec) }
WITH rec, g.name as genre, count(*) AS count
WITH rec, collect([genre, count]) AS scoreComponents
RETURN rec.title AS recommendation, rec.year AS year, scoreComponents,
       reduce(s=0,x in scoreComponents | s+x[1]) AS score
ORDER BY score DESC LIMIT 10
"""

# Compute a weighted sum based on the number and types of overlapping traits
# Find similar movies by common genres
cypher_query6 = """
MATCH (m:Movie) WHERE m.title = 'Wizard of Oz, The'
MATCH (m)-[:IN_GENRE]->(g:Genre)<-[:IN_GENRE]-(rec:Movie)

WITH m, rec, count(*) AS gs,
count { (m)<-[:ACTED_IN]-()-[:ACTED_IN]->(rec) } AS as,
count { (m)<-[:DIRECTED]-()-[:DIRECTED]->(rec) } AS ds

WITH rec, (5*gs)+(3*as)+(4*ds) AS score
ORDER BY score DESC LIMIT 25
RETURN rec.title AS recommendation, score
"""

# What movies are most similar to "Inception" based on Jaccard similarity of genres?
cypher_query7 = """
MATCH (m:Movie {title:'Inception'})-[:IN_GENRE]->
      (g:Genre)<-[:IN_GENRE]-(other:Movie)
WITH m, other, count(g) AS intersection, collect(g.name) as common

WITH m,other, intersection, common,
     [(m)-[:IN_GENRE]->(mg) | mg.name] AS set1,
     [(other)-[:IN_GENRE]->(og) | og.name] AS set2

WITH m,other,intersection, common, set1, set2,
     set1+[x IN set2 WHERE NOT x IN set1] AS union

RETURN m.title, other.title, common, set1,set2,
       ((1.0*intersection)/size(union)) AS jaccard

ORDER BY jaccard DESC LIMIT 25
"""

# We can apply cypher_query7 approach to all "traits" of the movie (genre, actors, directors, etc.)
cypher_query8 = """
MATCH (m:Movie {title: 'Inception'})-[:IN_GENRE|ACTED_IN|DIRECTED]-
                   (t)<-[:IN_GENRE|ACTED_IN|DIRECTED]-(other:Movie)
WITH m, other, count(t) AS intersection, collect(t.name) AS common,
     [(m)-[:IN_GENRE|ACTED_IN|DIRECTED]-(mt) | mt.name] AS set1,
     [(other)-[:IN_GENRE|ACTED_IN|DIRECTED]-(ot) | ot.name] AS set2

WITH m,other,intersection, common, set1, set2,
     set1 + [x IN set2 WHERE NOT x IN set1] AS union

RETURN m.title, other.title, common, set1,set2,
       ((1.0*intersection)/size(union)) AS jaccard
ORDER BY jaccard DESC LIMIT 25
"""

# Show all ratings by Andrew Freeman
cypher_query9 = """
MATCH (u:User {name: 'Andrew Freeman'})
MATCH (u)-[r:RATED]->(m:Movie)
RETURN *
LIMIT 100;
"""

# Show average ratings by Andrew Freeman
cypher_query10 = """
MATCH (u:User {name: 'Andrew Freeman'})
MATCH (u)-[r:RATED]->(m:Movie)
RETURN avg(r.rating) AS average;
"""

# What are the movies that Andrew liked more than average?
cypher_query11 = """
MATCH (u:User {name: 'Andrew Freeman'})
MATCH (u)-[r:RATED]->(m:Movie)
WITH u, avg(r.rating) AS average
MATCH (u)-[r:RATED]->(m:Movie)
WHERE r.rating > average
RETURN *
LIMIT 100;
"""

# Simple collaborative filtering
# Here we just use the fact that someone has rated a movie, not their actual rating to demonstrate the structure of finding the peers. Then we look at what else the peers rated, that the user has not rated themselves yet.
cypher_query12 = """
MATCH (u:User {name: 'Cynthia Freeman'})-[:RATED]->
      (:Movie)<-[:RATED]-(peer:User)
MATCH (peer)-[:RATED]->(rec:Movie)
WHERE NOT EXISTS { (u)-[:RATED]->(rec) }
RETURN rec.title, rec.year, rec.plot
LIMIT 25
"""

# Modification of simple collabortaive filtering that takes into account movie popularity and using their rating and frequency to sort results.
cypher_query13 = """
MATCH (u:User {name: 'Cynthia Freeman'})-[r1:RATED]->
      (:Movie)<-[r2:RATED]-(peer:User)
WHERE abs(r1.rating-r2.rating) < 2 // similarly rated
WITH distinct u, peer
MATCH (peer)-[r3:RATED]->(rec:Movie)
WHERE r3.rating > 3
  AND NOT EXISTS { (u)-[:RATED]->(rec) }
WITH rec, count(*) as freq, avg(r3.rating) as rating
RETURN rec.title, rec.year, rating, freq, rec.plot
ORDER BY rating DESC, freq DESC
LIMIT 25
"""

# blend of collaborative filtering and content-based approaches
cypher_query14 = """
// compute mean rating
MATCH (u:User {name: 'Andrew Freeman'})-[r:RATED]->(m:Movie)
WITH u, avg(r.rating) AS mean

// find genres with higher than average rating and their number of rated movies
MATCH (u)-[r:RATED]->(m:Movie)
       -[:IN_GENRE]->(g:Genre)
WHERE r.rating > mean

WITH u, g, count(*) AS score

// find movies in those genres, that have not been watched yet
MATCH (g)<-[:IN_GENRE]-(rec:Movie)
WHERE NOT EXISTS { (u)-[:RATED]->(rec) }

// order by sum of scores
RETURN rec.title AS recommendation, rec.year AS year,
       sum(score) AS sscore,
       collect(DISTINCT g.name) AS genres
ORDER BY sscore DESC LIMIT 10
"""

# Cosine similarity
# Find the users with the most similar preferences to Roy Sweeney, according to cosine
cypher_query15 = """
MATCH (p1:User {name: "Roy Sweeney"})-[x:RATED]->
      (m:Movie)<-[y:RATED]-(p2:User)
WITH p1, p2, count(m) AS numbermovies,
     sum(x.rating * y.rating) AS xyDotProduct,
     collect(x.rating) as xRatings, collect(y.rating) as yRatings
WHERE numbermovies > 10
WITH p1, p2, xyDotProduct,
sqrt(reduce(xDot = 0.0, a IN xRatings | xDot + a^2)) AS xLength,
sqrt(reduce(yDot = 0.0, b IN yRatings | yDot + b^2)) AS yLength
RETURN p1.name, p2.name, xyDotProduct / (xLength * yLength) AS sim
ORDER BY sim DESC
LIMIT 100;
"""

# Pearson similarity
# Find users most similar to a user, according to Pearson similarity
cypher_query16 = """
MATCH (u1:User {name:"Cynthia Freeman"})-[r:RATED]->(m:Movie)
WITH u1, avg(r.rating) AS u1_mean

MATCH (u1)-[r1:RATED]->(m:Movie)<-[r2:RATED]-(u2)
WITH u1, u1_mean, u2, collect({r1: r1, r2: r2}) AS ratings
WHERE size(ratings) > 10

MATCH (u2)-[r:RATED]->(m:Movie)
WITH u1, u1_mean, u2, avg(r.rating) AS u2_mean, ratings

UNWIND ratings AS r

WITH sum( (r.r1.rating-u1_mean) * (r.r2.rating-u2_mean) ) AS nom,
     sqrt( sum( (r.r1.rating - u1_mean)^2) * sum( (r.r2.rating - u2_mean) ^2)) AS denom,
     u1, u2 WHERE denom <> 0

RETURN u1.name, u2.name, nom/denom AS pearson
ORDER BY pearson DESC LIMIT 100
"""

# kNN movie recommendation using Pearson similarity
cypher_query17 = """
MATCH (u1:User {name:"Katelyn Morgan"})-[r:RATED]->(m:Movie)
WITH u1, avg(r.rating) AS u1_mean

MATCH (u1)-[r1:RATED]->(m:Movie)<-[r2:RATED]-(u2)
WITH u1, u1_mean, u2, COLLECT({r1: r1, r2: r2}) AS ratings WHERE size(ratings) > 10

MATCH (u2)-[r:RATED]->(m:Movie)
WITH u1, u1_mean, u2, avg(r.rating) AS u2_mean, ratings

UNWIND ratings AS r

WITH sum( (r.r1.rating-u1_mean) * (r.r2.rating-u2_mean) ) AS nom,
     sqrt( sum( (r.r1.rating - u1_mean)^2) * sum( (r.r2.rating - u2_mean) ^2)) AS denom,
     u1, u2 WHERE denom <> 0

WITH u1, u2, nom/denom AS pearson
ORDER BY pearson DESC LIMIT 10

MATCH (u2)-[r:RATED]->(m:Movie) WHERE NOT EXISTS( (u1)-[:RATED]->(m) )

RETURN m.title, SUM( pearson * r.rating) AS score
ORDER BY score DESC LIMIT 25
"""

cypher_query_list = [cypher_query1, cypher_query2, cypher_query3, cypher_query4, cypher_query5, cypher_query6, cypher_query7, cypher_query8, cypher_query9, cypher_query10,
cypher_query11, cypher_query12, cypher_query13, cypher_query14, cypher_query15, cypher_query16, cypher_query17]


# # To run ALL queries
# with driver.session(database="neo4j") as session:
#     for query in cypher_query_list:
#         print("\n\n-----Query Results-----")
#         results = session.execute_read(
#             lambda tx: tx.run(query).data()
#         )
#         for record in results:
#             print(record)

# driver.close()

# To run a particular query
# Enter any cypher_query(#)
query = cypher_query1
with driver.session(database="neo4j") as session:

    print("\n\n-----Query Results-----")
    results = session.execute_read(
        lambda tx: tx.run(query).data()
    )
    for record in results:
        print(record)

driver.close()
