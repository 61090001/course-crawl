from abc import ABCMeta, abstractmethod, abstractstaticmethod
from bs4 import BeautifulSoup
import logger
import re

from .course import Course
from .professor import Professor

log = logger.get_logger(__name__)

class Parser(metaclass=ABCMeta):

    def __init__(self, html, pool=None):
        self.html = html
        self.pool = pool
        if not self.pool:
            self.pool = dict()
    
    @abstractmethod
    def get_follow_links(self):
        pass

    @abstractstaticmethod
    def get_professor_name(soup):
        pass

    @abstractstaticmethod
    def get_courses(soup, pool=None):
        pass

    @abstractmethod
    def extract(self):
        pass

class ICKMITLParser(Parser):

    def __init__(self, html, pool=None):
        super().__init__(html, pool)
    
    def get_follow_links(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        lecturers = soup.find(id='tab-lecturers')
        if not lecturers:
            return []
        links = [
            link.get('href') for link in lecturers.find_all('a')
        ]

        return links
    
    @staticmethod
    def get_professor_name(soup):
        header = soup.find('span', {'itemprop':'name'})
        if header is None:
            return None
        if not header.string:
            return header.string
        return header.string.strip()
    
    @staticmethod
    def get_courses(soup, pool=None):
        list_courses = []

        try:
            professor = ICKMITLParser.get_professor_name(soup)
            if professor:
                if not pool:
                    professor = Professor(professor)
                else:
                    if not (professor.lower() in pool):
                        pool[professor.lower()] = Professor(professor)
                    professor = self.pool[professor.lower()]

            courses = soup.find('div', {'id':'tab-courses'})
            if courses is None:
                return list_courses
            courses = courses.find('div', 'accordion')
            if courses is None:
                return list_courses
            
            for course in courses.find_all('div', 'accordion-group'):
                header = course.next
                courseName = header.next.string

                content = course.find('div', 'accordion-inner')
                courseID = content.next.next.next

                list_courses.append(Course(courseid=courseID, coursename=courseName, professor=professor))
            
            return list_courses
        except Exception as e:
            log.error(f"Error: {str(e)}")
        finally:
            return list_courses
    
    def extract(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        courses = ICKMITLParser.get_courses(soup, self.pool)
        for course in courses:
            log.debug(course)
        
        return courses

class MITParser(Parser):

    def __init__(self, html, pool=None):
        super().__init__(html, pool)
    
    def get_follow_links(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        sitemap = soup.find('div', class_='sitemap')
        if not sitemap:
            return []
        links = [
            link.get('href') for link in sitemap.find_all('a')
        ]

        return links
    
    @staticmethod
    def get_professor_name(soup):
        instructorsblock = soup.find('p', class_='courseblockinstructors')
        if instructorsblock is None:
            return None
        if not instructorsblock.string:
            return instructorsblock.string
        return instructorsblock.string.strip()
    
    @staticmethod
    def get_courses(soup, pool=None):
        list_courses = []

        try:
            courses = soup.find_all('div', 'courseblock')
            for course in courses:
                courseid = None
                coursename = None
                professors = []
                titleblock = course.find('h4', class_='courseblocktitle')
                if not titleblock:
                    continue
                titleblock = titleblock.strong.string.split(' ')
                courseid = titleblock[0]
                coursename = ' '.join(titleblock[1:])
                instructors = MITParser.get_professor_name(course)
                if not instructors:
                    continue
                instructors = instructors.split(', ')
                for instructor in instructors:
                    if not pool:
                        professors.append(Professor(instructor))
                    else:
                        if not (instructor.lower() in pool):
                            pool[instructor.lower()] = Professor(instructor)
                        professors.append(self.pool[instructor.lower()])

                list_courses.append(Course(courseid=courseid, coursename=coursename, professors=professors))
        except Exception as e:
            log.error(f"Error: {str(e)}")
        finally:
            return list_courses
    
    def extract(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        courses = MITParser.get_courses(soup, self.pool)
        for course in courses:
            log.debug(course)
        
        return courses

class UCBerkeleyParser(Parser):

    def __init__(self, html, pool=None):
        super().__init__(html, pool)
    
    def get_follow_links(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        sitemap = soup.find('div', id='atozindex')
        if not sitemap:
            return []
        links = [
            link.get('href') for list in sitemap.find_all('li') for link in list.find_all('a')
        ]

        return links
    
    @staticmethod
    def get_professor_name(soup):
        instructorsblock = soup.find('strong', text=re.compile('Instructor:|Instructors:'))
        if instructorsblock is None:
            return None
        if len(instructorsblock.parent.contents) < 2:
            return None
        if not instructorsblock.parent.contents[1].string:
            return instructorsblock.parent.contents[1].string
        return instructorsblock.parent.contents[1].string.strip()
    
    @staticmethod
    def get_courses(soup, pool=None):
        list_courses = []

        try:
            courses = soup.find_all('div', 'courseblock')
            for course in courses:
                courseid = None
                coursename = None
                professors = []
                code = course.find('span', 'code')
                if not code:
                    continue
                courseid = code.string
                coursename = course.find('span', 'title')
                if not coursename:
                    continue
                coursename = coursename.string
                instructors = UCBerkeleyParser.get_professor_name(course)
                if not instructors:
                    continue
                instructors = instructors.split(', ')
                for instructor in instructors:
                    if not pool:
                        professors.append(Professor(instructor))
                    else:
                        if not (instructor.lower() in pool):
                            pool[instructor.lower()] = Professor(instructor)
                        professors.append(self.pool[instructor.lower()])
                
                list_courses.append(Course(courseid=courseid, coursename=coursename, professors=professors))
        except Exception as e:
            log.error(f"Error: {str(e)}")
        finally:
            return list_courses
    
    def extract(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        courses = UCBerkeleyParser.get_courses(soup, self.pool)
        for course in courses:
            log.debug(course)
        
        return courses
