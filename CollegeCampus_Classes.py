# Construct a class hierarchy for people on a college campus. Include faculty, staff, and students. What do they have in common? What distinguishes them from one another?

class Upenn(object):
    def __init__(self, name, phone, idnum, position):
        self.name = name
        self.phone = phone
        self.idnum = idnum
        self.position = position

    def getInfo(self):
        return self.name + " is a " + self.position + " at Upenn with ID Number:" + self.idnum + " and can be reached at " + self.phone +"."

class Student(Upenn): 
    def __init__(self, name, phone, idnum, position, major, gradyear):
        Upenn.__init__(self, name, phone, idnum, position)
        self.major = major 
        self.gradyear = gradyear
    def __str__(self):
        return str(Upenn.getInfo(self)) + " She is studying " + self.major + " and will be graduating in " + self.gradyear

def main():
    shilpa = Student("Shilpa", "732-979-7459", "7677", "Student", "Computer Science", "2018")
    print shilpa.__str__()

main()

