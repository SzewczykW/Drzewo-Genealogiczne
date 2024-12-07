MATCH (n) DETACH DELETE n; 

// Validate if Person has no more than 2 parents.
CALL apoc.trigger.add(
  'validateParentLimit',
  '
  MATCH (c:Person)<-[r:PARENT]-()
  WITH c, COUNT(r) AS parentCount
  WHERE parentCount > 2
  CALL apoc.util.validate(true, "Person cannot have more than 2 parents", [])
  RETURN NULL
  ',
  {phase: "before"}
);

// Validate if Person is not a Parent to itself
CALL apoc.trigger.add(
  'validateParentSelfRelationship',
  '
  MATCH (p:Person)-[r:PARENT]->(p)
  CALL apoc.util.validate(true, "A person cannot be their own parent", [])
  RETURN NULL
  ',
  {phase: "before"}
);

// Validate if there is no cyclic Parent relation
CALL apoc.trigger.add(
  'validateParentChildCycle',
  '
  MATCH (child:Person)-[newRel:PARENT]->(parent:Person)
  WHERE EXISTS {
      MATCH path = (parent)-[:PARENT*]->(child)
      RETURN path
  }
  CALL apoc.util.validate(true, "A child cannot be a parent of their own parent", [])
  RETURN NULL
  ',
  {phase: "before"}
);

// Validate if Person is married to no more than 1 Person and also if there is no cyclic
// MARRIED relation
CALL apoc.trigger.add(
  'validateMarriageLimit',
  '
  MATCH (p:Person)-[r:MARRIED]-()
  WHERE r.status = "Married"
  WITH p, COUNT(r) AS marriageCount
  WHERE marriageCount > 1
  CALL apoc.util.validate(true, "Person cannot have more than 1 active marriage", [])
  RETURN NULL
  ',
  {phase: "before"}
);

// Validate if Person is not maried to itself
CALL apoc.trigger.add(
  'validateMarriageSelfRelationship',
  '
  MATCH (p:Person)-[r:MARRIED]->(p)
  CALL apoc.util.validate(true, "A person cannot be married to themselves", [])
  RETURN NULL
  ',
  {phase: "before"}
);

// Validate death_date > birth_date
CALL apoc.trigger.add(
  'validateBirthBeforeDeath',
  '
  MATCH (p:Person)
  WHERE p.death_date IS NOT NULL AND p.birth_date > p.death_date
  CALL apoc.util.validate(true, "Birth date must be earlier than death date", [])
  RETURN NULL
  ',
  {phase: "before"}
);

CREATE CONSTRAINT person_id_unique IF NOT EXISTS
FOR (p:Person)
REQUIRE p.id IS UNIQUE;


CREATE
  // Nodes

  // People
  (helen:Person {id: randomUUID(), first_name: 'Helen', last_name: 'Nowak', gender: 'Female', birth_date: date('1945-05-16'), death_date: date('2010-06-16')}),
  (john:Person {id: randomUUID(), first_name: 'John', last_name: 'Nowak', gender: 'Male', birth_date: date('1950-01-01')}),
  (mary:Person {id: randomUUID(), first_name: 'Mary', last_name: 'Lewandowska', gender: 'Female', birth_date: date('1952-02-02')}),
  (peter:Person {id: randomUUID(), first_name: 'Peter', last_name: 'Lewandowski', gender: 'Male', birth_date: date('1955-03-03')}),
  (susan:Person {id: randomUUID(), first_name: 'Susan', last_name: 'Lewandowska', gender: 'Female', birth_date: date('1980-05-05')}),
  (linda:Person {id: randomUUID(), first_name: 'Linda', last_name: 'Lewandowska', gender: 'Female', birth_date: date('1977-04-04')}),
  (james:Person {id: randomUUID(), first_name: 'James', last_name: 'Lewandowski', gender: 'Male', birth_date: date('1982-06-06')}),
  (robert:Person {id: randomUUID(), first_name: 'Robert', last_name: 'Lewandowski', gender: 'Male', birth_date: date('1985-12-12')}),
  (nancy:Person {id: randomUUID(), first_name: 'Nancy', last_name: 'Nowak-Lewandowska', gender: 'Female', birth_date: date('1987-01-13')}),
  (sophie:Person {id: randomUUID(), first_name: 'Sophie', last_name: 'Lewandowska', gender: 'Female', birth_date: date('2012-10-10')}),
  (paul:Person {id: randomUUID(), first_name: 'Paul', last_name: 'Nowak', gender: 'Male', birth_date: date('2014-07-07')}),
  (alice:Person {id: randomUUID(), first_name: 'Alice', last_name: 'Lewandowska', gender: 'Female', birth_date: date('2015-11-11')}),
 
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
