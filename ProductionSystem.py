# This will store all the rules
class LongTermMemory:
    def __init__(self):
        print ("constructing long term memory")
        self.rules = []

    def addRule(self, rule):
        self.rules.append(rule)

    def process(self, stm):
        print("processing long term memory")
        while True:
            count = 0
            for r in self.rules:
                count += r.process(stm)
            if count == 0:
                break

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

    def process(self, stm):
        print("processing rule")

class RuleLeftToRight(Rule):
    def __init__(self):
        Rule.__init__(self)

    def process(self, stm):
        Rule.process(self, stm)
        count = 0
        sc = "left of"
        if sc in stm.conditions:
            for c in stm.conditions[sc]:
                isAdded = stm.addCondition(Condition("right of", [c.variableList[1],c.variableList[0]]))
                if isAdded:
                    count += 1
        return count

class RuleRightToLeft(Rule):
    def __init__(self):
        Rule.__init__(self)

    def process(self, stm):
        Rule.process(self, stm)
        count = 0
        sc = "right of"
        if sc in stm.conditions:
            for c in stm.conditions[sc]:
                isAdded = stm.addCondition(Condition("left of", [c.variableList[1], c.variableList[0]]))
                if isAdded:
                    count += 1
        return count


# if a is at left of b and b is at left of c then a is at left of c
class RuleCombineLeft(Rule):
    def __init__(self):
        Rule.__init__(self)

    def process(self, stm):
        Rule.process(self, stm)
        count = 0
        sc = "left of"
        if sc in stm.conditions:
            for c in stm.conditions[sc]:
                a = c.variableList[0]
                b = c.variableList[1]
                for cb in stm.dictConditionsByIndVar[b]:
                    if cb.type == sc:
                        if cb.variableList[1] == a:
                            continue
                        isAdded = stm.addCondition(Condition("left of", [a, cb.variableList[1]]))
                        if isAdded:
                            count += 1
        return count

# if a is at top of b and b is at top of c then a is at top of c
class RuleCombineRight(Rule):
    def __init__(self):
        Rule.__init__(self)

    def process(self, stm):
        Rule.process(self, stm)
        count = 0
        sc = "right of"
        if sc in stm.conditions:
            for c in stm.conditions[sc]:
                a = c.variableList[0]
                b = c.variableList[1]
                for cb in stm.dictConditionsByIndVar[b]:
                    if cb.type == sc:
                        if cb.variableList[1] == a:
                            continue
                        isAdded = stm.addCondition(Condition("right of", [a, cb.variableList[1]]))
                        if isAdded:
                            count += 1
        return count


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

if __name__ == "__main__":
    pd = ProductionSystem()
    pd.stm.addCondition(Condition("left of", ["fork","plate"]))
    pd.stm.addCondition(Condition("left of", ["plate", "knife"]))
    pd.stm.printConditions()

    pd.ltm.addRule(RuleLeftToRight())
    pd.ltm.addRule(RuleCombineLeft())

    # pd.ltm.process(pd.stm)
    # pd.stm.printConditions()

    pd.query("fork", "knife")