CREATE TABLE machine (
        machine_id INTEGER NOT NULL, 
        serial_no VARCHAR NOT NULL, 
        site VARCHAR NOT NULL, 
        installed DATE NOT NULL, 
        PRIMARY KEY (machine_id), 
        CONSTRAINT uq_machine_serial UNIQUE (serial_no)
) ;

CREATE TABLE part (
        part_no VARCHAR NOT NULL, 
        description VARCHAR NOT NULL, 
        unit_price NUMERIC(9, 2) NOT NULL, 
        PRIMARY KEY (part_no)
) ;

CREATE TABLE maint_job (
        job_id INTEGER NOT NULL, 
        machine_id INTEGER NOT NULL, 
        technician VARCHAR NOT NULL, 
        done_on DATE NOT NULL, 
        PRIMARY KEY (job_id), 
        FOREIGN KEY(machine_id) REFERENCES machine (machine_id)
) ;

CREATE TABLE job_part (
        job_id INTEGER NOT NULL, 
        part_no VARCHAR NOT NULL, 
        PRIMARY KEY (job_id, part_no), 
        FOREIGN KEY(job_id) REFERENCES maint_job (job_id), 
        FOREIGN KEY(part_no) REFERENCES part (part_no)
) ;

- -**Python model rule:** A maintenance job’s date must be valid and cannot be in the future. This belongs in the Python model because it is a rule about whether the entered information makes sense for this course's maintenance records.
- -**Database rule:** Every maint_job must reference an existing machine, enforced with a foreign key. This belongs in the database because the database can protect that relationship for every insert or update, even if the data is added through a different program.