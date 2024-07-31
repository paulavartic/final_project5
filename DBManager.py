import psycopg2


class DBManager:
    def __init__(self, dbname: str, params):
        self.conn = psycopg2.connect(dbname=dbname, **params)
        self.dbname = dbname

    def get_companies_and_vacancies_count(self):
        """gets full list of companies and vacancies count of each"""
        cur = self.conn.cursor()
        cur.execute("""
            SELECT employers.name, COUNT(vacancies.id)
            FROM employers
            JOIN vacancies ON employers.id = vacancies.company_id
            GROUP BY employers.name;
        """)
        return cur.fetchall()

    def get_all_vacancies(self):
        """gets list of vacancies indicating company name, salary and url"""
        cur = self.conn.cursor()
        cur.execute("""
            SELECT job_title, company_name, salary_from, link_to_vacancy
            FROM vacancies
            JOIN companies ON vacancies.company_id = companies.id
        """)
        return cur.fetchall()

    def get_avg_salary(self):
        """gets average salary for vacancy"""
        cur = self.conn.cursor()
        cur.execute("""
            SELECT AVG(salary_from)
            FROM vacancies
        """)
        return cur.fetchall()

    def get_vacancies_with_higher_salary(self):
        """gets list of vacancies that have the salary higher than average"""
        cur = self.conn.cursor()
        cur.execute("""
               SELECT job_title, salary_from
               FROM vacancies
               GROUP BY vacancies.job_title, vacancies.salary_from 
               HAVING vacancies.salary_from > (SELECT AVG(salary_from) FROM vacancies) 
               ORDER BY salary_from    
                """)
        return cur.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        """gets list of vacancies by keyword"""
        cur = self.conn.cursor()
        q = """SELECT * 
               FROM vacancies
               WHERE LOWER(vacancies.job_title) LIKE %s"""
        cur.execute(q, ('%' + keyword.lower() + '%',))
        return cur.fetchall()
