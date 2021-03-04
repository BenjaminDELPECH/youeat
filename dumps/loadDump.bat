cd dumps/fix_table/to_execute
forfiles /M *.sql /C "cmd /c docker exec -h 127.0.0.1 -i db mysql -u root -psecret123 simplenutrition < @path"
cd ../../../