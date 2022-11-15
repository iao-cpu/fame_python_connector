import csv

l = [[1, 2], [2, 3], [4, 5]]

out = open('c:\\python_connector\\fame_connector_beta2\\out.csv', 'w')
for row in l:
    for column in row:
        out.write('%d,' % column)
    out.write('\n')
    print(row)
out.close()