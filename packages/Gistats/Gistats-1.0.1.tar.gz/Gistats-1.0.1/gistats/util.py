def sep(stats, sep, until):
    worked = []

    for key in stats:
        stat = f' {key} '
        string = (stats[key]['emoji'] + stat if 'emoji' in stats[key]
                  else stat)

        while until > len(string):
            string += sep

        string += f' {stats[key]["value"]}\n'

        worked.append(string)

    return ''.join(string for string in worked)
