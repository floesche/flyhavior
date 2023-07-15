load-data:
	#python flyhavior/cli.py --post --flyflix ~/xtmp/data/repeater_20230706_155303.csv --fictrac ~/xtmp/data/fictrac-20230706_155322.dat
	#mv -f data/test.db data/cshl001.db
	# sqlite3 -header -csv data/cshl001.db "select * from v_move;" > data/cshl001.csv

