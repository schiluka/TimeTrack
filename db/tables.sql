mysql -u root -p
create user 'test'@'localhost' identified by 'test';
GRANT ALL PRIVILEGES ON *.* TO 'test'@'localhost' WITH GRANT OPTION;
mysql -u test -p test
use tt;

CREATE TABLE EMPLOYEE
( 	emp_id INT(8) NOT NULL AUTO_INCREMENT PRIMARY KEY,
	  emp_email VARCHAR(100) NOT NULL,
	  emp_pswd VARCHAR(250),
  	fst_nam VARCHAR(100) NOT NULL,
  	lst_nam VARCHAR(100) NOT NULL,
  	emp_typ VARCHAR(10),	-- EMP/MGR
  	ts_typ VARCHAR(10),		-- Weekly, Monthly, BiMonthly
  	clnt_id VARCHAR(10),
  	clnt_nam VARCHAR(100),
  	emp_sta VARCHAR(10),	-- ACTIVE, DELETED
  	proj_sta VARCHAR(10),	-- IN/OUT
  	visa_typ VARCHAR(20),	-- OPT/H1/L1/EAD/GC/Citizen
  	visa_sta_dt DATE,
  	visa_end_dt DATE,
  	UNIQUE (emp_email)
);

ALTER TABLE EMPLOYEE
  CHANGE COLUMN `emp_id` `emp_id` INT(8) NOT NULL AUTO_INCREMENT,
  DROP PRIMARY KEY,
  ADD PRIMARY KEY (`emp_id`);

ALTER TABLE EMPLOYEE AUTO_INCREMENT = 12000;

CREATE TABLE TIMESHEET
(   ts_id INT(10) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    emp_id INT(8) NOT NULL,
    fst_nam VARCHAR(100) NOT NULL,
    lst_nam VARCHAR(100) NOT NULL,
    ts_typ VARCHAR(10),   -- Weekly, Monthly, BiMonthly
    appr_id INT(8),
    clnt_id VARCHAR(10),
    clnt_nam VARCHAR(100),
    ts_sta VARCHAR(10),  -- Submitted, Approved, Rejected, Deleted
    wrk_hrs VARCHAR(150),
    total_hrs INT(4),
    start_dt DATE,
    end_dt DATE,
    sub_dt DATE,
    appr_dt DATE,
    UNIQUE(emp_id,start_dt,end_dt)
);

ALTER TABLE TIMESHEET
  CHANGE COLUMN `ts_id` `ts_id` INT(10) NOT NULL AUTO_INCREMENT,
  DROP PRIMARY KEY,
  ADD PRIMARY KEY (`ts_id`);

ALTER TABLE TIMESHEET AUTO_INCREMENT = 100000;

ALTER TABLE tablename MODIFY columnname INTEGER;

INSERT INTO TIMESHEET (`emp_id`, `fst_nam`, `lst_nam`, `ts_typ`, `appr_id`, `clnt_id`, `clnt_nam`, `ts_sta`, `wrk_hrs`, `total_hrs`, `start_dt`, `end_dt`, `sub_dt`, `appr_dt`)
VALUES
  (120011, 'san1wer', 'san1ewr', 'Weekly', 120002, '10001', 'Clients', 'Submitted', '0,8,8,8,8,8,0', 40, '2016-06-07', '2016-06-14', '2016-07-14', NULL),
  (120012, 'san2666', 'san2', 'Weekly', 120002, '10034', 'Client1', 'Submitted', '0,8,8,8,8,8,0', 40, '2016-06-07', '2016-06-14', '2016-07-14', NULL),
  (120013, 'san36', 'san3dfg', 'Weekly', 120002, '10002', 'Client2', 'Submitted', '0,8,8,8,8,8,0', 40, '2016-06-07', '2016-06-14', '2016-07-14', NULL),
  (120014, 'san45fdg', 'san4', 'Weekly', 120002, '10234', 'Client2', 'Approved', '0,8,8,8,8,8,0', 40, '2016-06-07', '2016-06-14', '2016-07-14', NULL),
  (120015, 'san44', 'san5', 'Weekly', 120002, '10002', 'Client2', 'Approved', '0,8,8,8,8,8,0', 40, '2016-06-07', '2016-06-14', '2016-07-14', NULL),
  (120016, 'san63', 'san6dfg', 'Weekly', 120002, '10002', 'Client2', 'Approved', '0,8,8,8,8,8,0', 40, '2016-06-07', '2016-06-14', '2016-07-14', NULL);

INSERT INTO EMPLOYEE (`emp_email`, `emp_pswd`, `fst_nam`, `lst_nam`, `emp_typ`, `ts_typ`, `clnt_id`, `clnt_nam`, `emp_sta`, `proj_sta`, `visa_typ`, `visa_sta_dt`, `visa_end_dt`)
VALUES
  ('san2@san2.com', 'pbkdf2:sha1:1000$0H09oMb1$30afb473c25d939c21f7d35ce375768cb92d705a', 'san2', 'san2', 'Employee', 'Weekly', '1001', 'clien1', 'active', 'in', 'Citizen', NULL, NULL),
  ('san@san.com', 'pbkdf2:sha1:1000$0H09oMb1$30afb473c25d939c21f7d35ce375768cb92d705a', 'san', 'san', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
  ('san4@san4.com', 'pbkdf2:sha1:1000$0H09oMb1$30afb473c25d939c21f7d35ce375768cb92d705a', 'san4', 'san4', 'Employee', 'Weekly', '1001', 'clien1', 'active', 'in', 'Citizen', NULL, NULL),
  ('san5@san5.com', 'pbkdf2:sha1:1000$0H09oMb1$30afb473c25d939c21f7d35ce375768cb92d705a', 'san5', 'san5', 'Employee', 'Weekly', '1001', 'clien1', 'active', 'in', 'Citizen', NULL, NULL),
  ('san6@san6.com', 'pbkdf2:sha1:1000$0H09oMb1$30afb473c25d939c21f7d35ce375768cb92d705a', 'san6', 'san6', 'Employee', 'Weekly', '1001', 'clien1', 'active', 'in', 'Citizen', NULL, NULL),
  ('san7@san7.com', 'pbkdf2:sha1:1000$0H09oMb1$30afb473c25d939c21f7d35ce375768cb92d705a', 'san7', 'san7', 'Employee', 'Weekly', '1001', 'clien1', 'active', 'in', 'Citizen', NULL, NULL),
  ('san8@san8.com', 'pbkdf2:sha1:1000$0H09oMb1$30afb473c25d939c21f7d35ce375768cb92d705a', 'san8', 'san8', 'Employee', 'Weekly', '1001', 'clien1', 'active', 'in', 'Citizen', NULL, NULL);



CREATE TABLE CLIENT
(   clnt_id INT(8) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    clnt_nam VARCHAR(200) NOT NULL,
    clnt_addr VARCHAR(200) NOT NULL,
    clnt_cty VARCHAR(50) NOT NULL,
    clnt_ste VARCHAR(50) NOT NULL,
    clnt_zip VARCHAR(20) NOT NULL,
    UNIQUE (clnt_nam)
);

ALTER TABLE CLIENT AUTO_INCREMENT = 90000;

