from ai_model import recommend_crops
from quantum_optimizer import quantum_inspired_optimize


def run_pipeline(farmers_inputs, water_limit=200, market_limit=None):
    """
    Orchestrates the full AgriQ pipeline:
    AI recommendations -> Quantum-inspired coordination

    farmers_inputs:
        list of dicts, each dict represents one farmer input

    water_limit:
        total water limit shared across all farmers

    market_limit:
        dict defining max number of farmers per crop
        example: {"orange": 1, "pigeonpeas": 2}
    """

    farmers_options = []

    # =========================
    # 1️⃣ Run AI for each farmer
    # =========================
    for farmer_input in farmers_inputs:
        recommendations = recommend_crops(farmer_input, top_k=2)

        # --- SAFETY HANDLING ---
        # Ensure exactly 2 options per farmer
        if len(recommendations) == 0:
            recommendations = [
                {"crop": "orange", "water": 60, "profit": -10},
                {"crop": "orange", "water": 60, "profit": -10},
            ]
        elif len(recommendations) == 1:
            recommendations = recommendations * 2

        farmers_options.append(recommendations)

    # =========================
    # 2️⃣ Quantum-inspired optimization
    # =========================
    solution, score = quantum_inspired_optimize(
        farmers_options=farmers_options,
        water_limit=water_limit,
        market_limit=market_limit
    )

    # =========================
    # 3️⃣ Build final coordinated plan
    # =========================
    final_plan = []

    for i in range(len(farmers_options)):
        # If optimizer provided a decision
        if solution is not None and i < len(solution):
            choice_index = solution[i]
        else:
            # Fixed decision (only one viable option)
            choice_index = 0

        chosen = farmers_options[i][choice_index]

        final_plan.append({
            "farmer_id": i,
            "crop": chosen["crop"],
            "water": chosen["water"],
            "profit_score": chosen["profit"]
        })

    return final_plan, score
