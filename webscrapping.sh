page_content=$(curl https://fr.investing.com/equities/nike-historical-data)
page_table=$(echo "$page_content" | grep -oP '<table((?!<table).)*?<span>Date.*?</table>')
table_header=$(echo "$page_table" | grep -oP '(?<=<th).*?(?=</th>)' | grep -oP '(?<=<span>).*?(?=</span>)' | sed 's/ //g')
table_rows=$(echo "$page_table" | grep -oP '(?<=<td|time).*?>\K.*?(?=</td|</time)' | sed 's/<time.*>//g' |  sed 's/ //g' | sed 's/,/./g')
echo $(echo "$table_header") | sed 's/ /;/g' > table.csv
column=0
for col in $table_header; do
    column=$((column+1))
done
i=0
for row in $table_rows; do
    i=$((i+1))
    if [ $((i%column)) -eq 0 ]; then
        echo "$row" >> table.csv
    else
        echo -n "$row;" >> table.csv
    fi
done

