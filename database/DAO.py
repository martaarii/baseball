from database.DB_connect import DBConnect
from model.team import Team

class DAO():
    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()
        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct(YEAR) from teams t
                    where `year`  >= 1980
                    order by `year` desc"""

        cursor.execute(query)

        for row in cursor:
            result.append(row["YEAR"])

        cursor.close()
        conn.close()
        return result
    @staticmethod
    def getTeamsYear(year):
        conn = DBConnect.get_connection()
        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select * from teams t 
                    where t.`year` = %s"""

        cursor.execute(query, (year,))

        for row in cursor:
            result.append(Team(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getSalaryOfTeams(year, idMap):
        conn = DBConnect.get_connection()
        result = {}

        cursor = conn.cursor(dictionary=True)
        query = """select t.teamCode , t.ID, sum(s.salary) as totSalary
                from salaries s , teams t, appearances a 
                where s.`year` = t.`year` and t.`year`  = a.`year` 
                and a.`year` = %s
                and t.ID = a.teamID 
                and s.playerID = a.playerID 
                group by t.teamCode"""

        cursor.execute(query, (year,))

        for row in cursor:
            # result.append(idMap[row["ID"]], row["totSalary"]))
            result[idMap[row["ID"]]] = row["totSalary"]

        cursor.close()
        conn.close()
        return result
