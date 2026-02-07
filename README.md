# AgriQ — AI & Quantum-Inspired Agricultural Coordinator

AgriQ is an intelligent decision engine that combines **Artificial Intelligence** and **Quantum-Inspired Optimization** to coordinate agricultural decisions across farmers.  
Instead of optimizing each farmer individually, AgriQ creates a **balanced national-level crop planning strategy** that respects water scarcity and market demand — preventing oversupply and price collapse.

---

## 🌍 Motivation & Problem

Traditional agricultural advisory tools focus on individual farmers without considering system-level effects. This leads to:

-  Oversupply of certain crops
-  Market price collapse
-  Wasteful water usage
-  Lack of coordinated planning

In regions like **Palestine**, where water access is limited and agricultural markets are fragile, these problems are amplified.

Example challenges:
- Farmers copy each other’s successful crops
- Prices crash due to oversupply
- Water scarcity leads to inefficient farming
- Dependency on imports increases

AgriQ solves this by coordinating farming decisions rather than recommending in isolation.

---

## 🧠 Concept & Approach

AgriQ works in two complementary stages:

1. **AI Crop Recommendation**
   - Predicts suitable crops for each farmer based on:
     - Soil data  
     - Weather conditions  
     - Water access  
     - Market demand  
   - Outputs a ranked list of crop options per farmer.

2. **Quantum-Inspired Optimization**
   - Coordinates all farmers simultaneously to:
     - Respect total water limits
     - Avoid market collapse
     - Maximize overall efficiency
   - Uses combinatorial optimization inspired by quantum algorithms

This combination ensures system-wide balance, not just individual success.

---

## 📈 Key Equations

###  Market Balance Score
\[
Score_{market} = \frac{1}{n} \sum_{i=1}^{n} \left(1 - |ActualRatio_i - TargetRatio_i|\right)
\]

Measures how close the current crop distribution is to a balanced target distribution.

---

###  Non-Linear Penalty
\[
Penalty = 
\begin{cases}
\left(\frac{Actual}{Target}\right)^2 & \text{if } Actual > 1.5 \times Target \\
0 & \text{otherwise}
\end{cases}
\]

Applies a progressive penalty when production exceeds safe limits, encouraging diversity.

---

###  Efficiency (Value per Water)
\[
Efficiency = \frac{TotalProfit}{TotalWaterConsumption}
\]

Evaluates economic benefit per unit of water — essential in water-scarce environments.

---

## 🚀 Features

-  Individual AI recommendations
-  Collective coordination using quantum-inspired logic
-  Real-time decision simulation
-  Water constraint awareness
-  Market stability optimization
- 📉 Reduces waste and inefficiency

