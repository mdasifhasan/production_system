# This will store all the rules
class LongTermMemory:
    def __init__(self):
        print ("constructing long term memory")
        self.rules = []
        self.dictConditionToRules = {}

    def addRule(self, rule):
        self.rules.append(rule)
        # map condition type to list of related rules

        for type in rule.conditions:
            if type not in self.dictConditionToRules:
                ca = [rule]
                self.dictConditionToRules[type] = ca
            else:
                self.dictConditionToRules[type].append(rule)

    def process(self, stm):
        print("processing long term memory")
        i = 0
        while True:
            count = 0
            for r in self.rules:
                i += 1
                count += r.process(stm)
            if count == 0:
                break
        print("Number of rules processed:", i)
# This class will keep current conditions that are true
# It will keep the conditions sorted by condition type in a dictionary
# the dictionary format: conditions = <condition_type, conditions[]>
class ShortTermMemory:
    def __init__(self):
        print ("constructing short term memory")
        self.conditions = {}
        self.dictConditions = {}
        self.dictConditionsByVars = {}
        self.dictConditionsByIndVar = {}

    def addCondition(self, condition):
        if self.isConditionExists(condition):
            #print("condition exists:",condition)
            return False

        # map condition type to list of conditions of that type
        if condition.type not in self.conditions:
            ca = [condition]
            self.conditions[condition.type] = ca
        else:
            self.conditions[condition.type].append(condition)

        self.dictConditions[self.getKeyForCondition(condition)] = condition

        # map variable list to list of related conditions
        kv = self.getKeyForConditionByVars(condition)
        if kv not in self.dictConditionsByVars:
            ca = [condition]
            self.dictConditionsByVars[kv] = ca
        else:
            self.dictConditionsByVars[kv].append(condition)

        # map individual var to list of related conditions
        for kv in condition.variableList:
            if kv not in self.dictConditionsByIndVar:
                ca = [condition]
                self.dictConditionsByIndVar[kv] = ca
            else:
                self.dictConditionsByIndVar[kv].append(condition)

        return True

    def getKeyForCondition(self, condition):
        key = condition.type
        for v in condition.variableList:
            key = key + "_" + v
        return key


    def getKeyForConditionByVars(self, condition):
        key = ""
        for v in condition.variableList:
            key = key + "_" + v
        return key

    def isConditionExists(self, condition):
        key = condition.type
        for v in condition.variableList:
            key = key + "_" + v

        if key in self.dictConditions:
            return True
        return False

    def printConditions(self):
        print("current conditions:")
        for type in self.conditions:
            for c in self.conditions[type]:
                print(c)


# Each instance of this class will represent a type of condition
# for example, x -> left of -> y, here left of is a type of condition
class Condition:
    def __init__(self, type, variableList):
        self.type = type
        self.variableList = variableList

        #print("constructing condition:", self)

    def getVariables(self):
        return self.variableList

    def __str__(self):
        return self.type + ": " + str(self.variableList)

# Rule will check if all of a set of conditions of certain types are true
# If yes, it will claim another set of conditions to be true and insert them within the short term memory
class Rule:
    def __init__(self):
        print("constructing rule")
        self.conditions = []

    def process(self, stm):
        print("processing rule")
        pass


# if a is at left of b then b is at left of a
class RuleAtoB(Rule):
    def __init__(self, A, B):
        Rule.__init__(self)
        self.A = A
        self.B = B
        self.conditions = [A, B]

    def process(self, stm):
        Rule.process(self, stm)
        count = 0
        sc = self.A
        if sc in stm.conditions:
            for c in stm.conditions[sc]:
                isAdded = stm.addCondition(Condition(self.B, [c.variableList[1],c.variableList[0]]))
                if isAdded:
                    count += 1
        return count


# if a is at left of b and b is at left of c then a is at left of c
class RuleCombineA(Rule):
    def __init__(self, A):
        Rule.__init__(self)
        self.A = A
        self.conditions = [A]

    def process(self, stm):
        Rule.process(self, stm)
        count = 0
        sc = self.A
        if sc in stm.conditions:
            for c in stm.conditions[sc]:
                a = c.variableList[0]
                b = c.variableList[1]
                for cb in stm.dictConditionsByIndVar[b]:
                    if cb.type == sc:
                        if cb.variableList[1] == a:
                            continue
                        isAdded = stm.addCondition(Condition(self.A, [a, cb.variableList[1]]))
                        if isAdded:
                            count += 1
        return count

class RuleCreator():
    def createRules(self, ruleA, ruleB, ltm = None):
        self.ruleA = ruleA
        self.ruleB = ruleB

        r1 = RuleAtoB(ruleA, ruleB)
        r2 = RuleAtoB(ruleB, ruleA)
        r3 = RuleCombineA(ruleA)
        r4 = RuleCombineA(ruleB)

        if ltm != None:
            ltm.addRule(r1)
            ltm.addRule(r2)
            ltm.addRule(r3)
            ltm.addRule(r4)

        return [r1, r2, r3, r4]

# This is the core of the production system
# It will keep a Long Term Memory a Short Term Memory
# It will support functions to enter a condition to be true, new rules
# and to find answer of a certain type of inference query about conditions between to variables
class ProductionSystem:
    def __init__(self):
        print("constructing production system")
        self.ltm = LongTermMemory()
        self.stm = ShortTermMemory()

    def query(self, a, b):
        print("\n***********\nquerying spatial relation between", a, "and", b)
        # all the rules need to be executed unless no new conditions are added in the last iteration
        # then, the conditions should have the relation between a and b already there, just find and repot that
        self.ltm.process(self.stm)
        print("All rules processed.")
        self.stm.printConditions()
        print("\nSpatial relation between", a, "and", b + ":")
        rk = "_" + a + "_" + b
        if rk in self.stm.dictConditionsByVars:
            relations = self.stm.dictConditionsByVars[rk]
            for r in relations:
                print(r)
        else:
            print("I don't know!")


    def queryFast(self, a, b):
        # step 1: find all the conditions related to variable a and b
        # step 2: execute only those rules that will deal with the set of conditions selected in previous step
        # repeat until no new conditions is added

        print("\n***********\nfast querying spatial relation between", a, "and", b)

        i = 0
        while True:
            # step 1
            cl = []
            if a in self.stm.dictConditionsByIndVar:
                for c in self.stm.dictConditionsByIndVar[a]:
                    if c not in cl:
                        cl.append(c)
            if b in self.stm.dictConditionsByIndVar:
                for c in self.stm.dictConditionsByIndVar[b]:
                    if c not in cl:
                        cl.append(c)

            print ("Related conditions:")
            for c in cl:
                print(c)

            # step 2:
            rulesProcessed = []
            count = 0
            for c in cl:
                if c.type in self.ltm.dictConditionToRules:
                    for r in self.ltm.dictConditionToRules[c.type]:
                        if r not in rulesProcessed:
                            rulesProcessed.append(r)
                            i += 1
                            count += r.process(self.stm)
            if count == 0:
                break

        print("Number of rules processed:", i)
        print("Query processing finished.")
        self.stm.printConditions()
        print("\nSpatial relation between", a, "and", b + ":")
        rk = "_" + a + "_" + b
        if rk in self.stm.dictConditionsByVars:
            relations = self.stm.dictConditionsByVars[rk]
            for r in relations:
                print(r)
        else:
            print("I don't know!")

# The fork is to the left of the plate. The plate is to the left of the knife.
def test1():
    pd = ProductionSystem()
    rc = RuleCreator()
    rc.createRules("left of", "right of", pd.ltm)

    pd.stm.addCondition(Condition("left of", ["fork","plate"]))
    pd.stm.addCondition(Condition("left of", ["plate", "knife"]))
    pd.stm.printConditions()

    pd.queryFast("fork", "knife")

# The fork is to the left of the plate. The plate is above the napkin
def test2():
    pd = ProductionSystem()

    rc = RuleCreator()
    rc.createRules("left of", "right of", pd.ltm)
    rc.createRules("above of", "below of", pd.ltm)

    pd.stm.addCondition(Condition("left of", ["fork","plate"]))
    pd.stm.addCondition(Condition("above of", ["plate", "napkin"]))
    pd.stm.printConditions()

    pd.queryFast("fork", "napkin")


# The fork is to the left of the plate. The spoon is to the left of the plate.
def test3():
    pd = ProductionSystem()

    rc = RuleCreator()
    rc.createRules("left of", "right of", pd.ltm)
    rc.createRules("above of", "below of", pd.ltm)

    pd.stm.addCondition(Condition("left of", ["fork","plate"]))
    pd.stm.addCondition(Condition("left of", ["spoon", "plate"]))
    pd.stm.printConditions()

    pd.queryFast("fork", "spoon")


# The fork is to the left of the plate. The spoon is to the left of the fork. The knife is to the left
# of the spoon. The pizza is to the left of the knife. The cat is to the left of the pizza.
def test4():
    pd = ProductionSystem()

    rc = RuleCreator()
    rc.createRules("left of", "right of", pd.ltm)
    rc.createRules("above of", "below of", pd.ltm)

    pd.stm.addCondition(Condition("left of", ["fork","plate"]))
    pd.stm.addCondition(Condition("left of", ["spoon", "fork"]))
    pd.stm.addCondition(Condition("left of", ["knife", "spoon"]))
    pd.stm.addCondition(Condition("left of", ["pizza", "knife"]))
    pd.stm.addCondition(Condition("left of", ["cat", "pizza"]))
    pd.stm.printConditions()

    pd.queryFast("plate", "cat")

# The fork is to the left of the plate. The plate is to the left of the knife.
def testQueryFast():
    pd = ProductionSystem()
    rc = RuleCreator()
    rc.createRules("left of", "right of", pd.ltm)
    rc.createRules("above of", "below of", pd.ltm)
    rc.createRules("west", "east", pd.ltm)
    rc.createRules("south", "nort", pd.ltm)

    pd.stm.addCondition(Condition("left of", ["fork","plate"]))
    pd.stm.addCondition(Condition("left of", ["plate", "knife"]))
    pd.stm.addCondition(Condition("left of", ["plate1", "knife1"]))
    pd.stm.addCondition(Condition("left of", ["plate1", "knife1"]))
    pd.stm.addCondition(Condition("left of", ["plate2", "knife2"]))
    pd.stm.addCondition(Condition("left of", ["plate4", "knife3"]))
    pd.stm.printConditions()

    # pd.query("fork", "knife")
    pd.queryFast("fork", "knife")

if __name__ == "__main__":
    testQueryFast()
    # test4()