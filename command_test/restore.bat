for %%G in (*.sql) do docker exec -i db mysql -u root --password=secret123 simplenutrition < "%%G"  --init-command="SET SESSION FOREIGN_KEY_CHECKS=0;" --force
