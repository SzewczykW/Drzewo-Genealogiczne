FROM neo4j:5.25.1

ENV NEO4J_PLUGINS='["apoc", "apoc-extended"]'
ENV NEO4J_apoc_export_file_enabled=true
ENV NEO4J_apoc_import_file_enabled=true
ENV NEO4J_apoc_import_file_use__neo4j__config=true
ENV NEO4J_dbms_security_procedures_allowlist=apoc.* 
ENV NEO4J_dbms_security_procedures_unrestricted=apoc.* 
ENV NEO4J_initial_dbms_default__database=neo4j
ENV NEO4J_server_config_strict__validation_enabled=false

COPY ./init.cypher /var/lib/neo4j/import

EXPOSE 7474 7687
