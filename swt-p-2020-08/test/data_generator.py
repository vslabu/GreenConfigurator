import itertools
import csv
from app.backend.config import Config
from app.backend.model import Model


# @param feature_number: number of features in model
# writes all possible configurations into csv-file
def config_to_csv(feature_number):
    # possible feature values
    feature_values = [0, 1]

    # returns list of all possible configurations
    all_configs = list(map(list, itertools.product(feature_values, repeat=feature_number)))

    mod = Model()

    with open('test_data.csv', mode='w', newline='') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for x in all_configs:
            con = list(mod.checkAndCalculate(Config(None, x)))

            # table row consists of: {Check={True|False}, Config={(0,1)^18}, NFPs if valid}
            row = [con[0] + [feat for feat in con[1].options] + con[2]]
            writer.writerow(row)
        f.flush()
    f.close()


# calling script for the model1 with 18 options
config_to_csv(feature_number=18)



