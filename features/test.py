
from volatility import calculate_volatility

# numlist = [1,2,3,4,5,6,7,8,9,1,2,3,4,5,45,6,7,89,12,23,34,45,5,6]




# stddev = compute_individual_volatility(numlist)

# print(stddev)


vol_frame = calculate_volatility("return1day.parquet")

print(vol_frame.head())