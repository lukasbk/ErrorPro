from output import Output
from quantities import Quantity

# not suitable for automated testing, so must be tested manually


if __name__ == '__main__':

    config = {"unit_system":"si",
              "directory":"results",
              "auto_results":"results.csv",
              "rounding":True}
    output=Output()

    data = {}

    output.save(data, config)
