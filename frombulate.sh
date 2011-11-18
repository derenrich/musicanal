cat data.csv | grep -v "  " | shuf > clean_data.csv
cat clean_data.csv |  head -n -50000 | cut -d" " -f 1,2 --complement > train_features.csv
cat clean_data.csv |  head -n -50000 | cut -d" " -f 1,2 > train_labels.csv
cat clean_data.csv |  tail -n 50000 | cut -d" " -f 1,2 --complement > test_features.csv
cat clean_data.csv |  tail -n 50000 | cut -d" " -f 1,2 > test_labels.csv
