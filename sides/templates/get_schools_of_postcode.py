# Code by  : Anushi Shah
import sys
import json

def main():
    # my code here
	
	print "hello"
	json_array = get_schools_postcode(2000)
	
	for each_obj in json_array:
		json_str = json.loads(each_obj)
		print json_str
	

def get_schools_postcode(postcode):
		print "school function"
		print postcode
		
		json_array = []
		
		with open('Government-School-Locations.txt') as f:
			first_line = f.readline()
			lines = f.readlines()
			
			for each_line in lines:
				cols = each_line.split("\t")
				
				school_name_col = cols[2]
				postcode_col = cols[19]
				total_enrollments = cols[10]
				lat = cols[20]
				long = cols[21]
				
			
				if(str(postcode) == postcode_col):
					#print "---------------------"
					#print postcode_col
					#print school_name_col
					#print total_enrollments
					#print lat
					#print long
					
					data = {
					'json_school_name' : school_name_col,
					'json_total_enrollments' : total_enrollments,
					'lat' : lat,
					'long' : long
					}
			
					json_school_output = json.dumps(data)
					json_array.append(json_school_output)
					
			return json_array
		

if __name__ == "__main__":
	main()
	
	







