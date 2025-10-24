"""
Neo4j service for organizational hierarchy
"""

from neo4j import GraphDatabase
from django.conf import settings


class OrgChartService:
    """
    Service to manage organizational hierarchy in Neo4j
    """
    
    def __init__(self):
        neo4j_settings = settings.NEO4J_SETTINGS
        self.driver = GraphDatabase.driver(
            neo4j_settings['uri'],
            auth=(neo4j_settings['user'], neo4j_settings['password'])
        )
    
    def close(self):
        """Close Neo4j connection"""
        self.driver.close()
    
    def create_employee_node(self, employee_id, name, job_title):
        """Create employee node in Neo4j"""
        with self.driver.session() as session:
            session.execute_write(
                self._create_employee_node,
                employee_id, name, job_title
            )
    
    @staticmethod
    def _create_employee_node(tx, employee_id, name, job_title):
        query = """
        MERGE (e:Employee {employee_id: $employee_id})
        SET e.name = $name, e.job_title = $job_title
        RETURN e
        """
        tx.run(query, employee_id=employee_id, name=name, job_title=job_title)
    
    def create_reports_to_relationship(self, employee_id, manager_id):
        """Create REPORTS_TO relationship"""
        with self.driver.session() as session:
            session.execute_write(
                self._create_reports_to,
                employee_id, manager_id
            )
    
    @staticmethod
    def _create_reports_to(tx, employee_id, manager_id):
        query = """
        MATCH (e:Employee {employee_id: $employee_id})
        MATCH (m:Employee {employee_id: $manager_id})
        MERGE (e)-[:REPORTS_TO]->(m)
        """
        tx.run(query, employee_id=employee_id, manager_id=manager_id)
    
    def get_org_chart(self, root_employee_id=None):
        """Get organizational chart starting from root"""
        with self.driver.session() as session:
            if root_employee_id:
                return session.execute_read(
                    self._get_org_chart_from_employee,
                    root_employee_id
                )
            else:
                return session.execute_read(self._get_full_org_chart)
    
    @staticmethod
    def _get_org_chart_from_employee(tx, employee_id):
        query = """
        MATCH path = (root:Employee {employee_id: $employee_id})<-[:REPORTS_TO*0..]-(subordinate)
        RETURN subordinate, path
        ORDER BY length(path)
        """
        result = tx.run(query, employee_id=employee_id)
        return [record for record in result]
    
    @staticmethod
    def _get_full_org_chart(tx):
        query = """
        MATCH (e:Employee)
        OPTIONAL MATCH (e)-[:REPORTS_TO]->(m:Employee)
        RETURN e, m
        """
        result = tx.run(query)
        return [record for record in result]
    
    def get_direct_reports(self, employee_id):
        """Get direct reports for an employee"""
        with self.driver.session() as session:
            return session.execute_read(
                self._get_direct_reports,
                employee_id
            )
    
    @staticmethod
    def _get_direct_reports(tx, employee_id):
        query = """
        MATCH (e:Employee {employee_id: $employee_id})<-[:REPORTS_TO]-(subordinate)
        RETURN subordinate
        """
        result = tx.run(query, employee_id=employee_id)
        return [record['subordinate'] for record in result]
    
    def delete_employee_node(self, employee_id):
        """Delete employee node and relationships"""
        with self.driver.session() as session:
            session.execute_write(
                self._delete_employee_node,
                employee_id
            )
    
    @staticmethod
    def _delete_employee_node(tx, employee_id):
        query = """
        MATCH (e:Employee {employee_id: $employee_id})
        DETACH DELETE e
        """
        tx.run(query, employee_id=employee_id)


# Singleton instance
_org_chart_service = None


def get_org_chart_service():
    """Get or create org chart service instance"""
    global _org_chart_service
    if _org_chart_service is None:
        _org_chart_service = OrgChartService()
    return _org_chart_service
