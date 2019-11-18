import math
import numpy as np
import matplotlib.pyplot as plt

# calculate_area: this function is used to calculate the risk areas based on the fuzzy function results and multi-
# criteria calculations of data in the three risk categories.
# The code is not optimised, the construction of the three triangles could be rewritten as one function, but for the
# purpose of the prototype left in the main program.

def calculate_area(line1, line2, line3):
    # Three sides of the triangle is a, b and c:
    a = float(line1)
    b = float(line2)
    c = float(line3)

    # calculate the semi-perimeter
    s = (a + b + c) / 2

    # calculate the area
    area = (s * (s - a) * (s - b) * (s - c)) ** 0.5
    return area


# create the risk triangle
A = [0, 0]
B = [100, 0]
AB = 100
Ab = AB / 2
c1 = math.tan(60 * math.pi / 180) * Ab
o1 = math.tan(30 * math.pi / 180) * Ab  # Origin point
C = [50, c1]

OriginPoint = [Ab, o1]
LineAO = Ab / math.cos(30 * math.pi / 180)
# print(LineAO)

X = np.array([A, B, C])
Y = ['red', 'red', 'red']
risk_triangle = calculate_area(AB, AB, AB)

# Set the risk level for each edge, hard coded for now, but linked to the previous step when the country levels are
# calculated
LineAB = 70    # Hazard
LineBC = 60    # Vulnerability
LineCA = 30    # Exposure

# Set the Hazard Triangle based on %
HazardRatio = LineAB / AB
AA2 = (AB / 2) - ((AB * HazardRatio) / 2)
aa2 = (1 - HazardRatio) * o1
HPa = [AA2, aa2]
BB2 = (AB / 2) + ((AB * HazardRatio) / 2)
HPb = [BB2, aa2]

hazard_triangleX = np.array([HPa, HPb, OriginPoint])
hazard_triangleY = ['green', 'grey', 'grey']
A2O = LineAO * HazardRatio
hazard_triangle = calculate_area(LineAB, A2O, A2O)

# Set the Vulnerability Triangle based on %
VulnRatio = LineBC / AB
CC2 = (AB / 2)
cc2 = (VulnRatio * LineAO) + o1
VPa = [CC2, cc2]
aa2 = (1 - VulnRatio) * o1
BB2 = (AB / 2) + ((AB * VulnRatio) / 2)
VPb = [BB2, aa2]

vuln_triangleX = np.array([VPa, VPb, OriginPoint])
vuln_triangleY = ['blue', 'grey', 'grey']
A2O = LineAO * VulnRatio
vuln_triangle = calculate_area(LineBC, A2O, A2O)

# Set the Exposure Triangle based on %
ExpRatio = LineCA / AB
AA2 = (AB / 2) - ((AB * ExpRatio) / 2)
aa2 = (1 - ExpRatio) * o1
EPa = [AA2, aa2]
CC2 = (AB / 2)
cc2 = (ExpRatio * LineAO) + o1
EPb = [CC2, cc2]

exp_triangleX = np.array([EPa, EPb, OriginPoint])
exp_triangleY = ['black', 'grey', 'grey']
A2O = LineAO * ExpRatio
exp_triangle = calculate_area(LineCA, A2O, A2O)

# Calculate the country risk as:
# RISK  = R(H*E) + R(E*V) + R(H*V)
#       = 2083333,333 + 2083333,333 + 2083333,333 = 6250000
#       + R(1443,375673 * 1443,375673)

RiskHE = hazard_triangle * exp_triangle
RiskEV = exp_triangle * vuln_triangle
RiskHV = hazard_triangle * vuln_triangle
RISK = RiskEV + RiskHE + RiskHV
RiskRatio = RISK / 6250000
print(RiskRatio)

# Calculate the Risk Score
# = IF(RiskRatio<0,001;0,01;14,47648273*LN(RiskRatio) + 100)
# Expressing the Vaccination Risk is possible as risk ratio, but is  not very useful because the risk ratios are small
# for most combinations.
# Better is to rescale the ratio to a score using the function above, with the scoring it is possible to apply a
# classification as well (five classes in steps of 20)
if RiskRatio <= 0.001:
    RiskScore = 1
else:
    RiskScore = 14.47648273 * math.log(RiskRatio) + 100

RiskScore = int(RiskScore*1000)/1000

print(RiskScore)
if RiskScore > 80:
    RiskClass = "Very High"
elif RiskScore > 60:
    RiskClass = "High"
elif RiskScore > 40:
    RiskClass = "Elevated"
elif RiskScore > 20:
    RiskClass = "Low"
else:
    RiskClass = "Normal"

# plot the figure
plt.figure()
plt.title('Risk Triangle')
plt.suptitle('Risk Level is {} with a score of {}'.format(RiskClass, RiskScore), fontsize=14, fontweight='bold')
plt.text(1, -10, 'Hazard',
         verticalalignment='bottom', horizontalalignment='left',
         color='green', fontsize=15)
plt.text(80, 5, 'Vulnerability',
         verticalalignment='bottom', horizontalalignment='left',
         color='blue', fontsize=15,
         rotation=-60)
plt.text(20, 50, 'Exposure',
         verticalalignment='bottom', horizontalalignment='left',
         color='black', fontsize=15,
         rotation=60)

plt.scatter(X[:, 0], X[:, 1], s=170, color='grey')

t1 = plt.Polygon(X[:3, :], facecolor="none", edgecolor=Y[0])
plt.gca().add_patch(t1)

t2 = plt.Polygon(hazard_triangleX[:6, :], facecolor="none", edgecolor=hazard_triangleY[0])
plt.gca().add_patch(t2)

t3 = plt.Polygon(vuln_triangleX[:6, :], facecolor="none", edgecolor=vuln_triangleY[0])
plt.gca().add_patch(t3)

t4 = plt.Polygon(exp_triangleX[:6, :], facecolor="none", edgecolor=exp_triangleY[0])
plt.gca().add_patch(t4)

plt.gca().set_xbound(-20, 120)
plt.gca().set_ybound(-20, 100)
plt.gca().set_aspect('equal', 'datalim')

plt.show()


