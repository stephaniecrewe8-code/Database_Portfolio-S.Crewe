# Module 2 Study Log

## 1) References used
- Source: Adrienne Watt, 'https://opentextbc.ca/dbdesign01/chapter/chapter-8-entity-relationship-model/'
- Concept I understood best: Entities have attributes, and relationships connect entities. An associative entity can represent a many-to-many relationship that has its own details.

- Source: Adrienne Watt and Nelson Eng, 'https://opentextbc.ca/dbdesign01/chapter/chapter-4-types-of-data-models/'
- Concept I understood best: An employee can be modeled as an entity with attributes such as name and address; “works on” relates employees to projects.

- Source: William E. Burrows, 'https://faculty.washington.edu/burrows/IS579/dataModelingGuide.pdf'
- Concept I understood best: A student’s grade belongs to the particular Student–Course pairing, so it fits in an associative entity such as Enrollment.

- Source: Harvard CS50, 'https://cs50.harvard.edu/extension/sql/2024/spring/notes/1/'
- Concept I understood best: Crow’s-foot marks show how many related records are allowed, including optional participation.

## 2) Things I googled
ER models show entities, their attributes, and relationships. Source: https://opentextbc.ca/dbdesign01/chapter/chapter-8-entity-relationship-model/

crow’s foot ER diagram optional many notation. the circle means zero/optional, the bar means one, and the fork means many. Source: https://cs50.harvard.edu/extension/sql/2024/spring/notes/1/

## 3) Remarkable things
- A machine name is not a reliable substitute for a foreign key because names can change and may not be unique.
- An ER diagram communicates the intended model, but the database schema and actual data must be inspected to determine whether the intended rules are enforced.
- "Exactly four wheels" cannot be drawn. Mermaid's cardinality markers stop at zero, one and many.

## 4) LLM Q&A
### What is an ER model?
- Prompt:"I am a student in a third-semester database class. Explain briefly what entity–relationship models are, with simple examples. Highlight the main concepts and explain how I can teach them to a peer."
- Summary of answer: An ER model describes the data a system needs to store. Entities represent things such as machines, parts, and technicians; attributes describe those things; relationships describe how they are associated. Cardinality specifies how many instances can participate in each relationship.
- How I verified it: Compared the explanation with the ER model reference and its definitions of entities, attributes, relationships, and cardinalities.


### How can an undocumented schema be reconstructed?
- Prompt: "Here is a legacy schema. What entities, attributes, and relationships does it intend? What cardinalities are hidden in it, and how would I prove each with a COUNT query?"
- Summary of answer: The tables and their columns provide clues about the intended entities and attributes. Primary keys and foreign keys indicate identifiers and declared relationships, while repeated values and data patterns can reveal likely cardinalities. Queries such as COUNT(*) and COUNT(DISTINCT column) can help test these assumptions.
- How I verified it: The proposed model must be compared with the actual table definitions and query results. Data patterns alone cannot prove every business rule or guarantee that a relationship is enforced.


###  What is the difference between natural and surrogate keys?
- Prompt: "Explain the difference between a natural key and a surrogate key, and give a real scenario where choosing the wrong one causes a data bug."
- Summary of answer: A natural key comes from meaningful business data, while a surrogate key is generated specifically to identify a record. A machine's serial number can be a natural key, while machine_id can be a surrogate key. A surrogate key avoids depending on a potentially changeable business identifier, but the natural key may still need a uniqueness constraint.
- How I verified it: Compared the definitions with database key concepts. The appropriate key choice depends on business rules, identifier stability, and uniqueness requirements.


### Why does a comma-separated list violate first normal form?
- Prompt: "A column holds a comma-separated list: parts_used = 'P-1001,P-1002'. Why is this problematic, and what would the corrected schema look like?"
- Summary of answer: Multiple part numbers are stored in one field instead of being represented as separate associations. This makes filtering, joining, counting, and enforcing references to individual parts more complicated. A junction table such as job_part(job_id, part_no) represents each job–part association as a separate row.
- How I verified it: Checked the explanation against first normal form and relational modeling concepts. The proposed junction table also needs foreign keys and an appropriate key to prevent duplicate associations.


### What does Crow's-foot notation mean?
- Prompt: "Explain Crow's-foot notation for 1:1, 1:n, and m:n relationships."
- Summary of answer: Crow's-foot notation represents the multiplicity of relationships. A single line denotes one, while a crow's-foot symbol denotes many. Optionality symbols indicate whether participation is optional or mandatory. A machine with many maintenance jobs is a one-to-many example; jobs and parts form a many-to-many relationship if each job can use multiple parts and each part can be used in multiple jobs.
- How I verified it: Compared the examples with ER diagram notation. Exact optionality must be determined from business requirements and constraints.


### What can missing foreign keys cause?
- Prompt: "Give three realistic problems caused by missing foreign keys or orphan rows."
- Summary of answer: An orphan maintenance job may reference a machine that does not exist. An order may reference a nonexistent customer, making reporting unreliable. A maintenance record may refer to a part that has been deleted, making historical usage difficult to interpret.
- How I verified it: These are plausible failure scenarios. In the maintenance database, the orphan-job example can be verified directly by joining maint_job to machine and selecting rows without a matching machine.


## 5) My two best ER sketches
### ER sketch 1
- Source: Wikipedia, https://en.wikipedia.org/wiki/Entity%E2%80%93relationship_model, crow's foot notation section.
 Drawn figure is under my partner's portfolio, https://github.com/MichaelKonsduAmpadu/michael-sql.portfolio/tree/main
- What I learned: In crow's foot notation a relationship cannot carry attributes. "An artist performs a song" needs a date and a venue, so the relationship becomes its own entity, PERFORMANCE. This is the same move as turning the maintenance job into an entity in Task B. The article also shows how to read each end: the inner symbol is the minimum and the outer symbol is the maximum.

### ER sketch 2
- Source: HCL Informix documentation, https://help.hcl-software.com/hclinformix/15.0/ddi/ids_ddi_069.html, symbols of an Entity-Relationship diagram.
  Drawn figure is under my partner's portfolio, https://github.com/MichaelKonsduAmpadu/michael-sql.portfolio/tree/main
- What I learned: Optionality is a separate symbol from cardinality. A circle (zero allowed) and a bar (exactly one) are drawn independently of the crow's foot, and each symbol sits next to the entity it describes. So ||--o{ reads in two halves: exactly one customer per order, zero or more orders per customer. A customer with no orders is legal; an order with no customer is not.

## 6) Agreed learning (pod discussion)
- 
- 
- 
- 
