cd dumps
cd fix_table
cd to_execute
for sql_file in `ls`
do
  docker exec -i db mysql -uroot -psecret123 simplenutrition < $sql_file --init-command="SET SESSION FOREIGN_KEY_CHECKS=0;" --force
done