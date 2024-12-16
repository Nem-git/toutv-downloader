


from services.noovo.search import Search
from services.noovo.info import Info

search = Search()

query = "Occupation Double"

shows = search.Shows(query)

show = shows[0]

Info().Shows(show)

print("WAIT")