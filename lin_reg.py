import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy

def runRiskPlant(param = None):
	ppdf = pd.read_csv("cali_powerplant_out.csv")
	riskdf = pd.read_csv("risk_data.csv")

	arr1 = ppdf['County']
	arr2 = riskdf[['COUNTY','RISK_SCORE','AREA']]

	all_counties = arr2['COUNTY'].to_numpy()
	pp_counties = arr1.unique()


	res = np.zeros((len(all_counties),2))
	res[:,1] = arr2['RISK_SCORE'].to_numpy()

	for county in pp_counties:
		pp_count = arr1.value_counts()[county]
		if county in all_counties:
			idx = np.where(all_counties == county)[0]
			res[idx,0] = arr1.value_counts()[county]

	if param == "area":
		res[:,0] = res[:,0]/arr2['AREA'].to_numpy()

	result = scipy.stats.linregress(res)
	plt.plot(res[:,0], result.intercept + result.slope*res[:,0], 'r', label='Linear Regression')

	for i in range(len(all_counties)):
		plt.scatter(res[i,0], res[i,1])
		# plt.annotate(all_counties[i],(res[i,0], res[i,1]))
	plt.xlabel("Number of Plants")
	plt.ylabel("Risk Index")
	plt.show()
	print("R-squared:",result.rvalue**2)


runRiskPlant()
