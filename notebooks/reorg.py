import csv

##organize fish records , each fish needs length, maturity, sex on 1 row

file1 = '../data/raw/IBS2_First_2_Years/Organism_values.csv'

data_dict = []

def csv_to_dict( infile  ):
	
	with open( infile , 'r') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
		header = next(spamreader)
		for row in spamreader:
			row_dict = { header[i]: row[i] for i in range(len(header)) }
			data_dict.append( row_dict ) 
	return 

csv_to_dict(file1)

#get unique fish
org_ids = [ int(i['ORGANISM_ID']) for i in data_dict ]
org_id_set = list(set( org_ids ))
print( "number unique fish", len( org_id_set ))

return_dict = {}
ex = [0,0,0]

#each fish gets one record
for org_id in org_id_set:
	try:
		#get sex
		sex = [d['VALUE'] for d in data_dict if int(d['ORGANISM_ID']) == org_id and d['PARAM'] == 'Sex Value'][0]
	except: 
		ex[0] += 1
		sex = None

	try:
		#get len
		length = [d['VALUE'] for d in data_dict if int(d['ORGANISM_ID']) == org_id and d['PARAM'] == 'Length'][0]
	except:
		ex[1] += 1
		length = None	

	try:
		#get maturity  
		maturity = [d['VALUE'] for d in data_dict if int(d['ORGANISM_ID']) == org_id and d['PARAM'] == 'Record GF Maturity'][0]
	except:
		ex[2] += 1
		maturity = None

	op_id = [d['OPERATION_ID'] for d in data_dict if int(d['ORGANISM_ID']) == org_id and d['PARAM'] == 'Length'][0]
	cruise_id = [d['CRUISE_ID'] for d in data_dict if int(d['ORGANISM_ID']) == org_id and d['PARAM'] == 'Length'][0]

	record_dict = { 'OPERATION_ID': op_id, 'CRUISE_ID': cruise_id, 'ORGANISM_ID': org_id, 'sex': sex, 'length': length, 'maturity': maturity,  }
	return_dict[ org_id ] = record_dict


print( "total exceptions", ex )
print( "return dict size ", len(return_dict) )
	
output_file = '../data/raw/reorg.csv'
def to_csv( output_obj, output_file ):
	with open(output_file, 'w', newline='') as csvfile:
	    spamwriter = csv.writer(csvfile, delimiter=',',
	                            quoting=csv.QUOTE_MINIMAL)	    
	    spamwriter.writerow( next(iter( output_obj.values())).keys() )
	    for row in output_obj:
	    	spamwriter.writerow( [ output_obj[row][i] for i in output_obj[row]] )
	return
to_csv( return_dict,  output_file )