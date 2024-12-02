// Delete all existing data
MATCH (n) DETACH DELETE n;

// Create constraints for unique identifiers
CREATE CONSTRAINT person_id_unique IF NOT EXISTS ON (p:Person) ASSERT p.id IS UNIQUE;

// Create example data

// Grandparents generation
CREATE (p1:Person {
    id: '1',
    first_name: 'Stanisław',
    last_name: 'Nowak',
    gender: 'Male',
    birth_data: date('1940-01-01'),
    death_data: date('2000-01-01')
});

CREATE (p2:Person {
    id: '2',
    first_name: 'Helena',
    last_name: 'Nowak',
    gender: 'Female',
    birth_data: date('1942-02-02')
});

CREATE (p3:Person {
    id: '3',
    first_name: 'Jan',
    last_name: 'Kowalski',
    gender: 'Male',
    birth_data: date('1938-03-03'),
    death_data: date('1998-04-04')
});

CREATE (p4:Person {
    id: '4',
    first_name: 'Maria',
    last_name: 'Kowalska',
    gender: 'Female',
    birth_data: date('1940-05-05')
});

// Parents generation
CREATE (p5:Person {
    id: '5',
    first_name: 'Andrzej',
    last_name: 'Nowak',
    gender: 'Male',
    birth_data: date('1965-05-05')
});

CREATE (p6:Person {
    id: '6',
    first_name: 'Anna',
    last_name: 'Nowak',
    gender: 'Female',
    birth_data: date('1967-06-06')
});

CREATE (p7:Person {
    id: '7',
    first_name: 'Piotr',
    last_name: 'Kowalski',
    gender: 'Male',
    birth_data: date('1968-07-07')
});

CREATE (p8:Person {
    id: '8',
    first_name: 'Ewa',
    last_name: 'Kowalska',
    gender: 'Female',
    birth_data: date('1970-08-08')
});

// Children generation
CREATE (p9:Person {
    id: '9',
    first_name: 'Tomasz',
    last_name: 'Nowak',
    gender: 'Male',
    birth_data: date('1990-09-09')
});

CREATE (p10:Person {
    id: '10',
    first_name: 'Katarzyna',
    last_name: 'Nowak',
    gender: 'Female',
    birth_data: date('1992-10-10')
});

CREATE (p11:Person {
    id: '11',
    first_name: 'Marek',
    last_name: 'Kowalski',
    gender: 'Male',
    birth_data: date('1991-11-11')
});

CREATE (p12:Person {
    id: '12',
    first_name: 'Agnieszka',
    last_name: 'Kowalska',
    gender: 'Female',
    birth_data: date('1993-12-12')
});

// Grandchildren generation
CREATE (p13:Person {
    id: '13',
    first_name: 'Paweł',
    last_name: 'Nowak',
    gender: 'Male',
    birth_data: date('2015-01-13')
});

CREATE (p14:Person {
    id: '14',
    first_name: 'Zofia',
    last_name: 'Nowak',
    gender: 'Female',
    birth_data: date('2017-02-14')
});

CREATE (p15:Person {
    id: '15',
    first_name: 'Krystian',
    last_name: 'Kowalski',
    gender: 'Male',
    birth_data: date('2018-03-15')
});

CREATE (p16:Person {
    id: '16',
    first_name: 'Magdalena',
    last_name: 'Kowalska',
    gender: 'Female',
    birth_data: date('2020-04-16')
});

// Create parent-child relationships

// Stanisław and Helena are parents of Andrzej and Anna
CREATE (p1)-[:PARENT]->(p5);
CREATE (p2)-[:PARENT]->(p5);

CREATE (p1)-[:PARENT]->(p6);
CREATE (p2)-[:PARENT]->(p6);

// Jan and Maria are parents of Piotr and Ewa
CREATE (p3)-[:PARENT]->(p7);
CREATE (p4)-[:PARENT]->(p7);

CREATE (p3)-[:PARENT]->(p8);
CREATE (p4)-[:PARENT]->(p8);

// Andrzej and Anna are parents of Tomasz and Katarzyna
CREATE (p5)-[:PARENT]->(p9);
CREATE (p6)-[:PARENT]->(p9);

CREATE (p5)-[:PARENT]->(p10);
CREATE (p6)-[:PARENT]->(p10);

// Piotr and Ewa are parents of Marek and Agnieszka
CREATE (p7)-[:PARENT]->(p11);
CREATE (p8)-[:PARENT]->(p11);

CREATE (p7)-[:PARENT]->(p12);
CREATE (p8)-[:PARENT]->(p12);

// Tomasz and Agnieszka are parents of Paweł and Zofia
CREATE (p9)-[:PARENT]->(p13);
CREATE (p12)-[:PARENT]->(p13);

CREATE (p9)-[:PARENT]->(p14);
CREATE (p12)-[:PARENT]->(p14);

// Marek and Katarzyna are parents of Krystian and Magdalena
CREATE (p11)-[:PARENT]->(p15);
CREATE (p10)-[:PARENT]->(p15);

CREATE (p11)-[:PARENT]->(p16);
CREATE (p10)-[:PARENT]->(p16);

// Create marriage relationships

// Stanisław and Helena
CREATE (p1)-[:MARRIED {since: '1960-05-15', status: 'ended'}]->(p2);
CREATE (p2)-[:MARRIED {since: '1960-05-15', status: 'ended'}]->(p1);

// Andrzej and Anna
CREATE (p5)-[:MARRIED {since: '1985-07-20', status: 'current'}]->(p6);
CREATE (p6)-[:MARRIED {since: '1985-07-20', status: 'current'}]->(p5);

// Piotr and Ewa
CREATE (p7)-[:MARRIED {since: '1990-08-25', status: 'current'}]->(p8);
CREATE (p8)-[:MARRIED {since: '1990-08-25', status: 'current'}]->(p7);

// Tomasz and Agnieszka
CREATE (p9)-[:MARRIED {since: '2012-09-01', status: 'current'}]->(p12);
CREATE (p12)-[:MARRIED {since: '2012-09-01', status: 'current'}]->(p9);

// Marek and Katarzyna
CREATE (p11)-[:MARRIED {since: '2015-10-10', status: 'current'}]->(p10);
CREATE (p10)-[:MARRIED {since: '2015-10-10', status: 'current'}]->(p11);

// Create sibling relationships

// Andrzej and Anna are siblings
CREATE (p5)-[:SIBLING]->(p6);
CREATE (p6)-[:SIBLING]->(p5);

// Piotr and Ewa are siblings
CREATE (p7)-[:SIBLING]->(p8);
CREATE (p8)-[:SIBLING]->(p7);

// Tomasz and Katarzyna are siblings
CREATE (p9)-[:SIBLING]->(p10);
CREATE (p10)-[:SIBLING]->(p9);

// Marek and Agnieszka are siblings
CREATE (p11)-[:SIBLING]->(p12);
CREATE (p12)-[:SIBLING]->(p11);

// Paweł and Zofia are siblings
CREATE (p13)-[:SIBLING]->(p14);
CREATE (p14)-[:SIBLING]->(p13);

// Krystian and Magdalena are siblings
CREATE (p15)-[:SIBLING]->(p16);
CREATE (p16)-[:SIBLING]->(p15);
