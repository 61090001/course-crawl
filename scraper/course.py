import logger

log = logger.get_logger(__name__)

class Course:
    def __init__(self, courseid=None, coursename=None, professor=None, professors=None):
        self.courseid = courseid
        self.coursename = coursename
        self.professors = professors
        if not professors:
            self.professors = []
        if professor:
            self.professors.append(professor)
    
    def setCourseId(self, courseid):
        self.courseid = courseid
    
    def getCourseId(self):
        return self.courseid
    
    def setCourseName(self, coursename):
        self.coursename = coursename
    
    def getCourseName(self):
        return self.coursename
    
    def addProfessor(self, professor):
        self.professors.append(professor)
    
    def setProfessors(self, professors):
        self.professors = professors
    
    def getProfessors(self):
        return self.professors
    
    def __str__(self):
        return f'{", ".join(str(professor) for professor in self.professors)} {self.courseid} {self.coursename}'
