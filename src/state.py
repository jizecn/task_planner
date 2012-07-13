
class State:
    def __init__(self, subject, predicate, obj):
        self.subject = subject
        self.predicate = predicate
        self.object = obj

    def __str__(self):
        """
        print 'subject is ', self.subject
        print 'predicate is ', self.predicate
        print 'object is ', self.object
        """
        return '[subject: ' + str(self.subject) + ', predicate: ' + str(self.predicate) + ', object: ' + str(self.object) + ']' 

class Action:
    def __init__(self, name, param, preCondition, postCondition):
        self.name = name
        self.param = param
        self.preCondition = preCondition
        self.postCondition = postCondition
        print name + '  ' + param
        print preCondition
        print postCondition

    def __str__(self):
        return self.name + ' ' + self.param + '  ' + str(self.preCondition) + ' ' + str(self.postCondition)

class WorldState:
    def __init__(self):
        """
        a collection of states
        """
        self.states = []
        
    def addState(self, state):
        self.states.append(state)

    def __str__(self):
        ret = ''
        for s in self.states:
            #print self.states[1]
            ret = ret + str(s) + '\n'
        return ret

class ActionDict:
    def __init__(self):
        """
        collection of actions
        """
        self.actionDict = []

    def addAction(self, action):
        self.actionDict.append(action)

    def __str__(self):
        ret = ''
        for a in self.actionDict:
            ret = ret + str(a) + '\n'
        return ret

def test_state():
    state = State("Robot", "At", "Kitchen")
    state = State("Robot", "At", [10,20,30])

def test_action():
    preCond = State("Robot", "At", "Kitchen")
    #print 'preCondition is ', preCond
    postCond = State("Robot", "At", "LivingRoom")
    #print 'postCondition is ', postCond
    act = Action('move', 'LivingRoom', preCond, postCond)

def test_world_state():
    world = WorldState()

    state = State("Robot", "At", "Kitchen")
    world.addState(state)

    state = State("Robot", "At", [10,20,30])
    world.addState(state)
    print 'world: \n', world

def test_action_dict():
    actDict = ActionDict()
    
    preCond = State("Robot", "At", "Kitchen")
    #print 'preCondition is ', preCond
    postCond = State("Robot", "At", "LivingRoom")
    #print 'postCondition is ', postCond
    act = Action('move', 'LivingRoom', preCond, postCond)
    actDict.addAction(act)
    
    preCond = State("Robot", "At", "Kitchen")
    #print 'preCondition is ', preCond
    postCond = State("Robot", "At", "LivingRoom")
    #print 'postCondition is ', postCond
    act = Action('move', 'LivingRoom', preCond, postCond)
    actDict.addAction(act)

    print actDict
    
if __name__ == "__main__":
    test_action()
    test_state()
    test_world_state()
    test_action_dict()
