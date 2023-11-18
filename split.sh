file_rows=wc -l ./collected-proxies/row-url/all.txt|awk '{print 1}'
file_num=3
file_num_row=$((${file_rows} + 2))
every_file_row=$((${file_num_row}/${file_num}))
split -d -a 1 -l ${every_file_row} ./collected-proxies/row-url/all.txt ./collected-proxies/row-url/all_
