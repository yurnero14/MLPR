import sys

def compute_Avg_scores(lscores):
    return sum(sorted(lscores)[1:-1])
    """
    In the function above, as per the first requirement the highest and lowest score is removed but first it is sorted
    in ascending order
    """

class Competitor:
    def __init__(self, name, surname, country, scores):
        self.name = name
        self.surname = surname
        self.country = country
        self.scores = scores
        self.avg_score = compute_Avg_scores(scores)

"""
A class is created since we have different attributes for the competitor and we need an object to store the information
regarding the competitor 
"""

if __name__ == '__main__':
    l_bestCompetitors = []  # we are storing the best competitors in a list
    hCountryScores ={}  # instantiating a dictionary
    with open(sys.argv[1]) as f:
        # here we are specifying that we will take the file from command line's second argument [1]
        for line in f:
            name, surname, country = line.split()[0:3]
            scores = line.split()[3:]
            scores = [float(i) for i in scores]
            comp = Competitor(
                name,
                surname,
                country,
                scores
            )

            l_bestCompetitors.append(comp)

            if len(l_bestCompetitors) >= 4:
                # we need three best competitors so it makes sense that we start sorting them on their scores
                l_bestCompetitors = sorted(l_bestCompetitors, key=lambda i: i.avg_score)[::-1][0:3]
                # [::-1] means to traverse the iterable in reverse since sorted gives ascending order and then we sliced

            if comp.country not in hCountryScores:
                hCountryScores[comp.country] = 0
            hCountryScores[comp.country] += comp.avg_score
            # using country as key we are populating the dictionary. this is second requirement of excercise 1

    if len(hCountryScores) == 0:
        print('No competitors')
        sys.exit(0)

    best_country = None
    for count in hCountryScores:
        # count is the dummy variable for the key of the dictionary and its value is then being compared
        if best_country is None or hCountryScores[count] > hCountryScores[best_country]:
            best_country = count

    print('Final ranking:')
    for pos, comp in enumerate(l_bestCompetitors):
        print('%d: %s %s - Score: %.1f' % (pos + 1, comp.name, comp.surname, comp.avg_score))
    print()
    print('Best Country:')
    print("%s - Total score: %.1f" % (best_country, hCountryScores[best_country]))

    """
    The final part of the code is C-style formatting which looks like a pain in the ass. there are different 
    and easier ways for me to do it 
    """
