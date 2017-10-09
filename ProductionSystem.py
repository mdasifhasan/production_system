# This will store all the rules
class LongTermMemory:
    def __init__(self):
        print ("constructing long term memory")
        self.rules = []

    def addRule(self, rule):
        self.rules.append(rule)

    def process(self, stm):
        print("\nprocessing long term memory")
        for r in self.rules:
            r.process(stm)

# This class will keep current conditions that are true
# It will keep the conditions sorted by condition type in a dictionary
# the dictionary format: conditions = <condition_type, conditions[]>
class ShortTermMemory:
    def __init__(self):
        print ("constructing short term memory")
        self.conditions = {}

    def addCondition(self, condition):
        if condition.type not in self.conditions:

            ca = [condition]
            self.conditions[condition.type] = ca
        else:
            self.conditions[condition.type].append(condition)

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
        for sc in self.conditions:
            if sc in stm.conditions:
                for c in stm.conditions[sc]:
                    stm.addCondition(Condition("right of", ["plate", "knife"]))

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
        print("querying spatial relation between a and b")


if __name__ == "__main__":
    pd = ProductionSystem()
    pd.stm.addCondition(Condition("left of", ["fork","plate"]))
    pd.stm.addCondition(Condition("left of", ["plate", "knife"]))
    pd.stm.printConditions()

    pd.ltm.addRule(RuleLeftToRight())

    pd.ltm.process(pd.stm)
    pd.stm.printConditions()