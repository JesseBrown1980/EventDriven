import json

import save
import make_graph
import total_calc


def lambda_handler(event, context):

    covid_csv = save.get_s3()
    to_dash = make_graph.transform(covid_csv)
    comparison = make_graph.by_month(to_dash)
    save.graph_to_s3(comparison)

    covid_csv = save.get_s3()
    to_dash = total_calc.transform(covid_csv)
    totals = total_calc.total_numbers(to_dash)

    # expose return total values to api
    return json.dumps([{"total": total} for total in totals])


def main():
    lambda_handler()


if __name__ == '__main__':
    main()
