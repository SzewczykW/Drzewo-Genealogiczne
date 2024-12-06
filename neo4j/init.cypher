MATCH (n) DETACH DELETE n; 
CREATE
  // Nodes

  // People
  (helen:Person {id: randomUUID(), first_name: 'Helen', last_name: 'Nowak', gender: 'Female', birth_date: '1945-05-16', death_date: '2010-06-16'}),
  (john:Person {id: randomUUID(), first_name: 'John', last_name: 'Nowak', gender: 'Male', birth_date: '1950-01-01'}),
  (mary:Person {id: randomUUID(), first_name: 'Mary', last_name: 'Lewandowska', gender: 'Female', birth_date: '1952-02-02'}),
  (peter:Person {id: randomUUID(), first_name: 'Peter', last_name: 'Lewandowski', gender: 'Male', birth_date: '1955-03-03'}),
  (susan:Person {id: randomUUID(), first_name: 'Susan', last_name: 'Lewandowska', gender: 'Female', birth_date: '1980-05-05'}),
  (linda:Person {id: randomUUID(), first_name: 'Linda', last_name: 'Lewandowska', gender: 'Female', birth_date: '1977-04-04'}),
  (james:Person {id: randomUUID(), first_name: 'James', last_name: 'Lewandowski', gender: 'Male', birth_date: '1982-06-06'}),
  (robert:Person {id: randomUUID(), first_name: 'Robert', last_name: 'Lewandowski', gender: 'Male', birth_date: '1985-12-12'}),
  (nancy:Person {id: randomUUID(), first_name: 'Nancy', last_name: 'Nowak-Lewandowska', gender: 'Female', birth_date: '1987-01-13'}),
  (sophie:Person {id: randomUUID(), first_name: 'Sophie', last_name: 'Lewandowska', gender: 'Female', birth_date: '2012-10-10'}),
  (paul:Person {id: randomUUID(), first_name: 'Paul', last_name: 'Nowak', gender: 'Male', birth_date: '2014-07-07'}),
  (alice:Person {id: randomUUID(), first_name: 'Alice', last_name: 'Lewandowska', gender: 'Female', birth_date: '2015-11-11'}),
 
  // Relationships
  
  // Parents
  (helen)-[:PARENT]->(linda), // Nowak
  (john)-[:PARENT]->(linda),
  (helen)-[:PARENT]->(susan), // Nowak
  (john)-[:PARENT]->(susan),
  (helen)-[:PARENT]->(nancy), // Nowak
  (john)-[:PARENT]->(nancy),
  
  (mary)-[:PARENT]->(james), // Lewandowski
  (peter)-[:PARENT]->(james),
  (mary)-[:PARENT]->(robert), // Lewandowski
  (peter)-[:PARENT]->(robert),

  (susan)-[:PARENT]->(paul), // Lewandowski
  (james)-[:PARENT]->(paul),
  (susan)-[:PARENT]->(sophie), // Lewandowska
  (james)-[:PARENT]->(sophie),

  (nancy)-[:PARENT]->(alice), // Lewandowska
  (robert)-[:PARENT]->(alice),

  // Marriages
  (helen)-[:MARRIED {since: '1970-04-02', status: 'Married'}]->(john), // np. Zielińska -> Nowak
  (mary)-[:MARRIED {since: '1977-04-02', status: 'Married'}]->(peter), // np. Kowalska -> Lewandowska
  (susan)-[:MARRIED {since: '2005-04-02', status: 'Married'}]->(james), // Nowak -> Lewandowska
  (nancy)-[:MARRIED {since: '2007-04-02', status: 'Married'}]->(robert); // Nowak -> Nowak -> Lewandowska
