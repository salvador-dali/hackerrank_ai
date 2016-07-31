# https://www.hackerrank.com/challenges/predicting-house-prices
# http://scikit-learn.org/stable/modules/linear_model.html
#
# y' = w_0 + sum(w_i * x_i)
# vector w (w_1, ..., w_n) is coef
#
# if we have just a simple linear regression, you can use curve_fit from scipy curve_fit
# this allow us to do a simple regression (not multivariate) and it allows to fit in any
# function. Not only linear and polynomial. Check SciPy and NumPy page 18/28
# time complexity is O(n*m^2), where matrix is n*m size and m > n
from sklearn import linear_model
#from numpy import dot

matrix = [[0.18, 0.89], [1.0, 0.26], [0.92, 0.11], [0.07, 0.37], [0.85, 0.16], [0.99, 0.41], [0.87, 0.47]]
vector = [109.85, 155.72, 137.66, 76.17, 139.75, 162.6, 151.77]
predict= [0.49, 0.18]
# matrix is the matrix of dependent variables (the one you already know: all your features)
# vector is the result of all your computations for your features
# predict is vector for which we need to find the result.

clf = linear_model.LinearRegression()
clf.fit(matrix, vector)

# clf.intercept_ is our w_0
# clf.coef_ is the vector w_i
#print dot(clf.coef_, predict) + clf.intercept_
print clf.predict(predict)

