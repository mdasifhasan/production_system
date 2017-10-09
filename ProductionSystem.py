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

    def addCondition(self, condition):
        if self.isConditionExists(condition):
            print("condition exists:",condition)
            return False
        if condition.type not in self.conditions:
            ca = [condition]
            self.conditions[condition.type] = ca
        else:
            self.conditions[condition.type].append(condition)

        self.dictConditions[self.getKeyForCondition(condition)] = condition

        kv = self.getKeyForConditionByVars(condition)
        if kv not in self.dictConditionsByVars:
            ca = [condition]
            self.dictConditionsByVars[kv] = ca
        else:
            self.dictConditionsByVars[kv].append(condition)


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

        print("constructing condition:", self)

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

class RuleLeftToRight(Rule):
    def __init__(self):
        Rule.__init__(self)
        self.conditions.append("left of")

    def process(self, stm):
        Rule.process(self, stm)
        count = 0
        for sc in self.conditions:
            if sc in stm.conditions:
                for c in stm.conditions[sc]:
                    isAdded = stm.addCondition(Condition("right of", [c.variableList[1],c.variableList[0]]))
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
        print("All rules processed. The answer is:")
        rk = a + "_" + b
        if rk in self.stm.dictConditionsByVars:
            relations = self.stm.dictConditionsByVars[rk]
            print(relations)
        else:
            print("I don't know!")

if __name__ == "__main__":
    pd = ProductionSystem()
    pd.stm.addCondition(Condition("left of", ["fork","plate"]))
    pd.stm.addCondition(Condition("left of", ["plate", "knife"]))
    pd.stm.printConditions()

    pd.ltm.addRule(RuleLeftToRight())

    # pd.ltm.process(pd.stm)
    # pd.stm.printConditions()

    pd.query("fork", "knife")