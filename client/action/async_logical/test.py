from sympy import Point, Circle

# Coordinates of the two known points
p1 = Point(0, 0)
p2 = Point(5, 5)

# Distance from the unknown point to the two known points
d1 = 5
d2 = 5

# Define the circles centered at the known points with radii equal to the distances
c1 = Circle(p1, d1)
c2 = Circle(p2, d2)

# Find the intersection points of the circles
intersections = c1.intersection(c2)

# Print the coordinates of the intersection points
for p in intersections:
    print(f"The coordinates of the intersection point are: ({float(p.x)}, {float(p.y)})")

# from sympy import Point, Circle
#
# # Coordinates of the two known points
# p1 = Point(1, 1)
# p2 = Point(5, 5)
#
# # Distance from the unknown point to the two known points
# d1 = 3
# d2 = 4
#
# # Find the intersection points of the two circles
# circ1 = Circle(p1, d1)
# circ2 = Circle(p2, d2)
# intersections = circ1.intersection(circ2)
#
# # Select the intersection point that is closest to p1
# p3 = min(intersections, key=lambda x: x.distance(p1))
#
# # Format the coordinates of the unknown point
# x = "{:.2f}".format(p3.x)
# y = "{:.2f}".format(p3.y)
#
# # Print the coordinates of the unknown point
# print(f"The coordinates of the unknown point are: ({x}, {y})")