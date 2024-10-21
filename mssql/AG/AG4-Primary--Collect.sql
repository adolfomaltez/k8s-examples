/*    Collect local database replica states    */
SELECT cs.[database_name], 'database_replica', rs.synchronization_health
FROM sys.dm_hadr_database_replica_states rs
join sys.dm_hadr_database_replica_cluster_states cs ON rs.replica_id = cs.replica_id and rs.group_database_id = cs.group_database_id
WHERE rs.is_local = 1