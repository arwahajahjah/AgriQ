import itertools


def quantum_inspired_optimize(
    farmers_options,
    water_limit=200,
    market_limit=None
):
    """
    Quantum-inspired combinatorial optimization (QAOA-inspired)

    farmers_options:
    [
      [ {crop, water, profit}, {crop, water, profit} ],
      [ {crop, water, profit}, {crop, water, profit} ],
      ...
    ]

    water_limit: الحد الأقصى لاستهلاك المياه
    market_limit: dict يحدد أقصى عدد مزارعين لكل محصول
                  مثال: {"orange": 1, "pigeonpeas": 2}
    """

    num_farmers = len(farmers_options)
    best_solution = None
    best_score = float("-inf")

    # جميع التوليفات الممكنة (اختيار واحد لكل مزارع)
    all_choices = list(itertools.product([0, 1], repeat=num_farmers))

    for choice in all_choices:
        total_water = 0.0
        total_profit = 0.0
        valid = True

        crop_counter = {}

        for i, option_index in enumerate(choice):
            if option_index >= len(farmers_options[i]):
             valid = False
            break


            crop = option["crop"]
            water = option["water"]
            profit = option["profit"]

            # تجميع القيم
            total_water += water
            total_profit += profit

            # قيد المياه
            if total_water > water_limit:
                valid = False
                break

            # قيد السوق (منع الفائض)
            crop_counter[crop] = crop_counter.get(crop, 0) + 1
            if market_limit is not None:
                if crop_counter[crop] > market_limit.get(crop, num_farmers):
                    valid = False
                    break

        # اختيار أفضل حل صالح
        if valid and total_profit > best_score:
            best_score = total_profit
            best_solution = choice

    return best_solution, round(best_score, 2)


# =========================
# Example run (اختياري)
# =========================
if __name__ == "__main__":

    farmers = [
        [
            {"crop": "orange", "water": 61.6, "profit": -1.8},
            {"crop": "pigeonpeas", "water": 62.0, "profit": -14.9},
        ],
        [
            {"crop": "orange", "water": 60.2, "profit": -3.5},
            {"crop": "pigeonpeas", "water": 55.1, "profit": -6.2},
        ],
        [
            {"crop": "orange", "water": 70.0, "profit": -9.0},
            {"crop": "pigeonpeas", "water": 54.3, "profit": -4.1},
        ],
    ]

    market_limit = {
        "orange": 1,
        "pigeonpeas": 2
    }

    solution, score = quantum_inspired_optimize(
        farmers_options=farmers,
        water_limit=180,
        market_limit=market_limit
    )

    print("Best solution:", solution)
    print("Best score:", score)

    for i, choice in enumerate(solution):
        print(f"Farmer {i} should plant: {farmers[i][choice]['crop']}")
