


from services.noovo.search import Search
from services.noovo.info import Info

search = Search()

query = "Occupation Double"

shows = search.Shows(query)

show = shows[0]

Info().Show(show)

for s in show.seasons:
    Info().Season(s)
    for e in s.episodes:
        Info().Episode(e)


print("WAIT")